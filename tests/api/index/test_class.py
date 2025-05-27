import pytest
from httpx import AsyncClient, ASGITransport
from tnfsh_timetable_api.main import app

pytestmark = pytest.mark.asyncio

async def test_get_classes():
    """測試獲取所有班級列表"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/index/classes")
        assert response.status_code == 200
        data = response.json()
        assert "classes" in data
        assert isinstance(data["classes"], list)
        assert "307" in data["classes"]

async def test_get_class():
    """測試獲取特定班級資訊"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/index/classes/307")
        assert response.status_code == 200
        data = response.json()
        assert data["class_code"] == "307"
        assert "info" in data

async def test_get_class_not_found():
    """測試獲取不存在的班級"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/index/classes/999")
        assert response.status_code == 404
        assert "不存在" in response.json()["detail"]
