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
    def send_post_method_request_in_update(self, meme_id):
        return requests.post(f"{self.url}/{meme_id}", headers=self.headers)

    @allure.step('Check status is 403 when deleting meme with another users token')
    def check_status_403_with_another_user_token(self):
        assert self.response.status_code == 403, f"Expected 403, but got {self.response.status_code}"

