import datetime
import WazeRouteCalculator
import logging
import re
from colorama import Fore
from datetime import datetime

YEAR = "2023"

class Ev:
    def __init__(self, date, store, location, frmt):
        self.date = date
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

    if(month == "June" or month == "june"):
        month = "Jun"
    elif(month == "July" or month == "july"):
        month = "Jul"
    
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

def isBadEvent(line):
    return len(line.split(" - ")) != 4

def performRegex(line):
    newLine = line
    if re.search("\w-\w", line):
        newLine = re.sub("(\w)-(\w)", r"\1 \2", newLine)
    return newLine

def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    total = len(iterable)

    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)

    printProgressBar(0)

    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)

    print()

def parseData():
    #logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
    #logger.setLevel(logging.DEBUG)
    #handler = logging.StreamHandler()
    #logger.addHandler(handler)

    allEvents = []
    badEvents = []

    isDSM = input("IA and NE events only? (y/n)")

    if(isDSM == "n"):
        drivingFrom = input("Your address: ")
        showAll = input("Show all events? (y/s/n) ")
    else:
        drivingFrom = "Des Moines, IA"
        showAll = "y"

    isSpecificDateRange = input("Specify date range? (y/n) ")

    if(isSpecificDateRange == "y"):
        dateRangeStart = convertToDate(input("Date range start? Example: Jun 8 "))
        dateRangeEnd = convertToDate(input("Date range end? Example: Jun 10 "))
    
    with open("events.txt") as data:
        lines = data.readlines()
        #for line in lines:
        for line in progressBar(lines, prefix="Progress:", suffix="Complete"):
            cleanLine = performRegex(line)
            if isBadEvent(cleanLine):
                badEvents.append(cleanLine)
                continue

            values = cleanLine.split(" - ")

            date = convertToDate(values[0].strip())
            store = values[1]
            location = values[2]
            mtgFormat = values[3]

            if (isDSM == "y" and (location.endswith("IA") or location.endswith("NE"))) or (isSpecificDateRange == "y" and dateRangeStart <= date and dateRangeEnd >= date) or (isSpecificDateRange == "n" and isDSM == "n"):
                drivingTo = store.strip() + ", " + location.strip()
                route = WazeRouteCalculator.WazeRouteCalculator(drivingFrom, drivingTo, "US", avoid_toll_roads=True)
                routeDuration = route.calc_route_info()[0]

                evnt = Ev(date, store, location, mtgFormat)
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

    if len(badEvents) > 0:
        print("***Found issues with the following events: ")
        for event in badEvents:
            print(event)

parseData()