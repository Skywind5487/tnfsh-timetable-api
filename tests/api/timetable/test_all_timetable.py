import pytest
from httpx import AsyncClient, ASGITransport
from tnfsh_timetable_api.main import app

pytestmark = pytest.mark.asyncio


def check_timetable_structure(data: dict):
    """檢查課表資料結構"""
    assert "target" in data
    assert isinstance(data["target"], str)
    assert "info" in data
    assert isinstance(data["info"], dict)


@pytest.mark.asyncio
async def test_get_all_teacher_timetable():
    """測試獲取所有教師課表"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/teacher/all")
        assert response.status_code == 200
        data = response.json()
        
        # 確認回傳是列表
        assert isinstance(data, list)
        assert len(data) > 0
        
        # 檢查第一筆資料結構
        first_item = data[0]
        check_timetable_structure(first_item)
        
        # 確認是教師資料
        assert any("顏永進" in item["target"] for item in data), "應該包含顏永進老師的課表"


@pytest.mark.asyncio
async def test_get_all_class_timetable():
    """測試獲取所有班級課表"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/class/all")
        assert response.status_code == 200
        data = response.json()
        
        # 確認回傳是列表
        assert isinstance(data, list)
        assert len(data) > 0
        
        # 檢查第一筆資料結構
        first_item = data[0]
        check_timetable_structure(first_item)
        
        # 確認是班級資料
        assert any("307" in item["target"] for item in data), "應該包含307班的課表"


@pytest.mark.asyncio
async def test_get_all_timetable():
    """測試獲取所有課表（包含教師和班級）"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/timetable/all")
        assert response.status_code == 200
        data = response.json()
        
        # 確認回傳是列表
        assert isinstance(data, list)
        assert len(data) > 0
        
        # 檢查資料結構
        for item in data:
            check_timetable_structure(item)
        
        # 確認同時包含教師和班級資料
        has_teacher = any("顏永進" in item["target"] for item in data)
        has_class = any("307" in item["target"] for item in data)
        assert has_teacher and has_class, "應該同時包含教師和班級的課表"


@pytest.mark.asyncio
async def test_timetable_response_time():
    """測試課表回應時間（應在合理範圍內）"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        import time
        start_time = time.time()
        
        response = await client.get("/api/timetable/all")
        assert response.status_code == 200
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # 回應時間不應超過 30 秒
        assert response_time < 30, f"回應時間過長：{response_time}秒"


@pytest.mark.asyncio
async def test_error_handling():
    """測試錯誤處理"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 測試不存在的路徑
        response = await client.get("/api/timetable/invalid/all")
        assert response.status_code == 404
        
        # 驗證錯誤訊息格式
        error_data = response.json()
        assert "detail" in error_data
        assert isinstance(error_data["detail"], str)
