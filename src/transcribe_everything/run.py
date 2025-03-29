"""
Main entry point.
"""

from dataclasses import dataclass
from typing import Callable, Iterator

from virtual_fs import FSPath, Vfs

from transcribe_everything.args import Args
from transcribe_everything.transcribe import transcribe
from transcribe_everything.util import is_media_file


def _reduce(files: list[FSPath]) -> list[FSPath]:
    # take all the media files, remove the suffix, add .txt. If that file
    # exists then remove it from the list
    files_set: set[FSPath] = set(files)
    files_out: list[FSPath] = []
    for file in files:
        if file.with_suffix(".txt") in files_set:
            continue
        files_out.append(file)
    return files_out


@dataclass
class Batch:
    files: list[FSPath]
    root: FSPath

    def __post_init__(self) -> None:
        assert isinstance(self.files, list), f"Expected list, got {type(self.files)}"
        assert isinstance(self.root, FSPath), f"Expected FSPath, got {type(self.root)}"

    def __str__(self) -> str:
        return f"Batch(root={self.root}, files={self.files})"

    def __repr__(self) -> str:
        return str(self)

    def unprocessed(self, max_size: int | None = None) -> list[FSPath]:
        out = _reduce(self.files)
        if max_size is not None:
            out = out[:max_size]
        return out

    def processed(self) -> list[FSPath]:
        return [file.with_suffix(".txt") for file in self.files]

    def __bool__(self) -> bool:
        return bool(self.unprocessed())

    def __len__(self) -> int:
        return len(self.unprocessed())

    def __iter__(self) -> Iterator[FSPath]:
        return iter(self.unprocessed())


def find_batches(args: Args) -> list[Batch]:
    max_batches = args.max_batches
    vfs_src = Vfs.begin(src=args.src)

    with vfs_src:
        batches: list[Batch] = []

        with vfs_src.walk_begin() as walker:
            for root, _, files in walker:
                if len(batches) >= max_batches:
                    return batches
                media_files: list[FSPath] = []
                for file in files:
                    if is_media_file(file):
                        media_files.append(root / file)
                if len(media_files) > 0:
                    batch = Batch(files=media_files, root=root)
                    if batch:
                        batches.append(batch)
    return batches


def _run_witch_callback(
    args: Args, callback: Callable[[FSPath, FSPath], None]
) -> Exception | None:
    try:
        batch_size = args.batch_size
        batches = find_batches(args)

        for batch in batches:
            unprocessed = batch.unprocessed()[:batch_size]
            for file in unprocessed:
                dst_file = file.with_suffix(".txt")
                callback(file, dst_file)
    except Exception as e:
        return e
    return None


def run(args: Args) -> tuple[int, Exception | None]:

    count = 0

    def task(file: FSPath, dst: FSPath) -> None:
        nonlocal count
        transcribe(file, dst)
        count += 1

    err = _run_witch_callback(args, task)
    if err:
        import warnings

        warnings.warn(f"Error: {err}")
    return count, err
