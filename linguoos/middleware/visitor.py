import uuid

from starlette.middleware.base import BaseHTTPMiddleware


class VisitorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        visitor_id = request.headers.get("X-Visitor-Id") or uuid.uuid4().hex
        request.state.visitor_id = visitor_id
        response = await call_next(request)
        response.headers["X-Visitor-Id"] = visitor_id
        return response
