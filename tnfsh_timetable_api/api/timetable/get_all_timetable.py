import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List


class Timetable(BaseModel):
    target: str
    info: Dict[str, Any]

router = APIRouter()

@router.get("/teacher/all", response_model=List[Timetable])
async def get_all_teacher_timetable() -> List[Timetable]:
    """獲取指定班級或教師的完整課表

    Args:
        target: 目標代碼（班級代碼如 "307" 或教師名稱如 "顏永進"）
    """
    try:
        from tnfsh_timetable_api import TNFSHTimetableAPI
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

@router.get("/class/all", response_model=List[Timetable])
async def get_all_class_timetable():
    """獲取所有班級的完整課表"""
    try:
        from tnfsh_timetable_api import TNFSHTimetableAPI
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


@router.get("/all", response_model=List[Timetable])
async def get_all_timetable() -> List[Timetable]:
    """獲取所有班級和教師的完整課表"""
    try:
        from tnfsh_timetable_api import TNFSHTimetableAPI
        api = TNFSHTimetableAPI()
        index_api = await api.fetch_index_api()

        teacher_list = await index_api.fetch_all_teacher_list().teachers
        class_list = await index_api.fetch_all_class_list().classes

        import asyncio
        timetables = await asyncio.gather(
            *[index_api.fetch_teacher_timetable(teacher) for teacher in teacher_list],
            *[index_api.fetch_class_timetable(class_code) for class_code in class_list]
        )

        return [
            Timetable(
                target=teacher,
                info=timetable.info.model_dump()
            ) for teacher, timetable in zip(teacher_list, timetables[:len(teacher_list)])
        ] + [
            Timetable(
                target=class_code,
                info=timetable.info.model_dump()
            ) for class_code, timetable in zip(class_list, timetables[len(teacher_list):])
        ]
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"找不到課表資訊， error: {str(e)}"
        )