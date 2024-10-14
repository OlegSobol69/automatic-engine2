import allure
import requests
from project_automatic.endpoints.general_endpoints import Endpoint


class UpdateMeme(Endpoint):

    def __init__(self, token):
        super().__init__(token)

    @allure.step('Update meme')
    def update(self, meme_id):
        body = {
            "id": meme_id,
            "text": "Это пример текста.",
            "url": "https://example.com",
            "tags": ["bсправлено", "json", "данные"],
            "info": {
                "author": "Иван Иванов",
                "date": "2024-10-01",
                "views": 100
            }
        }
        self.response = requests.get(f"{self.url}/{meme_id}", json=body, headers=self.headers)
        return self.response

    # @allure.step('Check response status is 200')
    # def check_status_200(self):
    #     assert self.response.status_code == 200, f"Expected 200, but got {self.response.status_code}"
