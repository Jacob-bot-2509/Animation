from pathlib import Path
from unittest import mock
from html.parser import HTMLParser
import importlib.util,json,subprocess,contextlib,io,shutil,copy,sys,hashlib,re
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];sys.path[:0]=[str(ROOT),str(ROOT/'tools')]
def load(name,rel):
 p=OUT/'snapshot'/rel;spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m=load('frozen_render_review','tools/render_review.py');builder=load('frozen_review_builder','tools/build_review_pdf.py');publisher=load('frozen_row_publisher','tools/apply_row_patches_v5.py')
fixture=OUT/'negative-fixtures';fixture.mkdir(exist_ok=True);old_pdf=ROOT/'outputs/draft-review/draft-review-v4-final.pdf';results=[]
def run_case(name,dom,fresh):
 d=fixture/name;d.mkdir();md=d/'review.md';md.write_bytes(b'# fixture\n\n$\\frac{1}{3}$\n');pdf=d/'review.pdf'
 if not fresh:shutil.copyfile(old_pdf,pdf)
 calls=[]
 def edge(args,**kwargs):
  calls.append(args)
  if '--dump-dom' in args:return subprocess.CompletedProcess(args,0,dom.encode(),b'')
  if fresh:shutil.copyfile(old_pdf,pdf);return subprocess.CompletedProcess(args,0,b'',b'')
  return subprocess.CompletedProcess(args,1,b'',b'Print failure: no new output')
 log=io.StringIO()
 with mock.patch.object(m,'run_edge',side_effect=edge),contextlib.redirect_stdout(log):rc=m.main([str(md),'--out-dir',str(d)])
 results.append({'case':name,'actual_tool_returncode':rc,'print_called':any(any(a.startswith('--print-to-pdf=') for a in args) for args in calls),'false_success':rc==0,'real_edge_launched':False,'pdf_fixture_is_unmodified_copy':pdf.read_bytes()==old_pdf.read_bytes(),'stdout':log.getvalue()})
