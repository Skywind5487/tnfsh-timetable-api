from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class TeacherClassInfo(BaseModel):
    teacher: List[str]
    class_codes: List[str]
    weekday: int
    period: int
    streak: Optional[int] = None


class RotationStep(BaseModel):
    from_: TeacherClassInfo
    to: TeacherClassInfo


class RotationSinglePath(BaseModel):
    steps: List[RotationStep]


class RotationPaths(BaseModel):
    target: str
    paths: List[RotationSinglePath]


router = APIRouter()

@router.get("/rotation", response_model=RotationPaths)
async def get_rotation_paths(
    target: str = Query(..., description="教師名稱"),
    weekday: int = Query(..., ge=1, le=5, description="星期幾（1-5，1為星期一）"),
    period: int = Query(..., ge=1, le=8, description="節次（1-8）"),
    max_depth: int = Query(default=20, ge=1, le=50, description="最大搜尋深度")
):
    """搜尋指定教師特定時段的課程輪調路徑"""
    try:
        from tnfsh_timetable_core import TNFSHTimetableCore
        
        core = TNFSHTimetableCore()
        scheduling = await core.fetch_scheduling()
        cycles = await scheduling.rotation(target, weekday=weekday, period=period, max_depth=max_depth)
        cycles_list = list(cycles)

        paths = []
        for cycle in cycles_list:
            steps = []
            for j in range(len(cycle)-1):
                node1, node2 = cycle[j], cycle[j+1]
                
                from_info = TeacherClassInfo(
                    teacher=[t.teacher_name for t in node1.teachers.values()],
                    class_codes=[c.class_code for c in node1.classes.values()],
                    weekday=node1.time.weekday,
                    period=node1.time.period,
                    streak=node1.time.streak if node1.time.streak and node1.time.streak != 1 else None
                )
                
                to_info = TeacherClassInfo(
                    teacher=[t.teacher_name for t in node2.teachers.values()],
                    class_codes=[c.class_code for c in node2.classes.values()],
                    weekday=node2.time.weekday,
                    period=node2.time.period,
                    streak=node2.time.streak if node2.time.streak and node2.time.streak != 1 else None
                )
                
                steps.append(RotationStep(from_=from_info, to=to_info))
            
            paths.append(RotationSinglePath(steps=steps))

        return RotationPaths(target=target, paths=paths)

    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"搜尋輪調路徑時發生錯誤: {str(e)}"
        )