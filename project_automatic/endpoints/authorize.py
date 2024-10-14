import allure
import requests


class GetUserToken:
    url = "http://167.172.172.115:52355/authorize"
    headers = {'Content-Type': 'application/json'}
    response = None
    token = None

    @allure.step('Get token')
    def authorize_endpoint(self, user_name):
        body = {
            "name": user_name
        }
        self.response = requests.post(self.url, json=body, headers=self.headers)
        response_data = self.response.json()
        self.token = response_data.get("token")
        self.response = requests.post(self.url, json=body, headers=self.headers)
        return self.response

    @allure.step('Check response status is 200')
    def check_status_200(self):
        assert self.response.status_code == 200, f"Expected 200, but got {self.response.status_code}"

    @allure.step('Check that delete response time is within acceptable limits')
    def check_response_time(self, max_time_ms=300):
        response_time = self.response.elapsed.total_seconds() * 1000
        assert response_time <= max_time_ms, f"Response time {response_time} ms exceeded the limit of {max_time_ms} ms"
