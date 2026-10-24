"""Remove only manifest-listed program files; retain all managed data."""
import argparse
import json
from pathlib import Path
from runtime_support import PRODUCT, MANIFEST, area_path, safe_path, require_runtime, verify, core_lock

def main():
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['uninstall'])
    p.add_argument('--skill-area', required=True)
    p.add_argument('--quiescent', action='store_true')
    p.add_argument('--retain-data', action='store_true')
    a = p.parse_args()
    require_runtime()
    if not (a.quiescent and a.retain_data):
        raise ValueError('Stop new calls, drain work; --quiescent --retain-data are required')
    area = area_path(a.skill_area)
    home = safe_path(area / PRODUCT)
    if safe_path(Path(__file__).parent) != home:
        raise ValueError('Run the installed management entry for exactly this home')
    value = verify(home)
    record = json.loads((home / 'INSTALL_RECORD.json').read_text(encoding='utf-8'))
    if (record['series_root'] != str(area) or record['artifact_id'] != value['artifact_id']
            or record['state'] != 'INSTALLED'):
        raise ValueError('Installation identity mismatch')
    # Host quiescence declaration is required; the Core lock also rejects an active writer.
    with core_lock(home)(home):
        for name in [*value['files'], MANIFEST, 'isolated_target.json']:
            safe_path(home / name).unlink()
        record['state'] = 'PROGRAM_REMOVED_DATA_RETAINED'
        (home / 'INSTALL_RECORD.json').write_text(json.dumps(record), encoding='utf-8')
        program_dirs = {parent for name in value['files'] for parent in (home / name).parents
            if parent != home and parent.is_relative_to(home)}
        for folder in sorted(program_dirs, key=lambda p: len(p.parts), reverse=True):
            try:
                folder.rmdir()  # Empty directories only; never recursive deletion.
            except OSError:
                pass
    print(json.dumps({'status': 'PROGRAM_REMOVED_DATA_RETAINED', 'home': str(home)}))

if __name__ == '__main__':
    main()
