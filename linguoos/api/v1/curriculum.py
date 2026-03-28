from __future__ import annotations

import random

from fastapi import APIRouter, HTTPException

from linguoos.content.curriculum.explanations import EXPLANATIONS
from linguoos.content.curriculum.levels import LEVELS
from linguoos.content.curriculum.modules import MODULES
from linguoos.content.curriculum.questions import QUESTIONS
from linguoos.schemas.curriculum import ExplainContent, LevelInfo, ModuleInfo, ProgressUpdate, Question, UserProgress
from linguoos.storage import sqlite

router = APIRouter(prefix="/curriculum", tags=["curriculum"])


@router.get("/levels", response_model=list[LevelInfo])
async def list_levels():
    return [LevelInfo(**level) for level in LEVELS]


@router.get("/modules/{level_id}", response_model=list[ModuleInfo])
async def list_modules(level_id: str):
    if not any(level["id"] == level_id for level in LEVELS):
        raise HTTPException(status_code=404, detail="level not found")
    modules = [module for module in MODULES if module["level_id"] == level_id]
    modules.sort(key=lambda item: item["order"])
    return [ModuleInfo(**module) for module in modules]


@router.get("/questions/{module_id}", response_model=list[Question])
async def module_questions(module_id: str):
    items = QUESTIONS.get(module_id)
    if not items:
        raise HTTPException(status_code=404, detail="module not found")
    count = 3 if len(items) >= 3 else len(items)
    sample = random.sample(items, count)
    return [Question(**item) for item in sample]


@router.get("/explain/{module_id}", response_model=ExplainContent)
async def module_explain(module_id: str):
    content = EXPLANATIONS.get(module_id)
    if not content:
        raise HTTPException(status_code=404, detail="module not found")
    return ExplainContent(**content)


@router.post("/progress")
async def update_progress(payload: ProgressUpdate):
    sqlite.save_progress(
        user_id=payload.user_id,
        level_id=payload.level_id,
        module_id=payload.module_id,
        completed=payload.completed,
        score=payload.score,
    )
    return {"ok": True}


@router.get("/progress/{user_id}", response_model=UserProgress)
async def read_progress(user_id: str):
    progress = sqlite.get_progress(user_id)
    level_id = progress["level_id"]
    if not level_id:
        return UserProgress(user_id=user_id, level_id="", modules={})
    modules_for_level = [module for module in MODULES if module["level_id"] == level_id]
    modules = {module["id"]: progress["modules"].get(module["id"], 0.0) for module in modules_for_level}
    return UserProgress(user_id=user_id, level_id=level_id, modules=modules)
