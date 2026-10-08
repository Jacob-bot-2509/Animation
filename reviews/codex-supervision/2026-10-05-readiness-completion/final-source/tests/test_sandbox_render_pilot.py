import hashlib,json,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from tools import sandbox_render_pilot as pilot

class SandboxPilotTests(unittest.TestCase):
    def setUp(self):
        base=pilot.ROOT/'reviews/codex-supervision/2026-10-05-readiness-completion/test-tmp';base.mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=base);self.addCleanup(self.temp.cleanup);self.base=Path(self.temp.name)
    def test_non_png_disguised_as_png_is_rejected(self):
        p=self.base/'bad.png';p.write_bytes(b'not an image')
        with self.assertRaises(Exception):pilot.decode_artifact(p,'png')
    def test_truncated_mp4_is_rejected(self):
        p=self.base/'bad.mp4';p.write_bytes(b'\x00\x00\x00\x18ftypisom')
        with self.assertRaises(Exception):pilot.decode_artifact(p,'mp4')
    def test_png_is_fully_loaded_and_hash_bound(self):
        from PIL import Image
        p=self.base/'good.png';Image.new('RGB',(3,2)).save(p);r=pilot.decode_artifact(p,'png')
        self.assertEqual((r['width'],r['height']),(3,2));self.assertTrue(r['decoded']);self.assertEqual(r['sha256'],hashlib.sha256(p.read_bytes()).hexdigest())
    def test_manifest_cannot_bind_changed_source(self):
        path=self.base/'rows.jsonl';path.write_text('{}\n',encoding='utf-8');mp=self.base/'manifest.json';mp.write_text(json.dumps({'entries':[{'split':'eval','path':path.name,'sha256':'0'*64}]}))
        with self.assertRaises(ValueError):pilot.load_records(mp,['eval'])
    def rec(self):return {'id':'test','_input_sha256':'a'*64,'problem':'$x$','answer':'$x$','scene_spec':{'steps':['一步']},'category':'测试'}
    def test_tex_file_access_is_rejected_before_spawn(self):
        rec=self.rec();rec['problem']=r'$\input{private}$'
        with patch.object(pilot.ac,'run_appcontainer') as spawn:
            r=pilot.render_one(rec,self.base/'scene',{},'mp4',1000)
        self.assertFalse(r['ok']);spawn.assert_not_called()
    def test_invalid_appcontainer_identity_cannot_pass(self):
        stdout=b'TOKEN_EVIDENCE={"api_ok":true,"is_appcontainer":false,"capability_count":0,"sid":"fake"}\n'
        with patch.object(pilot.ac,'run_appcontainer',return_value=subprocess.CompletedProcess([],0,stdout,b'')),patch.object(pilot.ac,'appcontainer_sid',return_value=b'x'),patch.object(pilot.ac,'_sid_sddl',return_value='expected'):
            r=pilot.render_one(self.rec(),self.base/'scene',{},'mp4',1000)
        self.assertFalse(r['ok']);self.assertIn('identity',r['error'])
    def test_process_success_without_final_media_cannot_pass(self):
        stdout=b'TOKEN_EVIDENCE={"api_ok":true,"is_appcontainer":true,"capability_count":0,"sid":"expected"}\n'
        with patch.object(pilot.ac,'run_appcontainer',return_value=subprocess.CompletedProcess([],0,stdout,b'')),patch.object(pilot.ac,'appcontainer_sid',return_value=b'x'),patch.object(pilot.ac,'_sid_sddl',return_value='expected'):
            r=pilot.render_one(self.rec(),self.base/'scene',{},'mp4',1000)
        self.assertFalse(r['ok']);self.assertIn('artifact',r['error'])
    def test_existing_work_cannot_supply_stale_artifact(self):
        work=self.base/'scene';work.mkdir()
        with patch.object(pilot.ac,'run_appcontainer') as spawn:r=pilot.render_one(self.rec(),work,{},'mp4',1000)
        self.assertFalse(r['ok']);spawn.assert_not_called()
    def test_spawn_timeout_cannot_pass(self):
        with patch.object(pilot.ac,'run_appcontainer',side_effect=subprocess.TimeoutExpired(['python'],1)):
            r=pilot.render_one(self.rec(),self.base/'scene',{},'mp4',1000)
        self.assertFalse(r['ok']);self.assertIn('TimeoutExpired',r['error'])
if __name__=='__main__':unittest.main()
