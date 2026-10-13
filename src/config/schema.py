"""Typed config dataclasses. Kept deliberately flat."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class EngineSection:
    sample_rate: int = 24000
    bit_depth: int = 16
    channels: int = 1
    device: str = "cpu"
    num_workers: int = 3
    queue_depth: int = 64


@dataclass(slots=True)
class ModelSection:
    acoustic: str = ""
    vocoder: str = ""
    phonemizer: str = "espeak-ng"
    max_text_chars: int = 4000


@dataclass(slots=True)
class VocoderSection:
    upsample: list[int] = field(default_factory=lambda: [8, 8, 2, 2])
    mel_bins: int = 80
    mel_fmin: float = 40.0
    mel_fmax: float = 7600.0


@dataclass(slots=True)
class OutputSection:
    driver: str = "file"
    out_dir: str = "out"
    loudness_target_lufs: float = -16.0
    normalize_peak: float = 0.97


@dataclass(slots=True)
class LoggingSection:
    level: str = "INFO"
    json: bool = False


@dataclass(slots=True)
class EngineConfig:
    engine: EngineSection = field(default_factory=EngineSection)
    model: ModelSection = field(default_factory=ModelSection)
    vocoder: VocoderSection = field(default_factory=VocoderSection)
    output: OutputSection = field(default_factory=OutputSection)
    logging: LoggingSection = field(default_factory=LoggingSection)

    @classmethod
    def from_dict(cls, d: dict) -> "EngineConfig":
        return cls(
            engine=EngineSection(**d.get("engine", {})),
            model=ModelSection(**d.get("model", {})),
            vocoder=VocoderSection(**d.get("vocoder", {})),
            output=OutputSection(**d.get("output", {})),
            logging=LoggingSection(**d.get("logging", {})),
        )