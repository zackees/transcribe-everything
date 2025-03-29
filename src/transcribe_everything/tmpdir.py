import os
import shutil
from logging import getLogger
from pathlib import Path

from transcribe_everything.util import random_str

logger = getLogger(__name__)

_PROCESS_ID = os.getpid()

_TEMP_DIR = Path(".tmp")
_THIS_TEMP_DIR = _TEMP_DIR / f"{_PROCESS_ID}"


class TempDir:
    def __init__(self):
        self._tmpdir_path = _THIS_TEMP_DIR / random_str()
        self._tmpdir = str(self._tmpdir_path)

    def __enter__(self):
        self._tmpdir_path.mkdir(exist_ok=True, parents=True)
        return self._tmpdir_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: atexit
        shutil.rmtree(self._tmpdir, ignore_errors=True)
