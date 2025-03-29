"""
Main entry point.
"""

from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

from transcribe_anything import transcribe_anything
from virtual_fs import FSPath

from transcribe_everything.util import is_media_file

_MODEL = "large"
_DEVICE = "insane"

_N_TRANSCRIBERS = 1
_N_UPLOADERS = 2 * _N_TRANSCRIBERS
_N_DOWNLOADERS = 2 * _N_TRANSCRIBERS
_N_TOP_LEVEL = _N_UPLOADERS + _N_DOWNLOADERS + _N_TRANSCRIBERS

_THREAD_POOL_UPLOAD = ThreadPoolExecutor(max_workers=_N_UPLOADERS)
_THREAD_POOL_DOWNLOAD = ThreadPoolExecutor(max_workers=_N_DOWNLOADERS)
_THREAD_POOL_TRANSCRIBE = ThreadPoolExecutor(max_workers=_N_TRANSCRIBERS)
_THREAD_POOL_TOP_LEVEL = ThreadPoolExecutor(max_workers=_N_TOP_LEVEL)


def transcribe(src: FSPath, dst: FSPath) -> Exception | None:
    print(f"Transcribing {src} to {dst}")
    try:
        assert is_media_file(src.suffix), f"Expected .mp3, got {src.suffix}"
        assert dst.suffix == ".txt", f"Expected .txt, got {dst.suffix}"
        # move file to temp location
        with TemporaryDirectory() as tmpdir:
            filename = Path(src.path).name
            tmp = Path(tmpdir)
            dst_tmp = tmp / filename
            dst_txt = dst_tmp.with_suffix(".txt")
            src_bytes = src.read_bytes()
            dst_tmp.write_bytes(src_bytes)
            transcribe_anything(
                url_or_file=dst_tmp.as_posix(),
                output_dir=tmp.as_posix(),
                model=_MODEL,
                device=_DEVICE,
            )
            # find the transcribed file called out.txt
            out_txt = tmp / "out.txt"
            assert out_txt.exists(), f"Expected {out_txt} to exist"
            # move it to the destination
            bytes = out_txt.read_bytes()
            dst_txt.write_bytes(bytes)
    except Exception as e:
        return e


def transcribe_async(src: FSPath, dst: FSPath) -> Future[Exception | None]:
    print(f"Transcribing {src} to {dst}")
    try:
        assert is_media_file(src.suffix), f"Expected .mp3, got {src.suffix}"
        assert dst.suffix == ".txt", f"Expected .txt, got {dst.suffix}"
        # move file to temp location
        with TemporaryDirectory() as tmpdir:
            filename = Path(src.path).name
            tmp = Path(tmpdir)
            dst_tmp = tmp / filename
            dst_txt = dst_tmp.with_suffix(".txt")
            src_bytes = src.read_bytes()
            # find the transcribed file called out.txt
            out_txt = tmp / "out.txt"

            def task_download(src_bytes=src_bytes, dst_tmp=dst_tmp) -> Exception | None:
                try:
                    dst_tmp.write_bytes(src_bytes)
                except Exception as e:
                    return e

            def task_transcribe(
                url_or_file=dst_tmp.as_posix(),
                output_dir=tmp.as_posix(),
                model=_MODEL,
                device=_DEVICE,
            ) -> Exception | None:
                try:
                    transcribe_anything(
                        url_or_file=url_or_file,
                        output_dir=output_dir,
                        model=model,
                        device=device,
                    )
                except Exception as e:
                    return e

            def task_upload(out_txt=out_txt, dst_txt=dst_txt) -> Exception | None:
                try:
                    assert out_txt.exists(), f"Expected {out_txt} to exist"
                    bytes = out_txt.read_bytes()
                    dst_txt.write_bytes(bytes)
                except Exception as e:
                    return e

            def wait_task(
                task_download=task_download,
                task_transcribe=task_transcribe,
                task_upload=task_upload,
            ):
                err = _THREAD_POOL_DOWNLOAD.submit(task_download).result()
                if err:
                    return err
                err = _THREAD_POOL_TRANSCRIBE.submit(task_transcribe).result()
                if err:
                    return err
                err = _THREAD_POOL_UPLOAD.submit(task_upload).result()
                if err:
                    return err
                return None

            return _THREAD_POOL_TOP_LEVEL.submit(wait_task)

    except Exception as e:
        top_e = e
        return _THREAD_POOL_TRANSCRIBE.submit(lambda: top_e)
