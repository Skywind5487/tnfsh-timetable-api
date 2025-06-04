import pytest
from httpx import AsyncClient, ASGITransport
from tnfsh_timetable_api.main import app

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_get_rotation_paths_basic():
    """測試基本的課程輪調功能"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/rotation?teacher=顏永進&weekday=3&period=2&max_depth=3")
        assert response.status_code == 200
        data = response.json()
        import json
        print(json.dumps(data, ensure_ascii=False, indent=4))
        """
        # 基本結構檢查
        assert "target" in data
        assert data["target"] == "顏永進"
        assert "paths" in data
        assert isinstance(data["paths"], list)
        
        # 每個路徑的結構檢查
        if data["paths"]:
            path = data["paths"][0]
            assert "steps" in path
            assert isinstance(path["steps"], list)
            
            if path["steps"]:
                step = path["steps"][0]
                # 檢查步驟的資料結構
                assert "teacher" in step
                assert isinstance(step["teacher"], str)
                assert "class_" in step
                assert isinstance(step["class_"], str)
                assert "subject" in step
                assert isinstance(step["subject"], str)
                
                # 檢查時間資訊
                assert "time" in step
                time = step["time"]
                assert "weekday" in time
                assert isinstance(time["weekday"], int)
                assert 1 <= time["weekday"] <= 5
                assert "period" in time
                assert isinstance(time["period"], int)
                assert 1 <= time["period"] <= 8
                
                # 檢查目標時間資訊
                assert "to_time" in step
                to_time = step["to_time"]
                assert "weekday" in to_time
                assert isinstance(to_time["weekday"], int)
                assert 1 <= to_time["weekday"] <= 5
                assert "period" in to_time
                assert isinstance(to_time["period"], int)
                assert 1 <= to_time["period"] <= 8
            """

@pytest.mark.asyncio
async def test_get_rotation_paths_not_found():
    """測試找不到課程時的處理"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/rotation?teacher=不存在的老師&weekday=1&period=1")
        assert response.status_code == 404
        error_data = response.json()
        assert "detail" in error_data
        assert "錯誤" in error_data["detail"]


@pytest.mark.asyncio
async def test_get_rotation_paths_invalid_weekday():
    """測試無效的星期數"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/rotation?teacher=顏永進&weekday=6&period=1")
        assert response.status_code == 422  # FastAPI 參數驗證錯誤


@pytest.mark.asyncio
async def test_get_rotation_paths_invalid_period():
    """測試無效節次"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/rotation?teacher=顏永進&weekday=1&period=9")
        assert response.status_code == 422  # FastAPI 參數驗證錯誤


@pytest.mark.asyncio
async def test_get_rotation_paths_with_depth():
    """測試指定搜尋深度"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/rotation?teacher=顏永進&weekday=3&period=2&max_depth=5")
        assert response.status_code == 200
        data = response.json()
        assert data["target"] == "顏永進"
        assert isinstance(data["paths"], list)
