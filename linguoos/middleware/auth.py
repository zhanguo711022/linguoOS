from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from linguoos.config import settings


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if settings.require_api_key:
            api_key = request.headers.get("X-API-Key")
            if api_key != settings.api_key:
                return JSONResponse(
                    {
                        "ok": False,
                        "error": {"type": "auth", "message": "invalid api key"},
                    },
                    status_code=401,
                )
        return await call_next(request)
