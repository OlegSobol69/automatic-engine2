import allure
import requests
from project_automatic.endpoints.general_endpoints import Endpoint
from project_automatic.endpoints.delete_meme import DeleteMeme


class CreateMeme(Endpoint):

    def __init__(self, token):
        super().__init__(token)
        self.meme_id = None
        self.token = token

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
        print(f"Using token for create: {self.headers['Authorization']}")
        self.response = requests.post(self.url, json=body, headers=self.headers)
        response_data = self.response.json()
        self.meme_id = response_data.get("id")
        return self.response

    @allure.step('Check response status is 200')
    def check_status_200(self):
        assert self.response.status_code == 200, f"Expected 200, but got {self.response.status_code}"

    @allure.step('Get meme ID')
    def get_meme_id(self):
        return self.meme_id

    @allure.step('Deleting created meme using DeleteMeme class')
    def delete_meme(self):
        deleter = DeleteMeme(self.token)
        deleter.delete(self.meme_id)
        deleter.check_status_200()
        print(f"Using token for delete : {self.token}")

