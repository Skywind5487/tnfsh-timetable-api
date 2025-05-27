from fastapi import APIRouter, HTTPException
from tnfsh_timetable_core import TNFSHTimetableCore
from pydantic import BaseModel
from typing import List

class CategoryList(BaseModel):
    categories: List[str]

class CategoryInfo(BaseModel):
    category_name: str
    info: dict

router = APIRouter()

@router.get("/categories", response_model=CategoryList)
async def get_categories():
    """獲取所有分類列表"""
    core = TNFSHTimetableCore()
    index = await core.fetch_index()
    return CategoryList(categories=list(index.index.teacher.data.keys()))

@router.get("/categories/{category_name}", response_model=CategoryInfo)
async def get_category(category_name: str):
    """獲取指定分類的課程資訊"""
    core = TNFSHTimetableCore()
    index = await core.fetch_index()
    
    try:
        category_info = index.index.teacher.data[category_name]
        return CategoryInfo(
            category_name=category_name,
            info=category_info
        )
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"分類 '{category_name}' 不存在"
        )