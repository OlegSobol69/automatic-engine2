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
