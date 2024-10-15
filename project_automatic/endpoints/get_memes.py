import allure
import requests
from project_automatic.endpoints.general_endpoints import Endpoint


class GetMemes(Endpoint):

    def __init__(self, token):
        super().__init__(token)

    @allure.step('Get memes')
    def get_all_memes(self):
        print(f"Using token : {self.headers['Authorization']}")
        self.response = requests.get(self.url, headers=self.headers)
        return self.response

    @allure.step('Check response structure')
    def check_response_structure(self):
        response_data = self.response.json()
        assert 'data' in response_data, "Key 'data' is missing in response"
        assert isinstance(response_data['data'], list), "Field 'data' should be a list"

    @allure.step('Check each meme has required fields')
    def check_each_meme_fields(self):
        response_data = self.response.json()
        for meme in response_data['data']:
            assert 'id' in meme, "Missing 'id' in meme"
            assert 'text' in meme, "Missing 'text' in meme"
            assert 'url' in meme, "Missing 'url' in meme"
            assert 'tags' in meme, "Missing 'tags' in meme"
            assert 'info' in meme, "Missing 'info' in meme"

    @allure.step('Check field types for each meme')
    def check_field_types_for_each_meme(self):
        response_data = self.response.json()
        for meme in response_data['data']:
            assert isinstance(meme['text'], str), "Field 'text' should be a string"
            assert isinstance(meme['url'], str), "Field 'url' should be a string"
            assert isinstance(meme['tags'], list), "Field 'tags' should be a list"
            assert isinstance(meme['info'], dict), "Field 'info' should be a dictionary"

    @allure.step('Check for duplicate memes')
    def check_for_duplicate_memes(self):
        response_data = self.response.json()
        meme_ids = [meme['id'] for meme in response_data['data']]
        assert len(meme_ids) == len(set(meme_ids)), "Duplicate meme IDs found in the response"

    @allure.step('Check memes are sorted by id')
    def check_memes_sorted_by_id(self):
        response_data = self.response.json()
        meme_ids = [int(meme['id']) for meme in response_data['data']]
        assert meme_ids == sorted(meme_ids), "Memes are not sorted by id"

    @allure.step('Get memes without token (expecting 401)')
    def get_memes_without_token_status_401(self):
        headers_without_token = {key: value for key, value in self.headers.items() if key != 'Authorization'}
        self.response = requests.get(self.url, headers=headers_without_token)
        assert self.response.status_code == 401, f"Expected 401, but got {self.response.status_code}"
        return self.response

    @allure.step('Get memes with invalid method (expecting 405)')
    def get_memes_with_invalid_method_status_405(self):
        self.response = requests.put(self.url, headers=self.headers)
        assert self.response.status_code == 405, f"Expected 405, but got {self.response.status_code}"
        return self.response
