import re


class IndexAPI:
    async def fetch_all_grade_list(self):
        from tnfsh_timetable_api.api.index.grade import get_grades
        return await get_grades()

    async def fetch_grade_info(self, grade: str):
        from tnfsh_timetable_api.api.index.grade import get_grade
        return await get_grade(grade=grade)

    async def fetch_all_category_list(self):
        from tnfsh_timetable_api.api.index.category import get_categories
        return await get_categories()

    async def fetch_category_info(self, category_name: str):
        from tnfsh_timetable_api.api.index.category import get_category
        return await get_category(category_name=category_name)

    async def fetch_all_class_list(self):
        from tnfsh_timetable_api.api.index.class_ import get_classes
        return await get_classes()

    async def fetch_class_info(self, class_name: str):
        from tnfsh_timetable_api.api.index.class_ import get_class
        return await get_class(class_name=class_name)

    async def fetch_all_teacher_list(self):
        from tnfsh_timetable_api.api.index.teacher import get_teachers
        return await get_teachers()

    async def fetch_teacher_info(self, teacher_name: str):
        from tnfsh_timetable_api.api.index.teacher import get_teacher
        return await get_teacher(teacher_name=teacher_name)
