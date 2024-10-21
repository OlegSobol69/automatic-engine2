import allure
import requests
from endpoints.general_endpoints import Endpoint


class UpdateMeme(Endpoint):

    def __init__(self, token):
        super().__init__(token)

    @allure.step('Update meme')
    def update(self, meme_id, body, custom_headers=None):
        headers = custom_headers if custom_headers else self.headers
        body["id"] = meme_id
        self.response = requests.put(f"{self.url}/{meme_id}", json=body, headers=headers)
        return self.response

    @allure.step('Get memes with invalid method (expecting 405)')
    def put_memes_with_invalid_method_status_405(self, meme_id):
        self.response = requests.post(f"{self.url}/{meme_id}", headers=self.headers)
        assert self.response.status_code == 405, f"Expected 405, but got {self.response.status_code}"

    @allure.step('Check status is 403 when deleting meme with another users token')
    def check_status_403_with_another_user_token(self):
        assert self.response.status_code == 403, f"Expected 403, but got {self.response.status_code}"
