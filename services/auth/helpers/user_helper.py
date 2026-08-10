import requests

from services.general.helpers.base_helper import BaseHelper


class UserHelper(BaseHelper):
    ENDPOINT_PREFIX = "/users"
    ENDPOINT_USERS = f"{ENDPOINT_PREFIX}/me/"

    def get_me(self) -> requests.Response:
        response = self.api_utils.get(self.ENDPOINT_USERS)
        return response
