import time

from starlette.middleware.base import BaseHTTPMiddleware

from linguoos.system.events import EVENTS


class EventMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.monotonic()
        try:
            response = await call_next(request)
        except Exception as exc:
            dur_ms = int((time.monotonic() - start) * 1000)
            EVENTS.record(
                "http_error",
                {
                    "method": request.method,
                    "path": request.url.path,
                    "dur_ms": dur_ms,
                    "error": str(exc),
                },
            )
            raise
        dur_ms = int((time.monotonic() - start) * 1000)
        EVENTS.record(
            "http_request",
            {
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "dur_ms": dur_ms,
            },
        )
        return response
