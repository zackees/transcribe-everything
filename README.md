# transcribe-everything

Transcribes everything!

# Docker
  * Install
    * docker pull niteris/transcribe-everything

  * Help
    * docker run --rm -it niteris/transcribe-everything --help

  * Running
    * Windows cmd.exe: `docker run --rm -it -v "%cd%\rclone.conf:/app/rclone.conf" niteris/transcribe-everything dst:TorrentBooks/podcast/dialogueworks01/youtube`
    * Macos/Linux: `docker run --rm -it -v "$(pwd)/rclone.conf:/app/rclone.conf" niteris/transcribe-everything dst:TorrentBooks/podcast/dialogueworks01/youtube`
