from uszipcode import SearchEngine
import mpu
from colorama import Fore

engine = SearchEngine()

WDM_ZIP = engine.by_zipcode('50265')

class Ev:
    def __init__(self, date, store, location, frmt):
        self.date = date.strip()
        self.store = store.strip()
        self.location = location.strip()
        self.frmt = frmt.strip()
        self.dist = 0

    def __lt__(self, other):
        return self.dist < other.dist
        
def calcDistance(zip1, zip2):
    return mpu.haversine_distance((zip1.lat, zip1.lng), (zip2.lat, zip2.lng)) * 0.7

def printColor(someEvent):
    color = Fore.WHITE

    if(someEvent.dist > 0):
        color = Fore.GREEN
    if(someEvent.dist > 130):
        color = Fore.YELLOW
    if(someEvent.dist > 200):
        color = Fore.RED

    print(color + "Loc: " + someEvent.location + "\tDistance: ", someEvent.dist, " (" + someEvent.date + " " + someEvent.store + ", " + someEvent.frmt + ")")

def parseData():
    allEvents = []
    with open('events.txt') as data:
        lines = data.readlines()
        for line in lines:
            values = line.split('-')
            evnt = Ev(values[0], values[1], values[2], values[3])
            allEvents.append(evnt)

            c = evnt.location.split(',')[0]
            s = evnt.location.split(',')[1].strip()
            zipcodes = engine.by_city_and_state(city=c, state=s)

            farthest = 0
            for zip in zipcodes:
                dist = calcDistance(WDM_ZIP, engine.by_zipcode(zip.zipcode))
                if dist > farthest:
                    farthest = dist
            evnt.dist = farthest

            
            #print("Loc: " + evnt.location + " - Distance: ", evnt.dist)
        
    for sortedEvent in sorted(allEvents):
        printColor(sortedEvent)


parseData()
#print(calcDistance(WDM_ZIP, engine.by_zipcode('50560')))