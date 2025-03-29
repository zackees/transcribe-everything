"""
Unit test file.
"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from transcribe_everything import run
from transcribe_everything.args import Args

COMMAND = "transcribe_everything"


class MainTester(unittest.TestCase):
    """Main tester class."""

    def setUp(self):
        """Run before tests."""
        # Monkey patch so that the test doesn't fail with fake files.
        run.transcribe = lambda src, dst: None

    def test_demo_run_with_real_fs(self) -> None:
        """Test command line interface (CLI)."""

        with TemporaryDirectory() as tmpdir:
            cwd: Path = Path(tmpdir)
            (cwd / "test.mp4").touch()
            (cwd / "test.txt").touch()
            (cwd / "test.mp3").touch()
            args: Args = Args(
                src=cwd.as_posix(),
                max_batches=1,
                batch_size=1,
            )
            count, err = run.run(args)
            self.assertEqual(1, count)
            self.assertIsNone(err)


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
