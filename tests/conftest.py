import pytest
from faker import Faker

from services.auth.auth_services import AuthServices
from services.auth.models.login_request import LoginRequest
from services.auth.models.register_request import RegisterRequest
from services.university.university_services import UniversityServices
from utils.api_utils import ApiUtils

faker = Faker()


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_anonym():
    api_utils = ApiUtils(url=AuthServices.SERVICES_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_anonym():
    api_utils = ApiUtils(url=UniversityServices.SERVICES_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def auth_service_anonym(auth_api_utils_anonym):
    auth_service = AuthServices(auth_api_utils_anonym)
    return auth_service


@pytest.fixture(scope="function", autouse=False)
def access_token(auth_service_anonym):
    username = faker.user_name()
    password = faker.password(
        length=30,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True)

    auth_service_anonym.register_user(register_request=RegisterRequest(
        username=username,
        password=password,
        password_repeat=password,
        email=faker.email()
    ))

    login_response = auth_service_anonym.login_user(login_request=LoginRequest(username=username, password=password))
    return login_response.access_token


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_admin(access_token):
    api_utils = ApiUtils(url=AuthServices.SERVICES_URL, headers={"Authorization": f"Bearer {access_token}"})
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_admin(access_token):
    api_utils = ApiUtils(url=UniversityServices.SERVICES_URL, headers={"Authorization": f"Bearer {access_token}"})
    return api_utils

@pytest.fixture(autouse=True)
def cleanup_data(university_api_utils_admin):
    yield
