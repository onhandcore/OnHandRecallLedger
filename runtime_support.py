"""Distribution integrity and interpreter preflight; not a business interface."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import sys

MANIFEST = 'RELEASE_MANIFEST.json'
PRODUCT = 'OnHandRecallLedger'

def require_runtime():
    if (os.name != 'nt' or sys.implementation.name != 'cpython'
            or sys.version_info[:3] != (3, 12, 14) or platform.machine().upper() != 'AMD64'
            or importlib.util.MAGIC_NUMBER.hex() != 'cb0d0d0a' or sys.flags.optimize != 0):
        raise ValueError('Requires Windows x64 CPython 3.12.14, magic cb0d0d0a, optimize=0')

def safe_path(path):
    path = Path(os.path.abspath(path))
    for node in (path, *path.parents):
        if node.is_symlink() or node.is_junction():
            raise ValueError('Linked paths are not supported')
    return path.resolve()

def area_path(value):
    area = safe_path(value)
    if area.name != 'ONHAND_SKILL_AREA':
        raise ValueError('The selected root must be named ONHAND_SKILL_AREA')
    return area

def manifest(home):
    value = json.loads((Path(home) / MANIFEST).read_text(encoding='utf-8'))
    if value['product'] != PRODUCT or value['product_version'] != '1.0.0':
        raise ValueError('Unexpected distribution identity')
    for name in value['files']:
        part = Path(name)
        if part.is_absolute() or part.drive or '..' in part.parts:
            raise ValueError('Unsafe manifest member')
    return value

def verify(home, strict=False):
    home = safe_path(home)
    value = manifest(home)
    for name, record in value['files'].items():
        path = safe_path(home / name)
        if not path.is_relative_to(home) or not path.is_file():
            raise ValueError('Missing payload: ' + name)
        body = path.read_bytes()
        if len(body) != record['size'] or hashlib.sha256(body).hexdigest() != record['sha256']:
            raise ValueError('Payload hash mismatch: ' + name)
    if strict:
        actual = {p.relative_to(home).as_posix() for p in home.rglob('*') if p.is_file()}
        if actual != set(value['files']) | {MANIFEST}:
            raise ValueError('Unexpected files in the extracted distribution')
    return value

def core_lock(home):
    home = safe_path(home)
    lib = home / 'lib'
    sys.path.insert(0, str(lib))
    from onhand_recallledger.common.os_exclusion import root_exclusion
    return root_exclusion
