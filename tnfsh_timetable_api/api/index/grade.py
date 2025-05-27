from fastapi import APIRouter, HTTPException
from tnfsh_timetable_core import TNFSHTimetableCore
from pydantic import BaseModel
from typing import List, Dict

class GradeList(BaseModel):
    grades: List[str]

class GradeInfo(BaseModel):
    grade: str
    info: Dict

router = APIRouter()

@router.get("/grades", response_model=GradeList)
async def get_grades():
    """獲取所有年級列表"""
    core = TNFSHTimetableCore()
    index = await core.fetch_index()
    return GradeList(grades=list(index.index.class_.data.keys()))

@router.get("/grades/{grade}", response_model=GradeInfo)
async def get_grade(grade: str):
    """獲取指定年級的課程資訊"""
    if not grade:
        grade = "高一"  # 預設年級
    
    core = TNFSHTimetableCore()
    index = await core.fetch_index()
    
    try:
        grade_info = index.index.class_.data[grade]
        return GradeInfo(
            grade=grade,
            info=grade_info
        )
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"年級 '{grade}' 不存在"
        )