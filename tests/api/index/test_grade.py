import pytest
from httpx import AsyncClient, ASGITransport
from tnfsh_timetable_api.main import app

pytestmark = pytest.mark.asyncio

async def test_get_grades():
    """測試獲取所有年級列表"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/index/grades")
        assert response.status_code == 200
        data = response.json()
        assert "grades" in data
        assert isinstance(data["grades"], list)
        assert "高一" in data["grades"]

async def test_get_grade():
    """測試獲取特定年級資訊"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/index/grades/高一")
        assert response.status_code == 200
        data = response.json()
        assert data["grade"] == "高一"
        assert "info" in data

async def test_get_grade_not_found():
    """測試獲取不存在的年級"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/index/grades/不存在的年級")
        assert response.status_code == 404
        assert "不存在" in response.json()["detail"]
