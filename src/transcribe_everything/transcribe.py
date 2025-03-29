"""
Main entry point.
"""

import shutil
from concurrent.futures import Future, ThreadPoolExecutor
from logging import getLogger
from pathlib import Path

from langdetect import detect
from transcribe_anything import transcribe_anything
from virtual_fs import FSPath

from transcribe_everything.util import is_media_file

logger = getLogger(__name__)

_MODEL = "large-v3"
_DEVICE = "insane"
_TEMP_DIR = Path(".tmp")


_OTHER_ARGS = [
    "--batch-size",
    str(8),
]


_N_TRANSCRIBERS = 1
_N_UPLOADERS = 2 * _N_TRANSCRIBERS
_N_DOWNLOADERS = 2 * _N_TRANSCRIBERS
_N_TOP_LEVEL = _N_UPLOADERS + _N_DOWNLOADERS + _N_TRANSCRIBERS

_THREAD_POOL_UPLOAD = ThreadPoolExecutor(max_workers=_N_UPLOADERS)
_THREAD_POOL_DOWNLOAD = ThreadPoolExecutor(max_workers=_N_DOWNLOADERS)
_THREAD_POOL_TRANSCRIBE = ThreadPoolExecutor(max_workers=_N_TRANSCRIBERS)
_THREAD_POOL_TOP_LEVEL = ThreadPoolExecutor(max_workers=_N_TOP_LEVEL)


def _random_str(n: int = 10) -> str:
    import random
    import string

    return "".join(random.choices(string.ascii_lowercase, k=n))


def _name_without_suffix(name: str) -> str:
    return Path(name).stem


def _is_english(text: str) -> bool | Exception:
    try:
        lang = _get_language(text)
        return lang == "en"
    except Exception:
        return False


def _get_language(text: str) -> str:
    text = _name_without_suffix(text)
    text = text.replace("_", " ")
    return detect(text)


class _TempDir:
    def __init__(self):
        self._tmpdir_path = _TEMP_DIR / _random_str()
        self._tmpdir = str(self._tmpdir_path)
        self._tmpdir_path.mkdir(exist_ok=True, parents=True)

    def __enter__(self):
        return self._tmpdir_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: atexit
        shutil.rmtree(self._tmpdir, ignore_errors=True)


def transcribe_async(src: FSPath, dst: FSPath) -> Future[Exception | None]:
    # print(f"Transcribing {src} to {dst}")

    lang = _get_language(src.name)
    if lang != "en":
        logger.info(
            f"Skipping {src} because the file title appears not to be in English, was instead {lang}"
        )
        return _THREAD_POOL_TRANSCRIBE.submit(lambda: None)
    try:
        assert is_media_file(src.suffix), f"Expected .mp3, got {src.suffix}"
        assert dst.suffix == ".txt", f"Expected .txt, got {dst.suffix}"
        # move file to temp location
        tmpobj = _TempDir()
        tmpdir = tmpobj.__enter__()
        # logger.info(f"Using temp dir {tmpdir}")
        filename = Path(src.path).name
        tmp = Path(tmpdir)
        dst_tmp = tmp / filename
        dst_txt = dst_tmp.with_suffix(".txt")

        # find the transcribed file called out.txt
        out_txt = tmp / "out.txt"
        # logger.info(f"out_txt: {out_txt}")

        def task_download(src=src, dst_tmp=dst_tmp) -> Exception | None:
            try:
                logger.info(f"BEGIN downloading {src} to {dst_tmp}")
                src_bytes = src.read_bytes()
                dst_tmp.write_bytes(src_bytes)
                logger.info(f"FINISHED downloading {src} to {dst_tmp}")
            except Exception as e:
                logger.error(f"ERROR downloading {src} to {dst_tmp}")
                return e

        def task_transcribe(
            url_or_file=dst_tmp.as_posix(),
            output_dir=tmp.as_posix(),
            model=_MODEL,
            device=_DEVICE,
        ) -> Exception | None:
            try:
                logger.info(f"BEGIN transcribing {url_or_file}")
                transcribe_anything(
                    url_or_file=url_or_file,
                    output_dir=output_dir,
                    model=model,
                    device=device,
                    other_args=_OTHER_ARGS,
                )
                logger.info(f"FINISHED transcribing {url_or_file}")
            except Exception as e:
                logger.error(f"ERROR transcribing {url_or_file}")
                return e

        def task_upload(out_txt=out_txt, dst_txt=dst_txt) -> Exception | None:
            try:
                logger.info(f"BEGIN uploading {out_txt} to {dst_txt}")
                assert out_txt.exists(), f"Expected {out_txt} to exist"
                bytes = out_txt.read_bytes()
                dst_txt.write_bytes(bytes)
                logger.info(f"FINISHED uploading {out_txt} to {dst_txt}")
            except Exception as e:
                logger.error(f"ERROR uploading {out_txt} to {dst_txt}")
                return e

        def wait_task(
            task_download=task_download,
            task_transcribe=task_transcribe,
            task_upload=task_upload,
        ):
            logger.info(f"START TOP level transcritpion pipeline of {src} to {dst}")
            try:
                err = _THREAD_POOL_DOWNLOAD.submit(task_download).result()
                if err:
                    return err
                err = _THREAD_POOL_TRANSCRIBE.submit(task_transcribe).result()
                if err:
                    return err
                err = _THREAD_POOL_UPLOAD.submit(task_upload).result()
                if err:
                    return err
                logger.info(
                    f"FINISHED TOP level transcription pipeline of {src} to {dst}"
                )
            finally:
                tmpobj.__exit__(None, None, None)
            return None

        return _THREAD_POOL_TOP_LEVEL.submit(wait_task)

    except Exception as e:
        top_e = e
        return _THREAD_POOL_TRANSCRIBE.submit(lambda: top_e)
