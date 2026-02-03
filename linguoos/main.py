from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from linguoos import config
from linguoos.api.v1.growth import router as growth_router
from linguoos.api.v1.decision import router as decision_router
from linguoos.api.v1.demo import router as demo_router
from linguoos.api.v1.explain import router as explain_router
from linguoos.api.v1.practice import router as practice_router
from linguoos.api.v1.correction import router as correction_router
from linguoos.api.v1.precision import router as precision_router
from linguoos.api.v1.profile import router as profile_router
from linguoos.api.v1.state import router as state_router
from linguoos.api.v1.system import router as system_router
from linguoos.api.v1.task import router as task_router
from linguoos.api.v1.workspace import router as workspace_router
from linguoos.middleware.errors import install_error_handlers
from linguoos.middleware.events import EventMiddleware
from linguoos.middleware.logging import JsonRequestLogMiddleware
from linguoos.system.metrics import MetricsMiddleware

app = FastAPI(title="LinguoOS External Interface Layer", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EXEMPT_PATH_PREFIXES = [
    "/docs",
    "/openapi.json",
    "/ui",
    "/webui",
    "/api/v1/system/",
]


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if not config.REQUIRE_API_KEY:
            return await call_next(request)
        path = request.url.path
        if any(path.startswith(prefix) for prefix in EXEMPT_PATH_PREFIXES):
            return await call_next(request)
        if path.startswith("/api/v1/"):
            key = request.headers.get("X-API-Key")
            if key != config.API_KEY:
                return JSONResponse({"detail": "Unauthorized"}, status_code=401)
        return await call_next(request)


app.add_middleware(ApiKeyMiddleware)
app.add_middleware(JsonRequestLogMiddleware)
app.add_middleware(EventMiddleware)
app.add_middleware(MetricsMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=500)
install_error_handlers(app)

UI_DIR = Path(__file__).parent / "webui"

app.mount("/webui", StaticFiles(directory=str(UI_DIR)), name="webui")


@app.get("/ui")
def ui_index():
    return FileResponse(str(UI_DIR / "index.html"))

app.include_router(task_router)
app.include_router(state_router)
app.include_router(growth_router)
app.include_router(demo_router)
app.include_router(explain_router)
app.include_router(profile_router)
app.include_router(workspace_router)
app.include_router(precision_router)
app.include_router(practice_router)
app.include_router(correction_router)
app.include_router(decision_router)
app.include_router(system_router)
