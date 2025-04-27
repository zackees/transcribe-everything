"""
Main entry point.
"""

import logging
import shutil

# for resource loading
from importlib.resources import as_file, files
from pathlib import Path
from tempfile import TemporaryDirectory

from transcribe_everything import Api

logger = logging.getLogger("transcribe_everything")
logger.setLevel(logging.INFO)


def main() -> int:
    """Main entry point for the transcribe_everything package."""
    # locate the bundled sample.mp3
    resource = files("transcribe_everything").joinpath("assets/sample.mp3")
    with as_file(resource) as mp3_path:
        with TemporaryDirectory() as tmpdir:
            cwd = tmpdir
            out_path = Path(cwd) / "test.mp3"
            out_txt = Path(cwd) / "test.txt"

            shutil.copy(mp3_path, out_path)
            assert out_path.exists(), f"File {out_path} does not exist"

            print(f"Transcribing {out_path} to {cwd}")
            result = Api.transcribe_async(str(out_path), str(out_txt)).result()

            if isinstance(result, Exception):
                print(f"Transcription failed with error: {result}")
                return 1

            print(result)
            print("Transcription completed.")
            return 0


if __name__ == "__main__":

    main()
