from email.policy import HTTP
from math import e
from fastapi import APIRouter
from tnfsh_timetable_core.timetable.crawler import fetch_raw_html, parse_html
from pydantic import BaseModel
from typing import Dict, List, Tuple

class PeriodInfo(BaseModel):
    periods: Dict[str, Tuple[str, str]]

router = APIRouter()

@router.get("/periods/{target}", response_model=PeriodInfo)
async def get_periods(target: str = "顏永進"):
    '''獲取課程節次資訊
    
    Args:
        target: 目標名稱（教師姓名或班級代碼），預設為"顏永進"
    '''
    try:
        html = await fetch_raw_html(target)
        periods = parse_html(html)["periods"]
        return PeriodInfo(periods=periods)
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail=f"無法獲取 '{target}' 的課程節次資訊， error: {str(e)}"
        )