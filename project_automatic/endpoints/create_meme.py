import allure
import requests
from project_automatic.endpoints.general_endpoints import Endpoint


class CreateMeme(Endpoint):

    @allure.step('Creating a new meme')
    def create(self):
        body = {
            "text": "Это пример текста.",
            "url": "https://example.com",
            "tags": ["пример", "json", "данные"],
            "info": {
                "author": "Иван Иванов",
                "date": "2024-10-01",
                "views": 100
            }
        }
        self.response = requests.post(self.url, json=body, headers=self.headers)
        return self.response

    @allure.step('Check response status is 200')
    def check_status_200(self):
        assert self.response.status_code == 200, f"Expected 200, but got {self.response.status_code}"


