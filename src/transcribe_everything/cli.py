"""
Main entry point.
"""

import logging
import sys
import warnings

from transcribe_everything.args import Args
from transcribe_everything.run import run

# Initialize logging for info on this package

logger = logging.getLogger("transcribe_everything")
logger.setLevel(logging.INFO)


def main() -> int:
    """Main entry point for the template_python_cmd package."""
    args = Args.parse_args()
    err_count = 0
    while True:
        count, err = run(args)
        err_count += 1 if err else 0
        if err:
            warnings.warn(str(err))
            err_count += 1
        if count == 0:
            break

    return 0 if not err_count else 1


if __name__ == "__main__":
    src = "dst:TorrentBooks/podcast"
    sys.argv.append(src)
    sys.argv.append("--max-batches")
    sys.argv.append("1")
    sys.argv.append("--batch-size")
    sys.argv.append("1")
    sys.exit(main())
