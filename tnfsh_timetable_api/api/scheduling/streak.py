from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from tnfsh_timetable_core import TNFSHTimetableCore
from tnfsh_timetable_core.scheduling.models import CourseNode


class StreakInfo(BaseModel):
    teacher: List[str]
    class_: List[str]  # 使用 class_ 避免與 Python 關鍵字衝突
    weekday: int
    period: int
    streak: Optional[int] = None


class CourseNodeInfo(BaseModel):
    target: str
    info: StreakInfo


router = APIRouter()

@router.get("/streak", response_model=CourseNodeInfo)
async def get_streak_start_node(
    target: str = Query(..., description="教師名稱"),
    weekday: int = Query(..., ge=1, le=5, description="星期幾（1-5，1為星期一）"),
    period: int = Query(..., ge=1, le=8, description="節次（1-8）")
):
    """獲取連續課程的起始節次"""
    try:
        core = TNFSHTimetableCore()
        scheduling = await core.fetch_scheduling()
        course_node: CourseNode = await scheduling.fetch_course_node(target, weekday=weekday, period=period)
        
        return CourseNodeInfo(
            target=target,
            info=StreakInfo(
                teacher=[t.teacher_name for t in course_node.teachers.values()],
                class_=[c.class_code for c in course_node.classes.values()],
                weekday=course_node.time.weekday,
                period=course_node.time.period,
                streak=course_node.time.streak if course_node.time.streak and course_node.time.streak != 1 else None
            )
        )

    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"獲取連續課程資訊時發生錯誤: {str(e)}"
        )
