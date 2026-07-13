import random
from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.students_request import StudentsRequest
from services.university.university_services import UniversityServices
from faker import Faker

faker = Faker()


class TestGetStudent:
    def test_student_get(self, university_api_utils_admin):
        university_service = UniversityServices(api_utils=university_api_utils_admin)
        # Создаем группу
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group_request=group)

        # Создаем студента
        student = StudentsRequest(first_name=faker.first_name(),
                                  last_name=faker.last_name(),
                                  email=faker.email(),
                                  degree=random.choice(list(DegreeEnum)),
                                  phone=faker.numerify("+79#########"),
                                  group_id=group_response.id)

        student_response = university_service.create_student(student_request=student)

        # Получаем студента
        get_student = university_service.get_student(student_id=student_response.id)

        assert get_student.id == student_response.id, "ID студента не совпадает"
        assert get_student.first_name == student_response.first_name, "Имя не совпадает"
        assert get_student.email == student_response.email, "Email не совпадает"
        assert get_student.group_id == group_response.id, "ID группы не совпадает"
