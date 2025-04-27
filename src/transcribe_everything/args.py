"""
Main entry point.
"""

import argparse
from dataclasses import dataclass


@dataclass
class Args:
    src: str
    batch_size: int
    max_batches: int
    randomize: bool

    @staticmethod
    def parse_args() -> "Args":
        return _parse_args()

    def __post_init__(self):
        assert isinstance(self.src, str), f"Expected str, got {type(self.src)}"


def _parse_args() -> Args:
    parser = argparse.ArgumentParser(description="Transcribe everything.")
    parser.add_argument("src", type=str, help="Source path.")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Maximum number of files to process in a batch.",
    )
    parser.add_argument(
        "--max-batches",
        type=int,
        default=10,
        help="Maximum number of batches to process.",
    )
    parser.add_argument(
        "--no-randomize",
        action="store_true",
        default=False,
    )

    tmp = parser.parse_args()
    return Args(
        src=tmp.src,
        batch_size=tmp.batch_size,
        max_batches=tmp.max_batches,
        randomize=not tmp.no_randomize,
    )
