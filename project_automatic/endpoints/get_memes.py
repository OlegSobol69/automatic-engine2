import allure
import requests
from project_automatic.endpoints.general_endpoints import Endpoint


class GetMemes(Endpoint):

    def __init__(self, token):
        super().__init__(token)

    @allure.step('Get memes')
    def get_all_memes(self):
        print(f"Using token : {self.headers['Authorization']}")
        self.response = requests.get(self.url, headers=self.headers)
        return self.response

    def check_status_200(self):
        assert self.response.status_code == 200, f"Expected 200, but got {self.response.status_code}"

