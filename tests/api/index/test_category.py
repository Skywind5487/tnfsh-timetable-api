import pytest
from httpx import AsyncClient, ASGITransport
from tnfsh_timetable_api.main import app

# 建立共享的非同步測試 client
@pytest.fixture
def async_client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")

# 測試取得所有分類
@pytest.mark.anyio
async def test_get_categories(async_client):
    async with async_client as client:
        response = await client.get("/api/index/categories")
        assert response.status_code == 200
        data = response.json()
        import json
        print(json.dumps(data, indent=4, ensure_ascii=False))
        assert "categories" in data
        assert isinstance(data["categories"], list)

# 測試取得特定分類
@pytest.mark.anyio
async def test_get_category(async_client):
    async with async_client as client:
        response = await client.get("/api/index/categories/藝能科")
        assert response.status_code == 200
        data = response.json()
        import json
        print(json.dumps(data, indent=4, ensure_ascii=False))
        assert data["category_name"] == "藝能科"
        assert "info" in data

# 測試找不到分類時回傳 404
@pytest.mark.anyio
async def test_get_category_not_found(async_client):
    async with async_client as client:
        response = await client.get("/api/index/categories/不存在的分類")
        assert response.status_code == 404
        assert "不存在" in response.json()["detail"]
