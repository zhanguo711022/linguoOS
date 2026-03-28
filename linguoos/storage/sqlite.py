from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from linguoos.config import settings
from linguoos.core.domain import LearningRecord, Session
from linguoos.storage.models import Base, InterventionModel, LearningRecordModel, SessionModel


class SQLiteRepository:
    def __init__(self) -> None:
        url = f"sqlite+aiosqlite:///{settings.db_path}"
        self._engine = create_async_engine(url, future=True)
        self._sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)

    async def init(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create_session(self, session: Session) -> None:
        async with self._sessionmaker() as db:
            db.add(
                SessionModel(
                    id=session.session_id,
                    user_id=session.user_id,
                    language=session.language,
                    status=session.status,
                    created_at=session.created_at,
                    updated_at=session.updated_at,
                )
            )
            await db.commit()

    async def get_session(self, session_id: str) -> Session | None:
        async with self._sessionmaker() as db:
            result = await db.execute(select(SessionModel).where(SessionModel.id == session_id))
            row = result.scalar_one_or_none()
            if not row:
                return None
            return Session(
                session_id=row.id,
                user_id=row.user_id,
                language=row.language,
                status=row.status,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )

    async def list_sessions_by_user(self, user_id: str) -> list[Session]:
        async with self._sessionmaker() as db:
            result = await db.execute(
                select(SessionModel)
                .where(SessionModel.user_id == user_id)
                .order_by(SessionModel.created_at.asc())
            )
            return [
                Session(
                    session_id=row.id,
                    user_id=row.user_id,
                    language=row.language,
                    status=row.status,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
                for row in result.scalars().all()
            ]

    async def list_sessions(self) -> list[Session]:
        async with self._sessionmaker() as db:
            result = await db.execute(select(SessionModel).order_by(SessionModel.created_at.asc()))
            return [
                Session(
                    session_id=row.id,
                    user_id=row.user_id,
                    language=row.language,
                    status=row.status,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
                for row in result.scalars().all()
            ]

    async def add_record(self, record: LearningRecord) -> None:
        async with self._sessionmaker() as db:
            db.add(
                LearningRecordModel(
                    session_id=record.session_id,
                    action_type=record.action_type,
                    payload=json.dumps(record.payload),
                    correct=record.correct,
                    created_at=record.created_at,
                )
            )
            await db.commit()

    async def list_records(self, session_id: str, limit: int = 20) -> list[LearningRecord]:
        async with self._sessionmaker() as db:
            result = await db.execute(
                select(LearningRecordModel)
                .where(LearningRecordModel.session_id == session_id)
                .order_by(LearningRecordModel.created_at.desc())
                .limit(limit)
            )
            records = []
            for row in result.scalars().all():
                payload = json.loads(row.payload) if row.payload else {}
                records.append(
                    LearningRecord(
                        session_id=row.session_id,
                        action_type=row.action_type,
                        payload=payload,
                        correct=row.correct,
                        created_at=row.created_at,
                    )
                )
            return list(reversed(records))

    async def update_session_status(self, session_id: str, status: str) -> None:
        async with self._sessionmaker() as db:
            result = await db.execute(select(SessionModel).where(SessionModel.id == session_id))
            row = result.scalar_one_or_none()
            if not row:
                return
            row.status = status
            row.updated_at = datetime.utcnow()
            await db.commit()

    async def create_intervention(self, session_id: str, reason: str, context: dict) -> int:
        async with self._sessionmaker() as db:
            model = InterventionModel(
                session_id=session_id,
                reason=reason,
                status="pending",
                teacher_response=json.dumps(context),
            )
            db.add(model)
            await db.flush()
            await db.commit()
            return int(model.id)

    async def list_interventions(self, status: str | None = None) -> list[dict]:
        async with self._sessionmaker() as db:
            stmt = select(InterventionModel)
            if status:
                stmt = stmt.where(InterventionModel.status == status)
            result = await db.execute(stmt)
            return [
                {
                    "id": row.id,
                    "session_id": row.session_id,
                    "reason": row.reason,
                    "status": row.status,
                    "teacher_response": row.teacher_response,
                    "created_at": row.created_at,
                }
                for row in result.scalars().all()
            ]

    async def resolve_intervention(self, intervention_id: int, teacher_response: str) -> None:
        async with self._sessionmaker() as db:
            result = await db.execute(select(InterventionModel).where(InterventionModel.id == intervention_id))
            row = result.scalar_one_or_none()
            if not row:
                return
            row.status = "resolved"
            row.teacher_response = teacher_response
            await db.commit()
