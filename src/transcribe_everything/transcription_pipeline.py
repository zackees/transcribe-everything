"""
Main entry point.
"""

import os
import traceback
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime
from logging import getLogger
from pathlib import Path

from transcribe_anything import transcribe_anything
from virtual_fs import FSPath

from transcribe_everything.lang import get_language, is_english
from transcribe_everything.tmpdir import TempDir
from transcribe_everything.util import is_media_file

logger = getLogger(__name__)

_MODEL = os.environ.get("TRANSCRIBE_EVERYTHING_MODEL", "large-v3")
_DEVICE = os.environ.get("TRANSCRIBE_EVERYTHING_DEVICE", "insane")
_BATCH_SIZE = int(os.environ.get("GPU_BATCH_SIZE", 8))

_OTHER_ARGS = [
    "--batch-size",
    str(_BATCH_SIZE),
]


def get_n_transcribers() -> int:
    """Get the number of transcribers."""
    try:
        out = int(os.environ.get("GPU_JOBS", 1))
        if out > 1:
            print(f"GPU_JOBS is set to {out}, using {out} transcribers")
        return out
    except ValueError:
        logger.warning(
            "TRANSCRIBE_EVERYTHING_N_TRANSCRIBERS is not an integer, using default value of 1"
        )
        return 1


_N_TRANSCRIBERS = get_n_transcribers()
_N_UPLOADERS = _N_TRANSCRIBERS + 2
_N_DOWNLOADERS = _N_UPLOADERS
_N_TOP_LEVEL = _N_UPLOADERS + _N_DOWNLOADERS + _N_TRANSCRIBERS

_THREAD_POOL_UPLOAD = ThreadPoolExecutor(max_workers=_N_UPLOADERS)
_THREAD_POOL_DOWNLOAD = ThreadPoolExecutor(max_workers=_N_DOWNLOADERS)
_THREAD_POOL_TRANSCRIBE = ThreadPoolExecutor(max_workers=_N_TRANSCRIBERS)
_THREAD_POOL_TOP_LEVEL = ThreadPoolExecutor(max_workers=_N_TOP_LEVEL)

_COUNT = 0


_START_TIME = datetime.now()


def transcribe_async(src: FSPath, dst: FSPath) -> Future[Exception | None]:
    # print(f"Transcribing {src} to {dst}")

    if not is_english(src.name):
        lang = get_language(src.name)
        logger.info(
            f"Skipping {src} because the file title appears not to be in English.\nThe language detector says this name is {lang}"
        )
        return _THREAD_POOL_TRANSCRIBE.submit(lambda: None)
    try:
        assert is_media_file(src.suffix), f"Expected media file got {src.suffix}"
        assert dst.suffix == ".txt", f"Expected .txt, got {dst.suffix}"
        # Prepare data context for the pipeline.
        tmpobj = TempDir()
        # TempDir will be opened and finally exited during the lifespan of the active job.
        tmpdir = tmpobj._tmpdir_path
        filename = Path(src.path).name
        tmp = Path(tmpdir)
        dst_tmp = tmp / filename
        dst_txt = dst.with_suffix(".txt")
        out_txt = tmp / "out.txt"

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
                stacktrace = traceback.format_exc()
                logger.error(f"ERROR transcribing {url_or_file}:\n{stacktrace}\n\n{e}")
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
        ) -> Exception | None:
            global _COUNT
            logger.info(f"START TOP level transcritpion pipeline of {src} to {dst}")
            with tmpobj:
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
                    _COUNT += 1
                    count = _COUNT
                    hours_running = (
                        datetime.now() - _START_TIME
                    ).total_seconds() / 3600
                    logger.info(
                        f"\n###################################################################\n"
                        f"# SUCCESS! TOP level transcription pipeline finished for conversion of:\n"
                        f"# {src} ->\n"
                        f"# {dst}\n"
                        f"# Count: {count}\n"
                        f"# Time running: {hours_running:.2f} hours\n"
                        f"###################################################################\n"
                    )
                except Exception as e:
                    logger.error(
                        f"ERROR TOP level transcription pipeline of {src} to {dst}"
                    )
                    return e
            return None

        return _THREAD_POOL_TOP_LEVEL.submit(wait_task)

    except Exception as e:
        top_e = e
        return _THREAD_POOL_TRANSCRIBE.submit(lambda: top_e)
