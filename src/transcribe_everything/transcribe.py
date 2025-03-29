"""
Main entry point.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from transcribe_anything import transcribe_anything
from virtual_fs import FSPath

from transcribe_everything.util import is_media_file

_MODEL = "large"
_DEVICE = "insane"

# def transcribe_anything(
#     url_or_file: str,
#     output_dir: Optional[str] = None,
#     model: Optional[str] = None,
#     task: Optional[str] = None,
#     language: Optional[str] = None,
#     device: Optional[str] = None,
#     embed: bool = False,
#     hugging_face_token: Optional[str] = None,
#     other_args: Optional[list[str]] = None,
# ) -> str


def transcribe(src: FSPath, dst: FSPath) -> Exception | None:
    print(f"Transcribing {src} to {dst}")
    try:
        assert is_media_file(src.suffix), f"Expected .mp3, got {src.suffix}"
        assert dst.suffix == ".txt", f"Expected .txt, got {dst.suffix}"
        # move file to temp location
        with TemporaryDirectory() as tmpdir:
            filename = Path(src.path).name
            dst_tmp = Path(tmpdir) / filename
            dst_txt = dst_tmp.with_suffix(".txt")
            src_bytes = src.read_bytes()
            dst_tmp.write_bytes(src_bytes)
            transcribe_anything(
                url_or_file=dst_tmp.as_posix(),
                output_dir=dst.parent.path,
                model=_MODEL,
                device=_DEVICE,
            )
            # find the transcribed file called out.txt
            out_txt = dst_tmp.parent / "out.txt"
            assert out_txt.exists(), f"Expected {out_txt} to exist"
            # move it to the destination
            bytes = out_txt.read_bytes()
            dst_txt.write_bytes(bytes)
    except Exception as e:
        return e
