from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from tnfsh_timetable_api import TNFSHTimetableAPI


class Timetable(BaseModel):
    target: str
    info: Dict[str, Any]


router = APIRouter()

@router.get("/all", response_model=List[Timetable])
async def get_all_teacher_timetable() -> List[Timetable]:
    """獲取所有教師的完整課表"""
    try:
        api = TNFSHTimetableAPI()
        index_api = await api.fetch_index_api()

        teacher_list = await index_api.fetch_all_teacher_list().teachers
        import asyncio
        timetables = await asyncio.gather(
            *[index_api.fetch_teacher_timetable(teacher) for teacher in teacher_list]
        )
        return [
            Timetable(
                target=teacher,
                info=timetable.info.model_dump()
            ) for teacher, timetable in zip(teacher_list, timetables)
        ]
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"找不到教師的課表資訊， error: {str(e)}"
        )
