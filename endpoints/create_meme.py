import allure
import requests
from endpoints.general_endpoints import Endpoint


class CreateMeme(Endpoint):

    def __init__(self, token):
        super().__init__(token)
        self.meme_id = None
        self.token = token

    @allure.step('Creating a new meme')
    def create(self, body, custom_headers=None, request=None):
        headers = custom_headers if custom_headers else self.headers
        self.response = requests.post(self.url, json=body, headers=headers)
        if self.response.status_code == 200:
            response_data = self.response.json()
            self.meme_id = response_data.get("id")
            if request:
                request.node.meme_id = self.meme_id
                request.node.token = self.token
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
