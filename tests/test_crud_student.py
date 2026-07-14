import random
from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.students_request import StudentsRequest
from services.university.university_services import UniversityServices
from faker import Faker

faker = Faker()


class TestCrudStudent:
    def test_crud_student(self, university_api_utils_admin):
        university_service = UniversityServices(api_utils=university_api_utils_admin)
        # Создаем группу
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group_request=group)

        assert group.name == group_response.name, \
            (f"Wrong group name. Actual: '{group_response.name}', "
             f"but expected: '{group.name}'")

        # Создаем студента
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

        # Обновляем данные студента
        update_student_data = StudentsRequest(
            first_name=faker.first_name(),
            last_name=student_response.last_name,
            email=student_response.email,
            degree=student_response.degree,
            phone=student_response.phone,
            group_id=student_response.group_id
        )

        university_service.update_student(student_id=student_response.id,
                                          student_request=update_student_data)

        updated_student = university_service.get_student(student_id=student_response.id)

        assert updated_student.first_name == update_student_data.first_name, \
            (f"First name was not updated. Actual: '{updated_student.first_name}', "
             f"but expected: '{update_student_data.first_name}'")

        assert updated_student.last_name == student_response.last_name, "Last name was corrupted"
        assert updated_student.email == student_response.email, "Email was corrupted"
        assert updated_student.degree == student_response.degree, "Wrong degree"
        assert updated_student.phone == student_response.phone, "Wrong phone"
        assert updated_student.group_id == student_response.group_id, "Group ID was corrupted"

        # Удаляем студента
        delete_response = university_service.delete_student(student_id=student_response.id)

        assert delete_response.success is True, \
            f"Student was not deleted. Message: {delete_response.message}"
