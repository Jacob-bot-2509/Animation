"""Stage source-bound scene patches as NEW unselected files; never switches a selector."""
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from scene_sweep_protocol import stage_scene_patches

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--drafts',type=Path,required=True)
    ap.add_argument('--inputs',type=Path,required=True)
    ap.add_argument('--patches',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--version',required=True)
    args=ap.parse_args(argv)
    try:
        result=stage_scene_patches(args.drafts,args.patches,args.out,args.version,input_dir=args.inputs)
        print(json.dumps({k:result[k] for k in ('status','patch_count','record_count','production_selector_updated')},indent=2))
        return 0
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print('[FAIL]',exc);return 1

if __name__=='__main__':sys.exit(main())
