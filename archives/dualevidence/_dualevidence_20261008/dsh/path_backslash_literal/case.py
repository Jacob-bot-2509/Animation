import json, sys
def emit(obj):
    print('__RESULT__' + json.dumps(obj))
try:
    from pathlib import Path
    n = len(list(Path(r'D:\\Animation-Model-Training\\src\\animgtrain').iterdir()))
    print(json.dumps({'entries': n}))
except Exception as exc:
    emit({'ok': False, 'error': f'{type(exc).__name__}: {exc}'})
    sys.exit(7)
