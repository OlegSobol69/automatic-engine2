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

    @allure.step('Send request using an invalid method')
    def send_post_method_request_in_delete(self, meme_id):
        return requests.post(f"{self.url}/{meme_id}", headers=self.headers)

    @allure.step('Check status 404 for attempting to delete already deleted meme')
    def check_status_404_for_confirm_deleted_meme(self):
        assert self.response.status_code == 404, (f"Expected 404 for already deleted meme, "
                                                  f"but got {self.response.status_code}")
