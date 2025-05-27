from fastapi import APIRouter
from tnfsh_timetable_core import TNFSHTimetableCore
from datetime import datetime
from pydantic import BaseModel
from fastapi import HTTPException


class LastUpdate(BaseModel):
    source_url: str
    last_update: datetime

router = APIRouter()

@router.get("/last-update/{target}", response_model=LastUpdate)
async def get_last_update(target: str = "顏永進"):
    """獲取課表最後更新時間"""
    from tnfsh_timetable_core.timetable.crawler import fetch_raw_html, parse_html
    try:
        # 解析 HTML 獲取最後更新時間
        html = await fetch_raw_html(target)
        last_update = parse_html(html)["last_update"]
        timestamp = datetime.strptime(last_update, "%Y/%m/%d %H:%M:%S")
        from tnfsh_timetable_core import TNFSHTimetableCore
        core = TNFSHTimetableCore()
        timetable = await core.fetch_timetable(target)
        source_url = timetable.target_url

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"教師 '{target}' 不存在"
        )
    return LastUpdate(source_url=source_url, last_update=timestamp)