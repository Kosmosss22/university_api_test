from services.general.base_service import BaseService
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentsHelper
from services.university.models.group_request import GroupRequest
from services.university.models.group_response import GroupResponse
from services.university.models.students_request import StudentsRequest
from services.university.models.students_response import StudentsResponse
from services.university.models.teacher_delete_response import DeleteResponse
from utils.api_utils import ApiUtils


class UniversityServices(BaseService):
    SERVICES_URL = "http://127.0.0.1:8001"

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)

        self.group_helper = GroupHelper(api_utils)
        self.student_helper = StudentsHelper(api_utils)

    def create_group(self, group_request: GroupRequest) -> GroupResponse:
        response = self.group_helper.post_group(json=group_request.model_dump())
        return GroupResponse(**response.json())

    def create_student(self, student_request: StudentsRequest) -> StudentsResponse:
        response = self.student_helper.post_student(json=student_request.model_dump())
        return StudentsResponse(**response.json())

    def get_student(self, student_id: int) -> StudentsResponse:
        response = self.student_helper.get_student(student_id=student_id)
        return StudentsResponse(**response.json())

    def update_student(self, student_id: int, student_request: StudentsRequest) -> StudentsResponse:
        response = self.student_helper.put_student(student_id=student_id, json=student_request.model_dump())
        return StudentsResponse(**response.json())

    def delete_student(self, student_id: int) -> DeleteResponse:
        response = self.student_helper.delete_student(student_id=student_id)

        if response.status_code in [200, 204]:
            return DeleteResponse(success=True, message="Student deleted")
        else:
            return DeleteResponse(success=False, message=f"Failed to delete: {response.status_code}")
