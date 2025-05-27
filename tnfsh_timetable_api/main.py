from fastapi import FastAPI
from .api.index.category import router as category_router
from .api.index.grade import router as grade_router
from .api.index.class_ import router as class_router
from .api.index.teacher import router as teacher_router
from .api.other.periods import router as periods_router
from .api.other.last_update import router as last_update_router
from .api.timetable.query import router as timetable_router

app = FastAPI(
    title="TNFSH Timetable API",
    description="台南一中課表查詢 API",
    version="0.1.0"
)

app.include_router(category_router, prefix="/api/index")
app.include_router(grade_router, prefix="/api/index")
app.include_router(class_router, prefix="/api/index")
app.include_router(teacher_router, prefix="/api/index")
app.include_router(periods_router, prefix="/api/other")
app.include_router(last_update_router, prefix="/api/other")
app.include_router(timetable_router, prefix="/api/timetable")