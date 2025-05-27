import pytest
from httpx import AsyncClient, ASGITransport
from tnfsh_timetable_api.main import app
from datetime import datetime

pytestmark = pytest.mark.asyncio

async def test_get_last_update():
    """測試獲取課表最後更新時間"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/other/last-update/307")
        assert response.status_code == 200
        data = response.json()
        import json
        print(json.dumps(data, indent=2, ensure_ascii=False))
        assert "last_update" in data
        # 驗證回傳的是有效的日期時間
        last_update = datetime.fromisoformat(data["last_update"].replace("Z", "+00:00"))
        assert isinstance(last_update, datetime)
