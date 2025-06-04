from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from tnfsh_timetable_api import TNFSHTimetableAPI


class Timetable(BaseModel):
    target: str
    info: Dict[str, Any]


router = APIRouter()

@router.get("/all", response_model=List[Timetable])
async def get_all_class_timetable():
    """獲取所有班級的完整課表"""
    try:
        api = TNFSHTimetableAPI()
        index_api = await api.fetch_index_api()

        class_list = await index_api.fetch_all_class_list().classes
        import asyncio
        timetables = await asyncio.gather(
            *[index_api.fetch_class_timetable(class_code) for class_code in class_list]
        )
        return [
            Timetable(
                target=class_code,
                info=timetable.info.model_dump()
            ) for class_code, timetable in zip(class_list, timetables)
        ]
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"找不到班級的課表資訊， error: {str(e)}"
        )
