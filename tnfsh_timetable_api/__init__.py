"""
台南一中課表 API
"""

class TNFSHTimetableAPI:
    async def fetch_index_api(self):
        from tnfsh_timetable_api.api.index import IndexAPI
        return IndexAPI()