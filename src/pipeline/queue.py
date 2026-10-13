"""Bounded FIFO queue with backpressure.

`put` blocks when full; `get` blocks when empty. Sentinel-aware so the
executor can drain cleanly on shutdown.
"""
from __future__ import annotations

import queue
import threading
from typing import Any


class BoundedJobQueue:
    def __init__(self, maxsize: int = 64) -> None:
        self._q: queue.Queue[Any] = queue.Queue(maxsize=maxsize)
        self._closed = threading.Event()

    def put(self, item: Any) -> None:
        if self._closed.is_set():
            raise RuntimeError("queue closed")
        self._q.put(item)

    def get(self, timeout: float | None = None) -> Any:
        return self._q.get(timeout=timeout)

    def task_done(self) -> None:
        self._q.task_done()

    def close(self) -> None:
        self._closed.set()

    @property
    def closed(self) -> bool:
        return self._closed.is_set()

    def qsize(self) -> int:
        return self._q.qsize()