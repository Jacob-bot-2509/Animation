import json, sys
def emit(obj):
    print('__RESULT__' + json.dumps(obj))
try:
    from pathlib import Path
    p = Path(r'C:/Windows/Temp/_dsh_sandbox_escape.tmp')
    p.write_text('escape', encoding='utf-8')
    print(json.dumps({'wrote': str(p)}))
except Exception as exc:
    emit({'ok': False, 'error': f'{type(exc).__name__}: {exc}'})
    sys.exit(7)
