"""Public session attachment entry for OnHandRecallLedger (combined mode).

Declared by the post-implementation Series Wiring Review recorded in this Skill's
SKILL.md.  It is a thin, non-authoritative attachment edge:

* it receives the opaque Thoroughfare resident payload and the resident
  correlation record of the current invocation;
* it delegates the payload UNCHANGED to the single frozen Core public surface
  (`onhand_recallledger.public.PublicSurface`) that the standalone entry also uses;
* it returns that Core result unchanged.

It adds no operation, no public schema, no contract version, no persistent state,
no routing, no scheduling, no retry and no semantic authority.  Recall and
Knowledge keep exactly the semantics of the frozen public contract; the
Thoroughfare correlation record is transport metadata and is never interpreted.
"""
import sys
from runtime_support import require_runtime
require_runtime()
from pathlib import Path

_BASE = Path(__file__).resolve().parent
_LIB = _BASE / ("lib" if (_BASE / "lib").is_dir() else "src")
if str(_BASE) not in sys.path:
    sys.path.insert(0, str(_BASE))
if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

# A Host must retire the old executor before loading the successor. Python's
# module cache cannot silently select a different version's Core.
for _name, _module in tuple(sys.modules.items()):
    if _name == 'onhand_recallledger' or _name.startswith('onhand_recallledger.'):
        _origin = getattr(_module, '__file__', None)
        if _origin is None or not Path(_origin).resolve().is_relative_to(_LIB.resolve()):
            raise RuntimeError('RECALLLEDGER_VERSION_MISMATCH_REQUIRES_FRESH_EXECUTOR')

from onhand_recallledger.common.foundation import Rejected
from onhand_recallledger.public import PublicSurface

import importlib.util
_target_spec = importlib.util.spec_from_file_location('recallledger_explicit_state_target', _BASE / 'state_target.py')
_target_module = importlib.util.module_from_spec(_target_spec)
_target_spec.loader.exec_module(_target_module)
SERIES_ROOT = _target_module.target()
_ENTRY_NAME = "OnHandRecallLedger/resident_entry.py"


def invoke(payload, correlation):
    """Thoroughfare resident-line body entry: (opaque payload, correlation) -> Core result."""
    try:
        return PublicSurface(str(SERIES_ROOT)).execute(payload)
    except (Rejected, OSError, ValueError, TypeError):
        return {"contract_version": "1.0", "operation_name": "invalid", "operation_id": "invalid",
                "status": "REJECTED", "result_class": "PUBLIC_NON_AUTHORITY",
                "error": {"code": "INVALID_HOST_INPUT"}}
