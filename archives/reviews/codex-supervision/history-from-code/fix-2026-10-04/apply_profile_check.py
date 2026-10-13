import hashlib
import json
from pathlib import Path
stage = Path(__file__).resolve().parent
root = Path(r'D:\Animation-Model-Training')
expected = json.loads((stage / 'profile-check-hashes.json').read_text(encoding='utf-8-sig'))
for name, old_hash in expected.items():
    if hashlib.sha256((root / name).read_bytes()).hexdigest() != old_hash:
        raise SystemExit('Concurrent change; no files written: ' + name)
for name in expected:
    (root / name).write_bytes((stage / name).read_bytes().replace(b'\r\n', b'\n'))
    print('Updated:', name)
