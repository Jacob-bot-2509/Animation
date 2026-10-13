import json, sys, traceback
try:
    from pathlib import Path
    p = Path('D:/Animation-Model-Training/.venv/Scripts/python.exe')
    print(json.dumps({'exists': p.exists(), 'bytes': p.stat().st_size if p.exists() else None}))
    print('__RESULT__' + json.dumps({'ok': True}))
except Exception as exc:
    print('__RESULT__' + json.dumps({'ok': False, 'error': f'{type(exc).__name__}: {exc}'}))
    sys.exit(7)
