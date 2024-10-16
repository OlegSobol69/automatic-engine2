import allure
import requests
from project_automatic.endpoints.authorize import GetUserToken


class TokenLive(GetUserToken):

    @allure.step('Token live')
    def token_live_endpoint(self):
        self.authorize_endpoint("user_1")
        self.response = requests.get(f"{self.url}/{self.token}", headers=self.headers)
        return self.response

    @allure.step('Check token is alive and matches the username')
    def check_token_is_alive(self, expected_user):
        assert self.response.status_code == 200, f"Expected 200, but got {self.response.status_code}"
        assert f"Username is {expected_user}" in self.response.text, \
            f"Token is not alive or username mismatch. Expected: {expected_user}"

    @allure.step('Check for invalid token (404)')
    def check_status_404_for_invalid_token(self):
        self.response = requests.get(f"{self.url}/invalid_token", headers=self.headers)
        assert self.response.status_code == 404, "Expected 404 for invalid token"
