"""Positive and negative regressions: no GPU, model load or production admission."""
import copy,hashlib,json,sys,tempfile,unittest,subprocess,shutil
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'tools'),str(ROOT/'src')]
from tools import review_guard as guard,render_review as render,build_review_pdf as builder,publish_row_patches as publisher,train_loop as loop,train_step as train,eval_step as evaluate
from tools.draft_io import fingerprint,NORMALIZED_HASH

def done(content):return '<html><head><title>MJDONE</title></head><body>'+content+'</body></html>'
INLINE='<span class="math"><mjx-container jax="SVG"><svg></svg></mjx-container></span>'
DISPLAY='<div class="math-block"><mjx-container jax="SVG"><svg></svg></mjx-container></div>'

class ReviewGuardTests(unittest.TestCase):
 def test_inline_and_display_valid_with_styles_not_errors(self):
  self.assertEqual(guard.verify_dom(done('<style>.mjx-merror { color:red; }</style>'+INLINE+DISPLAY),1,1),(0,2,0))
 def test_script_marker_does_not_certify_title(self):
  with self.assertRaises(ValueError):guard.verify_dom('<title>pending</title><script>document.title="MJDONE"</script>'+INLINE,1,0)
 def test_quoted_title_in_script_is_ignored(self):
  with self.assertRaises(ValueError):guard.verify_dom('<script>"<title>MJDONE</title>"</script>'+INLINE,1,0)
 def test_svg_red_undefined_command(self):
  with self.assertRaises(ValueError):guard.verify_dom(done(INLINE.replace('<svg></svg>','<svg><g data-mml-node="mtext" fill="red" stroke="red">\\t</g></svg>')),1,0)
 def test_unrendered_display(self):
  with self.assertRaises(ValueError):guard.verify_dom(done('<div class="math-block">$$x$$</div>'),0,1)
 def test_expected_formula_count(self):
  with self.assertRaises(ValueError):guard.verify_dom(done(INLINE),2,0)
 def test_multiple_containers_in_one_wrapper(self):
  with self.assertRaises(ValueError):guard.verify_dom(done(INLINE.replace('</span>',INLINE+'</span>')),1,0)
 def test_merror_real_node(self):
  with self.assertRaises(ValueError):guard.verify_dom(done(INLINE+'<g data-mml-node="merror"></g>'),1,0)
 def test_fake_pdf_header_and_eof_are_insufficient(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'fake.pdf';p.write_bytes(b'%PDF-1.7\n%%EOF\n')
   with self.assertRaises(ValueError):guard.validate_pdf(p)
 def test_check_skip_pdf_rejects_display_and_missing_title(self):
  for dom in [done('<div class="math-block">$$x$$</div>'),'<title>pending</title><script>MJDONE</script>'+DISPLAY]:
   with tempfile.TemporaryDirectory() as td:
    p=Path(td)/'input.md';p.write_text('$$x$$',encoding='utf8')
    with mock.patch.object(render,'run_edge',return_value=subprocess.CompletedProcess([],0,dom.encode(),b'')):
     self.assertNotEqual(render.main([str(p),'--out-dir',str(Path(td)/'out'),'--check','--skip-pdf']),0)
 def test_stale_pdf_rejected_unchanged_before_browser(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'input.md';p.write_text('$x$',encoding='utf8');pdf=Path(td)/'input.pdf';pdf.write_bytes(b'OLD')
   with mock.patch.object(render,'run_edge') as browser:self.assertNotEqual(render.main([str(p),'--out-dir',td]),0)
   browser.assert_not_called();self.assertEqual(pdf.read_bytes(),b'OLD')
 def test_valid_pdf_published_from_unique_target(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td);p=d/'input.md';p.write_text('$x$',encoding='utf8')
   def edge(args,**kw):
    if '--dump-dom' in args:return subprocess.CompletedProcess(args,0,done(INLINE).encode(),b'')
    target=Path(next(a.split('=',1)[1] for a in args if a.startswith('--print-to-pdf=')))
    self.assertNotEqual(target,d/'input.pdf');self.assertFalse(target.exists());shutil.copyfile(ROOT/'outputs/draft-review/draft-review-v4-final.pdf',target)
    return subprocess.CompletedProcess(args,0,b'',b'')
   with mock.patch.object(render,'run_edge',side_effect=edge):self.assertEqual(render.main([str(p),'--out-dir',td]),0)
   receipt=json.loads((d/'input.render.json').read_text());self.assertEqual(receipt['pages'],103);self.assertEqual(receipt['pdf_sha256'],hashlib.sha256((d/'input.pdf').read_bytes()).hexdigest())

class PublicationTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.d=Path(self.tmp.name);batch=self.d/'batch-01';batch.mkdir()
  self.row={'id':'q1','problem':'$x=1/3$','solution':'$3x=1$','answer':'$1/3$','scene_spec':{'objects':['point'],'steps':['draw $x=1/3$']},'versioned_id':'old-q1','strict_review':{},'revision_lineage':{},'admitted':False,'render_verified':False}
  self.source=batch/'draft-old.jsonl';self.source.write_text(json.dumps(self.row)+'\n',encoding='utf8');fp=fingerprint(self.source.read_bytes())
  self.report=batch/'report.md';self.report.write_text('# report\n\n## q1 · C\n\n'+builder.report_body(self.row)+'\n',encoding='utf8');rfp=fingerprint(self.report.read_bytes())
  self.entry={'batch':'batch-01','path':'batch-01/draft-old.jsonl','count':1,'version':'old',**fp,'report_path':'batch-01/report.md','report_sha256':rfp['sha256'],'report_raw_sha256':rfp['raw_sha256'],'report_hash_algorithm':NORMALIZED_HASH}
  self.selection={'schema':2,'hash_algorithm':NORMALIZED_HASH,'entries':[self.entry]};self.save_selection()
  fields={'answer':'$x=1/3$'};after=copy.deepcopy(self.row);after.update(fields)
  self.patch={'batch':'batch-01','id':'q1','fields':fields,'expected_selected_path':self.entry['path'],'expected_selected_sha256':fp['sha256'],'expected_selected_raw_sha256':fp['raw_sha256'],'expected_hash_algorithm':NORMALIZED_HASH,'expected_record_sha256':publisher.sorted_sha(self.row),'new_math_content_sha256':publisher.sorted_sha({k:after[k] for k in publisher.MATH_FIELDS})}
  self.patch_path=self.d/'patches.json';self.save_patches([self.patch])
 def tearDown(self):self.tmp.cleanup()
 def save_selection(self):(self.d/'draft-selection.json').write_text(json.dumps(self.selection),encoding='utf8')
 def save_patches(self,patches):self.patch_path.write_text(json.dumps({'records':patches}),encoding='utf8')
 def test_merge_dynamic_count_and_exact_content(self):
  out=self.d/'merged.md';self.assertEqual(builder.merge(self.d,out),{'batches':1,'questions':1,'steps':1});self.assertIn('1 批 / 1 题',out.read_text('utf8'))
 def test_report_hash_tamper_blocks_before_output(self):
  self.report.write_text('BAD',encoding='utf8')
  with self.assertRaises(ValueError):builder.merge(self.d,self.d/'merged.md')
  self.assertFalse((self.d/'merged.md').exists())
 def test_report_algorithm_rejected(self):
  self.entry['report_hash_algorithm']='unknown';self.save_selection()
  with self.assertRaises(ValueError):builder.merge(self.d,self.d/'merged.md')
 def test_report_root_escape_rejected(self):
  self.entry['report_path']='../outside.md';self.save_selection()
  with self.assertRaises(ValueError):builder.merge(self.d,self.d/'merged.md')
 def test_signed_report_wrong_answer_still_rejected(self):
  self.report.write_text(self.report.read_text('utf8').replace('**答案**\n\n$1/3$','**答案**\n\n$7$'),encoding='utf8');fp=fingerprint(self.report.read_bytes());self.entry.update(report_sha256=fp['sha256'],report_raw_sha256=fp['raw_sha256']);self.save_selection()
  with self.assertRaises(ValueError):builder.merge(self.d,self.d/'merged.md')
 def test_duplicate_batches_rejected(self):
  self.selection['entries'].append(copy.deepcopy(self.entry));self.save_selection()
  with self.assertRaises(ValueError):builder.merge(self.d,self.d/'merged.md')
 def test_prepatch_hash_tamper_creates_nothing(self):
  self.patch['expected_record_sha256']='0'*64;self.save_patches([self.patch]);old=(self.d/'draft-selection.json').read_bytes()
  with self.assertRaises(ValueError):publisher.publish(self.d,self.patch_path,'new')
  self.assertEqual((self.d/'draft-selection.json').read_bytes(),old);self.assertFalse((self.d/'batch-01/draft-new.jsonl').exists())
 def test_result_math_hash_tamper_creates_nothing(self):
  self.patch['new_math_content_sha256']='0'*64;self.save_patches([self.patch])
  with self.assertRaises(ValueError):publisher.publish(self.d,self.patch_path,'new')
  self.assertFalse((self.d/'batch-01/draft-new.jsonl').exists())
 def test_late_bad_batch_prevalidated_before_first_publication(self):
  batch=self.d/'batch-02';batch.mkdir();row=copy.deepcopy(self.row);row['id']='q2';source=batch/'draft-old.jsonl';source.write_text(json.dumps(row)+'\n',encoding='utf8');fp=fingerprint(source.read_bytes())
  report=batch/'report.md';report.write_text('## q2 · C\n\n'+builder.report_body(row)+'\n',encoding='utf8');rfp=fingerprint(report.read_bytes());entry=copy.deepcopy(self.entry);entry.update(batch='batch-02',path='batch-02/draft-old.jsonl',report_path='batch-02/report.md',**fp,report_sha256=rfp['sha256'],report_raw_sha256=rfp['raw_sha256']);self.selection['entries'].append(entry);self.save_selection()
  second=copy.deepcopy(self.patch);second.update(batch='batch-02',id='q2',expected_selected_path=entry['path'],expected_selected_sha256=fp['sha256'],expected_selected_raw_sha256=fp['raw_sha256'],expected_record_sha256='0'*64);self.save_patches([self.patch,second])
  with self.assertRaises(ValueError):publisher.publish(self.d,self.patch_path,'new')
  self.assertFalse((self.d/'batch-01/draft-new.jsonl').exists());self.assertFalse((batch/'draft-new.jsonl').exists())
 def test_valid_publication_new_version_and_merge(self):
  old=self.source.read_bytes();publisher.publish(self.d,self.patch_path,'new');self.assertEqual(self.source.read_bytes(),old)
  rows=publisher.rows_at(self.d/'batch-01/draft-new.jsonl');self.assertEqual(rows[0]['answer'],'$x=1/3$');self.assertFalse(rows[0]['admitted']);self.assertEqual(rows[0]['revision_lineage']['previous_selected_version']['version'],'old')
  builder.merge(self.d,self.d/'new-review.md')
 def test_overwrite_report_rejected_before_jsonl(self):
  (self.d/'batch-01/DRAFT_REPORT-new.md').write_text('old')
  with self.assertRaises(ValueError):publisher.publish(self.d,self.patch_path,'new')
  self.assertFalse((self.d/'batch-01/draft-new.jsonl').exists())
 def test_historical_publishers_fail_closed(self):
  from tools import apply_row_patches_v5,apply_row_patches_v6
  self.assertNotEqual(apply_row_patches_v5.main(),0);self.assertNotEqual(apply_row_patches_v6.main(),0)

class HarnessTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.d=Path(self.tmp.name);self.work=self.d/'round';self.work.mkdir();(self.work/'adapter').mkdir();(self.work/'adapter/a').write_text('adapter')
  hp={'learning_rate':'1/5000','batch_size':2,'gradient_accumulation_steps':4,'epochs':6,'lora_r':8,'lora_alpha':16,'max_seq_length':2048,'quantization':'4bit','seed':42}
  self.config={'hyperparameters':hp,'hyperparameter_approval':{'status':'CONFIRMED','sha256':hashlib.sha256(json.dumps(hp,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()}}
  entries=[]
  for split,n in [('eval',2),('test',1)]:
   p=self.d/f'{split}.jsonl';p.write_text('\n'.join(json.dumps({'id':f'{split}{i}'}) for i in range(n))+'\n');entries.append({'split':split,'path':p.name})
  self.manifest=self.d/'manifest.json';self.manifest.write_text(json.dumps({'entries':entries}));self.config['dataset_manifest']=str(self.manifest)
  cp=self.d/'config.json';cp.write_text(json.dumps(self.config));self.config['_config_path']=str(cp)
  (self.work/'training-manifest.json').write_text('{}');(self.work/'generated-specs.json').write_text('[]')
  self.report={'run_id':'run','bindings':self.bindings(),'by_split':{},'math':{'status':'UNVERIFIED'},'fidelity':{'status':'UNVERIFIED'}}
  for k in ('render','executable'):
   self.report[k]={'status':'VERIFIED','passed':3,'total':3,'rate':'1'}
   for sp,n in [('eval',2),('test',1)]:self.report['by_split'].setdefault(sp,{})[k]={'status':'VERIFIED','passed':n,'total':n,'rate':'1'}
 def tearDown(self):self.tmp.cleanup()
 def bindings(self):return {'config_sha256':loop._sha(Path(self.config['_config_path'])),'manifest_sha256':loop._sha(self.manifest),'training_manifest_sha256':loop._sha(self.work/'training-manifest.json'),'generated_specs_sha256':loop._sha(self.work/'generated-specs.json'),'adapter_sha256':loop.adapter_hash(self.work/'adapter')}
 def test_valid_exact_bound_split_metrics(self):self.assertEqual(loop.report_metrics(self.report,'run',self.config,self.work)['executable'],'1')
 def test_wrong_run_rejected(self):
  with self.assertRaises(ValueError):loop.report_metrics(self.report,'other',self.config,self.work)
 def test_changed_adapter_rejected(self):
  (self.work/'adapter/a').write_text('different')
  with self.assertRaises(ValueError):loop.report_metrics(self.report,'run',self.config,self.work)
 def test_unknown_status_with_rate_one_rejected(self):
  self.report['render']['status']='UNVERIFIED'
  with self.assertRaises(ValueError):loop.report_metrics(self.report,'run',self.config,self.work)
 def test_metric_fraction_must_equal_counts(self):
  self.report['render']['rate']='19/20'
  with self.assertRaises(ValueError):loop.report_metrics(self.report,'run',self.config,self.work)
 def test_partial_split_cannot_fake_aggregate_success(self):
  self.report['by_split'].pop('test')
  with self.assertRaises(ValueError):loop.report_metrics(self.report,'run',self.config,self.work)
 def test_subprocess_timeout_has_round_log_and_markdown(self):
  with mock.patch.object(loop,'RUNS',self.d/'runs'),mock.patch.object(loop,'STOP_FILE',self.d/'stop'),mock.patch.object(loop,'gate_ready',side_effect=subprocess.TimeoutExpired('gate',1)):
   self.assertEqual(loop.run_loop(self.config),2)
  work=next((self.d/'runs').iterdir());rec=json.loads((work/'round-1.json').read_text());self.assertEqual(rec['event'],'round_failed');self.assertTrue((work/'round-1.md').exists());self.assertIn('TimeoutExpired',(work/'log.jsonl').read_text())
 def test_complete_bound_round_writes_audit_and_manual_queue(self):
  def fake_train(config,work,run_id):
   (work/'adapter').mkdir();(work/'adapter/a').write_text('trained')
   training={'status':'TRAINED','run_id':run_id,'config_sha256':loop._sha(Path(config['_config_path'])),'manifest_sha256':loop._sha(self.manifest),'adapter_sha256':loop.adapter_hash(work/'adapter')}
   (work/'training-manifest.json').write_text(json.dumps(training));return {'status':'TRAINED'}
  def fake_eval(config,work,adapter,run_id):
   (work/'generated-specs.json').write_text('[]');report=copy.deepcopy(self.report);report['run_id']=run_id
   report['bindings']={'config_sha256':loop._sha(Path(config['_config_path'])),'manifest_sha256':loop._sha(self.manifest),'training_manifest_sha256':loop._sha(work/'training-manifest.json'),'generated_specs_sha256':loop._sha(work/'generated-specs.json'),'adapter_sha256':loop.adapter_hash(adapter)}
   (work/'eval-report.json').write_text(json.dumps(report));return {'status':'OK'}
  with mock.patch.object(loop,'RUNS',self.d/'runs'),mock.patch.object(loop,'STOP_FILE',self.d/'stop'),mock.patch.object(loop,'gate_ready',return_value=(True,'fixture only')),mock.patch.object(loop,'train_step',side_effect=fake_train),mock.patch.object(loop,'eval_step',side_effect=fake_eval):
   self.assertEqual(loop.run_loop(self.config),0)
  work=next((self.d/'runs').iterdir());rec=json.loads((work/'round-1.json').read_text());self.assertEqual(rec['final_verdict'],'stop_target_met');self.assertEqual(rec['report'],'round-1/eval-report.json');self.assertTrue(rec['report_sha256']);self.assertTrue((work/'log.jsonl').exists());self.assertTrue(json.loads((work/'hard-queue.json').read_text()))
 def test_evidence_disk_error_stops_without_unhandled_exception(self):
  with mock.patch.object(loop,'RUNS',self.d/'runs'),mock.patch.object(loop,'STOP_FILE',self.d/'stop'),mock.patch.object(loop,'gate_ready',return_value=(False,'closed')),mock.patch.object(loop,'persist_round',side_effect=OSError('disk full')):
   self.assertEqual(loop.run_loop(self.config),2)
 def test_relative_paths_resolve_from_project_not_shell(self):self.assertEqual(loop.project_path('data/manifest.json'),ROOT/'data/manifest.json')
 def test_invalid_fractional_integer_hyperparameter_rejected(self):
  self.config['hyperparameters']['epochs']='3/2';self.assertIn('integer',train.hyperparameter_approval_error(self.config))
 def test_unreviewed_execution_scripts_never_launched(self):
  with mock.patch('subprocess.run') as process:
   self.assertEqual(evaluate.render_check({'render_executor':'../other.py'},self.work,[])['status'],'UNVERIFIED');self.assertEqual(evaluate.judge({'judge_script':'../other.py'},self.work,[])['status'],'UNVERIFIED')
  process.assert_not_called()

if __name__=='__main__':unittest.main()
