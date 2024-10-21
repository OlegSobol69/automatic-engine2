import allure


class Endpoint:
    url = "http://167.172.172.115:52355/meme"
    response = None

    def __init__(self, token):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'{token}'
        }

    @allure.step('Check that delete response time is within acceptable limits')
    def check_response_time(self, max_time_ms=500):
        response_time = self.response.elapsed.total_seconds() * 1000
        assert response_time <= max_time_ms, f"Response time {response_time} ms exceeded the limit of {max_time_ms} ms"

    def check_status_200(self):
        assert self.response.status_code == 200, f"Expected 200, but got {self.response.status_code}"

    @allure.step('Check status is 401 without token')
    def check_status_401_without_token(self):
        assert self.response.status_code == 401, f"Expected 401, but got {self.response.status_code}"

    @allure.step('Check response status is 400')
    def check_status_400_bad_request(self):
        assert self.response.status_code == 400, f"Expected 400, but got {self.response.status_code}"

    @allure.step('Check status is 404 for already deleted meme')
    def check_status_404(self):
        assert self.response.status_code == 404, f"Expected 404, but got {self.response.status_code}"

    @allure.step('Check response is not empty')
    def check_response_is_not_empty(self):
        assert self.response.content, "Response content is empty"

    @allure.step('Check response contains all mandatory fields')
    def check_response_has_mandatory_fields(self):
        response_data = self.response.json()
        assert 'text' in response_data, "Response is missing 'text' field"
        assert 'url' in response_data, "Response is missing 'url' field"
        assert 'tags' in response_data, "Response is missing 'tags' field"
        assert 'info' in response_data, "Response is missing 'info' field"

    @allure.step('Check response has correct field types')
    def check_field_types(self):
        response_data = self.response.json()
        assert isinstance(response_data['text'], str), "Field 'text' should be of type string"
        assert isinstance(response_data['url'], str), "Field 'url' should be of type string"
        assert isinstance(response_data['tags'], list), "Field 'tags' should be of type array (list)"
        assert isinstance(response_data['info'], dict), "Field 'info' should be of type object"
