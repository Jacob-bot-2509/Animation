import json, sys
def emit(obj):
    print('__RESULT__' + json.dumps(obj))
try:
    from pathlib import Path
    d = Path(r'C:/Windows/win.ini').read_bytes()
    print(json.dumps({'bytes': len(d)}))
except Exception as exc:
    emit({'ok': False, 'error': f'{type(exc).__name__}: {exc}'})
    sys.exit(7)
