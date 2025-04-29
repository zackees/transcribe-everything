


# # Docker
#   * Install
#     * docker pull niteris/transcribe-everything

#   * Help
#     * docker run --rm -it niteris/transcribe-everything --help

#   * Running
#     * Windows cmd.exe: `docker run --rm -it -v "%cd%\rclone.conf:/app/rclone.conf" niteris/transcribe-everything dst:TorrentBooks/podcast/dialogueworks01/youtube`
#     * Macos/Linux: `docker run --rm -it -v "$(pwd)/rclone.conf:/app/rclone.conf" niteris/transcribe-everything dst:TorrentBooks/podcast/dialogueworks01/youtube`

import os
import argparse
from dataclasses import dataclass
from pathlib import Path

def _parse_args() -> "Args":
    parser = argparse.ArgumentParser(description="Transcribe everything.")
    parser.add_argument("src", type=str, help="Source path.")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Maximum number of files to process in a batch.",
    )
    parser.add_argument(
        "--max-batches",
        type=int,
        default=10,
        help="Maximum number of batches to process.",
    )
    parser.add_argument(
        "--no-randomize",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--rclone-conf",
        type=Path,
        default=Path("rclone.conf"),
        help="Path to rclone configuration file.",
    )

    tmp = parser.parse_args()
    return Args(
        src=tmp.src,
        batch_size=tmp.batch_size,
        max_batches=tmp.max_batches,
        randomize=not tmp.no_randomize,
        rclone_conf=tmp.rclone_conf
    )

@dataclass
class Args:
    src: str
    batch_size: int
    max_batches: int
    randomize: bool
    rclone_conf: Path

    @staticmethod
    def parse_args() -> "Args":
        return _parse_args()

    def __post_init__(self):
        assert isinstance(self.src, str), f"Expected str, got {type(self.src)}"
        assert isinstance(self.batch_size, int), f"Expected int, got {type(self.batch_size)}"
        assert isinstance(self.max_batches, int), f"Expected int, got {type(self.max_batches)}"
        assert isinstance(self.randomize, bool), f"Expected bool, got {type(self.randomize)}"
        assert isinstance(self.rclone_conf, Path), f"Expected Path, got {type(self.rclone_conf)}"

# def _rclone_volume_path() -> str:
#     import platform
#     is_windows = platform.system() == "Windows"
#     if is_windows:
#         return r"%cd%\rclone.conf"
#     else:
#         return "$(pwd)/rclone.conf"

def _to_volume_path(rclone_name: str) -> str:
    """Convert a Path to a volume path for Docker."""
    import platform
    is_windows = platform.system() == "Windows"
    if is_windows:
        return f"%cd%\{rclone_name}:/app/rclone.conf"
    else:
        return f"{rclone_name}:/app/rclone.conf"

def main() -> int:
    """Main entry point for the template_python_cmd package."""
    args = Args.parse_args()
    print(f"Running with args: {args}")
    # switch to the directory of the rclone.conf file
    os.chdir(args.rclone_conf.parent)
    # Here you would call your main function, e.g.:
    # err_count = run(args)
    # return 0 if not err_count else 1
    cmd_pull = "docker pull niteris/transcribe-everything"
    rclone_conf_str = _to_volume_path(args.rclone_conf.name)
    cmd_run = f"docker run --rm -it --gpus all -v {rclone_conf_str} niteris/transcribe-everything {args.src}"

    print(f"Running command: {cmd_pull}")
    os.system(cmd_pull)
    print(f"Running command: {cmd_run}")
    os.system(cmd_run)

if __name__ == "__main__":
    import sys
    src = "dst:TorrentBooks/podcast/dialogueworks01/youtube"
    sys.argv.append(src)
    # sys.argv.append("--batch-size")
    # sys.argv.append("20")
    # sys.exit(main())
    main()