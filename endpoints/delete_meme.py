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

    @allure.step('Check status is 403 when deleting meme with another users token')
    def check_status_403_with_another_user_token(self):
        assert self.response.status_code == 403, f"Expected 403, but got {self.response.status_code}"

    @allure.step('Check status is 405 for invalid method')
    def check_status_405_invalid_method(self, meme_id):
        response_405 = requests.post(f"{self.url}/{meme_id}", headers=self.headers)
        assert response_405.status_code == 405, f"Expected 405, but got {response_405.status_code}"
