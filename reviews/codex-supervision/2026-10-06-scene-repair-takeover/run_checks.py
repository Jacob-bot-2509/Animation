from pathlib import Path
import json,os,re,subprocess,sys
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
env=dict(os.environ);env['PYTHONIOENCODING']='utf-8'
argv=[str(R/'.venv/Scripts/python.exe'),'-B','-m','unittest',
 'tests.test_scene_sweep_protocol','tests.test_dataset_audit_latex_delimiters','tests.test_draft_hashes','-v']
result=subprocess.run(argv,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
for name,data in [('suite.stdout.raw.txt',result.stdout),('suite.stderr.raw.txt',result.stderr)]:
 with (O/name).open('xb') as f:f.write(data)
m=re.search(rb'Ran (\d+) tests',result.stderr)
summary={'argv':argv,'returncode':result.returncode,'tests':int(m.group(1)) if m else None,
 'passed':result.returncode==0,'no_native_render_or_training':True}
with (O/'suite-result.json').open('x',encoding='utf-8') as f:json.dump(summary,f,indent=2);f.write('\n')
print(json.dumps(summary));sys.exit(result.returncode)
