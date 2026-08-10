import random

from faker import Faker

from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.students_request import StudentsRequest
from services.university.university_services import UniversityServices

faker = Faker()


class TestStudent:
    def test_student_create(self, university_api_utils_admin):
        university_service = UniversityServices(api_utils=university_api_utils_admin)
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group_request=group)

        student = StudentsRequest(first_name=faker.first_name(),
                                  last_name=faker.last_name(),
                                  email=faker.email(),
                                  degree=random.choice(list(DegreeEnum)),
                                  phone=faker.numerify("+79#########"),
                                  group_id=group_response.id)

        student_response = university_service.create_student(student_request=student)

        assert student_response.group_id == group_response.id, \
            (f"Wrong group id. Actual: '{student_response.group_id}', "
             f"but expected: '{group_response.id}'")
