"""Mel spectrogram -> waveform, via the vocoder ONNX model."""
from __future__ import annotations

import numpy as np

from src.config.schema import EngineConfig
from src.models.vocoder_loader import VocoderModel
from src.pipeline.job import Job, JobStage


class VocoderProcessor:
    def __init__(self, cfg: EngineConfig, model: VocoderModel) -> None:
        self.cfg = cfg
        self.model = model

    def process(self, job: Job) -> Job:
        mel = job.payload.get("mel")
        if mel is None:
            job.stage = JobStage.FAILED
            job.error = "vocoder ran with no mel spectrogram"
            return job
        wav = self.model.infer(mel[None, :, :])   # (1, N)
        job.payload["wav"] = wav[0].astype(np.float32)
        job.stage = JobStage.VOCODED
        return job