from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tnfsh_timetable_core import TNFSHTimetableCore


class TargetUrl(BaseModel):
    target: str
    url: str


router = APIRouter()

@router.get("/{target}/url", response_model=TargetUrl)
async def get_target_url(target: str):
    """獲取指定班級或教師的課表網址

    Args:
        target: 目標代碼（班級代碼如 "307" 或教師名稱如 "顏永進"）
    """
    try:
        core = TNFSHTimetableCore()
        url = await core.fetch_timetable(target)
        url = url.target_url
        base_url = "http://w3.tnfsh.tn.edu.tw/deanofstudies/course"
        if not url.startswith(base_url):
            url = f"{base_url}/{url}"
        if not url:
            raise ValueError("未找到課表網址")
        return TargetUrl(
            target=target,
            url=url
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"找不到 '{target}' 的課表網址"
        )