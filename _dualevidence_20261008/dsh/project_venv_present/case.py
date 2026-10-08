import json, sys
def emit(obj):
    print('__RESULT__' + json.dumps(obj))
try:
    from pathlib import Path
    p = Path('D:/Animation-Model-Training/.venv/Scripts/python.exe')
    exists = p.exists()
    print(json.dumps({'exists': exists, 'bytes': p.stat().st_size if exists else None}))
except Exception as exc:
    emit({'ok': False, 'error': f'{type(exc).__name__}: {exc}'})
    sys.exit(7)
