import datetime
import WazeRouteCalculator
import logging
from colorama import Fore
from datetime import datetime

YEAR = "2022"

class Ev:
    def __init__(self, date, store, location, frmt):
        self.date = convertToDate(date.strip())
        self.store = store.strip()
        self.location = location.strip()
        self.frmt = frmt.strip()
        self.travelHrs = 0
        self.travelMins = 0

    def __lt__(self, other):
        return self.date < other.date
        
def convertToDate(dateString):
    splitDate = dateString.split(" ")
    month = splitDate[0]
    day = splitDate[1]

    return datetime.strptime(YEAR + "/" + month + "/" + day, "%Y/%b/%d").strftime("%Y/%m/%d")

def printColor(someEvent):
    color = Fore.WHITE

    if(someEvent.travelHrs >= 0):
        color = Fore.GREEN
    if(someEvent.travelHrs >= 2):
        color = Fore.YELLOW
    if(someEvent.travelHrs >= 3):
        color = Fore.RED

    duration = "\tDuration: " + str(someEvent.travelHrs) + " hrs " + str(someEvent.travelMins) + " mins"
    if len(someEvent.location) < 11:
        duration = "\t" + duration
    print(color + "Loc: " + someEvent.location + duration + " (" + someEvent.date + " " + someEvent.store + ", " + someEvent.frmt + ")")

def parseData():
    allEvents = []
    drivingFrom = input("Your address: ")
    showAll = input("Show all events? (y/s/n) ")

    logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    with open("events.txt") as data:
        lines = data.readlines()
        for line in lines:
            values = line.split("-")

            date = values[0]
            store = values[1]
            location = values[2]
            mtgFormat = values[3]
            evnt = Ev(date, store, location, mtgFormat)

            drivingTo = store.strip() + ", " + location.strip()
            route = WazeRouteCalculator.WazeRouteCalculator(drivingFrom, drivingTo, "US", avoid_toll_roads=True)
            routeDuration = route.calc_route_info()[0]
            evnt.travelHrs = int(routeDuration // 60)
            evnt.travelMins = int(routeDuration % 60)
            
            if showAll == "n":
                if evnt.travelHrs <= 2:
                    allEvents.append(evnt)
            elif showAll == "s":
                if evnt.travelHrs <= 3:
                    allEvents.append(evnt)
            else:
                allEvents.append(evnt)

    for thisEvent in allEvents:
        printColor(thisEvent)

parseData()