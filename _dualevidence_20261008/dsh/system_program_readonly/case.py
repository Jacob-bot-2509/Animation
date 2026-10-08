import json, sys
def emit(obj):
    print('__RESULT__' + json.dumps(obj))
try:
    import subprocess
    cp = subprocess.run(['cmd', '/c', 'ver'], capture_output=True)
    print(json.dumps({'rc': cp.returncode, 'stdout': cp.stdout.decode('utf-8','replace').strip()}))
except Exception as exc:
    emit({'ok': False, 'error': f'{type(exc).__name__}: {exc}'})
    sys.exit(7)
