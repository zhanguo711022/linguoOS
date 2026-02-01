from fastapi import FastAPI

from linguoos.api.v1.growth import router as growth_router
from linguoos.api.v1.state import router as state_router
from linguoos.api.v1.task import router as task_router

app = FastAPI(title="LinguoOS External Interface Layer", version="0.1.0")

app.include_router(task_router)
app.include_router(state_router)
app.include_router(growth_router)
