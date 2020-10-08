import requests

from bs4 import BeautifulSoup

LOGIN_URL = 'https://prod.geev.fr/api/v0.19/user/auth/local/login'
CONV_URL = 'https://prod.geev.fr/api/v0.19/user/self/conversations?limit=true'
OBJ_URL = 'https://www.geev.com/fr/recherche/objets'
ADDRESS_URL = 'https://prod.geev.fr/api/v0.19/autocomplete'
CONVID_URL = 'https://prod.geev.fr/api/v0.19/user/self/conversations?item_id='

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

    def getLocationFromAddress(self, address):
        url = ADDRESS_URL + "?address=" + address
        r = self.session.get(url).json()
        location = str(r[0]['location']['latitude']) + "%2C"
        location += str(r[0]['location']['longitude'])
        if r == None:
            print('Address not found')
            return None
        return location

    def getConversation(self):
        payload = {
            'x-geev-token': self.app_token
        }
        r = self.session.get(CONV_URL, headers=payload).json()
        convs = []
        for obj in r:
            conv = []
            conv.append(obj['_id'])
            if obj['author']['_id'] != self.id:
                conv.append(obj['title'])
                conv.append(obj['category'])
                conv.append( obj['author']['first_name'] + " " + obj['author']['last_name'])
                cs = []
                for c in obj['conversations']:
                    print(c)
                    cs = c['respondent']['first_name'] + ":" #+ c['respondent']['last_received_message']
                    print(c['last_received_message'])
                #print(obj['conversations'])

    def getObjects(self, page, location, distance):
        if (location == None):
            print('Location error')
            return None
        url = OBJ_URL + '?page=' + str(page) + '&location=' + location
        url += '&type=donation&distance=' + str(distance)
        r = self.session.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        soup = soup.find_all("a", class_="mol-itemCard")
        objs = []
        for s in soup:
            if (s['href'][:4] == "/fr/"):
                obj = []
                obj.append(s['href'])
                params = s.find("ul", class_="mol-itemCard-description-info").select('li')
                obj.append(params[1].text[:-1])
                obj.append(params[0].text)
                dispo = s.find("div", class_="mol-itemCard-cover-availability")
                if dispo == None:
                    obj.append('Available')
                else:
                    obj.append(dispo.text[1:-1])
                bannane = s.find("span", class_="mol-itemCard-cover-banner-text")
                if bannane == None:
                    obj.append('1bannane')
                else:
                    obj.append(bannane.text[1:])
                objs.append(obj)
        print(objs)
        return objs
    
    def getConversationFromId(self, id):
        url = CONV_URL + id
        r = self.session.get(url).json()