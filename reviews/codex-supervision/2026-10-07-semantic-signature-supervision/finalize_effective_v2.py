import json,hashlib,copy,datetime,re,difflib
from pathlib import Path
R=Path.cwd();D=R/'reviews/codex-supervision/2026-10-07-semantic-signature-supervision';N=D/'effective-core-v2';O=R/'reviews/codex-supervision/2026-10-07-continuous-math-review/current-core'
H=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def dense(v):return H(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
proof=read(N/'exact-proof.json');assert proof['symbolic_passed']==22 and all(c['passed'] for c in proof['symbolic_checks'])
idx=read(N/'current-index.json');idx['mathematical_review']='PASS_CURRENT_EXACT_TEXT_INHERITED_760_PLUS_NEW_1';write(N/'current-index.json',idx)
spec=read(D/'c18-revision-spec.json');after=read(N/'c18-after.json')
md='# draft-c18-02 修订题（同 ID，不增减题数）\n\n'+spec['problem']+'\n\n## 证明\n\n'+spec['solution']+'\n\n## 答案\n\n'+spec['answer']+'\n\n## 审核范围\n\n22 项精确符号检查及实定义域分支证明通过；题干、过程、答案和场景文字对应。原题与 test-geom-024 的同核心数值变式已改为交替投影的精确迭代与有限终止分类。本结论只关闭该具名配对问题，不能代替全局训练/评测隔离。新题视觉、浏览器排版与原生证据仍未验收，生产 CLOSED。\n'
(N/'draft-c18-02-corrected.md').write_text(md,encoding='utf8')
status={'schema':'effective-core-status-v2','scope':'CURRENT_CORE_761','records':761,'sources':24,'groups':idx['groups'],'changed_record_ids':['draft-c18-02'],
 'math_text':'PASS_CURRENT_EXACT_TEXT_INHERITED_760_PLUS_NEW_1','scene_text':'PASS_CURRENT_EXACT_TEXT_INHERITED_760_PLUS_NEW_1',
 'exact_new_checks':22,'manual_real_domain_implications':4,'known_pair_repair':'PASS_REVISED_PAIR_DISTINCT_CORE',
 'semantic_isolation':'NOT_ESTABLISHED','browser_typesetting_new_record':'NOT_RUN','visual':'NOT_INDEPENDENTLY_REVIEWED',
 'PDF':'NOT_RUN','native':'UNVERIFIED','production':'CLOSED','PASS_CORE_SCOPE_issued':False}
write(N/'CURRENT_STATUS.json',status)
(N/'README.md').write_text('# 核心候选继承版本 v2\n\n共 761 题、24 源；仅 draft-c18-02 改写，其他 760 条完整记录 SHA 不变，23 个源文件字节不变。父版本冻结清单 SHA 为 '+H((O/'delivery-manifest.json').read_bytes())+'。\n\n新题经过 22 项符号恒等式与 4 项实数分支论证。精确正文/场景文字复核通过；已确认的 c18-02 / test-geom-024 配对修复后核心不同。全局同核心隔离未建立，新题排版/视觉及原生验收未完成，生产 CLOSED，未发 PASS_CORE_SCOPE。\n\n签名与数学证明必须引用本版本 record-bindings.jsonl 的哈希；旧版本原件、历史风险及父证据保持可追溯。\n',encoding='utf8')
entries=[]
for p in sorted(N.rglob('*')):
 if p.is_file() and p.name!='delivery-manifest.json':
  raw=p.read_bytes();entries.append({'path':p.relative_to(N).as_posix(),'sha256':H(raw),'bytes':len(raw)})
manifest={'schema':'codex-frozen-core-successor-delivery-v2','scope':'CORE_SCOPE_ONLY','parent_manifest_sha256':H((O/'delivery-manifest.json').read_bytes()),
 'records':761,'sources':24,'changed_ids':['draft-c18-02'],'artifacts':entries,'production':'CLOSED','semantic_isolation':'NOT_ESTABLISHED'}
assert not (N/'delivery-manifest.json').exists();write(N/'delivery-manifest.json',manifest)
mh=H((N/'delivery-manifest.json').read_bytes())
tool=R/'tools/core_signatures.py';raw_before=tool.read_bytes();s=raw_before.decode('utf8')
s=s.replace('CORE=ROOT/"reviews/codex-supervision/2026-10-07-continuous-math-review/current-core"','CORE=ROOT/"'+N.relative_to(R).as_posix()+'"')
s=s.replace('CORE_MANIFEST_SHA256="972bd216b713bec7c48896e8f144d999dd6385b8c0e3e00a4c0116dfd1bbca22"','CORE_MANIFEST_SHA256="'+mh+'"')
s=s.replace('if path.is_relative_to(CORE):raise ValueError("Cannot write into frozen core")','if path.is_relative_to(CORE) or path.is_relative_to(ROOT/"reviews/codex-supervision/2026-10-07-continuous-math-review/current-core"):raise ValueError("Cannot write into frozen core or its frozen parent")')
assert 'CORE_MANIFEST_SHA256="'+mh+'"' in s
(D/'tool-before-successor-pin.py').write_bytes(raw_before);tool.write_text(s,encoding='utf8')
tests=R/'tests/test_core_signatures.py';test_before=tests.read_bytes()
marker='    def test_actual_761_records_and_24_sources_are_checked(self):'
add='    def test_old_frozen_parent_remains_protected(self):\n        parent=self.root/"reviews/codex-supervision/2026-10-07-continuous-math-review/current-core"\n        with self.assertRaises(ValueError):m.publish(parent/"new-unregistered-directory",{"x.txt":b"x"})\n        self.assertFalse(parent.exists())\n'
ts=test_before.decode('utf8');assert ts.count(marker)==1
(D/'tests-before-successor-pin.py').write_bytes(test_before);tests.write_text(ts.replace(marker,add+marker),encoding='utf8')
refs={x['id']:x for x in [json.loads(l) for l in (N/'record-bindings.jsonl').read_text(encoding='utf8').splitlines() if l.strip()]}
patches=read(D/'signature-patch-specs.json')
received=[json.loads(l) for l in (D/'received-complete-signatures.jsonl').read_text(encoding='utf8').splitlines() if l.strip()]
revised=[];reviews=[];changes=[]
for original in received:
 rid=original['id'];sig=copy.deepcopy(original);why=None
 if rid in patches:
  assert set(patches[rid]['fields'])<=set(['goal','domain','key_conditions','decisive_steps'])
  sig.update(patches[rid]['fields']);why=patches[rid]['reason']
 if rid=='draft-c18-02':
  sig.update(spec['signature']);sig.update({k:refs[rid][k] for k in ['group','record_sha256','math_sha256']})
  why='旧题与测试题同核心，题干/过程/答案/场景另版重写；本签名重新绑定修订数学版本。'
 assert sig['id']==rid and sig['group']==refs[rid]['group']
 assert sig['record_sha256']==refs[rid]['record_sha256'] and sig['math_sha256']==refs[rid]['math_sha256']
 revised.append(sig)
 row={'id':rid,'group':sig['group'],'before_signature_sha256':dense(original),'after_signature_sha256':dense(sig),
   'before_record_sha256':original['record_sha256'],'after_record_sha256':sig['record_sha256'],'before_math_sha256':original['math_sha256'],'after_math_sha256':sig['math_sha256'],
   'input_manifest_sha256':manifest['parent_manifest_sha256'],'output_manifest_sha256':mh,'mathematical_version_changed':rid=='draft-c18-02',
   'disposition':'PASS_SIGNATURE_FIDELITY_TO_CURRENT_TASK','review_basis':'Independent comparison of bound current problem with goal/domain/critical conditions/decisive steps; inspected exact proofs for flagged descriptions; prior exact mathematical review inherited for unchanged records.',
   'semantic_isolation':'NOT_ESTABLISHED','changed':why is not None,'rationale':why or '核心目标、对象/定义域及主要决定步骤与绑定题目相符；此项通过不等同跨集隔离。'}
 reviews.append(row)
 if why:changes.append({'id':rid,'rationale':why,'before':original,'after':sig,'verdict':'PASS_SIGNATURE_FIDELITY_TO_CURRENT_TASK'})
assert len(revised)==len(reviews)==761 and len(changes)==67
(D/'revised-complete-signatures-v2.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in revised),encoding='utf8')
(D/'signature-review.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in reviews),encoding='utf8')
write(D/'signature-before-after.json',changes)
write(D/'successor-pin.json',{'core_path':N.relative_to(R).as_posix(),'core_manifest_sha256':mh,'changed_signature_records':67,'descriptor_only_changes':66,
 'changed_mathematical_records':1,'unchanged_full_records':760,'signature_records':761,'tool_sha256':H(tool.read_bytes()),'test_sha256':H(tests.read_bytes())})
print(json.dumps({'core_manifest_sha256':mh,'signature_changes':67,'tool_sha256':H(tool.read_bytes()),'tests_sha256':H(tests.read_bytes())}))
