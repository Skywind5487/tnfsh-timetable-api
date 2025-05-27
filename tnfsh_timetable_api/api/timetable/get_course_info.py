import time
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any
from tnfsh_timetable_core import TNFSHTimetableCore


class CourseInfo(BaseModel):
    target: str
    weekday: int
    period: int
    info: Dict

router = APIRouter()

@router.get("/{target}/at", response_model=CourseInfo)
async def get_course(
    target: str,
    weekday: int = Query(default=1, ge=1, le=7, description="星期幾（1-7，1為星期一）"),
    period: int = Query(default=1, ge=1, le=8, description="節次（1-8）")
):
    """獲取指定班級或教師的特定時段課程資訊"""    
    try:
        if weekday > 5:
            raise HTTPException(
                status_code=400,
                detail="目前只支援星期一到星期五的課程查詢"
            )
        
        core = TNFSHTimetableCore()
        timetable = await core.fetch_timetable(target)
        course_info = timetable.table[weekday-1][period-1]
        if not course_info:
            raise HTTPException(
                status_code=404,
                detail=f"在 {target} 的第 {weekday} 星期和第 {period} 節沒有課程資訊"
            )
        return CourseInfo(
            target=target,
            weekday=weekday,
            period=period,
            info=course_info.model_dump()   
        )
        
    except HTTPException as e:
        raise e(f"查詢課程時發生錯誤: {e.detail}")
    
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"找不到 '{target}' 的課表資訊，error: {str(e)}"
        )