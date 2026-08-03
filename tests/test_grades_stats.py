import random
import requests
from faker import Faker
from services.university.helpers.grade_helper import GradeHelper
from services.university.models.base_student import DegreeEnum
from services.university.models.grades_stats_response import GradesStatsResponse, MIN_GRADE, MAX_GRADE
from services.university.models.group_request import GroupRequest
from services.university.models.students_request import StudentsRequest
from services.university.university_services import UniversityServices
from utils.soft_assert import SoftAssert

faker = Faker()


class TestGradesStats:

    def test_get_grades_stats_empty_for_new_student(self, university_api_utils_admin):
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

        response = grade_helper.get_grades_stats(student_id=student_response.id)
        stats = GradesStatsResponse(**response.json())

        expected = GradesStatsResponse(count=0, min=None, max=None, avg=None)
        assert stats == expected, f"Stats mismatch.\nExpected: {expected}\nActual: {stats}"

    def test_get_grades_stats_with_data(self, university_api_utils_admin):
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

        resp1 = grade_helper.post_grade(data={"student_id": student_response.id, "teacher_id": 1, "grade": MIN_GRADE})
        assert resp1.status_code == 201, f"Failed to post MIN_GRADE. Status: {resp1.status_code}"

        resp2 = grade_helper.post_grade(data={"student_id": student_response.id, "teacher_id": 1, "grade": MAX_GRADE})
        assert resp2.status_code == 201, f"Failed to post MAX_GRADE. Status: {resp2.status_code}"

        stats = GradesStatsResponse(**grade_helper.get_grades_stats(student_id=student_response.id).json())

        with SoftAssert() as sa:
            sa.assert_equal(stats.count, 2, "Count mismatch")
            sa.assert_equal(stats.min, MIN_GRADE, "Min grade mismatch")
            sa.assert_equal(stats.max, MAX_GRADE, "Max grade mismatch")
            sa.assert_equal(stats.avg, (MIN_GRADE + MAX_GRADE) / 2, "Average grade mismatch")

    def test_get_grades_stats_filter_by_group(self, university_api_utils_admin):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)
        university_service = UniversityServices(api_utils=university_api_utils_admin)

        group1 = university_service.create_group(group_request=GroupRequest(name=faker.name()))
        group2 = university_service.create_group(group_request=GroupRequest(name=faker.name()))

        student1 = StudentsRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice(list(DegreeEnum)),
            phone=faker.numerify("+79#########"),
            group_id=group1.id
        )
        student1_resp = university_service.create_student(student_request=student1)

        resp1 = grade_helper.post_grade(data={"student_id": student1_resp.id, "teacher_id": 1, "grade": 5})
        assert resp1.status_code == 201, f"Failed to post grade for student1. Status: {resp1.status_code}"

        student2 = StudentsRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=random.choice(list(DegreeEnum)),
            phone=faker.numerify("+79#########"),
            group_id=group2.id
        )
        student2_resp = university_service.create_student(student_request=student2)

        resp2 = grade_helper.post_grade(data={"student_id": student2_resp.id, "teacher_id": 1, "grade": 2})
        assert resp2.status_code == 201, f"Failed to post grade for student2. Status: {resp2.status_code}"

        stats = GradesStatsResponse(**grade_helper.get_grades_stats(group_id=group1.id).json())

        with SoftAssert() as sa:
            sa.assert_equal(stats.count, 1, "Group filter count mismatch")
            sa.assert_equal(stats.min, 5, "Group filter min mismatch")
            sa.assert_equal(stats.max, 5, "Group filter max mismatch")
            sa.assert_equal(stats.avg, 5.0, "Group filter avg mismatch")

    def test_get_grades_stats_anonym_forbidden(self, university_api_utils_anonym):
        grade_helper = GradeHelper(api_utils=university_api_utils_anonym)
        response = grade_helper.get_grades_stats()

        assert response.status_code == requests.status_codes.codes.forbidden, \
            f"Wrong status code. Actual: '{response.status_code}', but expected: '403'"

    def test_get_grades_stats_invalid_params(self, university_api_utils_admin):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)
        response = grade_helper.get_grades_stats(student_id="invalid_string")

        assert response.status_code == requests.status_codes.codes.unprocessable_entity, \
            f"Wrong status code. Actual: '{response.status_code}', but expected: '422'"
