"""Job/result dataclasses shared across handlers and processors."""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class JobStage(str, Enum):
    INGESTED = "ingested"
    PHONEMIZED = "phonemized"
    ACOUSTIC = "acoustic"
    VOCODED = "vocoded"
    POSTPROCESSED = "postprocessed"
    WRITTEN = "written"
    FAILED = "failed"


@dataclass(slots=True)
class Job:
    text: str
    voice: str
    out_path: Any = None
    stream: bool = False
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    stage: JobStage = JobStage.INGESTED
    t0: float = field(default_factory=time.perf_counter)
    payload: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass(slots=True)
class JobResult:
    job_id: str
    path: str
    duration_s: float
    wall_ms: float
    stage: JobStage