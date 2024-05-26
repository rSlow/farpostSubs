import sys
from contextlib import contextmanager
from importlib import import_module
from pathlib import Path
from typing import Any

from loguru import logger


@contextmanager
def add_cwd_in_path():
    """
    Adds current directory in python path.

    This context manager adds current directory in sys.path,
    so all python files are discoverable now, without installing
    current project.

    :yield: none
    """
    cwd = Path.cwd()
    if str(cwd) in sys.path:
        yield
    else:
        logger.debug(f"Inserting {cwd} in sys.path")
        sys.path.insert(0, str(cwd))
        try:
            yield
        finally:
            try:
                sys.path.remove(str(cwd))
            except ValueError:
                logger.warning(f"Cannot remove '{cwd}' from sys.path")


def import_object(object_spec: str) -> Any:
    """
    It parses python object spec and imports it.

    :param object_spec: string in format like `package.module:variable`
    :raises ValueError: if spec has unknown format.
    :returns: imported broker.
    """
    import_spec = object_spec.split(":")
    if len(import_spec) != 2:
        raise ValueError("You should provide object path in `module:variable` format.")
    with add_cwd_in_path():
        module = import_module(import_spec[0])
    return getattr(module, import_spec[1])
