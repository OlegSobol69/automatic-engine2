import allure
import requests

from endpoints.general_endpoints import Endpoint


class GetMemeById(Endpoint):

    def __init__(self, token):
        super().__init__(token)

    @allure.step('Get meme by id')
    def get_meme_by_id(self, meme_id, custom_headers=None):
        headers = custom_headers if custom_headers else self.headers
        self.response = requests.get(f"{self.url}/{meme_id}", headers=headers)
        return self.response

    @allure.step('Check meme ID matches requested ID')
    def check_meme_id_matches(self, requested_meme_id):
        response_data = self.response.json()
        assert response_data[
                   'id'
               ] == requested_meme_id, f"Expected meme ID '{requested_meme_id}', but got '{response_data['id']}'"

    @allure.step('Check status code is 405 (Method Not Allowed)')
    def send_patch_method_request_in_get_meme_by_id(self, meme_id):
        return requests.patch(f"{self.url}/{meme_id}", headers=self.headers)
