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
        self.response = requests.post(self.url, json=body, headers=self.headers)
        response_data = self.response.json()
        self.meme_id = response_data.get("id")
        return self.response

    @allure.step('Check response has meme ID')
    def check_response_has_id(self):
        assert self.meme_id is not None, "Meme ID is missing in the response"

    @allure.step('Check response content type is JSON')
    def check_content_type(self):
        assert self.response.headers.get(
            'Content-Type') == 'application/json', "Expected content type 'application/json'"

    @allure.step('Check URL format is valid')
    def check_url_format(self):
        response_data = self.response.json()
        assert response_data['url'].startswith('http'), "Field 'url' should start with 'http'"

    @allure.step('Deleting created meme using DeleteMeme class')
    def delete_meme(self):
        deleter = DeleteMeme(self.token)
        deleter.delete(self.meme_id)
        deleter.check_status_200()
        print(f"Using token for delete : {self.token}")

    @allure.step('Creating a new meme without token (expecting 401)')
    def create_without_token_check_status_401(self):
        headers_without_token = {key: value for key, value in self.headers.items() if key != 'Authorization'}
        self.response = requests.post(self.url, headers=headers_without_token)
        assert self.response.status_code == 401, f"Expected 401, but got {self.response.status_code}"

    @allure.step('Creating a new meme with custom body')
    def create_with_custom_body(self, body):
        self.response = requests.post(self.url, json=body, headers=self.headers)
        return self.response

    @allure.step('Check response status is 400')
    def check_status_400(self):
        assert self.response.status_code == 400, f"Expected 400, but got {self.response.status_code}"
