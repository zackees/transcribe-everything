"""
Main entry point.
"""

import argparse
from dataclasses import dataclass


@dataclass
class Args:
    src: str
    dst: str

    @staticmethod
    def parse_args() -> "Args":
        return _parse_args()

    def __post_init__(self):
        assert isinstance(self.src, str), f"Expected str, got {type(self.src)}"
        assert (
            isinstance(self.dst, str) or self.dst is None
        ), f"Expected str or None, got {type(self.dst)}"


def _parse_args() -> Args:
    parser = argparse.ArgumentParser(description="Transcribe everything.")
    parser.add_argument("src", type=str, help="Source path.")
    parser.add_argument(
        "dst", type=str, help="Destination path (can be the same as src)"
    )

    tmp = parser.parse_args()
    return Args(
        src=tmp.src,
        dst=tmp.dst,
    )
