"""
Unit test file.
"""

import unittest
from concurrent.futures import Future
from pathlib import Path
from tempfile import TemporaryDirectory

from transcribe_everything import run
from transcribe_everything.args import Args

COMMAND = "transcribe_everything"


def _fake_transcribe_async(src: Path, dst: Path) -> Future:
    """Dummy future callback."""
    out = Future()
    out.set_result(None)
    return out


class MainTester(unittest.TestCase):
    """Main tester class."""

    def setUp(self):
        """Run before tests."""
        # Monkey patch so that the test doesn't fail with fake files.
        run.transcribe_async = _fake_transcribe_async

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
