import json, sys, traceback
try:
    from pathlib import Path
    n = len(list(Path('D:/Animation-Model-Training/src/animtrain').iterdir()))
    print(json.dumps({'entries': n}))
    print('__RESULT__' + json.dumps({'ok': True}))
except Exception as exc:
    print('__RESULT__' + json.dumps({'ok': False, 'error': f'{type(exc).__name__}: {exc}'}))
    sys.exit(7)
