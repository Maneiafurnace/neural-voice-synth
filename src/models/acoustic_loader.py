"""ONNX-backed acoustic model wrapper (text/phonemes -> mel)."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import onnxruntime as ort


class AcousticModel:
    """Wraps an ONNX acoustic model.

    Input:  int64 tensor of shape (1, T) — phoneme ids.
    Output: float32 tensor of shape (1, T, mel_bins).
    """

    def __init__(self, path: str | Path, device: str = "cpu") -> None:
        providers = ["CPUExecutionProvider"]
        if device == "cuda":
            providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        self._session = ort.InferenceSession(str(path), providers=providers)
        self._input_name = self._session.get_inputs()[0].name

    def infer(self, phoneme_ids: np.ndarray) -> np.ndarray:
        return self._session.run(None, {self._input_name: phoneme_ids})[0]