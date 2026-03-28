import os
import pytest
from httpx import AsyncClient

os.environ["LINGUO_DB_PATH"] = "/tmp/linguoos_test.db"

from linguoos.api.deps import get_repo
from linguoos.config import settings
from linguoos.main import create_app


@pytest.mark.asyncio
async def test_session_endpoints(tmp_path):
    settings.db_path = str(tmp_path / "history.db")
    app = create_app()
    await get_repo().init()

    async with AsyncClient(app=app, base_url="http://test") as client:
        start = await client.post("/api/v1/session/start", json={"user_id": "u1", "language": "en"})
        assert start.status_code == 200
        payload = start.json()
        session_id = payload["session_id"]

        msg = await client.post("/api/v1/session/message", json={"session_id": session_id, "message": "hi"})
        assert msg.status_code == 200
        data = msg.json()
        assert "reply" in data
