from fastapi import APIRouter

router = APIRouter(prefix="/admin/courses", tags=["admin-courses"])


@router.get("")
async def list_courses():
    return {"ok": True, "data": []}


@router.post("")
async def create_course(payload: dict):
    return {"ok": True, "data": {"created": True, "course": payload}}
