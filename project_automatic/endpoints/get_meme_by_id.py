import allure
import requests

from project_automatic.endpoints.general_endpoints import Endpoint


class GetMemeById(Endpoint):

    def __init__(self, token):
        super().__init__(token)

    @allure.step('Get meme by id')
    def get_meme_by_id(self, meme_id):
        print(f"Using token : {self.headers['Authorization']}")
        self.response = requests.get(f"{self.url}/{meme_id}", headers=self.headers)
        return self.response

    @allure.step('Check meme ID matches requested ID')
    def check_meme_id_matches(self, requested_meme_id):
        response_data = self.response.json()
        assert response_data[
                   'id'
               ] == requested_meme_id, f"Expected meme ID '{requested_meme_id}', but got '{response_data['id']}'"

    @allure.step('Check status code is 404 for non-existent meme')
    def check_status_404(self, non_existent_meme_id):
        response_404 = requests.get(f"{self.url}/{non_existent_meme_id}", headers=self.headers)
        assert response_404.status_code == 404, f"Expected 404, but got {response_404.status_code}"

    @allure.step('Check status code is 405 (Method Not Allowed)')
    def check_status_405(self, meme_id):
        response_405 = requests.post(f"{self.url}/{meme_id}", headers=self.headers)
        assert response_405.status_code == 405, f"Expected 405, but got {response_405.status_code}"

    @allure.step('Get meme by id without token (expecting 401)')
    def get_meme_by_id_without_token_status_401(self, meme_id):
        headers_without_token = {key: value for key, value in self.headers.items() if key != 'Authorization'}
        self.response = requests.get(f"{self.url}/{meme_id}", headers=headers_without_token)
        assert self.response.status_code == 401, f"Expected 401, but got {self.response.status_code}"
        return self.response
