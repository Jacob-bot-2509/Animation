"""Bound lexical review support. No expression evaluation, rendering, or math approval."""
from __future__ import annotations
import hashlib,importlib.util,json,re,sys,uuid
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).absolute().parent
ROOT=HERE.parents[4]
CORE=HERE.parent/"content-geometry-mapping/build_content_mapping.py"
CORE_BYTES=CORE.read_bytes()
s=importlib.util.spec_from_file_location("review_content_core",CORE)
core=importlib.util.module_from_spec(s);s.loader.exec_module(core)
sha=core.sha
enc=core.encoded
DEC=re.compile(r"(?<![\w.])[+-]?(?:(?:[0-9]+\.[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?|[0-9]+[eE][+-]?[0-9]+)(?![\w.])")
TEXT_FRAC=re.compile(r"(?<![\w./])[+-]?[0-9]+/[+-]?[0-9]+(?![\w./])")
TEX_FRAC=re.compile(r"\\(?:dfrac|tfrac|frac)(?![A-Za-z])")
SYM=re.compile(r"\\(?:pi|sqrt|ln|log|exp|sin|cos|tan|arcsin|arccos|arctan|infty)\b")
INT=re.compile(r"[+-]?[0-9]+")
def escaped(text,i):
    n=0;i-=1
    while i>=0 and text[i]=="\\":
        n+=1;i-=1
    return bool(n%2)
def group(text,pos):
    while pos<len(text) and text[pos].isspace():pos+=1
    if pos>=len(text) or text[pos]!="{":return None
    start=pos;depth=1;pos+=1
    while pos<len(text):
        if not escaped(text,pos):
            if text[pos]=="{":depth+=1
            elif text[pos]=="}":
                depth-=1
                if depth==0:return text[start+1:pos],pos+1
        pos+=1
    return None
def formulas(text):
    out=[];start=None
    for i,c in enumerate(text):
        if c=="$" and not escaped(text,i):
            if start is None:start=i
            else:
                out.append({"start":start,"end":i+1,"text":text[start:i+1],"meaning":"RAW_FORMULA_NOT_EVALUATED"})
                start=None
    if start is not None:
        out.append({"start":start,"end":len(text),"text":text[start:],"meaning":"UNMATCHED_DELIMITER_REQUIRES_REVIEW"})
    return out
def sentences(text):
    out=[];start=0;in_math=False
    for i,c in enumerate(text):
        if c=="$" and not escaped(text,i):in_math=not in_math
        if c in "。;；\n" and not in_math:
            out.append({"start":start,"end":i+1,"text":text[start:i+1]});start=i+1
    if start<len(text):out.append({"start":start,"end":len(text),"text":text[start:]})
    return out
def scan(text):
    if type(text)is not str or len(text)>100000:raise ValueError("text_type_or_size")
    items=[]
    for match in DEC.finditer(text):
        value=match.group();candidate=None;note="LITERAL_VALUE_ONLY_NOT_ORIGINAL_QUANTITY_EXACTNESS"
        # Bound exponent/length before constructing Fraction to prevent huge integer work.
        exponent=re.search(r"[eE]([+-]?[0-9]+)$",value)
        if len(value)<=256 and (exponent is None or len(exponent[1].lstrip("+-"))<=3 and abs(int(exponent[1]))<=256):
            candidate=str(Fraction(value))
        else:note="LITERAL_TOO_LARGE_NOT_CONVERTED"
        items.append({"kind":"decimal_literal","value":value,"start":match.start(),"end":match.end(),
                      "literal_fraction_candidate":candidate,"meaning":note,"verdict":"PENDING_REVIEW"})
    for match in TEXT_FRAC.finditer(text):
        numerator,denominator=map(int,match.group().split("/"))
        items.append({"kind":"text_fraction_syntax","value":match.group(),"start":match.start(),"end":match.end(),
                      "literal_fraction_candidate":str(Fraction(numerator,denominator)) if denominator else None,
                      "meaning":"UNDEFINED_ZERO_DENOMINATOR" if not denominator else "INTEGER_RATIO_LITERAL_ONLY",
                      "verdict":"PENDING_REVIEW"})
    for match in TEX_FRAC.finditer(text):
        first=group(text,match.end())
        second=group(text,first[1]) if first else None
        end=second[1] if second else match.end()
        n=first[0].strip() if first else None;d=second[0].strip() if second else None
        value=None;meaning="SYMBOLIC_DENOMINATOR_AND_DOMAIN_REQUIRE_REVIEW"
        if not second:meaning="UNPARSED_FRACTION_COMMAND_REQUIRES_REVIEW"
        elif INT.fullmatch(n or "") and INT.fullmatch(d or ""):
            meaning="UNDEFINED_ZERO_DENOMINATOR" if int(d)==0 else "INTEGER_RATIO_LITERAL_ONLY"
            if int(d)!=0:value=str(Fraction(int(n),int(d)))
        items.append({"kind":"latex_fraction_syntax","value":text[match.start():end],"start":match.start(),"end":end,
                      "numerator":n,"denominator":d,"literal_fraction_candidate":value,"meaning":meaning,"verdict":"PENDING_REVIEW"})
    for match in SYM.finditer(text):
        items.append({"kind":"symbolic_command","value":match.group(),"start":match.start(),"end":match.end(),
                      "meaning":"RECOGNIZED_COMMAND_ONLY_NOT_EXHAUSTIVE_SEMANTIC_PARSE","verdict":"PENDING_REVIEW"})
    return {"text":text,"items":sorted(items,key=lambda x:(x["start"],x["end"],x["kind"])),
            "formula_spans":formulas(text),"segments":sentences(text),
            "scope":"LEXICAL_LOCATIONS_ONLY_NOT_MATHEMATICAL_PROOF"}
