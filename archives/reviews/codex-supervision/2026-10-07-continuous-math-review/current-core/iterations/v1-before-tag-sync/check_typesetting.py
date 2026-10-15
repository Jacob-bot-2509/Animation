"""Local Edge typesetting check. This does not certify visual layout or Manim."""
import pathlib,json,subprocess,re,html,hashlib,gzip
ROOT=pathlib.Path(__file__).resolve().parents[4]
OUT=pathlib.Path(__file__).resolve().parent
DST=OUT/'render/browser-check';DST.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,b):
 if p.exists() and p.read_bytes()!=b:raise ValueError('Refuse overwrite '+str(p))
 if not p.exists():p.write_bytes(b)
inputs=json.loads((OUT/'render-input-receipt.json').read_text(encoding='utf8'))
results=[]
for i,entry in enumerate(inputs['files']):
 src=ROOT/entry['path'];assert sha(src.read_bytes())==entry['sha256']
 if i==0:
  dom=(DST/'pilot-dom.html').read_bytes()
  stderr=(DST/'pilot-stderr.txt').read_bytes()
  rc=json.loads((DST/'pilot-result.json').read_text(encoding='utf8'))['exit_code']
 else:
  cmd=['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless','--disable-gpu','--disable-background-networking','--disable-component-update','--disable-sync','--no-first-run','--no-default-browser-check','--host-resolver-rules=MAP * ~NOTFOUND','--allow-file-access-from-files','--virtual-time-budget=12000','--user-data-dir='+str(DST/'profile-batch'),'--dump-dom',src.as_uri()]
  p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=45,creationflags=0x08000000)
  dom=p.stdout;stderr=p.stderr;rc=p.returncode
 m=re.search(r'<pre id="qa"[^>]*>(.*?)</pre>',dom.decode('utf8'),re.S)
 qa=json.loads(html.unescape(m.group(1))) if m else {'status':'NO_QA'}
 ok=rc==0 and qa.get('status')=='DONE' and qa.get('records')==entry['records'] and not qa.get('errors') and qa.get('math_count',0)>0
 compressed=gzip.compress(dom,mtime=0)
 f=DST/(src.stem+'.dom.html.gz');save(f,compressed)
 log=DST/(src.stem+'.stderr.txt');save(log,stderr)
 result={'source_html':entry['path'],'source_html_sha256':entry['sha256'],'source_jsonl':entry['source_path'],'source_jsonl_sha256':entry['source_sha256'],'exit_code':rc,'qa':qa,'verdict':'PASS_LOCAL_TYPESETTING' if ok else 'FAIL_LOCAL_TYPESETTING','dom_sha256':sha(dom),'dom_archive':f.relative_to(ROOT).as_posix(),'dom_archive_sha256':sha(compressed),'stderr_path':log.relative_to(ROOT).as_posix(),'stderr_sha256':sha(stderr)}
 results.append(result)
 print(json.dumps({'file':src.name,'records':qa.get('records'),'math':qa.get('math_count'),'errors':qa.get('errors'),'verdict':result['verdict']},ensure_ascii=False),flush=True)
report={'schema':'codex-current-core-local-typesetting-v1','render_input_receipt_sha256':sha((OUT/'render-input-receipt.json').read_bytes()),'browser':'INSTALLED_EDGE_HEADLESS_LOCAL_FILE','external_dns':'MAP * ~NOTFOUND','current_records':sum(x['qa'].get('records',0) for x in results),'typesetting':'PASS_LOCAL_TYPESETTING' if all(x['verdict']=='PASS_LOCAL_TYPESETTING' for x in results) else 'FAIL_LOCAL_TYPESETTING','files':results,'visual_layout':'NOT_INDEPENDENTLY_REVIEWED','pdf':'NOT_RUN','native_manim':'UNVERIFIED','production':'CLOSED'}
save(OUT/'browser-typesetting-receipt.json',(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
raise SystemExit(0 if report['typesetting']=='PASS_LOCAL_TYPESETTING' else 1)
