from __future__ import annotations

import random

from fastapi import APIRouter, HTTPException, Query

from linguoos.content.curriculum.explanations import EXPLANATIONS
from linguoos.content.curriculum.levels import LEVELS
from linguoos.content.curriculum.modules import MODULES
from linguoos.content.curriculum.questions import QUESTIONS
from linguoos.schemas.curriculum import ExplainContent, LevelInfo, ModuleInfo, ProgressUpdate, Question, UserProgress
from linguoos.storage import sqlite

router = APIRouter(prefix="/curriculum", tags=["curriculum"])


def get_modules_by_lang(lang: str) -> list:
    if lang == "fr":
        from linguoos.content.curriculum.modules_fr import MODULES_FR
        return MODULES_FR
    elif lang == "ja":
        from linguoos.content.curriculum.modules_ja import MODULES_JA
        return MODULES_JA
    elif lang == "ko":
        from linguoos.content.curriculum.modules_ko import MODULES_KO
        return MODULES_KO
    elif lang == "es":
        from linguoos.content.curriculum.modules_es import MODULES_ES
        return MODULES_ES
    elif lang == "ru":
        from linguoos.content.curriculum.modules_ru import MODULES_RU
        return MODULES_RU
    return MODULES


def get_questions_by_lang(lang: str) -> dict:
    if lang == "fr":
        from linguoos.content.curriculum.questions_fr import QUESTIONS as Q
        return Q
    elif lang == "ja":
        from linguoos.content.curriculum.questions_ja import QUESTIONS as Q
        return Q
    elif lang == "ko":
        try:
            from linguoos.content.curriculum.questions_ko import QUESTIONS as Q
            return Q
        except ImportError:
            return {}
    elif lang == "es":
        try:
            from linguoos.content.curriculum.questions_es import QUESTIONS as Q
            return Q
        except ImportError:
            return {}
    elif lang == "ru":
        try:
            from linguoos.content.curriculum.questions_ru import QUESTIONS as Q
            return Q
        except ImportError:
            return {}
    return QUESTIONS


@router.get("/levels", response_model=list[LevelInfo])
async def list_levels():
    return [LevelInfo(**level) for level in LEVELS]


@router.get("/modules/{level_id}", response_model=list[ModuleInfo])
async def list_modules(level_id: str, lang: str = Query(default="en")):
    modules_data = get_modules_by_lang(lang)
    if lang == "en" and not any(level["id"] == level_id for level in LEVELS):
        raise HTTPException(status_code=404, detail="level not found")
    modules = [module for module in modules_data if module["level_id"] == level_id]
    modules.sort(key=lambda item: item["order"])
    return [ModuleInfo(**module) for module in modules]


@router.get("/questions/{module_id}", response_model=list[Question])
async def module_questions(module_id: str, lang: str = Query(default="en")):
    questions_data = get_questions_by_lang(lang)
    items = questions_data.get(module_id)
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


# ── Scene routes ──────────────────────────────────────────────
from linguoos.content.curriculum.scenes import SCENES
from linguoos.content.curriculum.scene_questions import SCENE_QUESTIONS


@router.get("/scenes")
def list_scenes():
    return SCENES


@router.get("/scenes/{scene_id}/questions")
def get_scene_questions(scene_id: str):
    key = f"scene.{scene_id}" if not scene_id.startswith("scene.") else scene_id
    qs = SCENE_QUESTIONS.get(key, [])
    import random
    return random.sample(qs, min(5, len(qs)))


@router.get("/scenes/{scene_id}/dialog")
def get_scene_dialog(scene_id: str):
    key = f"scene.{scene_id}" if not scene_id.startswith("scene.") else scene_id
    scene = next((s for s in SCENES if s["id"] == key), None)
    if not scene:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Scene not found")
    return scene
