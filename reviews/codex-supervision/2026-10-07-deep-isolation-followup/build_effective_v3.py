"""Build a four-record mathematical successor without changing the frozen parent."""
from pathlib import Path
import copy,hashlib,importlib.util,json,datetime

ROOT=Path(__file__).resolve().parents[3]
REVIEW=Path(__file__).resolve().parent
PARENT=ROOT/'reviews/codex-supervision/2026-10-07-semantic-signature-supervision/effective-core-v2'
CORE=REVIEW/'effective-core-v3'
PARENT_SHA='78017f740969cd251f6c263bdcb14ef1bb5bd63de939df394fa24e33e57df4b5'
assert hashlib.sha256((PARENT/'delivery-manifest.json').read_bytes()).hexdigest()==PARENT_SHA
s=importlib.util.spec_from_file_location('bound_parent_core',ROOT/'tools/core_signatures.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
bindings=m.load_record_bindings()
old_by={b['id']:b for b in bindings}
sources=m.read_json((PARENT/'source-bindings.json').read_bytes())
specs={x['id']:x for x in m.read_json((REVIEW/'math-revision-specs.json').read_bytes())}
assert len(specs)==4
assert not CORE.exists()
CORE.mkdir()
new_sources,new_bindings,changed,unchanged=[],[],[],[]
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
for source in sources:
    old_path=ROOT/source['path']
    raw=old_path.read_bytes()
    lines=raw.splitlines(keepends=True)
    assert all(line.strip() for line in lines)
    current=[]
    for line in lines:
        r=m.read_json(line)
        before=copy.deepcopy(r)
        rid=r['id']
        if rid in specs:
            spec=specs[rid]
            for k in ('problem','solution','answer','scene_spec'):r[k]=spec[k]
            r['method']=spec['method']
            if 'concept' in r:r['concept']=spec['goal']
            if 'variant_kind' in r:r['variant_kind']='structural-isolation-rewrite'
            if 'versioned_id' in r:r['versioned_id']=rid+':codex-deep-v3'
            if 'admitted' in r:r['admitted']=False
            if 'animation_render_verified' in r:r['animation_render_verified']=False
            if 'review_status' in r:r['review_status']='PASS_MATH_SCENE_TEXT_CANDIDATE_ONLY'
            r['deep_core_revision']={'reviewed_at':now,'parent_record_sha256':old_by[rid]['record_sha256'],'parent_math_sha256':old_by[rid]['math_sha256'],'parent_core_manifest_sha256':PARENT_SHA,'reason':'Same/embedded evaluation core removed with actual task and proof revision','new_render':'NOT_RUN','production':'CLOSED'}
            if isinstance(r.get('revision_lineage'),list):
                r['revision_lineage'].append(r['deep_core_revision'])
            changed.append({'id':rid,'before':before,'after':r})
            current.append((json.dumps(r,ensure_ascii=False)+'\n').encode('utf-8'))
        else:
            unchanged.append(rid)
            current.append(line)
    newraw=b''.join(current)
    target=CORE/'candidate-sources'/old_path.relative_to(PARENT/'candidate-sources')
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(newraw)
    records=m.read_rows(newraw)
    relative=target.relative_to(ROOT).as_posix()
    new_sources.append({'path':relative,'sha256':m.digest(newraw),'bytes':len(newraw),'records':len(records),'group':source['group'],'parent_path':source['path'],'parent_sha256':source['sha256'],'unchanged_source_bytes':raw==newraw})
    for line_no,r in enumerate(records,1):
        old=old_by[r['id']]
        b={**old,'path':relative,'source_line':line_no,'source_sha256':m.digest(newraw),'record_sha256':m.dense(r),'math_sha256':m.math_digest(r),'parent_record_sha256':old['record_sha256'],'parent_math_sha256':old['math_sha256'],'review':'EXACT_NEW_REWRITE' if r['id'] in specs else 'INHERITED_IDENTICAL_COMPLETE_RECORD'}
        if r['id'] not in specs:assert b['record_sha256']==old['record_sha256']
        new_bindings.append(b)
assert len(new_bindings)==761 and len(new_sources)==24 and len(unchanged)==757 and len(changed)==4
assert {b['id'] for b in new_bindings}==set(old_by)
def write(name,obj): (CORE/name).write_bytes(m.encoded(obj))
write('source-bindings.json',new_sources)
(CORE/'record-bindings.jsonl').write_bytes(b''.join((json.dumps(b,ensure_ascii=False)+'\n').encode('utf-8') for b in new_bindings))
groups={g:sum(b['group']==g for b in new_bindings) for g in m.EXPECTED_GROUPS}
assert groups==m.EXPECTED_GROUPS
write('current-index.json',{'schema':'current-core-successor-v3','records':761,'sources':24,'groups':groups,'source_bindings_sha256':m.digest((CORE/'source-bindings.json').read_bytes()),'record_bindings_sha256':m.digest((CORE/'record-bindings.jsonl').read_bytes()),'parent_core':PARENT.relative_to(ROOT).as_posix(),'parent_manifest_sha256':PARENT_SHA,'changed_ids':sorted(specs),'unchanged_record_bodies':757,'semantic_isolation':'NOT_ESTABLISHED','production':'CLOSED'})
write('inheritance-receipt.json',{'parent_manifest_sha256':PARENT_SHA,'unchanged_complete_records':757,'changed_records':4,'unchanged_ids':unchanged,'changed_ids':sorted(specs),'unchanged_source_files':sum(s['unchanged_source_bytes'] for s in new_sources),'old_render_not_applicable_ids':['draft-c18-02',*sorted(specs)],'semantic_isolation':'NOT_ESTABLISHED','production':'CLOSED'})
write('mathematical-before-after.json',changed)
for c in changed:
    r=c['after']
    (CORE/(r['id']+'-corrected.md')).write_text('# '+r['id']+' 精确修订候选\n\n'+r['problem']+'\n\n## 证明与过程\n\n'+r['solution']+'\n\n## 答案\n\n'+r['answer']+'\n\n## 场景文字\n\n'+'\n\n'.join(r['scene_spec']['steps'])+'\n',encoding='utf-8')
new_by={b['id']:b for b in new_bindings}
sigpath=ROOT/'reviews/codex-supervision/2026-10-07-semantic-signature-supervision/revised-complete-signatures-v2.jsonl'
sigs=m.read_rows(sigpath.read_bytes())
for sig in sigs:
    rid=sig['id']
    if rid in specs:
        x=specs[rid]
        sig.update(goal=x['goal'],domain=x['domain'],key_conditions=x['conditions'],decisive_steps=x['steps'],record_sha256=new_by[rid]['record_sha256'],math_sha256=new_by[rid]['math_sha256'])
    else:
        assert sig['record_sha256']==new_by[rid]['record_sha256'] and sig['math_sha256']==new_by[rid]['math_sha256']
(REVIEW/'revised-complete-signatures-v3.jsonl').write_bytes(b''.join((json.dumps(x,ensure_ascii=False)+'\n').encode('utf-8') for x in sigs))
(REVIEW/'prepared-v3.json').write_bytes(m.encoded({'parent_sha256':PARENT_SHA,'changed_ids':sorted(specs),'records':761,'signature_changes':4,'unchanged_complete_records':757,'sources':24}))
print(json.dumps({'prepared_successor':'PASS','records':761,'sources':24,'changed_ids':sorted(specs),'unchanged_complete_records':757,'unchanged_source_files':sum(s['unchanged_source_bytes'] for s in new_sources)}))
