import requests

from services.general.helpers.base_helper import BaseHelper


class StudentsHelper(BaseHelper):
    ENDPOINT_PREFIX = "/students"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"

    def post_student(self, json: dict) -> requests.Response:
        return self.api_utils.post(self.ROOT_ENDPOINT, json=json)

    def get_students(self) -> requests.Response:
        return self.api_utils.get(self.ROOT_ENDPOINT)

    def get_student(self, student_id: int) -> requests.Response:
        return self.api_utils.get(f"{self.ROOT_ENDPOINT}{student_id}")

    def put_student(self, student_id: int, json: dict) -> requests.Response:
        return self.api_utils.put(f"{self.ROOT_ENDPOINT}{student_id}", json=json)

    def delete_student(self, student_id: int) -> requests.Response:
        return self.api_utils.delete(f"{self.ROOT_ENDPOINT}{student_id}")
