"""Coverage cannot be granted by a count, stale ledger or duplicate method rows."""
import unittest,tempfile,json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'src')]
from tools.training_data_policy import check_training_diversity
from tools import train_loop
from unittest import mock

class DiversityPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'reviews/codex-supervision/2026-10-05-mail-handling');self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.manifest=self.root/'manifest.json';self.policy=self.root/'policy.json';self.evidence=self.root/'evidence.json'
        raw=[];reviews=[]
        for i in range(5):
            row={'id':f't{i}','problem':f'distinct task {i}','category':'cat'};line=(json.dumps(row)+'\n').encode();raw.append(line)
            reviews.append({'id':row['id'],'concept_id':'C1','row_sha256':hashlib.sha256(line).hexdigest(),'user_review':'APPROVED','independent_math_verified':True,'independent_diversity_verified':True,'leakage_status':'CLEAR','variant_kind':['basic','boundary','inverse'][i%3]})
        source=self.root/'train.jsonl';source.write_bytes(b''.join(raw))
        self.write(self.manifest,{'entries':[{'path':source.name,'split':'train','sha256':self.sha(source)}]})
        self.write(self.policy,{'schema':1,'concepts':[{'id':'C1','category':'cat'}],'min_reviewed_samples_per_concept':5,'min_distinct_variant_kinds_per_concept':3})
        self.ledger={'schema':1,'status':'VERIFIED','manifest_sha256':self.sha(self.manifest),'policy_sha256':self.sha(self.policy),'record_reviews':reviews};self.save()
    def sha(self,p):return hashlib.sha256(p.read_bytes()).hexdigest()
    def write(self,p,x):p.write_text(json.dumps(x),encoding='utf8')
    def save(self):self.write(self.evidence,self.ledger)
    def check(self):return check_training_diversity(self.manifest,self.policy,self.evidence)
    def test_current_project_closed_before_snapshot_or_subprocess(self):
        with mock.patch('subprocess.run') as launch,mock.patch.object(train_loop,'prepare_snapshot') as snapshot:
            ok,reason=train_loop.gate_ready('density-block',{'dataset_manifest':str(ROOT/'data/manifest.json')})
        self.assertFalse(ok);self.assertIn('diversity',reason);launch.assert_not_called();snapshot.assert_not_called()
    def test_missing_evidence_fails_closed(self):
        self.evidence.unlink();self.assertFalse(self.check()[0])
    def test_bound_reviewed_diversity_can_pass_only_this_check(self):
        self.assertTrue(self.check()[0])
    def test_data_edit_invalidates_old_review(self):
        (self.root/'train.jsonl').write_text('{}\n',encoding='utf8');self.assertFalse(self.check()[0])
    def test_pending_math_or_known_overlap_blocks(self):
        for key,value in [('independent_math_verified',False),('independent_diversity_verified',False),('user_review','PENDING'),('leakage_status','KNOWN_OVERLAP')]:
            before=self.ledger['record_reviews'][0][key];self.ledger['record_reviews'][0][key]=value;self.save();self.assertFalse(self.check()[0]);self.ledger['record_reviews'][0][key]=before
    def test_extra_empty_concept_cannot_be_omitted(self):
        p=json.loads(self.policy.read_text());p['concepts'].append({'id':'C2','category':'cat'});self.write(self.policy,p);self.ledger['policy_sha256']=self.sha(self.policy);self.save();self.assertFalse(self.check()[0])
    def test_repeated_review_cannot_inflate_density(self):
        self.ledger['record_reviews'][-1]=self.ledger['record_reviews'][0];self.save();self.assertFalse(self.check()[0])
    def test_single_form_does_not_prove_diversity(self):
        for review in self.ledger['record_reviews']:review['variant_kind']='numeric-only'
        self.save();self.assertFalse(self.check()[0])
    def test_no_missing_active_row(self):
        self.ledger['record_reviews'].pop();self.save();self.assertFalse(self.check()[0])
    def test_policy_cannot_downgrade_minimum_to_one(self):
        p=json.loads(self.policy.read_text());p['min_reviewed_samples_per_concept']=1;self.write(self.policy,p);self.ledger['policy_sha256']=self.sha(self.policy);self.save();self.assertFalse(self.check()[0])
    def add_known_overlap_case(self):
        line=(json.dumps({'id':'q1','problem':'held-out query','category':'cat'})+'\n').encode()
        q=self.root/'eval.jsonl';q.write_bytes(line)
        m=json.loads(self.manifest.read_text());m['entries'].append({'path':q.name,'split':'eval','sha256':self.sha(q)});self.write(self.manifest,m)
        p=json.loads(self.policy.read_text());p['known_overlap_cases']=[{'train_id':'t0','query_id':'q1','query_row_sha256':hashlib.sha256(line).hexdigest()}];self.write(self.policy,p)
        self.ledger['manifest_sha256']=self.sha(self.manifest);self.ledger['policy_sha256']=self.sha(self.policy);self.save()

    def test_density_and_clear_flags_cannot_erase_known_overlap(self):
        self.add_known_overlap_case();ok,reason=self.check()
        self.assertFalse(ok);self.assertIn('Known train/held-out overlap',reason)

    def test_stale_case_does_not_override_changed_heldout_source(self):
        self.add_known_overlap_case();q=self.root/'eval.jsonl';q.write_text(json.dumps({'id':'q1','problem':'new reviewed task','category':'cat'})+'\n',encoding='utf8')
        m=json.loads(self.manifest.read_text());m['entries'][-1]['sha256']=self.sha(q);self.write(self.manifest,m)
        self.ledger['manifest_sha256']=self.sha(self.manifest);self.save();self.assertTrue(self.check()[0])

    def test_malformed_risk_ledger_fails_closed(self):
        p=json.loads(self.policy.read_text());p['known_overlap_cases']=[{}];self.write(self.policy,p)
        self.ledger['policy_sha256']=self.sha(self.policy);self.save();self.assertFalse(self.check()[0])

if __name__=='__main__':unittest.main()
