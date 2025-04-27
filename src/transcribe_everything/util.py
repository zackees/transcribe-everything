import random
import string
from pathlib import Path

from transcribe_everything.constants import MEDIA_EXTENSIONS


def is_media_file(filename: str) -> bool:
    filename = filename.lower()
    suffix = Path(filename).suffix
    return suffix in MEDIA_EXTENSIONS or filename in MEDIA_EXTENSIONS


def random_str(n: int = 10) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=n))
