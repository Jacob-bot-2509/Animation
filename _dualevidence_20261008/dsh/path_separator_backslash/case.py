import json, sys, traceback
try:
    from pathlib import Path
    n = len(list(Path(r'D:\\Animation-Model-Training\\src\\animgtrain').iterdir()))
    print(json.dumps({'entries': n}))
    print('__RESULT__' + json.dumps({'ok': True}))
except Exception as exc:
    print('__RESULT__' + json.dumps({'ok': False, 'error': f'{type(exc).__name__}: {exc}'}))
    sys.exit(7)
