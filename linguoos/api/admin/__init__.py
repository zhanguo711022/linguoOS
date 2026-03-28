from fastapi import APIRouter

from linguoos.api.admin.courses import router as courses_router
from linguoos.api.admin.interventions import router as interventions_router
from linguoos.api.admin.students import router as students_router

router = APIRouter(prefix="/api/admin")

router.include_router(students_router)
router.include_router(courses_router)
router.include_router(interventions_router)
