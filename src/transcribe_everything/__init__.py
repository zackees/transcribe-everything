from concurrent.futures import Future

from virtual_fs import FSPath, RealFS, Vfs

__version__ = "1.5.26"


class Api:
    """API class for transcribe_everything."""

    @staticmethod
    def get_version() -> str:
        """Get the version of the package."""
        return __version__

    @staticmethod
    def transcribe_async(src: str, dst: str) -> Future[Exception | None]:
        # Vfs.from_path(src)
        from transcribe_everything.transcription_pipeline import transcribe_async

        with Vfs.begin(src) as src_fs:
            with Vfs.begin(dst) as dst_fs:
                return transcribe_async(src_fs, dst_fs)


__all__ = ["__version__", "Api", "RealFS", "FSPath"]
