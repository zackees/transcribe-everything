from pathlib import Path

from langdetect import detect

from transcribe_everything.constants import MEDIA_EXTENSIONS


def is_media_file(filename: str) -> bool:
    filename = filename.lower()
    suffix = Path(filename).suffix
    return suffix in MEDIA_EXTENSIONS or filename in MEDIA_EXTENSIONS


def _name_without_suffix(name: str) -> str:
    return Path(name).stem


def get_language(text: str) -> str:
    if len(text) < 20:
        return "en"
    text = _name_without_suffix(text)
    text = text.replace("_", " ")
    return detect(text)


def random_str(n: int = 10) -> str:
    import random
    import string

    return "".join(random.choices(string.ascii_lowercase, k=n))
