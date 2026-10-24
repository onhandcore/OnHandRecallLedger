"""Explicit isolated runtime target; no discovery or additional state authority."""
from pathlib import Path
import json
def target():
 p=Path(__file__).resolve().parent/'isolated_target.json'
 v=json.loads(p.read_text(encoding='utf-8'))
 if set(v)!={'series_root'}:raise ValueError('invalid explicit state target')
 root=Path(v['series_root'])
 if not root.is_absolute() or root.name!='ONHAND_SKILL_AREA':raise ValueError('invalid series root')
 return root
