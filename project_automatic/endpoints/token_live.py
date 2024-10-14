import allure
import requests
from project_automatic.endpoints.authorize import GetUserToken


class TokenLive(GetUserToken):

    @allure.step('Token live')
    def token_live_endpoint(self):
        self.authorize_endpoint("user_1")
        print(f"live token {self.token}")
        self.response = requests.get(f"{self.url}/{self.token}", headers=self.headers)
        return self.response

    # def check_status_200(self):
    #     assert self.response.status_code == 200, f"Expected 200, but got {self.response.status_code}"
