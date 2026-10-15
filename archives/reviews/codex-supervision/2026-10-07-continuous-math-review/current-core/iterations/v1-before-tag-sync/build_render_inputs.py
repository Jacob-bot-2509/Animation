"""Generate offline-directory HTML from the current, hash-bound 761 candidates."""
import pathlib,json,hashlib,html,shutil
ROOT=pathlib.Path(__file__).resolve().parents[4]
OUT=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and p.read_bytes()!=b:raise ValueError('Refuse overwrite '+str(p))
 if not p.exists():p.write_bytes(b)
def dumps(o):return json.dumps(o,ensure_ascii=False,indent=2)
bindings=json.loads((OUT/'source-bindings.json').read_text(encoding='utf8'))
asset=ROOT/'tools/assets/mathjax-tex-svg.js'
save(OUT/'render/assets/mathjax-tex-svg.js',asset.read_bytes())
config={'loader':{'paths':{'mathjax':'../assets'}},'tex':{'inlineMath':[['$','$'],['\\(','\\)']],'displayMath':[['$$','$$'],['\\[','\\]']],'packages':['base','ams','newcommand','configmacros']},'svg':{'fontCache':'none'},'options':{'enableMenu':False}}
qa="""MathJax.startup.promise.then(function(){let errs=Array.from(document.querySelectorAll('[data-mml-node="merror"],[data-mjx-error]')).map(e=>({id:e.closest('section')?.dataset.id,field:e.closest('[data-field]')?.dataset.field,message:e.getAttribute('data-mjx-error')||e.textContent}));document.getElementById('qa').textContent=JSON.stringify({status:'DONE',errors:errs,math_count:document.querySelectorAll('mjx-container').length,records:document.querySelectorAll('section[data-id]').length});}).catch(function(e){document.getElementById('qa').textContent=JSON.stringify({status:'FAIL',error:String(e)});});"""
css="body{max-width:1000px;margin:24px auto;padding:16px;font:16px/1.75 'Microsoft YaHei',sans-serif;color:#222}section{border-top:1px solid #ccc;padding:12px 0}.value{white-space:pre-wrap;overflow-wrap:anywhere}h2{font-size:20px}mjx-container{max-width:100%;overflow-x:auto}label{color:#244a73;font-weight:bold}#qa{white-space:pre-wrap;font:12px monospace;background:#eee}"
reports=[]
def leaves(value,prefix):
 if isinstance(value,str):yield prefix,value
 elif isinstance(value,dict):
  for k,v in value.items():yield from leaves(v,prefix+'.'+k)
 elif isinstance(value,list):
  for i,v in enumerate(value):yield from leaves(v,prefix+'['+str(i)+']')
for idx,binding in enumerate(bindings,1):
 p=ROOT/binding['path'];data=p.read_bytes();assert sha(data)==binding['sha256']
 name=f"{idx:02d}-"+p.stem
 body=[];md=[];field_count=0
 for line in data.decode('utf8').splitlines():
  rec=json.loads(line);rid=rec['id']
  body.append('<section data-id="'+html.escape(rid,quote=True)+'"><h2>'+html.escape(rid)+'</h2>')
  md.append('## '+rid)
  for key in ('problem','solution','answer','scene_spec'):
   for field,text in leaves(rec.get(key),key):
    field_count+=1
    body.append('<div data-field="'+html.escape(field,quote=True)+'"><label>'+html.escape(field)+'</label><div class="value">'+html.escape(text)+'</div></div>')
    md.extend([field,text])
  body.append('</section>')
 intro='<h1>'+html.escape(name)+'</h1><p>Offline directory preview; current source SHA-256: '+binding['sha256']+'</p>'
 doc='<!doctype html><html lang="zh"><head><meta charset="utf-8"><title>'+html.escape(name)+'</title><style>'+css+'</style><script>window.MathJax='+json.dumps(config)+';</script><script src="../assets/mathjax-tex-svg.js"></script></head><body>'+intro+''.join(body)+'<pre id="qa">PENDING</pre><script>'+qa+'</script></body></html>'
 f=OUT/'render/html'/ (name+'.html');m=OUT/'render/md'/(name+'.md')
 save(f,doc.encode());save(m,('\n\n'.join(md)+'\n').encode())
 reports.append({'path':f.relative_to(ROOT).as_posix(),'sha256':sha(f.read_bytes()),'md_path':m.relative_to(ROOT).as_posix(),'md_sha256':sha(m.read_bytes()),'source_path':binding['path'],'source_sha256':binding['sha256'],'records':binding['records'],'rendered_text_fields':field_count})
report={'schema':'codex-current-core-offline-render-inputs-v1','records':sum(r['records'] for r in reports),'files':reports,'local_asset':{'path':(OUT/'render/assets/mathjax-tex-svg.js').relative_to(ROOT).as_posix(),'sha256':sha(asset.read_bytes()),'original_path':asset.relative_to(ROOT).as_posix()},'source_bindings_sha256':sha((OUT/'source-bindings.json').read_bytes()),'self_containment':'DIRECTORY_WITH_LOCAL_ASSET_NOT_SINGLE_FILE','external_script_urls':[],'browser_typesetting':'PENDING','native_render':'UNVERIFIED','production':'CLOSED'}
save(OUT/'render-input-receipt.json',(dumps(report)+'\n').encode())
print(json.dumps({'records':report['records'],'html_files':len(reports),'local_mathjax_sha256':sha(asset.read_bytes())}))
