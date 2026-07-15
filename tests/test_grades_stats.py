import random
import requests
from faker import Faker
from services.university.helpers.grade_helper import GradeHelper
from services.university.models.base_student import DegreeEnum
from services.university.models.grades_stats_response import GradesStatsResponse
from services.university.models.group_request import GroupRequest
from services.university.models.students_request import StudentsRequest
from services.university.university_services import UniversityServices

faker = Faker()


class TestGradesStats:
    def test_get_grades_stats_success(self, university_api_utils_admin):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)

        response = grade_helper.get_grades_stats()

        assert response.status_code == requests.status_codes.codes.ok, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.ok}'")

        stats_data = GradesStatsResponse(**response.json())

        assert stats_data.count >= 0

        if stats_data.count > 0:
            assert stats_data.min is not None
            assert stats_data.max is not None
            assert stats_data.avg is not None
            assert 2 <= stats_data.min <= 5
            assert 2 <= stats_data.max <= 5
            assert 2.0 <= stats_data.avg <= 5.0

    def test_get_grades_stats_with_student_filter(self, university_api_utils_admin):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)
        university_service = UniversityServices(api_utils=university_api_utils_admin)

        group1 = GroupRequest(name=faker.name())
        group1_response = university_service.create_group(group_request=group1)
        student1 = StudentsRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice(list(DegreeEnum)),
            phone=faker.numerify("+79#########"),
            group_id=group1_response.id
        )
        student1_response = university_service.create_student(student_request=student1)

        group2 = GroupRequest(name=faker.name())
        group2_response = university_service.create_group(group_request=group2)
        student2 = StudentsRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice(list(DegreeEnum)),
            phone=faker.numerify("+79#########"),
            group_id=group2_response.id
        )
        student2_response = university_service.create_student(student_request=student2)

        grade_helper.post_grade(data={
            "student_id": student1_response.id,
            "teacher_id": 1,
            "grade": 5
        })
        grade_helper.post_grade(data={
            "student_id": student1_response.id,
            "teacher_id": 1,
            "grade": 4
        })

        grade_helper.post_grade(data={
            "student_id": student2_response.id,
            "teacher_id": 1,
            "grade": 2
        })
        grade_helper.post_grade(data={
            "student_id": student2_response.id,
            "teacher_id": 1,
            "grade": 3
        })

        response = grade_helper.get_grades_stats(student_id=student1_response.id)

        assert response.status_code == requests.status_codes.codes.ok

        stats = GradesStatsResponse(**response.json())

        assert stats.count == 2
        assert stats.min == 4
        assert stats.max == 5
        assert stats.avg == 4.5

    def test_get_grades_stats_anonym_forbidden(self, university_api_utils_anonym):
        grade_helper = GradeHelper(api_utils=university_api_utils_anonym)

        response = grade_helper.get_grades_stats()

        assert response.status_code == requests.status_codes.codes.forbidden, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.forbidden}'")

    def test_get_grades_stats_invalid_params(self, university_api_utils_admin):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)

        response = grade_helper.get_grades_stats(student_id="invalid")

        assert response.status_code == requests.status_codes.codes.unprocessable_entity, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.unprocessable_entity}'")

    def test_get_grades_stats_math(self, university_api_utils_admin):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)
        university_service = UniversityServices(api_utils=university_api_utils_admin)

        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(group_request=group)
        student = StudentsRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice(list(DegreeEnum)),
            phone=faker.numerify("+79#########"),
            group_id=group_response.id
        )
        student_response = university_service.create_student(student_request=student)

        grades_to_add = [2, 3, 4, 5]
        for grade_value in grades_to_add:
            grade_helper.post_grade(data={
                "student_id": student_response.id,
                "teacher_id": 1,
                "grade": grade_value
            })

        response = grade_helper.get_grades_stats(student_id=student_response.id)
        assert response.status_code == requests.status_codes.codes.ok

        stats = GradesStatsResponse(**response.json())

        assert stats.count == 4, f"Expected count 4, got {stats.count}"
        assert stats.min == 2, f"Expected min 2, got {stats.min}"
        assert stats.max == 5, f"Expected max 5, got {stats.max}"
        assert stats.avg == 3.5, f"Expected avg 3.5, got {stats.avg}"
