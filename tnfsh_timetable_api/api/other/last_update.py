from fastapi import APIRouter

router = APIRouter()

@router.get("/last-update")
async def get_last_update():
    return {"last_update": "2023-10-01T12:00:00Z"}  # Replace with actual logic to fetch last update