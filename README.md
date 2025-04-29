# transcribe-everything

[![Build Docker Image](https://github.com/zackees/transcribe-everything/actions/workflows/build_docker_image.yml/badge.svg)](https://github.com/zackees/transcribe-everything/actions/workflows/build_docker_image.yml)

Transcribes everything! Point this solution to a remote directory and this tool will find all the media files (*.mp3, *.mp4) and if there is no *.txt present, it will be transcribed. Will continue until all files are transcribed.

# Docker
  * Install
    * 

  * Help
    * docker run --rm -it niteris/transcribe-everything --help

  * Make sure docker is installed for your system.

  * Install using the `transcribe-everything-run-docker` tool (easy)
    * `uv venv`
    * `uv pip install transcribe-everything`
    * `uv run transcribe-everything-run-docker --gpu-batch-size 8 --gpu-jobs 1`
      * Play `--gpu-batch-size` and `--gpu-jobs` for performance tuning.
      * Defaults are tested to run stable for Nvidia 3070 12gb card.

  * Install + Running (Manually)
    * Pull the image: `docker pull niteris/transcribe-everything`
    * Windows cmd.exe: `docker run --rm -it -v ".\rclone.conf:/app/rclone.conf" --gpus all niteris/transcribe-everything dst:TorrentBooks/podcast/dialogueworks01/youtube`
    * Macos/Linux: `docker run --rm -it -v "$./rclone.conf:/app/rclone.conf" --gpus all niteris/transcribe-everything dst:TorrentBooks/podcast/dialogueworks01/youtube`
