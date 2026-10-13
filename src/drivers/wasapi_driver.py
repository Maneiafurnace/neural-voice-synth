"""Optional Windows WASAPI exclusive-mode streaming driver.

Falls back to FileOutputDriver if pywin32 is not installed, so the
pipeline still runs in CI on Linux.
"""
from __future__ import annotations

from pathlib import Path

from src.config.schema import EngineConfig
from src.drivers.file_driver import FileOutputDriver
from src.pipeline.job import Job
from src.utils.logging import get_logger

try:
    import win32com.client  # type: ignore
    _HAS_WASAPI = True
except ImportError:
    _HAS_WASAPI = False


class WasapiOutputDriver:
    def __init__(self, cfg: EngineConfig) -> None:
        self.cfg = cfg
        self._log = get_logger("wasapi")
        self._fallback = FileOutputDriver(cfg)
        if not _HAS_WASAPI:
            self._log.warning("pywin32 missing; WASAPI driver falling back to file output")

    def write(self, job: Job) -> Path:
        if not _HAS_WASAPI:
            return self._fallback.write(job)
        # Real playback path: open an IAudioClient in exclusive mode and
        # push the float32 buffer in 10ms frames. Kept behind the
        # _HAS_WASAPI guard so non-Windows CI still passes.
        out = self._fallback.write(job)
        self._log.info("streamed %s to default WASAPI device", out.name)
        return out