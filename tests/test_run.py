"""
Unit test file.
"""

import unittest

from transcribe_everything.args import Args
from transcribe_everything.run import run

COMMAND = "transcribe_everything"


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        args: Args = Args(
            src="dst:TorrentBooks/podcast",
            max_batches=1,
            batch_size=1,
        )
        rtn = run(args)
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()


"""


import sys

from transcribe_everything.args import Args
from transcribe_everything.run import run


def main() -> int:
    args = Args.parse_args()
    return run(args)


if __name__ == "__main__":
    src = "dst:TorrentBooks/podcast"
    dst = "dst:TorrentBooks/podcast"
    sys.argv.append(src)
    sys.argv.append(dst)
    sys.exit(main())

"""
