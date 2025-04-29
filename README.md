# transcribe-everything

[![Build Docker Image](https://github.com/zackees/transcribe-everything/actions/workflows/build_docker_image.yml/badge.svg)](https://github.com/zackees/transcribe-everything/actions/workflows/build_docker_image.yml)

Transcribes everything! Point this solution to a remote directory and this tool will find all the media files (*.mp3, *.mp4) and if there is no *.txt present, it will be transcribed. Will continue until all files are transcribed.

# Docker
  * Install
    * docker pull niteris/transcribe-everything

  * Help
    * docker run --rm -it niteris/transcribe-everything --help

  * Running
    * Windows cmd.exe: `docker run --rm -it -v "%cd%\rclone.conf:/app/rclone.conf" niteris/transcribe-everything dst:TorrentBooks/podcast/dialogueworks01/youtube`
    * Macos/Linux: `docker run --rm -it -v "$(pwd)/rclone.conf:/app/rclone.conf" niteris/transcribe-everything dst:TorrentBooks/podcast/dialogueworks01/youtube`
