"""Ingest handler: normalize and validate incoming text."""
from __future__ import annotations

import re
import unicodedata

from src.config.schema import EngineConfig
from src.pipeline.job import Job

_WS = re.compile(r"\s+")


class TextIngestHandler:
    def __init__(self, cfg: EngineConfig) -> None:
        self.cfg = cfg

    def handle(self, job: Job) -> Job:
        text = unicodedata.normalize("NFC", job.text)
        text = _WS.sub(" ", text).strip()
        if len(text) > self.cfg.model.max_text_chars:
            raise ValueError(
                f"text length {len(text)} exceeds max_text_chars "
                f"{self.cfg.model.max_text_chars}"
            )
        job.payload["raw_text"] = text
        return job