import requests

from services.university.helpers.student_helper import StudentsHelper


class TestGetStudentsContract:
    def test_get_students_success(self, university_api_utils_admin):
        students_helper = StudentsHelper(api_utils=university_api_utils_admin)

        response = students_helper.get_students()

        assert response.status_code == requests.status_codes.codes.ok, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.ok}'")

    def test_get_students_anonym(self, university_api_utils_anonym):
        students_helper = StudentsHelper(api_utils=university_api_utils_anonym)

        response = students_helper.get_students()

        assert response.status_code == requests.status_codes.codes.forbidden, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.forbidden}'")
