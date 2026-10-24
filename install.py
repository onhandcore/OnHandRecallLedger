"""Fresh installation or explicit same-artifact program restoration; no migration."""
import argparse
import json
from pathlib import Path
import shutil
from runtime_support import PRODUCT, MANIFEST, area_path, safe_path, require_runtime, verify, core_lock

def copy_program(source, home, value):
    for name in [*value['files'], MANIFEST]:
        dest = safe_path(home / name)
        if not dest.is_relative_to(home):
            raise ValueError('Program destination escapes the owned home')
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, dest)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--skill-area', required=True)
    p.add_argument('--restore-program', action='store_true')
    p.add_argument('--quiescent', action='store_true')
    a = p.parse_args()
    require_runtime()
    source = safe_path(Path(__file__).parent)
    value = verify(source, strict=True)
    area = area_path(a.skill_area)
    home = safe_path(area / PRODUCT)
    if home == source:
        raise ValueError('Install into a separate root; retain the extracted distribution')
    if a.restore_program:
        if not a.quiescent:
            raise ValueError('Stop new calls, drain work and supply --quiescent')
        record = json.loads((home / 'INSTALL_RECORD.json').read_text(encoding='utf-8'))
        if (record['artifact_id'] != value['artifact_id'] or record['state'] != 'PROGRAM_REMOVED_DATA_RETAINED'
                or record['series_root'] != str(area) or not (home / 'successor.lock').is_file()):
            raise ValueError('Only the same artifact and intact retained state can be restored')
        for name in [*value['files'], MANIFEST]:
            if (home / name).exists():
                raise ValueError('Unexpected program residue; refuse overwrite')
        # Reuse the one existing Core root-lock domain; no second state lock.
        with core_lock(source)(home):
            copy_program(source, home, value)
            (home / 'isolated_target.json').write_text(json.dumps({'series_root': str(area)}), encoding='utf-8')
            record['state'] = 'INSTALLED'
            (home / 'INSTALL_RECORD.json').write_text(json.dumps(record), encoding='utf-8')
    else:
        if home.exists():
            raise ValueError('Fresh owned destination required; no overwrite or automatic migration')
        home.mkdir(parents=True)
        # On partial I/O failure leave this bounded new home visible for inspection.
        copy_program(source, home, value)
        (home / 'isolated_target.json').write_text(json.dumps({'series_root': str(area)}), encoding='utf-8')
        (home / 'INSTALL_RECORD.json').write_text(json.dumps({'artifact_id': value['artifact_id'],
            'series_root': str(area), 'state': 'INSTALLED'}), encoding='utf-8')
    print(json.dumps({'status': 'INSTALLED', 'home': str(home), 'artifact_id': value['artifact_id']}))

if __name__ == '__main__':
    main()
