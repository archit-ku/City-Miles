import math
from datetime import datetime

#read input from kiosk/scanner via RFID. for now this will just be text input in the format "[xCoord], [yCoord]". Coordinates range from 0-1000
def scan():
    coords = input("")
    try:
        #formatting coordinates into a list of strings. this will make calculating the manhattan distance between the locations easier and allows the coordinates to be written to a text file using writelines()
        coords = coords.split(",")
        return coords
    except:
        print("Error reading coordinates")
        return False

#update the journeyData to either set a start location, or to clear it
def writeToFile(currentLocation):
    with open("startCoordStorage.txt", "w") as x:
        if currentLocation != None:
            currentLocation = "\n".join(currentLocation)
            x.writelines(currentLocation)
            x.close()
        else:
            x.write("")

#calculate the distance between the start and end coordinates of a journey. more sophisticated versions of distance calculations could be used in future versions
def manhattanDistance(startCoord, endCoord):
    deltaX = abs(int(startCoord[0]) - int(endCoord[0]))
    deltaY = abs(int(startCoord[1]) - int(endCoord[1]))
    #use pythagorean theorem a^2 = b^2 + c^2
    distance = (deltaX*deltaX) + (deltaY*deltaY)
    return distance

#return multiplier for distance depending on journey time. this product will determine the points added for a journey
def timeMultiplier():
    now = datetime.now()
    secondsSinceMidnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    hoursSinceMidnight = secondsSinceMidnight/3600

    print(f"hours since midnight: {hoursSinceMidnight}")

    #implementation of the custom equation visualised in our documentation
    if hoursSinceMidnight >= 13:
        timeMultiplier = ((hoursSinceMidnight/2)-9)**2
    else:
        timeMultiplier = ((hoursSinceMidnight/2)-4)**2
    timeMultiplier *= -1
    timeMultiplier = math.pow((2.7182818),timeMultiplier)
    timeMultiplier *= 5
    timeMultiplier -= 10
    timeMultiplier *= -1
    print(f"time multipler is {timeMultiplier}")
    return timeMultiplier

#method that updates the points in "totalRewards.txt"
def updatePoints(points, distance):
    points += round((distance*timeMultiplier()))
    print(f"total points are: {points}")
    with open("totalRewards.txt", "w") as u:
        u.write(str(points))
    u.close()

#initialising the startCoord and total reward points for a user, without overwriting any data that already exists
try:
    open("startCoordStorage.txt", "r").close()
except:
    open("startCoordStorage.txt", "w").close()

try:
    open("totalRewards.txt", "r").close()
except:
    with open("totalRewards.txt", "w") as newFile:
        newFile.write("0")
    newFile.close()

#main function. this should be called on every interaction wtih kiosk/scanner
def main():
    with open("startCoordStorage.txt", "r") as f:
        startCoord = f.readlines()
        currentLocation = scan()
        if currentLocation: #only continue if scan is successful
            if startCoord == []: #this means we are starting a journey
                f.close()
                writeToFile(currentLocation)
            else: #this means we are ending a journey and awarding points
                startCoord[0] = startCoord[0].strip()
                distance = manhattanDistance(startCoord, currentLocation)
                points = None
                with open("totalRewards.txt", "r") as t:
                    points = int(t.read()) #calculate points to award based on distance of journey and time travelled. off peak and higher distance travelled awards more points
                    t.close()
                    updatePoints(points, distance)
                writeToFile(currentLocation=None) #clear current location

main()