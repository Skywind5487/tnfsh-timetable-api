import pytest
from httpx import AsyncClient, ASGITransport
from tnfsh_timetable_api.main import app

pytestmark = pytest.mark.asyncio

from tnfsh_timetable_core import TNFSHTimetableCore
core = TNFSHTimetableCore()
logger = core.get_logger()

@pytest.mark.asyncio
async def test_get_streak_start_node():
    """測試獲取連續課程起始節次"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 使用顏永進老師週二第3節的課程（應該是2節連堂）
        response = await client.get("/api/scheduling/streak?target=顏永進&weekday=2&period=3")
        assert response.status_code == 200
        data = response.json()
        logger.debug(f"Response data: {data}")

        assert data["target"] == "顏永進"
        assert "info" in data
        info = data["info"]
        
        # 基本資訊檢查
        assert "teacher" in info
        assert "class_" in info
        assert isinstance(info["class_"], list)
        assert info["weekday"] == 2
        assert info["period"] == 3
        # 這應該是連堂課
        assert info["streak"] is not None and info["streak"] > 1


@pytest.mark.asyncio
async def test_get_normal_course_node():
    """測試獲取一般課程（非連堂）的資訊"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/streak?target=顏永進&weekday=3&period=2")
        assert response.status_code == 200
        data = response.json()
        
        info = data["info"]
        # 這不應該是連堂課
        assert info["streak"] == 1


@pytest.mark.asyncio
async def test_get_streak_not_found():
    """測試獲取不存在的課程"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/streak?target=不存在的老師&weekday=1&period=1")
        assert response.status_code == 404
        assert "錯誤" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_streak_invalid_period():
    """測試無效的節次"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/streak?target=顏永進&weekday=1&period=1")
        assert response.status_code == 404  # 找不到該節次的課程
        assert "錯誤" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_streak_invalid_weekday():
    """測試無效的星期"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/streak?target=顏永進&weekday=6&period=1")
        assert response.status_code == 422  # 找不到該時段的課程
    


@pytest.mark.asyncio
async def test_preload_all():
    """測試預載入所有連堂課程"""
    from tnfsh_timetable_core.timetable.cache import preload_all
    await preload_all(max_concurrent=2, only_missing=False)