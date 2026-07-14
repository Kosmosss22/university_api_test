import requests
from services.university.helpers.grade_helper import GradeHelper


class TestGradesStats:
    def test_get_grades_stats_success(self, university_api_utils_admin):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)

        response = grade_helper.get_grades_stats()

        assert response.status_code == requests.status_codes.codes.ok, \
            (f"Wrong status code. Actual: '{response.status_code}', "
             f"but expected: '{requests.status_codes.codes.ok}'")

        stats_data = response.json()
        assert "count" in stats_data, "Response missing 'count' field"
        assert "min" in stats_data, "Response missing 'min' field"
        assert "max" in stats_data, "Response missing 'max' field"
        assert "avg" in stats_data, "Response missing 'avg' field"

    def test_get_grades_stats_with_student_filter(self, university_api_utils_admin):
        grade_helper = GradeHelper(api_utils=university_api_utils_admin)

        response_all = grade_helper.get_grades_stats()
        stats_all = response_all.json()

        response_filtered = grade_helper.get_grades_stats(student_id=1)
        stats_filtered = response_filtered.json()

        assert response_filtered.status_code == requests.status_codes.codes.ok
        assert stats_filtered["count"] <= stats_all["count"]

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