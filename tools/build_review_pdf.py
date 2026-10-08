"""Merge only hash-bound selected reports; publish a new review version exclusively."""
from pathlib import Path
import argparse,json,re,sys,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from draft_io import selected_path,verify_entry,write_utf8_lf,NORMALIZED_HASH
DRAFTS=ROOT/'reviews/2026-10-05-training-diversity-drafts'
OUT=ROOT/'outputs/draft-review/draft-review-selected-harness-v1.md'

def report_body(row):
    return '\n\n'.join(['**题目**',row['problem'],'**推导**',row['solution'],'**答案**',row['answer'],'**场景对象**',
        '\n'.join('- '+x for x in row['scene_spec']['objects']),'**场景步骤**','\n'.join('- '+x for x in row['scene_spec']['steps'])]).strip()

def merge(drafts,out):
    sel_path=drafts/'draft-selection.json'; sel_bytes=sel_path.read_bytes(); sel=json.loads(sel_bytes.decode('utf-8-sig'))
    if sel.get('schema')!=2 or sel.get('hash_algorithm')!=NORMALIZED_HASH: raise ValueError('schema2 normalized selector required')
    entries=sel.get('entries'); ids=set(); batches=set(); parts=[]; count=steps=0
    if not isinstance(entries,list) or not entries: raise ValueError('empty or invalid selection')
    for entry in entries:
        batch=entry['batch']
        if batch in batches: raise ValueError('duplicate selected batch')
        batches.add(batch); path=selected_path(drafts,entry); verify_entry(path,entry,hash_algorithm=NORMALIZED_HASH)
        report_rel=entry['report_path']; report=(drafts/report_rel).resolve()
        if Path(report_rel).is_absolute() or report.parent!=path.parent or report.suffix!='.md': raise ValueError('report path outside selected batch')
        verify_entry(report,{'batch':batch,'sha256':entry.get('report_sha256'),'raw_sha256':entry.get('report_raw_sha256'),
            'hash_algorithm':entry.get('report_hash_algorithm')},hash_algorithm=NORMALIZED_HASH)
        rows=[json.loads(line) for line in path.read_text('utf-8-sig').splitlines() if line.strip()]
        if not rows or type(entry.get('count')) is not int or entry['count']!=len(rows): raise ValueError('selector count mismatch')
        report_text=report.read_text('utf-8-sig'); sections=re.split(r'^## ([^\s]+)[^\n]*\n',report_text,flags=re.M)
        if sections[1::2]!=[row['id'] for row in rows]: raise ValueError('report IDs/order differ from selected JSONL')
        for row,body in zip(rows,sections[2::2]):
            if row['id'] in ids: raise ValueError('duplicate selected question')
            ids.add(row['id'])
            if body.strip()!=report_body(row): raise ValueError('report mathematical content differs from selected JSONL: '+row['id'])
            steps+=len(row['scene_spec']['steps'])
        count+=len(rows); parts.append(report_text.rstrip()+'\n')
    if sel_path.read_bytes()!=sel_bytes: raise ValueError('selection changed during merge')
    cover=(f'# 训练数据扩充题 · 审阅稿\n\n共 {len(entries)} 批 / {count} 题；全部 {steps} 条场景步骤。\n\n'
        '各批题目、推导、答案和场景内容与哈希绑定的选中 JSONL 完全对应。数学复算及泄漏判定以各批审阅证据为准。\n\n'
        '未正式准入；动画尚未渲染验收；许可证为仅内部研究。\n\n'
        f'选中账本 raw SHA-256：`{hashlib.sha256(sel_bytes).hexdigest()}`。\n\n---\n\n')
    write_utf8_lf(out,cover+'\n\n'.join(parts),exclusive=True)
    return {'batches':len(entries),'questions':count,'steps':steps}

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--drafts',type=Path,default=DRAFTS);ap.add_argument('--out',type=Path,default=OUT)
    args=ap.parse_args([] if argv is None else argv)
    try: print('Merged',merge(args.drafts,args.out),'->',args.out);return 0
    except (OSError,ValueError,KeyError,TypeError) as exc: print('[FAIL]',exc);return 1
if __name__=='__main__':sys.exit(main(sys.argv[1:]))
