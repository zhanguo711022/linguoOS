import threading

from starlette.middleware.base import BaseHTTPMiddleware


class InMemoryMetrics:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.requests_total = 0
        self.errors_total = 0
        self.per_path: dict[str, int] = {}

    def inc_request(self, path: str) -> None:
        with self._lock:
            self.requests_total += 1
            self.per_path[path] = self.per_path.get(path, 0) + 1

    def inc_error(self) -> None:
        with self._lock:
            self.errors_total += 1

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "requests_total": self.requests_total,
                "errors_total": self.errors_total,
                "per_path": dict(self.per_path),
            }


METRICS = InMemoryMetrics()


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        METRICS.inc_request(request.url.path)
        try:
            return await call_next(request)
        except Exception:
            METRICS.inc_error()
            raise
