from fastapi import FastAPI
from .api.index.category import router as category_router
from .api.index.grade import router as grade_router
from .api.index.class_ import router as class_router
from .api.index.teacher import router as teacher_router

app = FastAPI(
    title="TNFSH Timetable API",
    description="台南一中課表查詢 API",
    version="0.1.0"
)

app.include_router(category_router, prefix="/api/index")
app.include_router(grade_router, prefix="/api/index")
app.include_router(class_router, prefix="/api/index")
app.include_router(teacher_router, prefix="/api/index")