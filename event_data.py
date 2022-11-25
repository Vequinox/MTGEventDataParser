from uszipcode import SearchEngine
import mpu
from colorama import Fore
from datetime import datetime
#from bs4 import BeautifulSoup
#import requests

engine = SearchEngine()

WDM_ZIP = engine.by_zipcode('50265')
YEAR = "2022"

class Ev:
    def __init__(self, date, store, location, frmt):
        self.date = convertToDate(date.strip())
        self.store = store.strip()
        self.location = location.strip()
        self.frmt = frmt.strip()
        self.dist = 0

    def __lt__(self, other):
        return self.date < other.date
        
def convertToDate(dateString):
    splitDate = dateString.split(' ')
    month = splitDate[0]
    day = splitDate[1]

    return datetime.strptime(YEAR + '/' + month + '/' + day, '%Y/%b/%d').strftime('%Y/%m/%d')

def calcDistance(zip1, zip2):
    return round(mpu.haversine_distance((zip1.lat, zip1.lng), (zip2.lat, zip2.lng)) * 0.7, 2)

def printColor(someEvent):
    color = Fore.WHITE

    if(someEvent.dist >= 0):
        color = Fore.GREEN
    if(someEvent.dist > 130):
        color = Fore.YELLOW
    if(someEvent.dist > 200):
        color = Fore.RED

    distance = "\tDistance: " + str(someEvent.dist)
    if len(someEvent.location) < 11:
        distance = "\t" + distance
    print(color + "Loc: " + someEvent.location + distance + " (" + someEvent.date + " " + someEvent.store + ", " + someEvent.frmt + ")")

def parseData():
    allEvents = []
    showAll = input("Show all events? (y/s/n) ")
    with open('events.txt') as data:
        lines = data.readlines()
        for line in lines:
            #print(line)
            values = line.split('-')
            evnt = Ev(values[0], values[1], values[2], values[3])

            c = evnt.location.split(',')[0]
            s = evnt.location.split(',')[1].strip()
            zipcodes = engine.by_city_and_state(city=c, state=s)

            farthest = 0
            for zip in zipcodes:
                dist = calcDistance(WDM_ZIP, engine.by_zipcode(zip.zipcode))
                if dist > farthest:
                    farthest = dist
            evnt.dist = farthest

            if showAll == 'n':
                if evnt.dist <= 200:
                    allEvents.append(evnt)
            elif showAll == 's':
                if evnt.dist <= 400:
                    allEvents.append(evnt)
            else:
                allEvents.append(evnt)

    # URL = "https://www.facebook.com/groups/MidwestTournamentUpdater/permalink/356913484471420"
    # page = requests.get(URL)

    # soup = BeautifulSoup(page.content, "html.parser")

    # entries = soup.find_all("div", class_="mfn553m3")

    # print(len(entries))
    # for entry in entries:
    #     print(entry)
        
    for sortedEvent in sorted(allEvents):
        printColor(sortedEvent)


parseData()
#print(calcDistance(WDM_ZIP, engine.by_zipcode('50560')))