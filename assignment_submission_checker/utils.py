import os
import stat
from pathlib import Path
from typing import Callable


def on_readonly_error(f: Callable[[Path], None], path: Path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file) it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=on_readonly_error)``
    """
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWRITE)
        f(path)
    else:
        raise
