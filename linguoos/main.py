from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.responses import FileResponse

from linguoos.api.admin import router as admin_router
from linguoos.api.deps import get_repo
from linguoos.api.v1 import router as v1_router
from linguoos.api.v1.auth import router as auth_router
from linguoos.api.v1.tutor import router as tutor_router
from linguoos.api.v1.voice import router as voice_router
from linguoos.config import settings
from linguoos.middleware import (
    ApiKeyMiddleware,
    EventMiddleware,
    JsonRequestLogMiddleware,
    VisitorMiddleware,
    install_error_handlers,
)
from linguoos.system.metrics import MetricsMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title="LinguoOS", version=settings.version)

    app.add_middleware(JsonRequestLogMiddleware)
    app.add_middleware(EventMiddleware)
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(ApiKeyMiddleware)
    app.add_middleware(VisitorMiddleware)

    app.include_router(v1_router)
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(admin_router)
    app.include_router(voice_router)
    app.include_router(tutor_router)

    install_error_handlers(app)

    h5_root = os.path.join(os.path.dirname(__file__), "h5")
    h5_index = os.path.join(h5_root, "index.html")

    @app.get("/app")
    async def h5_app() -> FileResponse:
        return FileResponse(h5_index)

    @app.get("/app/{path:path}")
    async def h5_static(path: str) -> FileResponse:
        file_path = os.path.join(h5_root, path)
        if os.path.exists(file_path):
            return FileResponse(file_path)
        return FileResponse(h5_index)

    @app.on_event("startup")
    async def startup() -> None:
        db_path = settings.db_path
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        repo = get_repo()
        await repo.init()

    return app


app = create_app()
