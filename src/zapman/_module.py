import importlib.util
from pathlib import Path
from types import ModuleType


def load_module(file_path: str) -> ModuleType:
    """Load a Python file as a module."""
    # TODO: use paths, relative to Path.cwd() for specname?
    spec_name = Path(file_path).name.replace(".py", "")
    spec = importlib.util.spec_from_file_location(f"zaps.{spec_name}", file_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    # sys.modules["module_name"] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module
