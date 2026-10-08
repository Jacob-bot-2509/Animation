"""Apply only reviewed files; abort if a source was changed concurrently."""
import hashlib
import json
from pathlib import Path

stage = Path(__file__).resolve().parent
project = Path(r'D:\Animation-Model-Training')
original = json.loads((stage / 'original-hashes.json').read_text(encoding='utf-8-sig'))
names = list(original) + ['tests/test_version_lock_review.py']
for name in names:
    target = project / name
    if name in original:
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != original[name]:
            raise SystemExit('Concurrent change detected; no files written: ' + name)
    elif target.exists():
        raise SystemExit('New target already exists; no files written: ' + name)
for name in names:
    target = project / name
    content = (stage / name).read_bytes().replace(b'\r\n', b'\n')
    target.write_bytes(content)
    print('Updated:', name)
