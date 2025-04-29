# # Docker
#   * Install
#     * docker pull niteris/transcribe-everything

#   * Help
#     * docker run --rm -it niteris/transcribe-everything --help

#   * Running
#     * Windows cmd.exe: `docker run --rm -it -v "%cd%\rclone.conf:/app/rclone.conf" niteris/transcribe-everything dst:TorrentBooks/podcast/dialogueworks01/youtube`
#     * Macos/Linux: `docker run --rm -it -v "$(pwd)/rclone.conf:/app/rclone.conf" niteris/transcribe-everything dst:TorrentBooks/podcast/dialogueworks01/youtube`

import argparse
import subprocess
import sys
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
        "--config",
        type=Path,
        default=Path("rclone.conf"),
        help="Path to rclone configuration file.",
    )
    parser.add_argument(
        "--gpu-batch-size",
        type=int,
        required=False,
    )
    parser.add_argument(
        "--gpu-jobs",
        type=int,
        default=1,
        help="Number of GPU jobs to run in parallel.",
    )

    tmp = parser.parse_args()
    assert (
        tmp.rclone_conf.exists()
    ), f"Please specify --config and point to a rclone.conf file. File does not exist: {tmp.rclone_conf}"
    return Args(
        src=tmp.src,
        randomize=not tmp.no_randomize,
        rclone_conf=tmp.rclone_conf,
        gpu_batch_size=tmp.gpu_batch_size,
        gpu_jobs=tmp.gpu_jobs,
    )


@dataclass
class Args:
    src: str
    randomize: bool
    rclone_conf: Path
    gpu_batch_size: int | None
    gpu_jobs: int

    @staticmethod
    def parse_args() -> "Args":
        return _parse_args()

    def __post_init__(self):
        assert isinstance(self.src, str), f"Expected str, got {type(self.src)}"
        assert isinstance(
            self.randomize, bool
        ), f"Expected bool, got {type(self.randomize)}"
        assert isinstance(
            self.rclone_conf, Path
        ), f"Expected Path, got {type(self.rclone_conf)}"


def _to_volume_path(rclone_config_path: Path) -> str:
    """Convert a Path to a volume path for Docker."""
    abs_path = rclone_config_path.resolve()
    return f"{abs_path}:/app/rclone.conf"


def main() -> int:
    """Main entry point for the template_python_cmd package."""
    args = Args.parse_args()
    print(f"Running with args: {args}")
    # switch to the directory of the rclone.conf file
    # os.chdir(args.rclone_conf.parent)
    # Here you would call your main function, e.g.:
    # err_count = run(args)
    # return 0 if not err_count else 1
    cmd_pull = "docker pull niteris/transcribe-everything"
    rclone_conf_str = _to_volume_path(args.rclone_conf)

    # cmd_list_run: list[str] = [
    #     "docker",
    #     "run",
    #     "--rm",
    #     "-it",
    #     "--gpus",
    #     "all",
    #     "-v",
    #     rclone_conf_str,
    #     "niteris/transcribe-everything",
    #     args.src,
    # ]

    # if args.gpu_batch_size is not None:
    #     cmd_list_run.extend(["-e", "GPU_BATCH_SIZE=" + str(args.gpu_batch_size)])

    cmd_list_run: list[str] = [
        "docker",
        "run",
        "--rm",
    ]
    if sys.stdout.isatty():
        cmd_list_run.append("-t")
    cmd_list_run += [
        "--gpus",
        "all",
    ]
    if args.gpu_batch_size is not None:
        cmd_list_run.extend(["-e", "GPU_BATCH_SIZE=" + str(args.gpu_batch_size)])
    if args.gpu_jobs > 1:
        cmd_list_run.extend(["-e", "GPU_JOBS=" + str(args.gpu_jobs)])
    cmd_list_run += [
        "-v",
        rclone_conf_str,
        "niteris/transcribe-everything",
        args.src,
    ]
    cmd_run = subprocess.list2cmdline(cmd_list_run)
    print(f"Running command: {cmd_pull}")
    rtn = subprocess.call(cmd_pull, shell=True)
    if rtn != 0:
        print(f"Failed to pull docker image: {rtn}")
        return 1
    print(f"Running command: {cmd_run}")
    rtn = subprocess.call(cmd_run, shell=True)
    return rtn


# docker run --rm -it --gpus all -e GPU_BATCH_SIZE=40 -v /root/rclone.conf:/app/rclone.conf niteris/transcribe-everything dst:TorrentBooks/podcast

if __name__ == "__main__":
    import sys

    src = "dst:TorrentBooks/podcast/dialogueworks01/youtube"
    sys.argv.append(src)
    # sys.argv.append("--batch-size")
    # sys.argv.append("20")
    # sys.exit(main())
    main()