raw=m.build_html('# fixture\n\n$\\frac{1}{3}$','UNFINISHED');assert '<title>UNFINISHED</title>' in raw and "document.title='MJDONE'" in raw and '<mjx-container' not in raw
run_case('script-marker-not-real-title',raw,True)
completed='<html><head><title>MJDONE</title></head><body><span class="math"><mjx-container jax="SVG"><svg></svg></mjx-container></span></body></html>'
run_case('old-valid-pdf-after-failed-print',completed,False)
undefined='<html><head><title>MJDONE</title></head><body><span class="math"><mjx-container jax="SVG"><svg><g data-mml-node="mtext" fill="red" stroke="red">\\t</g></svg></mjx-container></span></body></html>'
run_case('svg-red-undefined-command',undefined,True)
display='<html><head><title>MJDONE</title></head><body><div class="math-block">$$\\frac{1}{3}$$</div></body></html>'
run_case('unrendered-display-formula',display,True)
# A valid HTML only run also returns success for the warn-only --check branch.
d=fixture/'skip-pdf-check';d.mkdir();md=d/'check.md';md.write_bytes(b'$x$\n');log=io.StringIO()
with mock.patch.object(m,'run_edge',return_value=subprocess.CompletedProcess([],0,raw.encode(),b'')),contextlib.redirect_stdout(log):rc=m.main([str(md),'--out-dir',str(d),'--check','--skip-pdf'])
results.append({'case':'check-skip-pdf-warn-only','actual_tool_returncode':rc,'false_success':rc==0,'stdout':log.getvalue()})
# The merger neither hashes reports nor computes the declared batch/question/step counts.
d=fixture/'builder-tamper';d.mkdir();report=d/'tampered.md';report.write_bytes(b'# WRONG REPORT\n');sel={'schema':2,'hash_algorithm':'sha256-utf8-sig-splitlines-lf-v1','entries':[{'batch':'batch-01','report_path':report.name,'report_sha256':'0'*64,'count':1}]};(d/'draft-selection.json').write_bytes(json.dumps(sel).encode());builder.DRAFTS=d;builder.OUT=d/'merged.md';log=io.StringIO()
with contextlib.redirect_stdout(log):rc=builder.main()
results.append({'case':'report-hash-tamper-and-wrong-counts','actual_tool_returncode':rc,'false_success':rc==0,'declares_18_batches_264_questions_for_one_tampered_report':'18 批 / 264' in builder.OUT.read_text('utf-8'),'stdout':log.getvalue()})
# Record digest must bind the original BEFORE applying fields; a bad expected digest must block publication.
d=fixture/'record-binding-tamper';d.mkdir();batch=d/'batch-02';batch.mkdir();src=ROOT/'reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v4-final.jsonl';shutil.copyfile(src,batch/src.name)
original_sel=json.loads((OUT/'snapshot/reviews/2026-10-05-training-diversity-drafts/draft-selection.json').read_text('utf-8'));e=copy.deepcopy(next(e for e in original_sel['entries'] if e['batch']=='batch-02'));e['path']='batch-02/'+src.name;e['version']='codex-repair-v4-final';(d/'draft-selection.json').write_bytes(json.dumps({'schema':2,'entries':[e]}).encode())
patches=json.loads((ROOT/'reviews/codex-supervision/2026-10-05-draft-hash-compatibility/ready-row-separator-patches.json').read_text('utf-8'));p=copy.deepcopy(next(p for p in patches['records'] if p['batch']=='batch-02'));p['expected_record_sha256']='0'*64;patch=d/'bad-patch.json';patch.write_bytes(json.dumps({'records':[p]}).encode());publisher.DRAFTS=d;publisher.SEL=d/'draft-selection.json';publisher.PATCHES=patch;log=io.StringIO()
with contextlib.redirect_stdout(log):rc=publisher.main()
results.append({'case':'forged-expected-original-record-sha','actual_tool_returncode':rc,'false_success':rc==0,'new_version_created':(batch/'draft-codex-repair-v5.jsonl').exists(),'warning_only_instead_of_refusal':'[WARN]' in log.getvalue(),'stdout':log.getvalue()})
assert all(x['false_success'] for x in results),results
result={'frozen_sources_from_checkpoint':True,'original_project_source_not_modified':True,'browser_calls_simulated':True,'old_pdf_not_modified':True,'cases':results};(OUT/'negative-regressions.json').write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode());print(json.dumps([{'case':x['case'],'rc':x['actual_tool_returncode'],'false_success':x['false_success']} for x in results]))
# Parse actual new DOM structurally; CSS text and scripts never count as error nodes.
class Dom(HTMLParser):
 def __init__(self):super().__init__();self.title=False;self.title_text='';self.formulas=0;self.containers=0;self.red=0;self.errors=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='title':self.title=True
  if tag=='span' and 'math' in a.get('class','').split():self.formulas+=1
  if tag=='mjx-container':self.containers+=1
  if tag=='g' and a.get('data-mml-node')=='mtext' and a.get('fill')=='red':self.red+=1
  if a.get('data-mml-node')=='merror' or tag=='mjx-merror' or 'data-mjx-error' in a:self.errors+=1
 def handle_endtag(self,tag):
  if tag=='title':self.title=False
 def handle_data(self,text):
  if self.title:self.title_text+=text
p=ROOT/'outputs/draft-review/draft-review-selected-v5.static.html';bits=p.read_bytes();dom=Dom();dom.feed(bits.decode('utf-8'));actual={'path':p.relative_to(ROOT).as_posix(),'raw_sha256':hashlib.sha256(bits).hexdigest(),'actual_title':dom.title_text,'formula_wrappers':dom.formulas,'rendered_containers':dom.containers,'red_undefined_mtext_nodes':dom.red,'actual_error_nodes':dom.errors,'new_pdf_exists':(p.parent/'draft-review-selected-v5.pdf').exists()};(OUT/'v5-dom-check.json').write_bytes((json.dumps(actual,ensure_ascii=False,indent=2)+'\n').encode());print(json.dumps(actual,ensure_ascii=False))
