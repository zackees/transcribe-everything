from pathlib import Path

from transcribe_everything.constants import MEDIA_EXTENSIONS


def is_media_file(filename: str) -> bool:
    suffix = Path(filename).suffix
    return suffix in MEDIA_EXTENSIONS
