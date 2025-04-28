"""
Main entry point.
"""

import warnings
from concurrent.futures import Future
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator

from virtual_fs import FSPath

from transcribe_everything import __version__
from transcribe_everything.args import Args
from transcribe_everything.batch import Batch, find_batches
from transcribe_everything.transcription_pipeline import transcribe_async

# _ERROR_SET: set[FSPath] = set()

# def _file_had_error_store(file: FSPath) -> None:
#     # Check if the file has a .txt suffix and if it exists
#     return _ERROR_SET.add(file)

# def _file_had_error(file: FSPath) -> bool:
#     # Check if the file has a .txt suffix and if it exists
#     return file in _ERROR_SET

_PROCESSED_SET: set[FSPath] = set()
def _mark_file_processed(file: FSPath) -> None:
    # Check if the file has a .txt suffix and if it exists
    _PROCESSED_SET.add(file)

def _file_was_processed(file: FSPath) -> bool:
    # Check if the file has a .txt suffix and if it exists
    return file in _PROCESSED_SET

def _run_with_callback(
    args: Args, callback: Callable[[FSPath, FSPath], Exception | None]
) -> Exception | None:
    exceptions: list[Exception] = []
    try:
        batch_size = args.batch_size
        batches: list[Batch] = find_batches(args)

        if args.randomize:
            import random

            random.shuffle(batches)

        for batch in batches:
            unprocessed = batch.unprocessed()
            # filter files that have already been processed
            unprocessed = [file for file in unprocessed if not _file_was_processed(file)]
            for file in unprocessed:
                _mark_file_processed(file)
            unprocessed = unprocessed[:batch_size]
            file: FSPath
            for file in unprocessed:
                dst_file = file.with_suffix(".txt")
                err = callback(file, dst_file)
                if err:
                    exceptions.append(err)
    except Exception as e:
        exceptions.append(e)
    if exceptions:
        return Exception(f"Multiple exceptions: {exceptions}", exceptions)
    return None


def _run_async(args: Args) -> list[Future[Exception | None]]:
    futures: list[Future[Exception | None]] = []

    def task(file: FSPath, dst: FSPath) -> Exception | None:
        futures.append(transcribe_async(file, dst))
        return None

    setup_error = _run_with_callback(args, task)
    if setup_error:
        warnings.warn(f"Error: {setup_error}")
    return futures


def run(args: Args) -> tuple[int, Exception | None]:
    print(f"Transcribe Everything version {__version__}")
    count = 0
    futures: list[Future[Exception | None]] = _run_async(args)
    errors: list[Exception] = []
    for future in futures:
        err = future.result()
        if err:
            warnings.warn(f"Error: {err}")
            errors.append(err)
        else:
            count += 1
    if errors:
        return count, Exception(f"Multiple exceptions: {errors}", errors)
    exception = (
        None if not errors else Exception(f"Multiple exceptions: {errors}", errors)
    )
    return count, exception

    return count, err
