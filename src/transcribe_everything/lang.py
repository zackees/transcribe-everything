from pathlib import Path

from langdetect import detect


def _name_without_suffix(name: str) -> str:
    return Path(name).stem


def get_language(text: str) -> str:
    if len(text) < 20:
        return "en"
    text = _name_without_suffix(text)
    text = text.replace("_", " ")
    return detect(text)
