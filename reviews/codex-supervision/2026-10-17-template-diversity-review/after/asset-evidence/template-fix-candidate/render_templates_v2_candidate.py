"""Text-only static candidate v2. No Manim import, rendering or production wiring.
Plans prove exact source-fragment coverage only. Physical layout needs real metrics.
Generated code rejects oversize rows and nonempty canvas; never shrinks content.
"""
from __future__ import annotations
import hashlib,json,re
from fractions import Fraction

class TemplateError(ValueError):pass

def _positive(n,name):
    if type(n) is not int or not 1<=n<=10000:raise TemplateError("invalid_"+name)
    return n

def _escaped(text,i):
    n=0;j=i-1
    while j>=0 and text[j]=="\\":
        n+=1;j-=1
    return n%2==1

def _text_units(text,start,end):
    out=[];i=start
    while i<end:
        if text[i:i+2]=="\r\n":
            out.append({"kind":"break","content":"\r\n","start":i,"end":i+2});i+=2
        elif text[i] in "\r\n":
            out.append({"kind":"break","content":text[i],"start":i,"end":i+1});i+=1
        elif text[i:i+2]==r"\$" and _escaped(text,i+1):
            out.append({"kind":"text","content":"$","start":i,"end":i+2});i+=2
        else:
            out.append({"kind":"text","content":text[i],"start":i,"end":i+1});i+=1
    return out

def tokenize(text):
    if type(text) is not str or not text.strip() or len(text)>100000:
        raise TemplateError("empty_or_invalid_text")
    # Explicitly unsupported delimiters must not silently become plain Text.
    if any(s in text for s in (r"\(",r"\)",r"\[",r"\]")):
        raise TemplateError("unsupported_math_delimiter")
    out=[];start=0;math_start=None;i=0
    while i<len(text):
        if text[i]=="$" and not _escaped(text,i):
            if i+1<len(text) and text[i+1]=="$":
                raise TemplateError("display_math_not_supported")
            if math_start is None:
                out.extend(_text_units(text,start,i));math_start=i
            else:
                content=text[math_start+1:i]
                if not content.strip() or "\n" in content or "\r" in content:
                    raise TemplateError("empty_or_multiline_math")
                # Keep LaTeX escaping, e.g. \$ inside a formula.
                out.append({"kind":"math","content":content,"start":math_start,"end":i+1})
                math_start=None;start=i+1
        i+=1
    if math_start is not None:raise TemplateError("unmatched_dollar")
    out.extend(_text_units(text,start,len(text)))
    return out

def split_mixed(text):
    """Visible ordered segments. Newlines are explicit 'break' segments."""
    out=[]
    for t in tokenize(text):
        if out and t["kind"]=="text" and out[-1][0]=="text":
            out[-1]=("text",out[-1][1]+t["content"])
        else:out.append((t["kind"],t["content"]))
    return out

def _rows(steps,chunk_chars):
    if type(steps) is not list or not steps or len(steps)>1000:
        raise TemplateError("invalid_sources")
    _positive(chunk_chars,"chunk_chars");rows=[]
    for index,text in enumerate(steps):
        current=[];text_run=[];budget=chunk_chars
        def flush_text():
            nonlocal text_run
            if text_run:
                current.append({"kind":"text","content":"".join(t["content"] for t in text_run),
                                "start":text_run[0]["start"],"end":text_run[-1]["end"]})
                text_run=[]
        def flush_row():
            nonlocal current,budget
            flush_text();rows.append({"source_index":index,"fragments":current})
            current=[];budget=chunk_chars
        for t in tokenize(text):
            if t["kind"]=="break":
                flush_text();current.append(t);flush_row()
            elif t["kind"]=="math":
                flush_text()
                if budget==0:flush_row()
                current.append(t);budget-=1
            else:
                if budget==0:flush_row()
                text_run.append(t);budget-=1
        if current or text_run:flush_row()
    return rows

def make_plan(steps,per_page_lines=5,chunk_chars=32):
    _positive(per_page_lines,"per_page_lines")
    rows=_rows(steps,chunk_chars)
    pages=[list(range(i,min(i+per_page_lines,len(rows)))) for i in range(0,len(rows),per_page_lines)]
    return {"schema":"text-fragment-plan-v2","sources":list(steps),"chunk_chars":chunk_chars,
            "per_page_lines":per_page_lines,"rows":rows,"provisional_pages":pages,
            "layout":"UNVERIFIED_REQUIRES_NATIVE_MEASUREMENTS",
            "source_sha256":hashlib.sha256(json.dumps(steps,ensure_ascii=True,separators=(",",":")).encode()).hexdigest()}

def coverage_ok(steps,plan):
    try:
        if type(plan) is not dict:return False
        expected=make_plan(steps,plan["per_page_lines"],plan["chunk_chars"])
        return plan==expected
    except (TemplateError,KeyError,TypeError,ValueError):return False

def paginate(step_indexes,per_page_lines,lines_per_step):
    """Legacy coarse step-only mapping removed: it cannot prove fragment coverage."""
    raise TemplateError("use_make_plan_with_exact_fragments")

def estimate_height(*args,**kwargs):
    raise TemplateError("native_measurements_required_not_height_estimates")

def exact_fraction_text(dec_str,verified_exact):
    if type(dec_str) is not str or type(verified_exact) is not bool:
        raise TemplateError("explicit_boolean_and_string_required")
    if not verified_exact:return dec_str
    if len(dec_str)>1000 or not re.fullmatch(r"-?[0-9]+\.[0-9]+",dec_str):
        raise TemplateError("not_exact_decimal_literal")
    f=Fraction(dec_str)
    if f.denominator==1:return str(f.numerator)
    sign="-" if f.numerator<0 else ""
    return sign+"\\frac{"+str(abs(f.numerator))+"}{"+str(f.denominator)+"}"

