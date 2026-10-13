"""Terminal sink: write the post-processed waveform to a WAV file."""
from __future__ import annotations

import hashlib
from pathlib import Path

import soundfile as sf

from src.config.schema import EngineConfig
from src.pipeline.job import Job, JobStage


class FileOutputDriver:
    def __init__(self, cfg: EngineConfig) -> None:
        self.cfg = cfg
        self.out_dir = Path(cfg.output.out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def write(self, job: Job) -> Path:
        wav = job.payload.get("wav")
        if wav is None:
            job.stage = JobStage.FAILED
            job.error = "driver got no waveform"
            return self.out_dir / f"{job.id}.wav"

        path = Path(job.out_path) if job.out_path else self._default_path(job)
        path.parent.mkdir(parents=True, exist_ok=True)
        sf.write(
            path,
            wav,
            self.cfg.engine.sample_rate,
            subtype=f"PCM_{self.cfg.engine.bit_depth}",
        )
        job.stage = JobStage.WRITTEN
        return path

    def _default_path(self, job: Job) -> Path:
        digest = hashlib.sha1(
            (job.text + job.voice).encode("utf-8")
        ).hexdigest()[:10]
        return self.out_dir / f"{job.voice}-{digest}.wav"