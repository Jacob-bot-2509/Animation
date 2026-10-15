"""Run three independent new-evidence shards; no agents, shell evaluation or old-cache reuse."""
from pathlib import Path
import json,subprocess,time,hashlib
ROOT=Path(__file__).resolve().parents[3]
OWNER=Path(__file__).resolve().parent
PY=ROOT/".venv/Scripts/python.exe"
QUALIFIED=ROOT/"reviews/codex-supervision/2026-10-08-real-formula-followup/qualified-records.jsonl"
def main():
    rows=[json.loads(l) for l in QUALIFIED.read_text("utf-8").splitlines()]
    assert len(rows)==165 and len({r["id"] for r in rows})==165
    ids=[r["id"] for r in rows]
    caches=[r["id"] for r in rows if ((ROOT/r["mp4_path"]).parents[3]/"Tex").exists()]
    (OWNER/"old-cache-presence.json").write_text(json.dumps({"old_cache_ids":caches,"final_shards_use_old_caches":False,"probe_is_preliminary_only":True},indent=2)+"\n","utf-8")
    jobs=[]
    for i in range(3):
        shard=ids[i::3]
        prefix=OWNER/("shard-"+str(i+1))
        stdout=(OWNER/("shard-"+str(i+1)+".stdout.bin")).open("xb")
        stderr=(OWNER/("shard-"+str(i+1)+".stderr.bin")).open("xb")
        args=[str(PY),"-X","utf8","-B",str(ROOT/"tools/readable_formula_pages.py"),"--qualified",str(QUALIFIED),"--ids",*shard,"--out",str(prefix)]
        job=subprocess.Popen(args,cwd=str(ROOT),stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW)
        jobs.append((job,stdout,stderr,prefix,shard))
    (OWNER/"shard-launch.json").write_text(json.dumps({"shards":[{"pid":j.pid,"out":p.relative_to(ROOT).as_posix(),"count":len(ids)} for j,_,_,p,ids in jobs],
          "tool_sha256":hashlib.sha256((ROOT/"tools/readable_formula_pages.py").read_bytes()).hexdigest(),"mode":"3_INDEPENDENT_SUBPROCESSES_NO_AGENTS"},indent=2)+"\n","utf-8")
    while any(j.poll() is None for j,*_ in jobs):
        completed=sum(len(list(p.glob("render-*/receipt.json"))) for _,_,_,p,_ in jobs)
        print(json.dumps({"completed_record_receipts":completed,"of":165,"active_shards":sum(j.poll() is None for j,*_ in jobs)}),flush=True)
        time.sleep(20)
    results=[]
    for job,stdout,stderr,path,ids in jobs:
        stdout.close();stderr.close()
        results.append({"shard":path.name,"rc":job.returncode,"records":len(ids)})
    (OWNER/"shard-results.json").write_text(json.dumps(results,indent=2)+"\n","utf-8")
    print(json.dumps({"shards":results}),flush=True)
    return 0 if all(x["rc"]==0 for x in results) else 3
if __name__=="__main__":raise SystemExit(main())
