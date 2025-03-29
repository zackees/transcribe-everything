"""
Main entry point.
"""

from dataclasses import dataclass
from typing import Iterator

from virtual_fs import FSPath, Vfs

from transcribe_everything.args import Args
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


def find_files(args: Args) -> list[Batch]:
    vfs_src = Vfs.begin(src=args.src)
    vfs_dst = Vfs.begin(src=args.dst)

    with vfs_src, vfs_dst:
        batches: list[Batch] = []

        with vfs_src.walk_begin() as walker:
            for root, _, files in walker:
                media_files: list[FSPath] = []
                for file in files:
                    if is_media_file(file):
                        media_files.append(root / file)
                if len(media_files) > 0:
                    batches.append(Batch(files=media_files, root=root))
    return batches


def run(args: Args) -> int:
    batches = find_files(args)
    print(f"Found {len(batches)} batches.")

    for batch in batches:
        for file in batch:
            print(f"Found unprocessed file: {file}")
    return 0
