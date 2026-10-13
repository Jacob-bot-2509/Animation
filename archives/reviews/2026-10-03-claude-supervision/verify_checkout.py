"""Independent read-only hash and freeze-binding verifier for supervision."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--manifest', default='data/v1/manifest.json')
    parser.add_argument('--locks', nargs='*', default=['data/eval-v1.lock.json', 'data/test-v1.lock.json'])
    parser.add_argument('--git-ref', default='HEAD')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    problems = []
    checked = []
    manifest_path = root / args.manifest
    manifest_bytes = manifest_path.read_bytes()
    manifest_hash = sha(manifest_bytes)
    for relative in [args.manifest, 'data/v1/manifest-train.json']:
        path = root / relative
        if not path.exists():
            continue
        data = path.read_bytes()
        manifest = json.loads(data)
        for entry in manifest.get('entries', []):
            target = path.parent / entry['path']
            if not target.is_file():
                problems.append(f'Missing entry: {relative}: {entry["path"]}')
                continue
            contents = target.read_bytes()
            if sha(contents) != entry.get('sha256') or len(contents) != entry.get('size'):
                problems.append(f'Entry hash/size mismatch: {relative}: {entry["path"]}')
        try:
            blob = subprocess.check_output(['git', '-C', str(root), 'show', f'{args.git_ref}:{relative}'], stderr=subprocess.DEVNULL)
            if data != blob:
                problems.append(f'Worktree differs from git blob: {relative}')
        except subprocess.CalledProcessError:
            problems.append(f'Manifest absent from git reference: {relative}')
        checked.append({'manifest': relative, 'sha256': sha(data), 'CR_count': data.count(b'\r')})
    for relative in args.locks:
        lock_path = root / relative
        try:
            lock = json.loads(lock_path.read_bytes())
            if lock.get('freeze_lock_version') != 1 or lock.get('locked') is not True:
                problems.append(f'Invalid lock marker: {relative}')
            entries = lock.get('entries')
            if not isinstance(entries, list) or not entries or lock.get('n_files') != len(entries):
                problems.append(f'Invalid lock entries: {relative}')
                continue
            bound = lock.get('meta', {}).get('manifest_sha256')
            if bound != manifest_hash:
                problems.append(f'Lock manifest binding mismatch: {relative}')
            for entry in entries:
                target = root / entry['path']
                if not target.is_file():
                    problems.append(f'Frozen entry missing: {relative}: {entry["path"]}')
                    continue
                data = target.read_bytes()
                if sha(data) != entry.get('sha256') or len(data) != entry.get('size'):
                    problems.append(f'Frozen hash/size mismatch: {relative}: {entry["path"]}')
            checked.append({'lock': relative, 'bound_manifest_sha256': bound, 'actual_manifest_sha256': manifest_hash})
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            problems.append(f'Lock invalid: {relative}: {type(exc).__name__}: {exc}')
    result = {'root': str(root), 'git_ref': args.git_ref, 'ok': not problems, 'problems': problems, 'checked': checked}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
