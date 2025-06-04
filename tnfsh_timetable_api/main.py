from fastapi import FastAPI
from tnfsh_timetable_api.api.index.category import router as category_router
from tnfsh_timetable_api.api.index.grade import router as grade_router
from tnfsh_timetable_api.api.index.class_ import router as class_router
from tnfsh_timetable_api.api.index.teacher import router as teacher_router

from tnfsh_timetable_api.api.other.periods import router as periods_router
from tnfsh_timetable_api.api.other.last_update import router as last_update_router

from tnfsh_timetable_api.api.timetable.get_timetable import router as timetable_router
from tnfsh_timetable_api.api.timetable.get_course_info import router as course_info_router
from tnfsh_timetable_api.api.timetable.get_target_url import router as target_url_router
from tnfsh_timetable_api.api.timetable.get_all_timetable import router as get_all_timetable_router
from tnfsh_timetable_api.api.timetable.get_all_teacher_timetable import router as all_teacher_timetable_router
from tnfsh_timetable_api.api.timetable.get_all_class_timetable import router as all_class_timetable_router
from tnfsh_timetable_api.api.timetable.get_all_combined_timetable import router as all_combined_timetable_router

from tnfsh_timetable_api.api.scheduling.rotation import router as rotation_router
from tnfsh_timetable_api.api.scheduling.swap import router as swap_router
from tnfsh_timetable_api.api.scheduling.streak import router as streak_router

app = FastAPI(
    title="TNFSH Timetable API",
    description="台南一中課表查詢 API",
    version="0.1.0"
)

router_prefix_tuple_list = [
    (category_router, "/api/index"),
    (grade_router, "/api/index"),
    (class_router, "/api/index"),
    (teacher_router, "/api/index"),
    (periods_router, "/api/other"),
    (last_update_router, "/api/other"),
    (target_url_router, "/api/timetable"),
    (timetable_router, "/api/timetable"),
    (course_info_router, "/api/timetable"),
    (all_teacher_timetable_router, "/api/timetable/teacher"),
    (all_class_timetable_router, "/api/timetable/class"),
    (all_combined_timetable_router, "/api/timetable"),
    (rotation_router, "/api/scheduling"),
    (swap_router, "/api/scheduling"),
    (streak_router, "/api/scheduling"),
]

for router, prefix in router_prefix_tuple_list:
    app.include_router(router, prefix=prefix)

import asyncio 
from tnfsh_timetable_core import TNFSHTimetableCore
core = TNFSHTimetableCore()
asyncio.run(core.preload_all_timetables())