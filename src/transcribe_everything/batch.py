"""
Main entry point.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from virtual_fs import FSPath, Vfs

from transcribe_everything.args import Args
from transcribe_everything.util import is_media_file


def _reduce(files: list[FSPath]) -> list[FSPath]:
    # take all the media files, remove the suffix, add .txt. If that file
    # exists then remove it from the list
    files_set: set[FSPath] = set(files)
    files_out: list[FSPath] = []
    # print("Files: ")
    # for file in files:
    #     print(f"  {file}")
    print("Now checking each file.")
    for file in files:
        if not is_media_file(file.name):
            # print(f"  Not a media file, skipping")
            continue
        file_as_txt = file.with_suffix(".txt")
        file_in_set = file_as_txt in files_set
        if file_in_set:
            # print(f"  File {file_as_txt} is already done, skipping")
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


def is_json_or_txt_file(file: str) -> bool:
    """Check if the file is a JSON or TXT file."""
    return Path(file).suffix in [".json", ".txt"]


def find_batches(args: Args) -> list[Batch]:
    max_batches = args.max_batches
    vfs_src = Vfs.begin(src=args.src)

    with vfs_src:
        batches: list[Batch] = []

        with vfs_src.walk_begin() as walker:
            for root, _, files in walker:
                if len(batches) >= max_batches:
                    return batches
                outfiles: list[FSPath] = []
                for file in files:
                    if is_media_file(file) or is_json_or_txt_file(file):
                        outfiles.append(root / file)
                if len(files) > 0:
                    batch = Batch(files=outfiles, root=root)
                    if batch:
                        batches.append(batch)
    return batches
