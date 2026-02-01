from datetime import datetime, timezone

from fastapi import APIRouter, Body, Query

from linguoos.schemas.profile import (
    AbilityDimension,
    AbilityName,
    LanguageProfile,
    LanguageProfileUpdate,
)

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])


@router.get("/current", response_model=LanguageProfile)
def get_current_profile(user_id: str = Query(...)) -> LanguageProfile:
    now = datetime.now(timezone.utc)
    return LanguageProfile(
        user_id=user_id,
        language="en",
        current_stage=2,
        ability_dimensions={
            AbilityName.precision: AbilityDimension(
                level=70,
                trend="steady",
                last_updated=now,
            ),
            AbilityName.structure: AbilityDimension(
                level=65,
                trend="up",
                last_updated=now,
            ),
            AbilityName.logic: AbilityDimension(
                level=60,
                trend="steady",
                last_updated=now,
            ),
            AbilityName.usage: AbilityDimension(
                level=72,
                trend="up",
                last_updated=now,
            ),
            AbilityName.sound: AbilityDimension(
                level=55,
                trend=None,
                last_updated=now,
            ),
        },
    )


@router.post("/update")
def update_profile(
    profile: LanguageProfile | LanguageProfileUpdate = Body(...),
) -> dict[str, bool]:
    return {"ok": True}
