import datetime
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
        self.directDistance = 0
        self.routeDistance = 0

    def __lt__(self, other):
        return self.date < other.date
        
def convertToDate(dateString):
    splitDate = dateString.split(' ')
    month = splitDate[0]
    day = splitDate[1]

    return datetime.strptime(YEAR + '/' + month + '/' + day, '%Y/%b/%d').strftime('%Y/%m/%d')

def calcDistance(zip1, zip2):
    return round(mpu.haversine_distance((zip1.lat, zip1.lng), (zip2.lat, zip2.lng)) * 0.7, 2)

def convertToMiles(steps):
    return steps/(5280/3)

def calcDrivingTime(zip1, zip2):
    req = requests.get(f"http://router.project-osrm.org/route/v1/car/{zip1.lng},{zip1.lat};{zip2.lng},{zip2.lat}?overview=false""")
    routes = json.loads(req.content)
    route = routes.get("routes")[0]
    distance = convertToMiles(route["distance"])
    return distance

def printColor(someEvent):
    textColor = Fore.WHITE
    backColor = Back.RESET

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
        numOfLines = len(lines)
        lineLoop = 1
        for line in lines:
            #print(line)
            values = line.split('-')
            evnt = Ev(values[0], values[1], values[2], values[3])

            c = evnt.location.split(',')[0]
            s = evnt.location.split(',')[1].strip()
            zipcodes = engine.by_city_and_state(city=c, state=s)
            numOfZips = len(zipcodes)
            farthest = 0
            zipLoop = 1
            for zip in zipcodes:
                print("Getting distances from " + HOME_CITY + " to " + zip.major_city + " zip: ", zip.zipcode, " #", zipLoop, "/", numOfZips, " - #", lineLoop, "/", numOfLines)
                zipLoop += 1
                routeDistance = calcDrivingTime(HOME_ZIP, engine.by_zipcode(zip.zipcode))
                directDistance = calcDistance(HOME_ZIP, engine.by_zipcode(zip.zipcode))
                if(routeDistance > 300 or directDistance > 300):
                    break
                if routeDistance > farthest:
                    farthest = routeDistance
                if directDistance > farthest:
                    farthest = directDistance
            lineLoop += 1
            evnt.routeDistance = routeDistance
            evnt.directDistance = directDistance

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
        
    #for sortedEvent in sorted(allEvents):
        #printColor(sortedEvent)
    for thisEvent in allEvents:
        printColor(thisEvent)


parseData()
#print(calcDistance(WDM_ZIP, engine.by_zipcode('50560')))