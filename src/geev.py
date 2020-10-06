import requests

from bs4 import BeautifulSoup

LOGIN_URL = 'https://prod.geev.fr/api/v0.19/user/auth/local/login'
CONV_URL = 'https://prod.geev.fr/api/v0.19/user/self/conversations?limit=true'
OBJ_URL = 'https://www.geev.com/fr/recherche/objets'

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
        r = self.session.post(LOGIN_URL, data=payload).json()
        self.id = r['user']['_id']
        self.app_token = r['app_token']

    def getConversation(self):
        payload = {
            'x-geev-token': self.app_token
        }
        r = self.session.get(CONV_URL, headers=payload).json()

    def getObjects(self, page, location, type, distance):
        url = OBJ_URL + '?page=' + str(page) + '&location=' + location
        url += '&type=' + type + '&distance=' + str(distance)
        
        r = self.session.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        #soup = soup.find_all("div", class_="mol-items-panel")
        soup = soup.find_all("a", class_="mol-itemCard")
        for s in soup:
            print (s['href'])
        #print(soup)