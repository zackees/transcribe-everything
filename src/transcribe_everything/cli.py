"""
Main entry point.
"""

import sys
import warnings

from transcribe_everything.args import Args
from transcribe_everything.run import run


def main() -> int:
    """Main entry point for the template_python_cmd package."""
    args = Args.parse_args()
    count, err = run(args)
    print(f"Processed {count} files.")
    if err:
        warnings.warn(str(err))
    return 0 if not err else 1


if __name__ == "__main__":
    src = "dst:TorrentBooks/podcast"
    sys.argv.append(src)
    sys.argv.append("--max-batches")
    sys.argv.append("1")
    sys.argv.append("--batch-size")
    sys.argv.append("1")
    sys.exit(main())
