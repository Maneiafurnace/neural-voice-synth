"""ONNX-backed HiFi-GAN vocoder wrapper (mel -> waveform)."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import onnxruntime as ort


class VocoderModel:
    """Input:  float32 (1, T, mel_bins). Output: float32 (1, N)."""

    def __init__(self, path: str | Path, device: str = "cpu") -> None:
        providers = ["CPUExecutionProvider"]
        if device in ("cuda", "dml"):
            providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        self._session = ort.InferenceSession(str(path), providers=providers)
        self._input_name = self._session.get_inputs()[0].name

    def infer(self, mel: np.ndarray) -> np.ndarray:
        return self._session.run(None, {self._input_name: mel})[0]