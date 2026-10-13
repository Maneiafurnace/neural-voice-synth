"""Resolve a voice profile name to a reference embedding path."""
from __future__ import annotations

from pathlib import Path

from src.config.schema import EngineConfig
from src.pipeline.job import Job, JobStage

_VOICES_DIR = Path(__file__).resolve().parents[2] / "voices" / "profiles"


class VoicePickerHandler:
    def __init__(self, cfg: EngineConfig) -> None:
        self.cfg = cfg

    def handle(self, job: Job) -> Job:
        profile = _VOICES_DIR / f"{job.voice}.toml"
        if not profile.exists():
            job.stage = JobStage.FAILED
            job.error = f"voice profile '{job.voice}' not found at {profile}"
            return job
        job.payload["voice_profile"] = profile
        return job