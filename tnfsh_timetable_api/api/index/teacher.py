from fastapi import APIRouter, HTTPException
from tnfsh_timetable_core import TNFSHTimetableCore
from pydantic import BaseModel
from typing import List, Dict, Any

class TeacherList(BaseModel):
    teachers: List[str]

class TeacherInfo(BaseModel):
    teacher_name: str
    info: Dict[str, Any]

router = APIRouter()

@router.get("/teachers", response_model=TeacherList)
async def get_teachers():
    """獲取所有教師列表"""
    core = TNFSHTimetableCore()
    index = await core.fetch_index()
    result = []
    for value in index.index.teacher.data.values():
        result.extend(list(value.keys()))
    return TeacherList(teachers=result)

@router.get("/teachers/{teacher_name}", response_model=TeacherInfo)
async def get_teacher(teacher_name: str):
    """獲取指定教師的課程資訊"""
    if not teacher_name:
        teacher_name = "顏永進"  # 預設教師名稱
    
    core = TNFSHTimetableCore()
    index = await core.fetch_index()
    
    try:
        teacher_info = index.reverse_index.root[teacher_name]
        return TeacherInfo(
            teacher_name=teacher_name,
            info=teacher_info.model_dump()
        )
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"教師 '{teacher_name}' 不存在"
        )