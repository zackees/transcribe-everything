"""
Main entry point.
"""

import sys

from virtual_fs import FSPath, Vfs

from transcribe_everything.cli_args import Args
from transcribe_everything.util import is_media_file


def run(args: Args) -> int:
    vfs_src = Vfs.begin(src=args.src)
    vfs_dst = Vfs.begin(src=args.dst)

    with vfs_src as src, vfs_dst as dst:

        print(f"src: {src}")
        print(f"dst: {dst}")

        media_files: list[FSPath] = []

        with vfs_src.walk_begin() as walker:
            for root, _, files in walker:
                for file in files:
                    if is_media_file(file):
                        media_files.append(root / file)
                if len(media_files) > 0:
                    break

        print(f"found {len(media_files)} media files")
        for media_file in media_files:
            print(media_file)
    return 0


def main() -> int:
    """Main entry point for the template_python_cmd package."""
    args = Args.parse_args()
    return run(args)


if __name__ == "__main__":
    src = "dst:TorrentBooks/podcast"
    dst = "dst:TorrentBooks/podcast"
    sys.argv.append(src)
    sys.argv.append(dst)
    sys.exit(main())
