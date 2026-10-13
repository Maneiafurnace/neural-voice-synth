"""Thin logging factory. Structured JSON when cfg.logging.json is set."""
from __future__ import annotations

import json
import logging
import sys

from src.config.schema import EngineConfig


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return