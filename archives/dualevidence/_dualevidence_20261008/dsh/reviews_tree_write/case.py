import json, sys
def emit(obj):
    print('__RESULT__' + json.dumps(obj))
try:
    from pathlib import Path
    p = Path(r'D:/Animation-Model-Training/reviews/codex-supervision/2026-10-08-sandbox-dual-end/evidence') / '_dsh_privileged_probe.tmp'
    p.write_text('probe', encoding='utf-8')
    p.unlink()
    print(json.dumps({'wrote_and_removed': str(p)}))
except Exception as exc:
    emit({'ok': False, 'error': f'{type(exc).__name__}: {exc}'})
    sys.exit(7)
