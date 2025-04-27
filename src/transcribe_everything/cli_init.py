"""
Main entry point.
"""

import logging
import os
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from transcribe_everything import Api

# from transcribe_everything.args import Args
# from transcribe_everything.run import run


# Initialize logging for info on this package

logger = logging.getLogger("transcribe_everything")
logger.setLevel(logging.INFO)


def main(mp3_path: str) -> int:
    """Main entry point for the template_python_cmd package."""
    here = Path(__file__).parent
    os.chdir(str(here))
    with TemporaryDirectory() as tmpdir:
        cwd: str = tmpdir
        out_path = cwd + "/test.mp3"
        out_txt = cwd + "/test.txt"
        shutil.copy(mp3_path, out_path)
        assert Path(out_path).exists(), f"File {out_path} does not exist"
        print(f"Transcribing {out_path} to {cwd}")
        result: Exception | None = Api.transcribe_async(
            out_path,
            out_txt,
        ).result()
        if isinstance(result, Exception):
            print(f"Transcription failed with error: {result}")
            return 1
        print(result)
        print("Transcription completed.")
        return 0


if __name__ == "__main__":
    mp3_path = "assets/sample.mp3"
    sys.exit(main(mp3_path))
