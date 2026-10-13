"""Strict, source-bound diagnostic sampling. Does not certify independence."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIR_SCHEMA = 'leakage-diagnostic-pairs-v2'
LABEL_SCHEMA = 'leakage-diagnostic-labels-v2'
SCORE_SCHEMA = 'leakage-diagnostic-score-v2'
LABEL_RULE = ('核心数学对象、条件、目标及求解结构保持不变，仅更换数值、符号或表述'
              '即为泄漏；训练与评测/测试需要隔离。共享知识点本身不足以判泄漏。')
INDEPENDENCE = {'status': 'DEVELOPMENT_DERIVED', 'calibration_eligible': False,
                'reason': 'Sampling uses development labels and draft parent lineage; '
                          'previously reviewed draft problems are not an untouched holdout.'}

def raw_sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')

def object_sha(value):
    return raw_sha(canonical_bytes(value))

RULE_SHA = raw_sha(LABEL_RULE.encode('utf-8'))

def _pairs_hook(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result

def strict_json(data):
    def invalid(value):
        raise ValueError('non-finite JSON constant: ' + value)
    result = json.loads(data.decode('utf-8-sig'), object_pairs_hook=_pairs_hook,
                        parse_constant=invalid)
    def finite(value):
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError('non-finite JSON number')
        if isinstance(value, dict):
            for item in value.values(): finite(item)
        elif isinstance(value, list):
            for item in value: finite(item)
    finite(result)
    return result

def json_object(data):
    value = strict_json(data)
    if not isinstance(value, dict):
        raise ValueError('JSON object required')
    return value

def required_text(record, field):
    if not isinstance(record, dict):
        raise ValueError('record object required')
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError('missing nonempty string: ' + field)
    return value

def jsonl(data):
    rows = [strict_json(line.encode('utf-8')) for line in data.decode('utf-8-sig').splitlines()
            if line.strip()]
    if not rows or any(not isinstance(row, dict) for row in rows):
        raise ValueError('JSONL must contain nonempty object records')
    return rows

class Snapshot:
    """Read each file once; bind and recheck all bytes used, including code."""
    def __init__(self, root=ROOT):
        self.root = root.resolve()
        self.data = {}

    def read(self, path):
        path = Path(path).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError('source outside project: ' + str(path))
        if path not in self.data:
            self.data[path] = path.read_bytes()
        return self.data[path]

    def bindings(self):
        return {p.relative_to(self.root).as_posix():
                {'raw_sha256': raw_sha(b), 'bytes': len(b)}
                for p, b in sorted(self.data.items())}

    def check_unchanged(self):
        for path, data in self.data.items():
            if path.read_bytes() != data:
                raise ValueError('source changed during operation: ' + str(path))

def question_payload(rec, *, query=False):
    payload = {key: required_text(rec, key) for key in ('id', 'problem', 'category')}
    payload['problem_sha256'] = raw_sha(payload['problem'].encode('utf-8'))
    if query:
        payload['split'] = required_text(rec, '_split')
        if payload['split'] not in ('eval', 'test'):
            raise ValueError('invalid query split')
        payload['record_sha256'] = object_sha(rec['_source_records'])
    else:
        payload['record_sha256'] = object_sha(rec)
    return payload

def make_pair(train, query):
    t = question_payload(train)
    q = question_payload(query, query=True)
    return {'pair_id': object_sha({'query': q, 'train': t}), 'query': q, 'train': t}

def require_pairs(pairs):
    if not isinstance(pairs, list) or not pairs:
        raise ValueError('nonempty pair list required')
    seen, contents = set(), set()
    for pair in pairs:
        if not isinstance(pair, dict) or set(pair) != {'pair_id', 'query', 'train'}:
            raise ValueError('pair fields mismatch')
        for side in ('query', 'train'):
            payload = pair[side]
            fields = {'id', 'problem', 'category', 'problem_sha256', 'record_sha256'}
            if side == 'query': fields.add('split')
            if not isinstance(payload, dict) or set(payload) != fields:
                raise ValueError('question payload fields mismatch')
            for field in fields: required_text(payload, field)
            if payload['problem_sha256'] != raw_sha(payload['problem'].encode('utf-8')):
                raise ValueError('question text/hash mismatch')
        pid = required_text(pair, 'pair_id')
        if pid in seen:
            raise ValueError('duplicate pair: ' + pid)
        seen.add(pid)
        if pid != object_sha({'query': pair['query'], 'train': pair['train']}):
            raise ValueError('pair content/identity mismatch')
        key = (pair['query']['problem_sha256'], pair['train']['problem_sha256'])
        if key in contents:
            raise ValueError('duplicate question-text pair')
        contents.add(key)
    return seen

def write_new_json(path, data, snapshot):
    path = Path(path).resolve()
    if not path.is_relative_to(snapshot.root):
        raise ValueError('output outside project')
    encoded = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False).encode('utf-8') + b'\n'
    snapshot.check_unchanged()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(encoded)
    snapshot.check_unchanged()
    return raw_sha(encoded)
