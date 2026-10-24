"""A content-free public CLI smoke: settings read, digest verification, exact replay."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import uuid

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--skill-area', required=True)
    a = p.parse_args()
    request = {'contract_version': '1.0', 'operation_name': 'recall.settings.read',
        'operation_id': 'settings-smoke-' + uuid.uuid4().hex,
        'owner_namespace': 'installation-smoke', 'payload': {}}
    request['request_digest'] = digest(request)
    results = []
    for _ in range(2):
        run = subprocess.run([sys.executable, '-B', str(Path(__file__).with_name('invoke.py')),
            '--skill-area', a.skill_area], input=json.dumps(request), text=True,
            encoding='utf-8', capture_output=True, timeout=30)
        if run.returncode != 0:
            raise ValueError('Public invocation failed: ' + run.stderr + run.stdout)
        response = json.loads(run.stdout)
        if response['status'] != 'OK' or response['result_digest'] != digest({k:v for k,v in response.items() if k != 'result_digest'}):
            raise ValueError('Unexpected response or result digest')
        results.append(response)
    if results[0] != results[1]:
        raise ValueError('Exact replay differs')
    print(json.dumps({'status': 'OK', 'exact_replay': True, 'response': results[0]}))

if __name__ == '__main__':
    main()
