"""Text -> phoneme id sequence. Wraps the configured G2P backend."""
from __future__ import annotations

from src.config.schema import EngineConfig
from src.pipeline.job import Job, JobStage
from src.utils.text import chunk_sentences


class PhonemeProcessor:
    def __init__(self, cfg: EngineConfig) -> None:
        self.cfg = cfg
        self._g2p = _load_backend(cfg.model.phonemizer)

    def process(self, job: Job) -> Job:
        text = job.payload.get("raw_text", job.text)
        chunks = chunk_sentences(text, max_chars=280)
        phoneme_ids: list[list[int]] = []
        for piece in chunks:
            try:
                phoneme_ids.append(self._g2p.encode(piece))
            except Exception as exc:  # noqa: BLE001
                job.stage = JobStage.FAILED
                job.error = f"phonemize failed on {piece[:40]!r}: {exc}"
                return job
        job.payload["phoneme_chunks"] = phoneme_ids
        job.stage = JobStage.PHONEMIZED
        return job


def _load_backend(name: str):
    if name.startswith("espeak"):
        from src.utils.espeak import EspeakBackend

        return EspeakBackend(language="en-us")
    raise ValueError(f"unknown phonemizer backend: {name}")