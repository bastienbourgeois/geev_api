import requests
import json

LOGIN_URL = 'https://prod.geev.fr/api/v0.19/user/auth/local/login'
CONV_URL = 'https://prod.geev.fr/api/v0.19/user/self/conversations?limit=true'

class Geev:
    session = any
    id = any
    app_token = any

    def __init__(self, username, password):
        self.session = requests.Session()
        self.login(username, password)

    def login(self, username, password):
        payload = {
            'login_id': username,
            'password': password
            }
        r = self.session.post(LOGIN_URL, data=json.dumps(payload)).json()
        self.id = r['user']['_id']
        self.app_token = r['app_token']
    
    def getConversation(self):
        header = {'content-type': 'application/json'}
        payload = {
            'x-geev-token': self.app_token
        }
        r = self.session.get(CONV_URL, params=payload, headers=header).json()
        print(r)
        