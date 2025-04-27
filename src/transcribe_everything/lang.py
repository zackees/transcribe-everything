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


def is_english(text: str) -> bool:
    """Different than get_language(), this function will count the number of ascii characters and non ascii characters."""
    count_ascii = 0
    count_non_ascii = 0
    for ch in text:
        if not ch.isascii():
            count_non_ascii += 1
        else:
            count_ascii += 1
    if count_ascii * 2 < count_non_ascii:
        return False
    return True
