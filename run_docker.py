


# # Docker
#   * Install
#     * docker pull niteris/transcribe-everything

#   * Help
#     * docker run --rm -it niteris/transcribe-everything --help

#   * Running
#     * Windows cmd.exe: `docker run --rm -it -v "%cd%\rclone.conf:/app/rclone.conf" niteris/transcribe-everything dst:TorrentBooks/podcast/dialogueworks01/youtube`
#     * Macos/Linux: `docker run --rm -it -v "$(pwd)/rclone.conf:/app/rclone.conf" niteris/transcribe-everything dst:TorrentBooks/podcast/dialogueworks01/youtube`

import subprocess
import os
import argparse
from dataclasses import dataclass
from pathlib import Path

def _parse_args() -> "Args":
    parser = argparse.ArgumentParser(description="Transcribe everything.")
    parser.add_argument("src", type=str, help="Source path.")

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
        randomize=not tmp.no_randomize,
        rclone_conf=tmp.rclone_conf
    )

@dataclass
class Args:
    src: str
    randomize: bool
    rclone_conf: Path

    @staticmethod
    def parse_args() -> "Args":
        return _parse_args()

    def __post_init__(self):
        assert isinstance(self.src, str), f"Expected str, got {type(self.src)}"
        assert isinstance(self.randomize, bool), f"Expected bool, got {type(self.randomize)}"
        assert isinstance(self.rclone_conf, Path), f"Expected Path, got {type(self.rclone_conf)}"


def _to_volume_path(rclone_name: str) -> str:
    """Convert a Path to a volume path for Docker."""
    import platform
    is_windows = platform.system() == "Windows"
    if is_windows:
        return f".\{rclone_name}:/app/rclone.conf"
    else:
        return f"./{rclone_name}:/app/rclone.conf"

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

    cmd_list: list[str] = [
        "docker",
        "run",
        "--rm",
        "-it",
        "--gpus",
        "all",
        "-v",
        rclone_conf_str,
        "niteris/transcribe-everything",
        args.src,
    ]

    cmd_run = subprocess.list2cmdline(cmd_list)
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