from pathlib import Path
import json,os,re,subprocess,sys
ROOT=Path(r'D:\Animation-Model-Training');OUT=Path(__file__).resolve().parent
p=ROOT/'tests/test_audit_staged_scenes.py';text=p.read_text('utf-8');needle="if __name__=='__main__':unittest.main()"
new=""" def test_receipt_drift_during_audit_fails(self):
  from unittest.mock import patch
  import audit_staged_scenes as module
  original=module.jsonl
  def drift(data):
   rows=original(data);self.rec['concurrent_change']=True;self.save();return rows
  with patch.object(module,'jsonl',side_effect=drift):
   with self.assertRaises(ValueError):self.audit()
"""
assert needle in text;text=text.replace(needle,new+needle);p.write_text(text,encoding='utf-8',newline='\n')
env=dict(os.environ,PYTHONIOENCODING='utf-8');argv=[sys.executable,'-X','utf8','-B','-m','unittest','tests.test_audit_staged_scenes','tests.test_scene_sweep_protocol','tests.test_dataset_audit_latex_delimiters','tests.test_draft_hashes','-v'];r=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True);(OUT/'suite.stdout.raw.txt').write_bytes(r.stdout);(OUT/'suite.stderr.raw.txt').write_bytes(r.stderr);m=re.search(rb'Ran (\d+) tests',r.stderr);v={'argv':argv,'returncode':r.returncode,'tests':int(m.group(1)) if m else None,'passed':r.returncode==0};(OUT/'suite-result.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');print(json.dumps(v));assert r.returncode==0,r.stderr.decode('utf-8')
argv=[sys.executable,'-X','utf8','-B',str(ROOT/'tools/audit_staged_scenes.py')]
for n in range(1,11):argv+=['--staged',str(ROOT/f'reviews/2026-10-06-scene-standard-sweep/batch{n}-staged-v1')]
argv+=['--staged',str(OUT/'scene-candidates-144-v5')];r=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True);(OUT/'staged-integrity.raw.json').write_bytes(r.stdout);(OUT/'staged-integrity.stderr.raw.txt').write_bytes(r.stderr);print('STAGED INTEGRITY',r.returncode);assert r.returncode==0,r.stdout.decode('utf-8')