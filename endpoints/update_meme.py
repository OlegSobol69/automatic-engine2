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

    @allure.step('Check 401 Unauthorized')
    def check_status_401_without_token(self):
        assert self.response.status_code == 401, f"Expected 401, but got {self.response.status_code}"

    @allure.step('Get memes with invalid method (expecting 405)')
    def put_memes_with_invalid_method_status_405(self, meme_id):
        self.response = requests.post(f"{self.url}/{meme_id}", headers=self.headers)
        assert self.response.status_code == 405, f"Expected 405, but got {self.response.status_code}"

    @allure.step('Check status is 403 when deleting meme with another users token')
    def check_status_403_with_another_user_token(self):
        assert self.response.status_code == 403, f"Expected 403, but got {self.response.status_code}"

    @allure.step('Check 400 for empty request body')
    def check_status_400(self):
        assert self.response.status_code == 400, f"Expected 400 for empty body, but got {self.response.status_code}"

    @allure.step('Check 404 for updating non-existent meme')
    def check_update_non_existent_meme_status_404(self):
        non_existent_meme_id = 0
        body = {
            "id": non_existent_meme_id,
            "text": "Попытка обновления",
            "url": "https://example.com",
            "tags": ["error"],
            "info": {
                "author": "Иван Иванов",
                "date": "2024-10-01"
            }
        }
        response = requests.put(f"{self.url}/{non_existent_meme_id}", json=body, headers=self.headers)
        assert response.status_code == 404, f"Expected 404 for non-existent meme, but got {response.status_code}"
