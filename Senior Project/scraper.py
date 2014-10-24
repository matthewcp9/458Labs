import pickle, os, time, json, requests, bs4,sys
from requests import Session
from urllib.request import Request, urlopen
from functools import lru_cache

#response = requests.get('http://www.metacritic.com/user/Overanalytical') # the user i used to check the html of the site
gameurl = 'https://byroredux-metacritic.p.mashape.com/search/game'
key = "clcFDDQWvcmshavNiBerDhWS2mPbp1VzntCjsnLyj1W2ZiKb97"
hdr = {'User-Agent': 'Chrome/37.0.2049.0'}

gamelist = {}

global userlist

class User:
    def __init__(self, username, gamesReviewed):
        self.username = username
        self.gamesReviewed = gamesReviewed
        self.updateAvgRating()
        self.updateNumReviews()
        self.updateAvgWordCt()
        
    def updateUser(self, newReviews):
        for review in newReviews not in self.gamesReviewed:
            self.gamesReviewed += review
        self.updateAvgRating()
        self.updateNumReviews()
        self.updateAvgWordCt()
        

    def updateAvgRating(self):
        if len(self.gamesReviewed) > 0:
            self.avgRating = sum(int(n[1]) for n in self.gamesReviewed)/len(self.gamesReviewed) #location of review score per game
        else :
            self.avgRating = 0

    def updateAvgWordCt(self):
        self.avgWordCt = sum(len(n[2]) for n in self.gamesReviewed)/len(self.gamesReviewed)
    
    def updateNumReviews(self):
        self.numReviews = len(self.gamesReviewed)
        


def findGame(gamename):
    global userlist
    
    session = Session()
    response = session.post(gameurl,
      headers={"X-Mashape-Key": key},
      params={"max_pages": 1, "platform": 0, "retry": 4, "title": gamename}
    )
    queriedRes = response.json()['results']
    if len(queriedRes) > 0:
        print("Found the following games: ")
        for idx in range(0, 5 if len(queriedRes) > 5 else len(queriedRes)):
            query = queriedRes[idx]
            print((str(idx + 1) + "."), query['name'], "for the", query['platform'])
        while True:
            try:
                selected = int(input("Select a game number: ")) - 1
                if selected < 0 or selected > 5:
                    raise Exception() 
                print("Searching for user reviews for %s for the %s" % (queriedRes[selected]['name'], queriedRes[selected]['platform']))
                url = queriedRes[selected]['url']
                beginGameSearch(url)
                break
            except:
                print ("Unexpected error:"), sys.exc_info()[0]
    else:
        print("No games found similar to %s" % gamename)


@lru_cache(maxsize=32)
def beginGameSearch(gameurl):
    global userlist
    global hdr
        
    game_req = Request(gameurl, headers = hdr)
    game_soup = bs4.BeautifulSoup(urlopen(game_req))
    usernames = [b.attrs.get('href') for b in (game_soup.select("div.name a[href^=/user]"))]
    for name in usernames:
        name = name.split('/')[2] #split out the /user/ part
        if name in userlist:
            userlist[name].updateUser(beginUserSearch(name))
        else:
            games = beginUserSearch(name) 
            new_user = User(name, games)
            userlist[name] = new_user
            
    for user in userlist:
        print(user, userlist[user].avgRating, userlist[user].numReviews, userlist[user].avgWordCt)
        print()
    return userlist

def beginUserSearch(username):
    start_time = time.time();
    game_users = getUserReviews(username + "?myscore-filter=Game", [])
    end_time = time.time();
    print('Getting username %s\'s data took %0.3f ms' % (username, ((end_time - start_time)*1000.0)))
    return game_users
    
    
def getPlatform(link):
    global hdr
    platform_req = Request('http://www.metacritic.com/' + link, headers = hdr)
    platform_soup = bs4.BeautifulSoup(urlopen(platform_req))
    platformString = platform_soup.find_all ("span", { "class" : "platform" })[0].get_text().strip()
    return platformString

def getUserReviews(user, games): 
    global hdr
    req = Request('http://www.metacritic.com/user/' + user, headers = hdr)
    page = urlopen(req)
    soup = bs4.BeautifulSoup(page)
    next_check_soup = soup.findAll("span", {"class" : "flipper next"})
    if next_check_soup:
       next_check_soup = next_check_soup[0].find_all("a", href=True)
    splitsoup = soup.select('div.user_profile_reviews')[0]
    platformLink = [a.attrs.get('href') for a in soup.select('div.review_content a[href^=/game]')]
    games.extend(list(zip([productName.get_text() for productName in splitsoup.find_all ("div", { "class" : "product_title" })],
                          #[getPlatform((link.attrs.get('href'))) for platformLink in soup.select('div.review_content a[href^=/game]')],
                          [userScore.get_text() for userScore in splitsoup.find_all ("div", { "class" : "metascore_w" })],
                          [reviewText.get_text() for reviewText in splitsoup.find_all("span", { "class" : "blurb_expanded" })])))
    if not next_check_soup:
        return games
    else:
        #print(next_check_soup[0]['href'].split('/')[2])
        return getUserReviews(next_check_soup[0]['href'].split('/')[2], games)

def reloadUsrList(userlist):
    if os.path.isfile('userlist.txt'):
        with open("userlist.txt", 'rb') as infile:       
            while True:
                try:
                    c = pickle.load(infile)
                    userlist[c.username] = c 
                except EOFError:
                    break
              
def main():
    global userlist
    userlist = {}
    reloadUsrList(userlist)
    print(userlist)
    gamename = ""
    while True:
        gamename = input('Enter a gamename: ')
        if gamename == 'Quit':
            break
        findGame(gamename)
    with open("userlist.txt", 'wb') as outfile:
        print(userlist)
        for user in userlist:
            pickle.dump(userlist[user], outfile, pickle.HIGHEST_PROTOCOL)

main()

