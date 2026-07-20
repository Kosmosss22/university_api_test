import random
import pytest
from services.university.models.base_student import DegreeEnum
from services.university.models.expected_student import ExpectedStudent
from services.university.models.group_request import GroupRequest
from services.university.models.students_request import StudentsRequest
from services.university.models.teacher_delete_response import DeleteSuccessResponse
from services.university.university_services import UniversityServices
from faker import Faker

faker = Faker()


class TestCrudStudent:

    @pytest.fixture
    def group(self, university_api_utils_admin):
        university_service = UniversityServices(api_utils=university_api_utils_admin)
        group = GroupRequest(name=faker.name())
        return university_service.create_group(group_request=group)

    def test_create_group(self, university_api_utils_admin):
        university_service = UniversityServices(api_utils=university_api_utils_admin)
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group_request=group)

        assert group.name == group_response.name, \
            (f"Wrong group name. Actual: '{group_response.name}', "
             f"but expected: '{group.name}'")

    def test_create_student(self, university_api_utils_admin, group):
        university_service = UniversityServices(api_utils=university_api_utils_admin)
        student = StudentsRequest(first_name=faker.first_name(),
                                  last_name=faker.last_name(),
                                  email=faker.email(),
                                  degree=random.choice(list(DegreeEnum)),
                                  phone=faker.numerify("+79#########"),
                                  group_id=group.id)

        student_response = university_service.create_student(student_request=student)

        assert student_response.group_id == group.id, \
            (f"Wrong group id. Actual: '{student_response.group_id}', "
             f"but expected: '{group.id}'")

    def test_update_student(self, university_api_utils_admin, group):
        university_service = UniversityServices(api_utils=university_api_utils_admin)

        student = StudentsRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice(list(DegreeEnum)),
            phone=faker.numerify("+79#########"),
            group_id=group.id
        )
        student_response = university_service.create_student(student_request=student)

        new_first_name = faker.first_name()

        university_service.update_student(
            student_id=student_response.id,
            student_request=StudentsRequest(
                first_name=new_first_name,
                last_name=student_response.last_name,
                email=student_response.email,
                degree=student_response.degree,
                phone=student_response.phone,
                group_id=student_response.group_id
            )
        )

        updated_student = university_service.get_student(student_id=student_response.id)

        expected_student = ExpectedStudent(
            first_name=new_first_name,
            last_name=student_response.last_name,
            email=student_response.email,
            degree=student_response.degree,
            phone=student_response.phone,
            group_id=student_response.group_id
        )

        updated_dict = updated_student.model_dump(exclude={'id'})
        expected_dict = expected_student.model_dump()

        assert updated_dict == expected_dict, \
            (f"Student data mismatch after update.\n"
             f"Expected: {expected_dict}\n"
             f"Actual: {updated_dict}")

    def test_delete_student(self, university_api_utils_admin, group):
        university_service = UniversityServices(api_utils=university_api_utils_admin)
        student = StudentsRequest(first_name=faker.first_name(),
                                  last_name=faker.last_name(),
                                  email=faker.email(),
                                  degree=random.choice(list(DegreeEnum)),
                                  phone=faker.numerify("+79#########"),
                                  group_id=group.id)
        student_response = university_service.create_student(student_request=student)

        delete_response = university_service.delete_student(student_id=student_response.id)

        expected = DeleteSuccessResponse(detail="Student deleted")
        assert delete_response == expected, \
            (f"Wrong group id. Actual: '{delete_response}', "
             f"but expected: '{expected}'")
