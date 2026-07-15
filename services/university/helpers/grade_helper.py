import requests
from services.general.helpers.base_helper import BaseHelper
from typing import Optional


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    STATS_ENDPOINT = f"{ENDPOINT_PREFIX}/stats/"

    def get_grades(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def post_grade(self, data: dict) -> requests.Response:
        return self.api_utils.post(self.ROOT_ENDPOINT, data=data)

    def get_grades_stats(
            self,
            student_id: Optional[int] = None,
            teacher_id: Optional[int] = None,
            group_id: Optional[int] = None
    ) -> requests.Response:
        params = {}
        if student_id is not None:
            params["student_id"] = student_id
        if teacher_id is not None:
            params["teacher_id"] = teacher_id
        if group_id is not None:
            params["group_id"] = group_id

        response = self.api_utils.get(self.STATS_ENDPOINT, params=params)
        return response
