import pytest
from httpx import AsyncClient, ASGITransport
from tnfsh_timetable_api.main import app

pytestmark = pytest.mark.asyncio

async def test_get_periods_teacher():
    """測試獲取教師的節次資訊"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/other/periods/顏永進")
        assert response.status_code == 200
        data = response.json()
        import json
        print(json.dumps(data, indent=2, ensure_ascii=False))
        assert "periods" in data
        assert isinstance(data["periods"], dict)
        # 確保至少有一節課
        assert len(data["periods"]) > 0
        # 檢查時間格式是否正確
        for period, time_range in data["periods"].items():
            assert isinstance(time_range, list)
            assert len(time_range) == 2
            assert isinstance(time_range[0], str)
            assert isinstance(time_range[1], str)

async def test_get_periods_class():

    """測試獲取班級的節次資訊"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/other/periods/307")
        assert response.status_code == 200
        data = response.json()
        assert "periods" in data
        assert isinstance(data["periods"], dict)
        # 確保至少有一節課
        assert len(data["periods"]) > 0
