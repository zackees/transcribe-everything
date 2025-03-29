"""
Main entry point.
"""

import argparse
import sys
from dataclasses import dataclass

from virtual_fs import Vfs


@dataclass
class Args:
    src: str
    dst: str

    def __post_init__(self):
        assert isinstance(self.src, str), f"Expected str, got {type(self.src)}"
        assert (
            isinstance(self.dst, str) or self.dst is None
        ), f"Expected str or None, got {type(self.dst)}"


def _parse_args() -> Args:
    parser = argparse.ArgumentParser(description="Transcribe everything.")
    parser.add_argument("src", type=str, help="Source path.")
    parser.add_argument(
        "dst", type=str, help="Destination path (can be the same as src)"
    )

    tmp = parser.parse_args()
    return Args(
        src=tmp.src,
        dst=tmp.dst,
    )


def main() -> int:
    """Main entry point for the template_python_cmd package."""
    args = _parse_args()

    vfs_src = Vfs.begin(src=args.src)
    vfs_dst = Vfs.begin(src=args.dst)

    with vfs_src as src, vfs_dst as dst:

        print(f"src: {src}")
        print(f"dst: {dst}")

        for root, files, dirs in vfs_src.walk():
            print(f"root: {root}")
            print(f"files: {files}")
            print(f"dirs: {dirs}")
    return 0


if __name__ == "__main__":
    src = "dst:TorrentBooks/podcast"
    dst = "dst:TorrentBooks/podcast"
    sys.argv.append(src)
    sys.argv.append(dst)
    sys.exit(main())
