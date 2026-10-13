"""Phoneme ids -> mel spectrogram, via the acoustic ONNX model."""
from __future__ import annotations

import numpy as np

from src.config.schema import EngineConfig
from src.models.acoustic_loader import AcousticModel
from src.pipeline.job import Job, JobStage


class AcousticProcessor:
    def __init__(self, cfg: EngineConfig, model: AcousticModel) -> None:
        self.cfg = cfg
        self.model = model

    def process(self, job: Job) -> Job:
        chunks = job.payload.get("phoneme_chunks")
        if not chunks:
            job.stage = JobStage.FAILED
            job.error = "no phoneme chunks to synthesize"
            return job

        mels: list[np.ndarray] = []
        for ids in chunks:
            arr = np.asarray(ids, dtype=np.int64)[None, :]
            mel = self.model.infer(arr)          # (1, T, mel_bins)
            mels.append(mel[0])                  # (T, mel_bins)

        mel = np.concatenate(mels, axis=0).astype(np.float32)
        job.payload["mel"] = mel
        job.stage = JobStage.ACOUSTIC
        return job