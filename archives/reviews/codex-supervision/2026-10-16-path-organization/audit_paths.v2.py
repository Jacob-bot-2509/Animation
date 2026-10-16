from pathlib import Path
import os,stat,json,sys,collections,re,urllib.parse
ROOTS=[Path(r"D:\Animation-Model-Training"),Path(r"D:\code")]
OUT=Path(sys.argv[1])
SKIP={".git","node_modules",".venv","venv",".models","__pycache__",".pytest_cache",".cache"}
records=[];dirs=[];excluded=[];reparse=[];errors=[];frozen=[];broken_links=[];links=[]
def scan(base,root,frozen_root=None):
 try: entries=list(os.scandir(root))
 except OSError as e: errors.append({"path":str(root),"error":str(e)});return
 names={x.name for x in entries}
 if frozen_root is None and "delivery-manifest.json" in names:
  frozen_root=root;frozen.append(str(root))
 for e in sorted(entries,key=lambda x:x.name.lower()):
  q=Path(e.path)
  if q==OUT.parent: excluded.append({"path":str(q),"reason":"THIS_AUDIT_OUTPUT"});continue
  try:s=e.stat(follow_symlinks=False)
  except OSError as ex:errors.append({"path":str(q),"error":str(ex)});continue
  if getattr(s,"st_file_attributes",0)&stat.FILE_ATTRIBUTE_REPARSE_POINT:
   reparse.append({"path":str(q),"attributes":s.st_file_attributes});continue
  if e.is_dir(follow_symlinks=False):
   dirs.append({"path":str(q),"root":str(base),"frozen":str(frozen_root) if frozen_root else None})
   if e.name in SKIP:excluded.append({"path":str(q),"reason":"DEPENDENCY_OR_CACHE"});continue
   scan(base,q,frozen_root)
  elif e.is_file(follow_symlinks=False):
   row={"path":str(q),"root":str(base),"bytes":s.st_size,"mtime_ns":s.st_mtime_ns,"frozen":str(frozen_root) if frozen_root else None}
   records.append(row)
   rel=q.relative_to(base)
   active_doc=(len(rel.parts)==1 or rel.parts[0]=="docs" or (base==ROOTS[1] and rel.parts[0] in ["backend","frontend"] and len(rel.parts)==2))
   if q.suffix.lower()==".md" and frozen_root is None and active_doc and q.stat().st_size<2_000_000:
    try:text=q.read_text(encoding="utf-8")
    except (UnicodeError,OSError):continue
    text=re.sub(r"^```[^\n]*\n.*?^```[^\n]*$","",text,flags=re.M|re.S)
    for m in re.finditer(r"!?\[[^\]\n]*\]\((<[^>\n]+>|[^)\n]+)\)",text):
     target=m.group(1).strip().strip("<>")
     if " " in target and not m.group(1).startswith("<"):target=target.split(' "',1)[0].split(" '",1)[0]
     if re.match(r"^(?:https?|mailto|data|app|plugin|vscode):",target,re.I) or target.startswith("#"):continue
     raw=urllib.parse.unquote(target.split("#",1)[0])
     if not raw or any(x in raw for x in ["{","}","*","<",">","\\("]):continue
     raw=re.sub(r":\d+$","",raw)
     dest=Path(raw) if re.match(r"^[A-Za-z]:[/\\]",raw) else q.parent/raw
     item={"source":str(q),"target":target,"resolved":str(dest),"exists":dest.exists()}
     links.append(item)
     if not item["exists"]:
      try: rel=dest.resolve(strict=False).relative_to(base)
      except ValueError:rel=None
      candidate=base/"archives"/rel if rel and rel.parts[0] in ["reviews","reports"] else None
      if candidate is not None and candidate.exists():item["archive_replacement"]=str(candidate)
      broken_links.append(item)
for base in ROOTS:scan(base,base)
summary={"files":len(records),"directories":len(dirs),"bytes":sum(x["bytes"] for x in records),"frozen_roots":len(frozen),"reparse_points":len(reparse),"errors":len(errors),"mutable_markdown_links":len(links),"broken_mutable_markdown_links":len(broken_links),"by_root":dict(collections.Counter(x["root"] for x in records)),"long_paths_over_240":sum(len(x["path"])>240 for x in records)}
payload={"schema":"codex-path-inventory-v1","summary":summary,"roots":[str(x) for x in ROOTS],"files":records,"directories":dirs,"frozen_roots":frozen,"excluded":excluded,"reparse_points":reparse,"errors":errors,"mutable_markdown_links":links,"broken_mutable_markdown_links":broken_links}
with OUT.open("x",encoding="utf-8") as f:json.dump(payload,f,ensure_ascii=False,indent=2);f.write("\n")
print(json.dumps(summary,ensure_ascii=True,indent=2))
print("BROKEN_LINKS",json.dumps(broken_links,ensure_ascii=True,indent=2))
print("REPARSE_POINTS",json.dumps(reparse,ensure_ascii=True,indent=2))
print("ERRORS",json.dumps(errors,ensure_ascii=True,indent=2))
