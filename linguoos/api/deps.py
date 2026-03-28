from __future__ import annotations

from fastapi import Depends

from linguoos.agents.assessor import AssessorAgent
from linguoos.agents.explainer import ExplainerAgent
from linguoos.agents.tutor import TutorAgent
from linguoos.config import settings
from linguoos.core.orchestrator import OrchestratorV2
from linguoos.providers.factory import get_provider
from linguoos.services.explain_service import ExplainService
from linguoos.services.intervention_service import InterventionService
from linguoos.services.practice_service import PracticeService
from linguoos.services.session_service import SessionService
from linguoos.storage.sqlite import SQLiteRepository


_repo_instance: SQLiteRepository | None = None
_repo_db_path: str | None = None
_provider_instance = None


def get_repo() -> SQLiteRepository:
    global _repo_instance, _repo_db_path
    if _repo_instance is None or _repo_db_path != settings.db_path:
        _repo_instance = SQLiteRepository()
        _repo_db_path = settings.db_path
    return _repo_instance


def get_provider_instance():
    global _provider_instance
    if _provider_instance is None:
        _provider_instance = get_provider()
    return _provider_instance


def get_orchestrator() -> OrchestratorV2:
    return OrchestratorV2()


def get_tutor_agent(provider=Depends(get_provider_instance)) -> TutorAgent:
    return TutorAgent(provider=provider)


def get_assessor_agent(provider=Depends(get_provider_instance)) -> AssessorAgent:
    return AssessorAgent(provider=provider)


def get_explainer_agent(provider=Depends(get_provider_instance)) -> ExplainerAgent:
    return ExplainerAgent(provider=provider)


def get_session_service(
    repo=Depends(get_repo),
    tutor=Depends(get_tutor_agent),
    orchestrator=Depends(get_orchestrator),
) -> SessionService:
    return SessionService(repo=repo, tutor=tutor, orchestrator=orchestrator)


def get_practice_service(
    repo=Depends(get_repo),
    provider=Depends(get_provider_instance),
    assessor=Depends(get_assessor_agent),
) -> PracticeService:
    return PracticeService(repo=repo, provider=provider, assessor=assessor)


def get_explain_service(
    repo=Depends(get_repo),
    explainer=Depends(get_explainer_agent),
) -> ExplainService:
    return ExplainService(repo=repo, explainer=explainer)


def get_intervention_service(
    repo=Depends(get_repo),
) -> InterventionService:
    return InterventionService(repo=repo)
