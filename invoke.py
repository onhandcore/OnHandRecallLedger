"""Standalone JSON stdin/stdout distribution launcher."""
from pathlib import Path
import sys
from runtime_support import require_runtime
require_runtime()
sys.path.insert(0, str(Path(__file__).resolve().parent / 'lib'))
from onhand_recallledger.host import main
if __name__ == '__main__':
    raise SystemExit(main())
