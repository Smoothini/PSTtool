import requests
from bs4 import BeautifulSoup as bs

class PSGame:
    baselink = 'https://www.playstationtrophies.org'
    def __init__(self, data):
        self.title = data.find('h4', {'class': 'h-5'}).text
        self.plat = 0
        self.gold = 0
        self.silver = 0
        self.bronze = 0
        self.secret = 0
        self.platforms = []
        
        link = data.find('a', {'class': 'list__item-link'})
        self.url = PSGame.baselink + link.get('href')

        spans = data.find_all('span')
        for span in spans:
            self.platforms.append(span.text)

        achievements = data.find('div', {'class': 'achievements'})
        #ugly asf but couldnt bother to make prettier
        tt = achievements.prettify().split('<img')
        for t in tt:
            axs = t.split('\n')
            if len(axs)>2:
                if axs[0].find('platinum') != -1:
                    self.plat = (int)(axs[1])
                if axs[0].find('gold') != -1:
                    self.gold = (int)(axs[1])
                if axs[0].find('silver') != -1:
                    self.silver = (int)(axs[1])
                if axs[0].find('bronze') != -1:
                    self.bronze = (int)(axs[1])
                if axs[0].find('secret') != -1:
                    self.secret = (int)(axs[1])
        

    def print(self):
        plist = ''
        for pl in self.platforms:
            plist += pl + '  '
        print(f"Title ...... {self.title}")
        print(f"Platform ... {plist}")
        print(f"Trophy ..... P: {self.plat}  G: {self.gold}  S: {self.silver}  B: {self.bronze}  H: {self.secret}")
        print(f"Url ........ {self.url}\n")

    

url = "https://www.playstationtrophies.org/search.php"
headers = {'Content-Type': "application/x-www-form-urlencoded", 'Accept': "text/html,application/xhtml+xml,application/xml"}

payload = {}

payload['gamesearch'] = input('Insert search tag: ')


req = requests.post(url=url, data=payload, headers=headers)

soup = bs(req.text, 'html.parser')
big = soup.find('ul', {'class': 'list'})

for item in big.find_all('li'):
    game = item.find('h4', {'class': 'h-5'})
    game = PSGame(item)
    game.print()
