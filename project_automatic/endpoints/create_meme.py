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

    @allure.step('Check response has meme ID')
    def check_response_has_id(self):
        assert self.meme_id is not None, "Meme ID is missing in the response"

    @allure.step('Check response content type is JSON')
    def check_content_type(self):
        assert self.response.headers.get(
            'Content-Type') == 'application/json', "Expected content type 'application/json'"

    @allure.step('Check response has correct field types')
    def check_field_types(self):
        response_data = self.response.json()
        assert isinstance(response_data['text'], str), "Field 'text' should be of type string"
        assert isinstance(response_data['url'], str), "Field 'url' should be of type string"
        assert isinstance(response_data['tags'], list), "Field 'tags' should be of type array (list)"
        assert isinstance(response_data['info'], dict), "Field 'info' should be of type object (dictionary)"

    @allure.step('Check URL format is valid')
    def check_url_format(self):
        response_data = self.response.json()
        assert response_data['url'].startswith('http'), "Field 'url' should start with 'http'"

    # @allure.step('Get meme ID')
    # def get_meme_id(self):
    #     return self.meme_id

    @allure.step('Deleting created meme using DeleteMeme class')
    def delete_meme(self):
        deleter = DeleteMeme(self.token)
        deleter.delete(self.meme_id)
        deleter.check_status_200()
        print(f"Using token for delete : {self.token}")

    @allure.step('Creating a new meme without token (expecting 401)')
    def create_without_token(self):
        body = {
          "text": "Это пример текста.",
          "url": "https://example.com",
          "tags": [],
          "info": {
          }
        }
        headers_without_token = {'Content-Type': 'application/json'}
        self.response = requests.post(self.url, json=body, headers=headers_without_token)
        return self.response

    @allure.step('Check response status is 401 (Unauthorized)')
    def check_status_401(self):
        assert self.response.status_code == 401, f"Expected 401, but got {self.response.status_code}"

    @allure.step('Creating a new meme with custom body')
    def create_with_custom_body(self, body):
        self.response = requests.post(self.url, json=body, headers=self.headers)
        return self.response

    @allure.step('Check response status is 400')
    def check_status_400(self):
        assert self.response.status_code == 400, f"Expected 400, but got {self.response.status_code}"
