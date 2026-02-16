from __future__ import annotations

import threading
import time
import uuid
from collections import deque
from dataclasses import asdict, dataclass
from typing import Any

from pathlib import Path

from linguoos import config


@dataclass(frozen=True)
class Event:
    event_id: str
    event: str
    timestamp: float
    data: dict[str, Any]


class EventStore:
    def __init__(self, max_events: int = 200, jsonl_path: str | None = None) -> None:
        self._lock = threading.Lock()
        self._events: deque[Event] = deque(maxlen=max_events)
        self._jsonl_path = jsonl_path

    def record(self, event: str, data: dict[str, Any] | None = None) -> Event:
        payload = data or {}
        entry = Event(
            event_id=uuid.uuid4().hex,
            event=event,
            timestamp=time.time(),
            data=payload,
        )
        with self._lock:
            self._events.append(entry)
            if self._jsonl_path:
                try:
                    path = Path(self._jsonl_path)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    # Append JSON line; keep it lightweight.
                    import json

                    with path.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
                except Exception:
                    # Best-effort only; never break API on event persistence errors.
                    pass
        return entry

    def list(self, limit: int | None = None) -> list[dict[str, Any]]:
        with self._lock:
            events = list(self._events)
        if limit is not None:
            events = events[-limit:]
        return [asdict(item) for item in events]

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            total = len(self._events)
            max_events = self._events.maxlen or 0
        return {"total": total, "max_events": max_events}


EVENTS = EventStore(max_events=config.EVENT_BUFFER_SIZE, jsonl_path=config.EVENTS_JSONL_PATH)
