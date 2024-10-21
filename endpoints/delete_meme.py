import allure
import requests
from endpoints.general_endpoints import Endpoint


class DeleteMeme(Endpoint):

    def __init__(self, token):
        super().__init__(token)

    @allure.step('Delete a new meme')
    def delete(self, meme_id, custom_headers=None):
        headers = custom_headers if custom_headers else self.headers
        self.response = requests.delete(f"{self.url}/{meme_id}", headers=headers)
        return self.response

    @allure.step('Check successful deletion message')
    def check_successful_deletion_message(self, meme_id):
        expected_message = f"Meme with id {meme_id} successfully deleted"
        actual_message = self.response.text
        assert actual_message == expected_message, f"Unexpected message: {actual_message}, expected: {expected_message}"

    @allure.step('Check status is 401 without token')
    def check_status_401_without_token(self):
        assert self.response.status_code == 401, f"Expected 401, but got {self.response.status_code}"

    @allure.step('Check status is 403 when deleting meme with another users token')
    def check_status_403_with_another_user_token(self):
        assert self.response.status_code == 403, f"Expected 403, but got {self.response.status_code}"

    @allure.step('Check status is 400 for invalid meme ID')
    def check_status_400_invalid_id(self, invalid_meme_id):
        response_400 = requests.delete(f"{self.url}/{invalid_meme_id}", headers=self.headers)
        full_url = f"{self.url}/{invalid_meme_id}"
        print(f"DELETE 400 URL: {full_url}")
        assert response_400.status_code == 400, f"Expected 400, but got {response_400.status_code}"

    @allure.step('Check status is 405 for invalid method')
    def check_status_405_invalid_method(self, meme_id):
        response_405 = requests.post(f"{self.url}/{meme_id}", headers=self.headers)
        assert response_405.status_code == 405, f"Expected 405, but got {response_405.status_code}"

    @allure.step('Check status is 404 for already deleted meme')
    def check_status_404(self, meme_id):
        response_404 = requests.delete(f"{self.url}/{meme_id}", headers=self.headers)
        assert response_404.status_code == 404, f"Expected 404, but got {response_404.status_code}"
