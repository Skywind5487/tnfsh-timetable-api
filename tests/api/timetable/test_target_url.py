import pytest
from httpx import AsyncClient, ASGITransport
from tnfsh_timetable_api.main import app

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_get_class_timetable_url():
    """測試獲取班級課表網址"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/307/url")
        assert response.status_code == 200
        data = response.json()
        
        assert data["target"] == "307"
        assert "url" in data
        assert isinstance(data["url"], str)


@pytest.mark.asyncio
async def test_get_teacher_timetable_url():
    """測試獲取教師課表網址"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/顏永進/url")
        assert response.status_code == 200
        data = response.json()
        assert data["target"] == "顏永進"
        assert "url" in data
        assert isinstance(data["url"], str)


@pytest.mark.asyncio
async def test_get_timetable_url_not_found():
    """測試獲取不存在目標的課表網址"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/不存在的目標/url")
        assert response.status_code == 404
        assert "找不到" in response.json()["detail"]
