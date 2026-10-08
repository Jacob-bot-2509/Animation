"""Regression checks without model loading, GPU work or gate opening."""
import json,sys,unittest
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'src')]
from tools import train_step as ts,train_loop as tl,eval_step as es

class FakeTokenizer:
    def apply_chat_template(self,messages,**kwargs):
        # A fixed fake chat boundary exposes exactly which target tokens get labels.
        prefix=[11,12,13]
        return {"input_ids":prefix if len(messages)==1 else prefix+[ord(c) for c in messages[1]['content']]+[99]}

class TrainingReadinessTests(unittest.TestCase):
    def row(self):return {'id':'train-a','problem':'P','solution':'S',
        'scene_spec':{'objects':['curve'],'steps':['draw curve']}}

    def test_prompt_json_braces_format_without_error(self):
        for prompt in (ts.PROMPT_TMPL,es.GEN_PROMPT):
            text=prompt.format(problem='P',solution='S',method='M')
            self.assertIn('"objects"',text);self.assertIn('题目:P',text)

    def test_target_is_supervised_and_prompt_masked(self):
        example=ts.training_example(FakeTokenizer(),self.row(),200)
        self.assertEqual(example['labels'][:3],[-100]*3)
        self.assertEqual(example['labels'][3:],example['input_ids'][3:])
        text=''.join(chr(c) for c in example['input_ids'][3:-1])
        self.assertEqual(json.loads(text),self.row()['scene_spec'])
        self.assertEqual(example['labels'][-1],99)  # EOS is retained.

    def test_complete_target_cannot_be_silently_truncated(self):
        with self.assertRaises(ValueError):ts.training_example(FakeTokenizer(),self.row(),4)

    def test_missing_target_is_rejected(self):
        row=self.row();row.pop('scene_spec')
        with self.assertRaises(ValueError):ts.training_example(FakeTokenizer(),row,200)

    def test_nonprefix_chat_template_fails_closed(self):
        tokenizer=FakeTokenizer();tokenizer.apply_chat_template=mock.Mock(side_effect=[{"input_ids":[1]},{"input_ids":[2,3]}])
        with self.assertRaises(ValueError):ts.training_example(tokenizer,self.row(),200)

    def test_direct_training_call_checks_gate_before_config_and_imports(self):
        with mock.patch.object(tl,'gate_ready',return_value=(False,'closed')) as gate:
            result=ts.train({},ROOT/'runs/never-created-by-test','test-gate')
        self.assertEqual(result['status'],'REFUSED');gate.assert_called_once()

    def test_changed_manifest_cannot_reuse_current_readiness(self):
        with mock.patch('subprocess.run') as process:
            self.assertFalse(tl.gate_ready('id',{'dataset_manifest':str(ROOT/'different.json')})[0])
        process.assert_not_called()

    def test_unknown_invalid_or_out_of_range_metrics_never_stop_success(self):
        for value in (None,True,'NaN','inf','2','-1','invalid'):
            with self.subTest(value=value):self.assertFalse(tl.metrics_met({'render':1,'executable':value}))
        self.assertTrue(tl.metrics_met({'render':'1','executable':'19/20'}))
        self.assertFalse(tl.metrics_met({'render':'1','executable':'9/10'}))

    def test_three_rounds_without_improvement_require_four_checkpoints(self):
        h=[{'metrics':{'render':'1/2','executable':'1/2','math':None,'fidelity':None}} for _ in range(4)]
        self.assertFalse(tl.plateau(h[:3]));self.assertTrue(tl.plateau(h))
        h[-1]['metrics']['render']='3/4';self.assertFalse(tl.plateau(h))

    def test_schema_is_not_execution_and_method_rows_group_by_question(self):
        rows=[{'split':'eval','problem_id':'same','sample_id':'e1','row_index':0,'schema_ok':True},
              {'split':'eval','problem_id':'same','sample_id':'e2','row_index':1,'schema_ok':False},
              {'split':'test','problem_id':'same','sample_id':'t1','row_index':2,'schema_ok':True}]
        report=es.aggregate(rows,{'status':'OK','rc':0},{'status':'OK','rc':0})
        self.assertEqual(report['total_questions'],2);self.assertEqual(report['schema']['rate'],'1/2')
        self.assertEqual(report['by_split']['eval']['schema']['rate'],'0')
        self.assertEqual(report['by_split']['test']['schema']['rate'],'1')
        for key in ('render','executable','math','fidelity'):self.assertIsNone(report[key]['rate'])

    def test_direct_evaluation_blocks_before_model_generation(self):
        with mock.patch.object(tl,'gate_ready',return_value=(False,'closed')), \
             mock.patch.object(es,'generate') as generate, \
             mock.patch.object(Path,'read_text',return_value='{}'):
            self.assertEqual(es.run(ROOT/'synthetic-config.json',ROOT/'runs/never',ROOT/'adapter','blocked'),2)
        generate.assert_not_called()

    def test_snapshot_rejects_missing_actual_config_without_launch(self):
        with mock.patch('subprocess.run') as process:
            self.assertFalse(tl.prepare_snapshot('test',{},ROOT/'data/manifest.json')[0])
        process.assert_not_called()

    def test_snapshot_rejects_run_id_traversal_before_reading(self):
        with mock.patch.object(Path,'read_text') as read:
            self.assertFalse(tl.prepare_snapshot('../escape',{},ROOT/'data/manifest.json')[0])
        read.assert_not_called()

    def test_unreviewed_executor_is_not_launched(self):
        with mock.patch('subprocess.run') as process:
            self.assertEqual(tl.train_step({'train_script':'other.py'},ROOT/'runs/x','id')['rc'],2)
            self.assertEqual(tl.eval_step({'eval_script':'other.py'},ROOT/'runs/x',ROOT/'adapter','id')['rc'],2)
        process.assert_not_called()

