import allure
import requests
from endpoints.general_endpoints import Endpoint


class GetMemes(Endpoint):

    def __init__(self, token):
        super().__init__(token)

    @allure.step('Get memes')
    def get_all_memes(self, custom_headers=None):
        headers = custom_headers if custom_headers else self.headers
        self.response = requests.get(self.url, headers=headers)
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

    @allure.step('Send GET request using an invalid method PUT')
    def send_put_method_request_in_get_memes(self):
        return requests.put(self.url, headers=self.headers)
