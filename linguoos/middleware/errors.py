import json

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse


def _log_exception(event: str, request: Request, error: str, status: int | None = None) -> None:
    payload = {
        "event": event,
        "method": request.method,
        "path": request.url.path,
        "error": error,
    }
    if status is not None:
        payload["status"] = status
    print(json.dumps(payload), flush=True)


def install_error_handlers(app) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        _log_exception("exception", request, str(exc.detail), exc.status_code)
        return JSONResponse(
            {
                "ok": False,
                "error": {
                    "type": "http_error",
                    "status": exc.status_code,
                    "message": str(exc.detail),
                },
            },
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        _log_exception("exception", request, "validation_error", 422)
        return JSONResponse(
            {
                "ok": False,
                "error": {
                    "type": "validation",
                    "details": exc.errors(),
                },
            },
            status_code=422,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        _log_exception("exception", request, str(exc), 500)
        return JSONResponse(
            {
                "ok": False,
                "error": {
                    "type": "server_error",
                    "message": "internal error",
                },
            },
            status_code=500,
        )
