import json, sys
def emit(obj):
    print('__RESULT__' + json.dumps(obj))
try:
    from pathlib import Path
    p = Path(r'D:/Animation-Model-Training/_dualevidence_20261008/dsh/workspace_write_inside') / 'case_inside.tmp'
    p.write_text('inside', encoding='utf-8')
    n = p.stat().st_size
    p.unlink()
    print(json.dumps({'bytes': n}))
except Exception as exc:
    emit({'ok': False, 'error': f'{type(exc).__name__}: {exc}'})
    sys.exit(7)