def fields(obj):
    out={}
    for key in ["problem","solution","answer"]:
        value=obj.get(key)
        if type(value)is not str or not value.strip():raise ValueError("missing_"+key)
        out[key]=scan(value)
    scene=obj.get("scene_spec")
    if type(scene)is not dict:raise ValueError("scene_shape")
    for key in ["objects","steps"]:
        values=scene.get(key)
        if type(values)is not list or not values or any(type(x)is not str or not x.strip() for x in values):
            raise ValueError("scene_"+key+"_shape")
        for i,text in enumerate(values):out[f"scene_spec.{key}[{i}]"]=scan(text)
    return out
def build():
    if CORE.read_bytes()!=CORE_BYTES:raise ValueError("binding_core_changed")
    bound=core.build()
    rows=[];source_pins={}
    for row in bound["records"]:
        b=row["source"];p=ROOT/b["path"];rawfile=p.read_bytes()
        if sha(rawfile)!=b["file_sha256"]:raise ValueError("source_changed")
        raw=rawfile.splitlines(keepends=True)[b["line"]-1];obj=core.strict_json(raw)
        if sha(raw)!=b["raw_line_sha256"] or sha(enc(obj))!=b["canonical_record_sha256"] or obj.get("id")!=row["sample_id"]:
            raise ValueError("source_identity_changed")
        rows.append({"sample_id":row["sample_id"],"source":b,"fields":fields(obj),
                     "math_verdict":"PENDING_REVIEW","geometry_verdict":"PENDING_REVIEW"})
        source_pins[b["path"]]={"sha256":sha(rawfile),"bytes":len(rawfile)}
    pins={**{x["path"]:{"sha256":x["sha256"],"bytes":x["bytes"]} for x in bound["input_pins"].values()},**source_pins}
    pins[CORE.relative_to(ROOT).as_posix()]={"sha256":sha(CORE_BYTES),"bytes":len(CORE_BYTES)}
    pins[Path(__file__).relative_to(ROOT).as_posix()]={"sha256":sha(Path(__file__).read_bytes()),"bytes":Path(__file__).stat().st_size}
    for rel,pin in pins.items():
        if sha((ROOT/rel).read_bytes())!=pin["sha256"]:raise ValueError("input_changed")
    return {"schema":"bound-math-correspondence-v2","qualification":"LEXICAL_REVIEW_SUPPORT_ONLY",
            "records":rows,"input_pins":pins,"production":"CLOSED"}
def publish(result,base=HERE):
    base=Path(base).absolute();core.selector.checked_path(str(base),root=ROOT)
    for p in (base,*base.parents):
        if (p/"delivery-manifest.json").exists():raise ValueError("frozen_output")
        if p==ROOT:break
    if not base.is_dir():raise ValueError("missing_output_parent")
    # Check actual pins once more immediately before writing the new generation.
    for rel,pin in result["input_pins"].items():
        p=core.safe_input(ROOT/rel,ROOT)
        if sha(p.read_bytes())!=pin["sha256"]:raise ValueError("input_changed_before_publish")
    out=base/("generation-"+uuid.uuid4().hex);out.mkdir(exist_ok=False)
    raw=b"".join(enc(x)+b"\n" for x in result["records"])
    with (out/"math-correspondence.jsonl").open("xb") as f:f.write(raw)
    index=enc({"schema":result["schema"],"qualification":result["qualification"],"input_pins":result["input_pins"]})+b"\n"
    with (out/"input-index.json").open("xb") as f:f.write(index)
    done={"schema":"math-correspondence-generation-v2","records":len(result["records"]),
          "qualification":result["qualification"],"artifacts":[
          {"path":"math-correspondence.jsonl","sha256":sha(raw),"bytes":len(raw)},
          {"path":"input-index.json","sha256":sha(index),"bytes":len(index)}],
          "durability":"COMPLETION_MARKER_ONLY_NOT_POWER_LOSS_OR_HOSTILE_PEER_GUARANTEE"}
    with (out/"COMPLETE.json").open("xb") as f:f.write(enc(done)+b"\n")
    return out
def main():
    if len(sys.argv)!=1:raise ValueError("no_extra_arguments")
    result=build();out=publish(result)
    print(json.dumps({"generation":str(out),"records":len(result["records"]),"qualification":result["qualification"]}))
    return 0
if __name__=="__main__":
    try:raise SystemExit(main())
    except (ValueError,KeyError,TypeError,OSError) as exc:
        print("ERROR: "+str(exc),file=sys.stderr);raise SystemExit(2)
