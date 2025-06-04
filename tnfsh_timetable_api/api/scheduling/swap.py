from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional


class CourseInfo(BaseModel):
    teacher_name: List[str]
    subject: str
    class_: List[str]  # 使用 class_ 避免與 Python 關鍵字衝突
    weekday: int
    period: int
    streak: Optional[int] = None


class SwapStep(BaseModel):
    from_: CourseInfo
    to: CourseInfo


class SwapSinglePath(BaseModel):
    steps: List[SwapStep]


class SwapPaths(BaseModel):
    target: str
    paths: List[SwapSinglePath]


router = APIRouter()

@router.get("/swap", response_model=SwapPaths)
async def get_swap_paths(
    target: str = Query(..., description="教師名稱"),
    weekday: int = Query(..., ge=1, le=5, description="星期幾（1-5，1為星期一）"),
    period: int = Query(..., ge=1, le=8, description="節次（1-8）"),
    max_depth: int = Query(default=20, ge=1, le=50, description="最大搜尋深度")
):
    """搜尋指定教師特定時段的課程互換路徑"""
    try:
        from tnfsh_timetable_core import TNFSHTimetableCore
        
        core = TNFSHTimetableCore()
        scheduling = await core.fetch_scheduling()
        cycles = await scheduling.swap(target, weekday=weekday, period=period, max_depth=max_depth)
        cycles_list = list(cycles)

        paths = []
        for cycle in cycles_list:
            steps = []
            # 跳過第一個和最後一個節點
            nodes = cycle[1:-1]
            
            # 每兩個節點一組進行輸出
            for j in range(0, len(nodes), 2):
                if j + 1 < len(nodes):
                    node1, node2 = nodes[j], nodes[j+1]
                    
                    from_info = CourseInfo(
                        teacher_name=[t.teacher_name for t in node1.teachers.values()],
                        subject=node1.subject,
                        class_=[c.class_code for c in node1.classes.values()],
                        weekday=node1.time.weekday,
                        period=node1.time.period,
                        streak=node1.time.streak if node1.time.streak and node1.time.streak != 1 else None
                    )
                    
                    to_info = CourseInfo(
                        teacher_name=[t.teacher_name for t in node2.teachers.values()],
                        subject=node2.subject,
                        class_=[c.class_code for c in node2.classes.values()],
                        weekday=node2.time.weekday,
                        period=node2.time.period,
                        streak=node2.time.streak if node2.time.streak and node2.time.streak != 1 else None
                    )
                    
                    steps.append(SwapStep(from_=from_info, to=to_info))
            
            paths.append(SwapSinglePath(steps=steps))

        return SwapPaths(target=target, paths=paths)

    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"搜尋互換路徑時發生錯誤: {str(e)}"
        )