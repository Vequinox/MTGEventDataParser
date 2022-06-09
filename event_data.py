import datetime
from uszipcode import SearchEngine
import mpu
from colorama import Fore
import requests
import json

engine = SearchEngine()

WDM_ZIP = engine.by_zipcode('50265')

class Ev:
    def __init__(self, date, store, location, frmt):
        self.date = date.strip()
        self.store = store.strip()
        self.location = location.strip()
        self.frmt = frmt.strip()
        self.directDistance = 0
        self.routeDistance = 0

    def __lt__(self, other):
        return (self.directDistance < other.directDistance) or (self.routeDistance < other.routeDistance)
        
def calcDistance(zip1, zip2):
    return mpu.haversine_distance((zip1.lat, zip1.lng), (zip2.lat, zip2.lng)) * 0.7

def convertToMiles(steps):
    return steps/(5280/3)

def calcDrivingTime(zip1, zip2):
    req = requests.get(f"http://router.project-osrm.org/route/v1/car/{zip1.lng},{zip1.lat};{zip2.lng},{zip2.lat}?overview=false""")
    routes = json.loads(req.content)
    route = routes.get("routes")[0]
    distance = convertToMiles(route["distance"])
    return distance

def printColor(someEvent):
    color = Fore.WHITE

    if(someEvent.directDistance > 0 or someEvent.routeDistance > 0):
        color = Fore.GREEN
    if(someEvent.directDistance > 130 or someEvent.routeDistance > 130):
        color = Fore.YELLOW
    if(someEvent.directDistance > 200 or someEvent.routeDistance > 200):
        color = Fore.RED

    print(color + "Loc: " + someEvent.location + "\tDistance: ", someEvent.directDistance, "  to ", someEvent.routeDistance, " miles (" + someEvent.date + " " + someEvent.store + ", " + someEvent.frmt + ")")

def parseData():
    allEvents = []
    with open('events.txt') as data:
        lines = data.readlines()
        numOfLines = len(lines)
        lineLoop = 1
        for line in lines:
            values = line.split('-')
            evnt = Ev(values[0], values[1], values[2], values[3])
            allEvents.append(evnt)

            c = evnt.location.split(',')[0]
            s = evnt.location.split(',')[1].strip()
            zipcodes = engine.by_city_and_state(city=c, state=s)
            numOfZips = len(zipcodes)
            farthest = 0
            zipLoop = 1
            for zip in zipcodes:
                print("Getting distances from West Des Moines to " + zip.major_city + " zip: ", zip.zipcode, " #", zipLoop, "/", numOfZips, " - #", lineLoop, "/", numOfLines)
                zipLoop += 1
                routeDistance = calcDrivingTime(WDM_ZIP, engine.by_zipcode(zip.zipcode))
                directDistance = calcDistance(WDM_ZIP, engine.by_zipcode(zip.zipcode))
                if routeDistance > farthest:
                    farthest = routeDistance
                if directDistance > farthest:
                    farthest = directDistance
            lineLoop += 1
            evnt.routeDistance = routeDistance
            evnt.directDistance = directDistance

            
            #print("Loc: " + evnt.location + " - Distance: ", evnt.dist)
        
    #for sortedEvent in sorted(allEvents):
        #printColor(sortedEvent)
    for thisEvent in allEvents:
        printColor(thisEvent)


parseData()
#print(calcDistance(WDM_ZIP, engine.by_zipcode('50560')))