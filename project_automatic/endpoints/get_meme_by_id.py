import allure
import requests

from project_automatic.endpoints.general_endpoints import Endpoint


class GetMemeById(Endpoint):

    @allure.step('Get meme by id')
    def get_meme_by_id(self, meme_id):
        print(f"Using token : {self.headers['Authorization']}")
        self.response = requests.get(f"{self.url}/{meme_id}", headers=self.headers)
        return self.response

    def check_status_200(self):
        assert self.response.status_code == 200, f"Expected 200, but got {self.response.status_code}"

