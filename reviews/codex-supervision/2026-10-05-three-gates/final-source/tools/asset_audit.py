"""Enumerate every CURRENT manifest asset; never infer math/semantic PASS from rendering.

Build and compile each scene, bind complete rows and source, record concrete omissions.
Write incomplete asset evidence with UNVERIFIED states so preflight remains closed.
"""
from __future__ import annotations
import argparse,ast,hashlib,json,re,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'src')]
from tools import render_templates as rt


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(manifest, output):
    data=json.loads(manifest.read_text(encoding='utf-8'));records={};counts=Counter()
    for entry in data['entries']:
        path=(manifest.parent/entry['path']).resolve()
        if not path.is_relative_to(ROOT) or sha(path)!=entry['sha256']:
            raise ValueError('Source path/hash mismatch')
        for line_no,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
            if not line.strip():continue
            rec=json.loads(line);sid=rec['id']
            if sid in records:raise ValueError('Duplicate ID')
            source=rt.build_scene(rec)
            scene=output/'sources'/(sid+'.py')
            if not re.fullmatch(r'[A-Za-z0-9_-]+',sid):raise ValueError('Unsafe ID')
            scene.parent.mkdir(parents=True,exist_ok=True);scene.write_text(source,encoding='utf-8')
            errors=[];warnings=[]
            try:compile(source,str(scene),'exec');syntax='compiled'
            except SyntaxError as exc:syntax='failed';errors.append(str(exc))
            steps=rec.get('scene_spec',{}).get('steps',[])
            if any(len(step)>28 for step in steps[:5]):errors.append('spec_step_text_truncated_at_28_characters')
            if len(steps)>5:errors.append('spec_steps_after_fifth_omitted')
            if not rt._math_segments(rec['answer']):errors.append('text_answer_not_displayed')
            if not rt._math_segments(rec['problem']):errors.append('problem_replaced_by_formula_extraction_failure_placeholder')
            # Fixed template geometry does not parameterize arbitrary record objects.
            template=rt.route(rec)
            if template!='fallback':warnings.append('fixed_template_geometry_requires_record_specific_validation')
            if any('$' in step for step in steps[:5]):warnings.append('tex_in_Text_not_typeset_as_MathTex')
            decimals=sorted(set(re.findall(r'(?<!\d)\d+\.\d+',rec['problem']+' '+rec['answer'])))
            if decimals:warnings.append('historical_decimal_literals_need_fraction_display_adapter')
            records[sid]={'input_sha256':hashlib.sha256(line.strip().encode()).hexdigest(),
                'source':{'path':str(path),'line':line_no,'sha256':entry['sha256']},
                'scene_source':{'path':str(scene),'sha256':sha(scene),'syntax':syntax,'template':template},
                'math':'UNVERIFIED','semantic':'failed' if errors else 'UNVERIFIED',
                'render':'UNVERIFIED','errors':errors,'warnings':warnings,
                'review_scope':'Source/static omissions only; no individual proof/real media acceptance claim'}
            counts['total']+=1;counts['source_'+syntax]+=1
            counts['semantic_failed' if errors else 'semantic_pending']+=1
    report={'schema':'asset-evidence-progress-v1','manifest_sha256':sha(manifest),
        'template_sha256':sha(Path(rt.__file__)),'n_total_records':len(records),
        'n_verified_assets':0,'records':records,'counts':dict(counts),
        'status':'NOT READY','scope':'Every registered source checked. Full math/scene/media acceptance is still pending.'}
    (output/'asset-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--publish-progress-evidence',action='store_true');a=p.parse_args(argv)
    output=a.output.resolve()
    if not output.is_relative_to(ROOT) or output.exists():p.error('Fresh project output required')
    output.mkdir(parents=True)
    report=audit(ROOT/'data/manifest.json',output)
    if a.publish_progress_evidence:
        target=ROOT/'data/asset_evidence.json'
        if target.exists():p.error('Existing evidence must be archived/reviewed explicitly')
        target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report['counts'],ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