class HyperparameterApprovalTests(unittest.TestCase):
    def config(self):
        return {'hyperparameters':{'learning_rate':'1/5000','batch_size':2,
            'gradient_accumulation_steps':8,'epochs':3,'lora_r':16,'lora_alpha':32,
            'max_seq_length':2048,'quantization':'4bit','seed':42}}

    def confirmed(self):
        import hashlib
        c=self.config();payload=json.dumps(c['hyperparameters'],ensure_ascii=False,
            sort_keys=True,separators=(',',':')).encode('utf8')
        c['hyperparameter_approval']={'status':'CONFIRMED','sha256':hashlib.sha256(payload).hexdigest()}
        return c

    def test_proposal_fields_do_not_authorize_model_loading(self):
        c=self.config()
        with mock.patch.object(tl,'gate_ready',return_value=(True,'ready')),mock.patch.object(ts,'load_train_rows') as rows:
            result=ts.train(c,ROOT/'runs/not-created','approval-test')
        self.assertEqual(result['status'],'REFUSED');self.assertIn('proposal',result['reason']);rows.assert_not_called()

    def test_confirmed_parameters_are_bound_to_exact_values(self):
        c=self.confirmed();self.assertIsNone(ts.hyperparameter_approval_error(c))
        c['hyperparameters']['lora_r']=8
        self.assertIn('stale',ts.hyperparameter_approval_error(c))

    def test_flag_without_hash_is_rejected(self):
        c=self.config();c['hyperparameter_approval']={'status':'CONFIRMED'}
        self.assertIn('missing',ts.hyperparameter_approval_error(c))

    def test_loop_proposal_stops_before_work_or_gate(self):
        with mock.patch.object(Path,'mkdir') as mkdir,mock.patch.object(tl,'gate_ready') as gate:
            self.assertEqual(tl.run_loop(self.config()),2)
        mkdir.assert_not_called();gate.assert_not_called()

    def test_cli_proposal_stops_before_work_or_training(self):
        with mock.patch.object(Path,'read_text',return_value=json.dumps(self.config())),mock.patch.object(Path,'mkdir') as mkdir,mock.patch.object(ts,'train') as train:
            self.assertEqual(ts.main(['--config','proposal.json','--work','never','--run-id','no-training']),2)
        mkdir.assert_not_called();train.assert_not_called()

    def test_sweep_proposal_stops_before_subset_or_model_work(self):
        from tools import hp_sweep as hs
        sweep={'candidates':[dict(self.config(),name='unconfirmed')]}
        with mock.patch.object(Path,'read_text',return_value=json.dumps(sweep)),mock.patch.object(Path,'mkdir') as mkdir,mock.patch.object(hs,'build_subset') as subset:
            self.assertEqual(hs.main(['--config','proposal.json']),2)
        mkdir.assert_not_called();subset.assert_not_called()

if __name__=='__main__':unittest.main()
