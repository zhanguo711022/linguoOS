from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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

app = FastAPI(title="LinguoOS External Interface Layer", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/webui", StaticFiles(directory="linguoos/webui"), name="webui")


@app.get("/ui")
def ui_index():
    return FileResponse("linguoos/webui/index.html")

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
