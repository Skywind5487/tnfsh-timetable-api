import pytest
from httpx import AsyncClient, ASGITransport
from tnfsh_timetable_api.main import app

pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_get_full_timetable_class():
    """測試獲取班級完整課表"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/307/full")
        assert response.status_code == 200
        data = response.json()
        
        assert data["target"] == "307"
        assert "info" in data

@pytest.mark.asyncio
async def test_get_full_timetable_teacher():
    """測試獲取教師完整課表"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/顏永進/full")
        assert response.status_code == 200
        data = response.json()
        assert data["target"] == "顏永進"
        assert "info" in data

@pytest.mark.asyncio
async def test_get_full_timetable_not_found():
    """測試獲取不存在目標的完整課表"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/不存在的目標/full")
        assert response.status_code == 404
        