"""
Unit test file.
"""

import unittest

from transcribe_everything.args import Args
from transcribe_everything.batch import Batch, find_batches


class BatchTester(unittest.TestCase):
    """Main tester class."""

    def test_find_batches(self) -> None:
        """Test command line interface (CLI)."""
        args: Args = Args(
            src="dst:TorrentBooks/podcast/dialogueworks01",
            max_batches=1,
            batch_size=1,
            randomize=False,
        )
        batches: list[Batch] = find_batches(args)
        self.assertEqual(1, len(batches))
        batch = batches[0]
        unprocessed_files = batch.unprocessed()
        # print(unprocessed_files)
        # print(batches)
        needle = "A_Recipe_for_Disaster_Joseph_Atkins.txt"
        found = False
        for file in unprocessed_files:
            if needle in file.name:
                found = True
                break
        self.assertFalse(found, f"File {needle} found in unprocessed files.")
        print("done")


if __name__ == "__main__":
    unittest.main()
