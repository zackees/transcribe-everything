"""
Main entry point.
"""

from virtual_fs import FSPath

from transcribe_everything.util import is_media_file


def transcribe(src: FSPath, dst: FSPath) -> None:
    print(f"Transcribing {src} to {dst}")
    assert is_media_file(src.suffix), f"Expected .mp3, got {src.suffix}"
    assert dst.suffix == ".txt", f"Expected .txt, got {dst.suffix}"
    # todo: implement transcribe function
