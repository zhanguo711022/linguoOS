from fastapi import APIRouter

router = APIRouter(prefix="/workspace", tags=["workspace"])


@router.get("/context")
async def workspace_context():
    return {"ok": True, "data": {"active": True, "context": "workspace placeholder"}}
