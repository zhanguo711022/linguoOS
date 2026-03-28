from fastapi import APIRouter

from linguoos.api.v1.correction import router as correction_router
from linguoos.api.v1.decision import router as decision_router
from linguoos.api.v1.explain import router as explain_router
from linguoos.api.v1.history import router as history_router
from linguoos.api.v1.practice import router as practice_router
from linguoos.api.v1.precision import router as precision_router
from linguoos.api.v1.profile import router as profile_router
from linguoos.api.v1.session import router as session_router
from linguoos.api.v1.system import router as system_router
from linguoos.api.v1.workspace import router as workspace_router

router = APIRouter(prefix="/api/v1")

router.include_router(session_router)
router.include_router(practice_router)
router.include_router(explain_router)
router.include_router(decision_router)
router.include_router(profile_router)
router.include_router(history_router)
router.include_router(workspace_router)
router.include_router(correction_router)
router.include_router(precision_router)
router.include_router(system_router)
