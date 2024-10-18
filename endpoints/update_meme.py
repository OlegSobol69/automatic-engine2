import allure
import requests
from endpoints.general_endpoints import Endpoint


class UpdateMeme(Endpoint):

    def __init__(self, token):
        super().__init__(token)

    @allure.step('Update meme')
    def update(self, meme_id):
        body = {
            "id": meme_id,
            "text": "Это пример текста.",
            "url": "https://example.com",
            "tags": ["bсправлено", "json", "данные"],
            "info": {
                "author": "Иван Иванов",
                "date": "2024-10-01",
                "views": 100
            }
        }
        self.response = requests.get(f"{self.url}/{meme_id}", json=body, headers=self.headers)
        return self.response

    @allure.step('Check 401 Unauthorized')
    def without_token_check_401(self, meme_id):
        headers_without_token = {key: value for key, value in self.headers.items() if key != 'Authorization'}
        response = requests.put(f"{self.url}/{meme_id}", headers=headers_without_token)
        assert response.status_code == 401, f"Expected 401, but got {response.status_code}"

    @allure.step('Get memes with invalid method (expecting 405)')
    def put_memes_with_invalid_method_status_405(self, meme_id):
        self.response = requests.post(f"{self.url}/{meme_id}", headers=self.headers)
        assert self.response.status_code == 405, f"Expected 405, but got {self.response.status_code}"

    @allure.step('Check status is 403 when deleting meme with another users token')
    def check_status_403_with_another_user_token(self, meme_id, other_token):
        print(f"Attempting to delete meme with id: {meme_id} using another user's token: {other_token}")
        headers_with_other_token = {'Authorization': other_token}
        response_403 = requests.put(f"{self.url}/{meme_id}", headers=headers_with_other_token)
        assert response_403.status_code == 403, f"Expected 403, but got {response_403.status_code}"

    @allure.step('Check 400 for empty request body')
    def check_empty_body_status_400(self, meme_id):
        response = requests.put(f"{self.url}/{meme_id}", json={}, headers=self.headers)
        assert response.status_code == 400, f"Expected 400 for empty body, but got {response.status_code}"

    @allure.step('Check 400 for missing required fields')
    def check_missing_fields_status_400(self, meme_id):
        body = {
            "tags": ["исправлено"],
            "info": {
                "author": "Иван Иванов",
                "date": "2024-10-01"
            }
        }
        response = requests.put(f"{self.url}/{meme_id}", json=body, headers=self.headers)
        assert response.status_code == 400, f"Expected 400 for missing fields, but got {response.status_code}"

    @allure.step('Check 400 for invalid data types')
    def check_invalid_data_types_status_400(self, meme_id):
        body = {
            "id": meme_id,
            "text": 123,
            "url": True,
            "tags": "json",
            "info": "invalid_info"
        }
        response = requests.put(f"{self.url}/{meme_id}", json=body, headers=self.headers)
        assert response.status_code == 400, f"Expected 400 for invalid data types, but got {response.status_code}"

    @allure.step('Check 400 for exceeding text length limit')
    def check_text_length_limit_status_400(self, meme_id):
        long_text = "A" * 10001
        body = {
            "id": meme_id,
            "text": long_text,
            "url": "https://example.com",
            "tags": ["long_text"],
            "info": {
                "author": "Иван Иванов",
                "date": "2024-10-01"
            }
        }
        response = requests.put(f"{self.url}/{meme_id}", json=body, headers=self.headers)
        assert response.status_code == 400, f"Expected 400 for exceeding text length, but got {response.status_code}"

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
