"""
Wrapper module for gsf-repair.py command-line tool.
"""
import importlib.util
import sys
from pathlib import Path
from typing import Callable

# Import the main function from gsf-repair.py
_script_path = Path(__file__).parent / "gsf-repair.py"
spec = importlib.util.spec_from_file_location("gsf_repair_module", _script_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Could not load module from {_script_path}")
module = importlib.util.module_from_spec(spec)
sys.modules["gsf_repair_module"] = module
spec.loader.exec_module(module)

main: Callable[[], None] = module.main

if __name__ == "__main__":
    main()

