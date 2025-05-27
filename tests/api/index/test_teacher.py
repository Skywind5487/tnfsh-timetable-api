import pytest
from httpx import AsyncClient, ASGITransport
from tnfsh_timetable_api.main import app

pytestmark = pytest.mark.asyncio

async def test_get_teachers():
    """測試獲取所有教師列表"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/index/teachers")
        assert response.status_code == 200
        data = response.json()
        assert "teachers" in data
        assert isinstance(data["teachers"], list)
        assert "顏永進" in data["teachers"]

async def test_get_teacher():
    """測試獲取特定教師資訊"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/index/teachers/顏永進")
        assert response.status_code == 200
        data = response.json()
        assert data["teacher_name"] == "顏永進"
        assert "info" in data

async def test_get_teacher_not_found():
    """測試獲取不存在的教師"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/index/teachers/不存在的教師")
        assert response.status_code == 404
        assert "不存在" in response.json()["detail"]
