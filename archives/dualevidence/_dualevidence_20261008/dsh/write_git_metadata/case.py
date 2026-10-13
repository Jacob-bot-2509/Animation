import json, sys
def emit(obj):
    print('__RESULT__' + json.dumps(obj))
try:
    from pathlib import Path
    p = Path(r'D:/Animation-Model-Training/.git/_dsh_sandbox_touch.tmp')
    p.write_text('x', encoding='utf-8')
    print(json.dumps({'wrote': str(p)}))
except Exception as exc:
    emit({'ok': False, 'error': f'{type(exc).__name__}: {exc}'})
    sys.exit(7)
