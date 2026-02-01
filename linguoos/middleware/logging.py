import json
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware


class JsonRequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        rid = uuid.uuid4().hex
        start = time.monotonic()
        print(
            json.dumps(
                {
                    "event": "request_start",
                    "method": request.method,
                    "path": request.url.path,
                    "rid": rid,
                }
            ),
            flush=True,
        )
        try:
            response = await call_next(request)
        except Exception as exc:
            dur_ms = int((time.monotonic() - start) * 1000)
            print(
                json.dumps(
                    {
                        "event": "request_error",
                        "method": request.method,
                        "path": request.url.path,
                        "rid": rid,
                        "dur_ms": dur_ms,
                        "error": str(exc),
                    }
                ),
                flush=True,
            )
            raise
        dur_ms = int((time.monotonic() - start) * 1000)
        print(
            json.dumps(
                {
                    "event": "request_end",
                    "method": request.method,
                    "path": request.url.path,
                    "rid": rid,
                    "status": response.status_code,
                    "dur_ms": dur_ms,
                }
            ),
            flush=True,
        )
        return response