def measured_pages(sizes,width,height,gap=Fraction(1,4)):
    """Pure algorithm on supplied dimensions. Synthetic sizes are not real evidence."""
    if (type(sizes) is not list or not sizes or any(type(v) not in (int,Fraction) for v in (width,height,gap))
        or width<=0 or height<=0 or gap<0):raise TemplateError("invalid_dimensions")
    pages=[];current=[];used=0
    for i,(w,h) in enumerate(sizes):
        if type(w) not in (int,Fraction) or type(h) not in (int,Fraction) or w<0 or h<=0 or w>width or h>height:raise TemplateError("row_exceeds_viewport")
        need=h+(gap if current else 0)
        if used+need>height:
            pages.append(current);current=[];used=0;need=h
        current.append(i);used+=need
    if current:pages.append(current)
    return pages

def generate_block(plan,font_size=22):
    """Generate only; never execute the scene. Use a dedicated empty canvas.
    All MathTex construction precedes all Text construction in this block.
    Runtime measured page map replaces the provisional static grouping.
    """
    if type(plan) is not dict or not coverage_ok(plan.get("sources"),plan):raise TemplateError("invalid_plan")
    if type(font_size) is not int or not 16<=font_size<=64:raise TemplateError("font_size")
    lines=["        from math import isfinite as candidate_isfinite",
           "        if self.mobjects:",
           "            raise ValueError('candidate_requires_dedicated_empty_canvas')",
           "        candidate_width = config.frame_width - 1",
           "        candidate_height = config.frame_height - 1",
           "        if not candidate_isfinite(candidate_width) or not candidate_isfinite(candidate_height) or candidate_width <= 0 or candidate_height <= 0:",
           "            raise ValueError('candidate_invalid_viewport')",
           "        candidate_objects = {}"]
    # Prebuild every formula before Pango/Text allocations.
    for ri,row in enumerate(plan["rows"]):
        for fi,f in enumerate(row["fragments"]):
            if f["kind"]=="math":
                lines.append(f"        candidate_objects[{(ri,fi)!r}] = MathTex({f['content']!r}, font_size={font_size})")
    for ri,row in enumerate(plan["rows"]):
        for fi,f in enumerate(row["fragments"]):
            if f["kind"]=="text" and f["content"].strip():
                lines.append(f"        candidate_objects[{(ri,fi)!r}] = Text({f['content']!r}, font='Microsoft YaHei', font_size={font_size})")
            elif f["kind"]=="text":
                # A measured invisible spacer preserves whitespace without dropping it.
                lines.append(f"        candidate_objects[{(ri,fi)!r}] = Text({'M'*len(f['content'])!r}, font='Microsoft YaHei', font_size={font_size}).set_opacity(0)")
    lines.append("        candidate_rows = []")
    for ri,row in enumerate(plan["rows"]):
        parts=[f"candidate_objects[{(ri,fi)!r}]" for fi,f in enumerate(row["fragments"]) if f["kind"]!="break"]
        expr="VGroup("+", ".join(parts)+").arrange(RIGHT, buff=0)"
        if not parts:
            expr=f"Text('M', font='Microsoft YaHei', font_size={font_size}).set_opacity(0)"
        lines.append("        candidate_rows.append("+expr+")")
    lines.extend([
        "        candidate_pages = []",
        "        candidate_page = []",
        "        candidate_used = 0",
        "        for candidate_index, candidate_row in enumerate(candidate_rows):",
        "            if not candidate_isfinite(candidate_row.width) or not candidate_isfinite(candidate_row.height) or candidate_row.width > candidate_width or candidate_row.height > candidate_height or candidate_row.height <= 0:",
        "                raise ValueError('candidate_row_exceeds_measured_viewport')",
        "            candidate_need = candidate_row.height + (1/4 if candidate_page else 0)",
        "            if candidate_used + candidate_need > candidate_height:",
        "                candidate_pages.append(candidate_page)",
        "                candidate_page = []",
        "                candidate_used = 0",
        "                candidate_need = candidate_row.height",
        "            candidate_page.append(candidate_index)",
        "            candidate_used += candidate_need",
        "        if candidate_page:",
        "            candidate_pages.append(candidate_page)",
        "        self.candidate_page_map = candidate_pages",
        "        for candidate_indices in candidate_pages:",
        "            candidate_group = VGroup(*[candidate_rows[i] for i in candidate_indices]).arrange(DOWN, aligned_edge=LEFT, buff=1/4)",
        "            candidate_group.move_to(ORIGIN)",
        "            if candidate_group.width > candidate_width or candidate_group.height > candidate_height:",
        "                raise ValueError('candidate_page_exceeds_measured_viewport')",
        "            self.play(FadeIn(candidate_group))",
        "            self.wait(1)",
        "            self.play(FadeOut(candidate_group))",
        "            self.remove(candidate_group)",
    ])
    return "\n".join(lines)+"\n"

def steps_block_v2(steps,font_size=22,per_page_lines=5):
    plan=make_plan(steps,per_page_lines)
    return generate_block(plan,font_size),plan

def title_block_v2(problem):return generate_block(make_plan([problem]),24)
def answer_block_v2(answer):return generate_block(make_plan([answer]),24)

def scene_blocks_v2(problem,steps,answer,font_size=22,per_page_lines=5):
    """Preferred combined text-only plan: formulas precede all Text allocations."""
    if type(steps) is not list:raise TemplateError("steps_type")
    sources=[problem,*steps,answer];plan=make_plan(sources,per_page_lines)
    return generate_block(plan,font_size),plan
