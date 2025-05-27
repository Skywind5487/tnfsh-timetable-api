from fastapi import APIRouter, HTTPException
from tnfsh_timetable_core import TNFSHTimetableCore
from pydantic import BaseModel
from typing import List, Dict, Any

class ClassList(BaseModel):
    classes: List[str]

class ClassInfo(BaseModel):
    class_code: str
    info: Dict[str, Any]

router = APIRouter()

@router.get("/classes", response_model=ClassList)
async def get_classes():
    """獲取所有班級列表"""
    core = TNFSHTimetableCore()
    index = await core.fetch_index()
    result = []
    for value in index.index.class_.data.values():
        result.extend(list(value.keys()))
    return ClassList(classes=result)

@router.get("/classes/{class_code}", response_model=ClassInfo)
async def get_class(class_code: str):
    """獲取指定班級的課程資訊
    
    Args:
        class_code: 班級代碼（如: "307"）
    """
    if not class_code:
        class_code = "307"  # 預設班級代碼
    
    core = TNFSHTimetableCore()
    index = await core.fetch_index()
    
    try:
        class_info = index.reverse_index.root[class_code]
        return ClassInfo(
            class_code=class_code,
            info=class_info.model_dump()
        )
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"班級 '{class_code}' 不存在"
        )