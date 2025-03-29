from pathlib import Path

from transcribe_everything.constants import MEDIA_EXTENSIONS


def is_media_file(filename: str) -> bool:
    filename = filename.lower()
    suffix = Path(filename).suffix
    return suffix in MEDIA_EXTENSIONS or filename in MEDIA_EXTENSIONS
