"""
Main entry point.
"""

import sys

from transcribe_everything.args import Args
from transcribe_everything.run import run


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
