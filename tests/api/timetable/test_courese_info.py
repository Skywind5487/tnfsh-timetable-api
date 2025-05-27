import pytest
from httpx import AsyncClient, ASGITransport
from tnfsh_timetable_api.main import app

pytestmark = pytest.mark.asyncio

# import logger
from tnfsh_timetable_core import TNFSHTimetableCore
core = TNFSHTimetableCore()
logger = core.get_logger()


@pytest.mark.asyncio
async def test_get_course_class():
    """測試獲取班級特定課程"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/307/at?weekday=1&period=1")
        assert response.status_code == 200
        data = response.json()
        logger.debug(f"獲取班級課程成功: {data}")
        assert data["target"] == "307"
        assert data["weekday"] == 1
        assert data["period"] == 1
        assert "info" in data

@pytest.mark.asyncio
async def test_get_course_teacher():
    """測試獲取教師特定課程"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/顏永進/at?weekday=3&period=2")
        assert response.status_code == 200
        data = response.json()
        assert data["target"] == "顏永進"
        assert data["weekday"] == 3
        assert data["period"] == 2
        assert "info" in data

@pytest.mark.asyncio
async def test_get_course_invalid_weekday():
    """測試無效的星期數"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/307/at?weekday=8&period=1")
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_course_weekend():
    """測試星期六日的課程查詢"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/307/at?weekday=6&period=1")
        assert response.status_code == 400
        assert "目前只支援星期一到星期五的課程查詢" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_course_invalid_period():
    """測試無效的節次"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/307/at?weekday=1&period=9")
        assert response.status_code == 422

