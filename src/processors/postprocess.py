"""Peak normalize + loudness target. Pure numpy, no scipy dependency at runtime."""
from __future__ import annotations

import numpy as np

from src.config.schema import EngineConfig
from src.pipeline.job import Job, JobStage


class PostProcessProcessor:
    def __init__(self, cfg: EngineConfig) -> None:
        self.cfg = cfg

    def process(self, job: Job) -> Job:
        wav = job.payload.get("wav")
        if wav is None:
            job.stage = JobStage.FAILED
            job.error = "postprocess ran with no waveform"
            return job

        peak = float(np.max(np.abs(wav))) or 1.0
        target = self.cfg.output.normalize_peak
        wav = wav * (target / peak)

        rms = float(np.sqrt(np.mean(wav ** 2))) or 1e-6
        target_rms = 10 ** (self.cfg.output.loudness_target_lufs / 20.0)
        wav = (wav * (target_rms / rms)).astype(np.float32)

        job.payload["wav"] = np.clip(wav, -1.0, 1.0)
        job.payload["duration_s"] = len(wav) / self.cfg.engine.sample_rate
        job.stage = JobStage.POSTPROCESSED
        return job