import random
import requests
from services.university.helpers.teacher_helper import TeacherHelper
from faker import Faker
from services.university.models.subject_enum import SubjectEnum

faker = Faker()


class TestTeachersContract:
    def test_post_teachers_success(self, university_api_utils_admin):
        teacher_helper = TeacherHelper(api_utils=university_api_utils_admin)

        response = teacher_helper.post_teacher(
            {"first_name": faker.first_name(),
             "last_name": faker.last_name(),
             "subject": random.choice(list(SubjectEnum)).value
             })

        assert response.status_code == requests.status_codes.codes.created, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.created}'")

    def test_post_teacher_anonym(self, university_api_utils_anonym):
        teacher_helper = TeacherHelper(api_utils=university_api_utils_anonym)

        response = teacher_helper.post_teacher({
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "subject": random.choice(list(SubjectEnum)).value
        })

        assert response.status_code == requests.status_codes.codes.forbidden, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.forbidden}'")

    def test_post_teacher_invalid_subject(self, university_api_utils_admin):
        teacher_helper = TeacherHelper(api_utils=university_api_utils_admin)

        response = teacher_helper.post_teacher({
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "subject": "InvalidSubject"
        })

        assert response.status_code == requests.status_codes.codes.unprocessable_entity, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.unprocessable_entity}'")
