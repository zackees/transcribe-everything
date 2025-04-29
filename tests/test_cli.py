"""
Unit test file.
"""

import os
import unittest


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_main(self) -> None:
        """Test command line interface (CLI)."""
        rtn = os.system("transcribe-everything --help")
        self.assertEqual(0, rtn)

    def test_docker_main(self) -> None:
        """Test docker command line interface (CLI)."""
        rtn = os.system("transcribe-everything-run-docker --help")
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()
