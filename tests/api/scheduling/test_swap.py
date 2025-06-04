import pytest
from httpx import AsyncClient, ASGITransport
from tnfsh_timetable_api.main import app

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_get_swap_paths_basic():
    """測試基本的課程互換功能"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/swap?target=顏永進&weekday=3&period=2")
        assert response.status_code == 200
        data = response.json()
        
        # 基本結構檢查
        assert "target" in data
        assert data["target"] == "顏永進"
        assert "paths" in data
        assert isinstance(data["paths"], list)
        
        # 每個路徑的結構檢查
        if data["paths"]:
            path = data["paths"][0]
            assert "steps" in path
            
            if path["steps"]:
                step = path["steps"][0]
                # 檢查 from_ 資料結構
                assert "from_" in step
                from_info = step["from_"]
                assert "teacher_name" in from_info
                assert isinstance(from_info["teacher_name"], list)
                assert "subject" in from_info
                assert "class_" in from_info
                assert isinstance(from_info["class_"], list)
                assert "weekday" in from_info
                assert isinstance(from_info["weekday"], int)
                assert "period" in from_info
                assert isinstance(from_info["period"], int)
                
                # 檢查 to 資料結構
                assert "to" in step
                to_info = step["to"]
                assert "teacher_name" in to_info
                assert isinstance(to_info["teacher_name"], list)
                assert "subject" in to_info
                assert "class_" in to_info
                assert isinstance(to_info["class_"], list)
                assert "weekday" in to_info
                assert isinstance(to_info["weekday"], int)
                assert "period" in to_info
                assert isinstance(to_info["period"], int)


@pytest.mark.asyncio
async def test_get_swap_paths_not_found():
    """測試找不到課程時的處理"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/swap?target=不存在的老師&weekday=1&period=1")
        assert response.status_code == 404
        error_data = response.json()
        assert "detail" in error_data
        assert "錯誤" in error_data["detail"]


@pytest.mark.asyncio
async def test_get_swap_paths_weekend():
    """測試週末的課程互換嘗試"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/swap?target=顏永進&weekday=6&period=1")
        assert response.status_code == 422  # FastAPI 參數驗證錯誤


@pytest.mark.asyncio
async def test_get_swap_paths_invalid_period():
    """測試無效節次的處理"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/swap?target=顏永進&weekday=1&period=9")
        assert response.status_code == 422  # FastAPI 參數驗證錯誤


@pytest.mark.asyncio
async def test_get_swap_paths_with_depth():
    """測試指定搜尋深度"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/scheduling/swap?target=顏永進&weekday=3&period=2&max_depth=5")
        assert response.status_code == 200
        data = response.json()
        assert data["target"] == "顏永進"
        assert isinstance(data["paths"], list)