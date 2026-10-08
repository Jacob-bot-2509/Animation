"""Build fresh, read-only scene inputs; old chunks are historical inputs."""
from __future__ import annotations
import argparse,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from scene_sweep_protocol import STANDARD,build_inputs

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--drafts',type=Path,default=ROOT/'reviews/2026-10-05-training-diversity-drafts')
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--chunks',type=int,default=20)
    ap.add_argument('--expected-count',type=int,default=264)
    args=ap.parse_args(argv)
    try:
        result=build_inputs(args.drafts,args.out,chunks=args.chunks,expected_count=args.expected_count)
        print('immutable chunks:',result['chunk_count'],'| records:',result['record_count'])
        return 0
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print('[FAIL]',exc);return 1

if __name__=='__main__':sys.exit(main())
