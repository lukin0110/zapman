import importlib.util
from pathlib import Path
from types import ModuleType

from orval import snake_case


def __module_name(file_path: str) -> str:
    relative = Path(file_path).relative_to(Path.cwd())
    results = [snake_case(part) for part in relative.parts]
    if relative.is_file() or relative.suffix:
        results[-1] = relative.stem
    return ".".join(results)


def load_module(file_path: str) -> ModuleType:
    """Load a Python file as a module."""
    module_name = __module_name(file_path)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    # sys.modules["module_name"] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module
