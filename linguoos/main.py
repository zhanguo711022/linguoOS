from __future__ import annotations

import os

from fastapi import FastAPI

from linguoos.api.admin import router as admin_router
from linguoos.api.deps import get_repo
from linguoos.api.v1 import router as v1_router
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
    app.include_router(admin_router)

    install_error_handlers(app)

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
