import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any


class Timetable(BaseModel):
    target: str
    info: Dict[str, Any]

router = APIRouter()

@router.get("/{target}/full", response_model=Timetable)
async def get_timetable(target: str):
    """獲取指定班級或教師的完整課表

    Args:
        target: 目標代碼（班級代碼如 "307" 或教師名稱如 "顏永進"）
    """
    try:
        from tnfsh_timetable_core import TNFSHTimetableCore

        core = TNFSHTimetableCore()
        timetable = await core.fetch_timetable(target)
        return Timetable(
            target=target,
            info=timetable.model_dump()
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"找不到 '{target}' 的課表資訊， error: {str(e)}"
        )
