from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional


class Time(BaseModel):
    weekday: int
    period: int


class CourseInfo(BaseModel):
    teacher_name: List[str]
    class_: List[str]  # 使用 class_ 避免與 Python 關鍵字衝突
    subject: str
    time: Time
    to_time: Time
    streak: Optional[int] = None


class RotationSinglePath(BaseModel):
    steps: List[CourseInfo]


class RotationPaths(BaseModel):
    target: str
    paths: List[RotationSinglePath]


router = APIRouter()

@router.get("/rotation", response_model=RotationPaths)
async def get_rotation_paths(
    teacher: str = Query(..., description="教師名稱"),
    weekday: int = Query(..., ge=1, le=5, description="星期幾（1-5，1為星期一）"),
    period: int = Query(..., ge=1, le=8, description="節次（1-8）"),
    max_depth: int = Query(default=2, ge=1, le=50, description="最大搜尋深度")
):
    """搜尋指定教師特定時段的課程輪調路徑"""
    try:
        from tnfsh_timetable_core import TNFSHTimetableCore
        
        core = TNFSHTimetableCore()
        scheduling = await core.fetch_scheduling()
        cycles = await scheduling.rotation(teacher, weekday=weekday, period=period, max_depth=max_depth)
        cycles_list = list(cycles)

        paths = []
        for cycle in cycles_list:
            steps = []
            # 對於每個節點（除了最後一個），取得當前節點和下一個節點的資訊
            for i in range(len(cycle)-1):
                current_node = cycle[i]
                next_node = cycle[i+1]
                
                step = CourseInfo(
                    teacher_name=[t.teacher_name for t in current_node.teachers.values()],
                    class_=[c.class_code for c in current_node.classes.values()],
                    subject=current_node.subject,
                    time=Time(
                        weekday=current_node.time.weekday,
                        period=current_node.time.period
                    ),
                    to_time=Time(
                        weekday=next_node.time.weekday,
                        period=next_node.time.period
                    ),
                    streak=current_node.time.streak if current_node.time.streak and current_node.time.streak != 1 else None
                )
                steps.append(step)
            
            if steps:  # 只有當有步驟時才加入路徑
                paths.append(RotationSinglePath(steps=steps))

        return RotationPaths(target=teacher, paths=paths)

    except Exception as e:
        raise (f"搜尋輪調路徑時發生錯誤: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail=f"搜尋輪調路徑時發生錯誤: {str(e)}"
        )