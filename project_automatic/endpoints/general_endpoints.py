class Endpoint:
    url = "http://167.172.172.115:52355/meme"
    response = None

    def __init__(self, token):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'{token}'
        }
