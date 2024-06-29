import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.app.main import app
from api.app.database import Base

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db/database_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_create_image(client: TestClient):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/images/", json={"filename": "test.jpg", "project_id": 1})
        assert response.status_code == 200
        response_json = response.json()
        assert "upload_link" in response_json
        assert response_json["image_id"] is not None

@pytest.mark.asyncio
async def test_websocket(client: TestClient):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        async with ac.websocket_connect("/ws/1") as ws:
            await ws.send_json({"message": "test"})
            data = await ws.receive_text()
            assert data == "Message text was: test"
