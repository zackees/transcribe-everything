from pathlib import Path

from langdetect import detect

from transcribe_everything.constants import MEDIA_EXTENSIONS


def _get_language(text: str) -> str:
    text = _name_without_suffix(text)
    text = text.replace("_", " ").lower()
    return detect(text)


def is_media_file(filename: str) -> bool:
    filename = filename.lower()
    suffix = Path(filename).suffix
    return suffix in MEDIA_EXTENSIONS or filename in MEDIA_EXTENSIONS


def _name_without_suffix(name: str) -> str:
    return Path(name).stem


def get_language(text: str) -> str:
    text = _name_without_suffix(text)
    text = text.replace("_", " ")
    return detect(text)
