import sys
import tkinter as tk
import random
import math
import numpy as np
import pandas as pd

from Counter import *


class Bot:
    def __init__(self, namep, canvasp, gridMap):
        self.x = random.randint(50, 950)
        self.y = random.randint(50, 800)
        self.theta = random.uniform(0.0, 2.0 * math.pi)
        # self.theta = 0
        self.name = namep
        self.ll = 60  # axle width
        self.vl = 0.0
        self.vr = 0.0
        self.battery = 1000
        self.turning = 0
        self.moving = random.randrange(50, 100)
        self.currentlyTurning = False
        self.canvas = canvasp

        self.map = gridMap
        self.empty_cell = True
        self.mapList = []

        self.dirtCapacity = 0

    def brain(self, chargerL, chargerR, locationL, locationR, binL, binR, method):
        if self.empty_cell and method == 'NearestGrid':
            if locationR > locationL:
                self.vl = 2.0
                self.vr = -2.0
            elif locationR < locationL:
                self.vl = -2.0
                self.vr = 2.0
            if abs(locationR - locationL) < locationL * 0.4:  # approximately the same
                self.vl = 5.0
                self.vr = 5.0
        else:
            # wandering behaviour
            if self.currentlyTurning:
                self.vl = -2.0
                self.vr = 2.0
                self.turning -= 1
            else:
                self.vl = 5.0
                self.vr = 5.0
                self.moving -= 1
            if self.moving == 0 and not self.currentlyTurning:
                self.turning = random.randrange(20, 40)
                self.currentlyTurning = True
            if self.turning == 0 and self.currentlyTurning:
                self.moving = random.randrange(50, 100)
                self.currentlyTurning = False

        # bin - these are later so they have priority
        if self.dirtCapacity > 10:
            if binR > binL:
                self.vl = 2.0
                self.vr = -2.0
            elif binR < binL:
                self.vl = -2.0
                self.vr = 2.0
            if abs(binR - binL) < binL * 0.1:  # approximately the same
                self.vl = 5.0
                self.vr = 5.0
            # self.vl = 5*math.sqrt(chargerR)
            # self.vr = 5*math.sqrt(chargerL)
        if binL + binR > 200 and self.dirtCapacity > 0:
            self.vl = 0.0
            self.vr = 0.0

        # battery - these are the latest, so they have the highest priority
        if self.battery < 600:
            if chargerR > chargerL:
                self.vl = 2.0
                self.vr = -2.0
            elif chargerR < chargerL:
                self.vl = -2.0
                self.vr = 2.0
            if abs(chargerR - chargerL) < chargerL * 0.1:  # approximately the same
                self.vl = 5.0
                self.vr = 5.0
            # self.vl = 5*math.sqrt(chargerR)
            # self.vr = 5*math.sqrt(chargerL)
        if chargerL + chargerR > 200 and self.battery < 1000:
            self.vl = 0.0
            self.vr = 0.0

    def draw(self, canvas):
        points = [(self.x + 30 * math.sin(self.theta)) - 30 * math.sin((math.pi / 2.0) - self.theta),
                  (self.y - 30 * math.cos(self.theta)) - 30 * math.cos((math.pi / 2.0) - self.theta),
                  (self.x - 30 * math.sin(self.theta)) - 30 * math.sin((math.pi / 2.0) - self.theta),
                  (self.y + 30 * math.cos(self.theta)) - 30 * math.cos((math.pi / 2.0) - self.theta),
                  (self.x - 30 * math.sin(self.theta)) + 30 * math.sin((math.pi / 2.0) - self.theta),
                  (self.y + 30 * math.cos(self.theta)) + 30 * math.cos((math.pi / 2.0) - self.theta),
                  (self.x + 30 * math.sin(self.theta)) + 30 * math.sin((math.pi / 2.0) - self.theta),
                  (self.y - 30 * math.cos(self.theta)) + 30 * math.cos((math.pi / 2.0) - self.theta)]
        canvas.create_polygon(points, fill="blue", tags=self.name)

        self.sensorPositions = [(self.x + 20 * math.sin(self.theta)) + 30 * math.sin((math.pi / 2.0) - self.theta),
                                (self.y - 20 * math.cos(self.theta)) + 30 * math.cos((math.pi / 2.0) - self.theta),
                                (self.x - 20 * math.sin(self.theta)) + 30 * math.sin((math.pi / 2.0) - self.theta),
                                (self.y + 20 * math.cos(self.theta)) + 30 * math.cos((math.pi / 2.0) - self.theta)]

        centre1PosX = self.x
        centre1PosY = self.y
        canvas.create_oval(centre1PosX - 20, centre1PosY - 20,
                           centre1PosX + 20, centre1PosY + 20,
                           fill="gold", tags=self.name)
        canvas.create_text(self.x, self.y - 8, text=str(self.battery), tags=self.name)
        canvas.create_text(self.x, self.y + 8, text=str(self.dirtCapacity), tags=self.name, fill='brown')

        wheel1PosX = self.x - 30 * math.sin(self.theta)
        wheel1PosY = self.y + 30 * math.cos(self.theta)
        canvas.create_oval(wheel1PosX - 3, wheel1PosY - 3,
                           wheel1PosX + 3, wheel1PosY + 3,
                           fill="red", tags=self.name)

        wheel2PosX = self.x + 30 * math.sin(self.theta)
        wheel2PosY = self.y - 30 * math.cos(self.theta)
        canvas.create_oval(wheel2PosX - 3, wheel2PosY - 3,
                           wheel2PosX + 3, wheel2PosY + 3,
                           fill="green", tags=self.name)

        sensor1PosX = self.sensorPositions[0]
        sensor1PosY = self.sensorPositions[1]
        sensor2PosX = self.sensorPositions[2]
        sensor2PosY = self.sensorPositions[3]
        canvas.create_oval(sensor1PosX - 3, sensor1PosY - 3,
                           sensor1PosX + 3, sensor1PosY + 3,
                           fill="yellow", tags=self.name)
        canvas.create_oval(sensor2PosX - 3, sensor2PosY - 3,
                           sensor2PosX + 3, sensor2PosY + 3,
                           fill="yellow", tags=self.name)

    def updateMap(self):
        xMapPosition = int(math.floor(self.x / 100))
        yMapPosition = int(math.floor(self.y / 85))
        self.map[xMapPosition, yMapPosition] = 1

    def drawMap(self, canvas):
        for xx in range(self.map.shape[0]):
            for yy in range(self.map.shape[1]):
                if self.map[xx, yy] == 1 and [xx, yy] not in self.mapList:
                    canvas.create_rectangle(100 * xx, 85 * yy, 100 * xx + 100, 85 * yy + 85, fill='pink', width=0,
                                            tags='maps')
                    self.mapList.append([xx, yy])
        canvas.tag_lower('maps')

    # cf. Dudek and Jenkin, Computational Principles of Mobile Robotics
    def move(self, canvas, registryPassives, dt):
        if self.battery > 0:
            self.battery -= 1
        if self.battery == 0:
            self.vl = 0
            self.vr = 0
        for rr in registryPassives:
            if isinstance(rr, Charger) and self.distanceTo(rr) < 80:
                if self.battery < 990:
                    self.battery += 10
                elif 990 <= self.battery < 1000:
                    self.battery += 1000 - self.battery
            if isinstance(rr, Bin) and self.distanceTo(rr) < 80:
                if self.dirtCapacity > 0:
                    self.dirtCapacity -= 1

        if self.vl == self.vr:
            R = 0
        else:
            R = (self.ll / 2.0) * ((self.vr + self.vl) / (self.vl - self.vr))
        omega = (self.vl - self.vr) / self.ll
        ICCx = self.x - R * math.sin(self.theta)  # instantaneous centre of curvature
        ICCy = self.y + R * math.cos(self.theta)
        m = np.matrix([[math.cos(omega * dt), -math.sin(omega * dt), 0],
                       [math.sin(omega * dt), math.cos(omega * dt), 0],
                       [0, 0, 1]])
        v1 = np.matrix([[self.x - ICCx], [self.y - ICCy], [self.theta]])
        v2 = np.matrix([[ICCx], [ICCy], [omega * dt]])
        newv = np.add(np.dot(m, v1), v2)
        newX = newv.item(0)
        newY = newv.item(1)
        newTheta = newv.item(2)
        newTheta = newTheta % (2.0 * math.pi)  # make sure angle doesn't go outside [0.0,2*pi)
        self.x = newX
        self.y = newY
        self.theta = newTheta
        if self.vl == self.vr:  # straight line movement
            self.x += self.vr * math.cos(self.theta)  # vr wlog
            self.y += self.vr * math.sin(self.theta)
        if self.x < 0.0:
            self.x = 999.0
        if self.x > 1000.0:
            self.x = 0.0
        if self.y < 0.0:
            self.y = 849.0
        if self.y > 850.0:
            self.y = 0.0

        self.updateMap()

        canvas.delete(self.name)

        self.draw(canvas)

        self.drawMap(canvas)

    def senseCharger(self, registryPassives):
        lightL = 0.0
        lightR = 0.0
        for pp in registryPassives:
            if isinstance(pp, Charger):
                lx, ly = pp.getLocation()
                distanceL = math.sqrt((lx - self.sensorPositions[0]) * (lx - self.sensorPositions[0]) +
                                      (ly - self.sensorPositions[1]) * (ly - self.sensorPositions[1]))
                distanceR = math.sqrt((lx - self.sensorPositions[2]) * (lx - self.sensorPositions[2]) +
                                      (ly - self.sensorPositions[3]) * (ly - self.sensorPositions[3]))
                lightL += 200000 / (distanceL * distanceL)
                lightR += 200000 / (distanceR * distanceR)

        return lightL, lightR

    def senseBin(self, registryPassives):
        lightL = 0.0
        lightR = 0.0
        for pp in registryPassives:
            if isinstance(pp, Bin):
                lx, ly = pp.getLocation()
                distanceL = math.sqrt((lx - self.sensorPositions[0]) * (lx - self.sensorPositions[0]) +
                                      (ly - self.sensorPositions[1]) * (ly - self.sensorPositions[1]))
                distanceR = math.sqrt((lx - self.sensorPositions[2]) * (lx - self.sensorPositions[2]) +
                                      (ly - self.sensorPositions[3]) * (ly - self.sensorPositions[3]))
                lightL += 200000 / (distanceL * distanceL)
                lightR += 200000 / (distanceR * distanceR)

        return lightL, lightR

    def senseLocation(self):
        lightL = 0.0
        lightR = 0.0
        nearest_distance = 10000
        location = []
        for xxx in range(self.map.shape[0]):
            for yyy in range(self.map.shape[1]):
                if self.map[xxx, yyy] != 1:
                    distance = math.sqrt((self.x - ((xxx * 100) + 50)) ** 2 + (self.y - ((yyy * 85) + 42.5)) ** 2)
                    if distance < nearest_distance:
                        nearest_distance = distance
                        location = [(xxx * 100) + 50, (yyy * 85) + 42.5]
        if not location:
            self.empty_cell = False
        else:
            distanceL = math.sqrt((location[0] - self.sensorPositions[0]) * (location[0] - self.sensorPositions[0]) +
                                  (location[1] - self.sensorPositions[1]) * (location[1] - self.sensorPositions[1]))
            distanceR = math.sqrt((location[0] - self.sensorPositions[2]) * (location[0] - self.sensorPositions[2]) +
                                  (location[1] - self.sensorPositions[3]) * (location[1] - self.sensorPositions[3]))
            lightL += 200000 / (distanceL * distanceL)
            lightR += 200000 / (distanceR * distanceR)

        return lightL, lightR

    def distanceTo(self, obj):
        xx, yy = obj.getLocation()
        return math.sqrt(math.pow(self.x - xx, 2) + math.pow(self.y - yy, 2))

    def collectDirt(self, canvas, registryPassives, count):
        toDelete = []
        for idx, rr in enumerate(registryPassives):
            if isinstance(rr, Dirt):
                if self.distanceTo(rr) < 30:
                    if self.dirtCapacity < 20:
                        canvas.delete(rr.name)
                        self.dirtCapacity += 1
                        toDelete.append(idx)
                        count.itemCollected()

        for ii in sorted(toDelete, reverse=True):
            del registryPassives[ii]
        return registryPassives


class Charger:
    def __init__(self, namep):
        self.centreX = random.randint(50, 950)
        self.centreY = random.randint(50, 800)
        self.name = namep

    def draw(self, canvas):
        body = canvas.create_oval(self.centreX - 10, self.centreY - 10,
                                  self.centreX + 10, self.centreY + 10,
                                  fill="gold", tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY


class Bin:
    def __init__(self, namep):
        self.centreX = random.randint(50, 950)
        self.centreY = random.randint(50, 800)
        self.name = namep

    def draw(self, canvas):
        body = canvas.create_oval(self.centreX - 10, self.centreY - 10,
                                  self.centreX + 10, self.centreY + 10,
                                  fill="brown", tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY


class WiFiHub:
    def __init__(self, namep, xp, yp):
        self.centreX = xp
        self.centreY = yp
        self.name = namep

    def draw(self, canvas):
        body = canvas.create_oval(self.centreX - 10, self.centreY - 10,
                                  self.centreX + 10, self.centreY + 10,
                                  fill="purple", tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY


class Dirt:
    def __init__(self, namep):
        self.centreX = random.randint(10, 990)
        self.centreY = random.randint(10, 840)
        self.name = namep

    def draw(self, canvas):
        body = canvas.create_oval(self.centreX - 1, self.centreY - 1,
                                  self.centreX + 1, self.centreY + 1,
                                  fill="grey", tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY


def buttonClicked(x, y, registryActives):
    for rr in registryActives:
        if isinstance(rr, Bot):
            rr.x = x
            rr.y = y


def initialise(window):
    window.resizable(False, False)
    canvas = tk.Canvas(window, width=1000, height=850)
    canvas.pack()
    return canvas


def register(canvas, noOfBots, gridMap):
    registryActives = []
    registryPassives = []
    noOfDirt = 300
    noOfBin = 1
    for i in range(0, noOfBots):
        bot = Bot("Bot" + str(i), canvas, gridMap)
        registryActives.append(bot)
        bot.draw(canvas)

    charger = Charger("Charger")
    registryPassives.append(charger)
    charger.draw(canvas)

    hub1 = WiFiHub("Hub1", 850, 50)
    registryPassives.append(hub1)
    hub1.draw(canvas)

    hub2 = WiFiHub("Hub1", 50, 500)
    registryPassives.append(hub2)
    hub2.draw(canvas)

    for i in range(0, noOfDirt):
        dirt = Dirt("Dirt" + str(i))
        registryPassives.append(dirt)
        dirt.draw(canvas)

    for i in range(0, noOfBin):
        rubbishBin = Bin("Bin" + str(i))
        registryPassives.append(rubbishBin)
        rubbishBin.draw(canvas)

    count = Counter(canvas)

    canvas.bind("<Button-1>", lambda event: buttonClicked(event.x, event.y, registryActives))
    return registryActives, registryPassives, count, noOfBots


def moveIt(canvas, window, registryActives, registryPassives, noOfBots, count, numberOfMoves, method):
    for rr in registryActives:
        chargerIntensityL, chargerIntensityR = rr.senseCharger(registryPassives)
        binIntensityL, binIntensityR = rr.senseBin(registryPassives)
        locationIntensityL, locationIntensityR = rr.senseLocation()
        rr.move(canvas, registryPassives, 1.0)
        rr.brain(chargerIntensityL, chargerIntensityR, locationIntensityL, locationIntensityR, binIntensityL, binIntensityR, method)
        registryPassives = rr.collectDirt(canvas, registryPassives, count)
    canvas.itemconfigure("time_remaining", text="Time remaining: " + str(1000 - numberOfMoves))
    if numberOfMoves < 1000:
        numberOfMoves += 1
    else:
        print(f"SIMULATION TERMINATED\nNumber of Robot Agent: {noOfBots}\nMethod Used: {method}\n"
              f"Number of Dirt Collected in {numberOfMoves} moves: {count.dirtCollected}")
        #sys.exit()
        canvas.destroy()
        window.destroy()

    canvas.after(50, moveIt, canvas, window, registryActives, registryPassives, noOfBots, count, numberOfMoves, method)


def main(noOfBots, method):
    gridMap = np.zeros((10, 10))
    window = tk.Tk()
    canvas = initialise(window)
    registryActives, registryPassives, count, noOfBots = register(canvas, noOfBots, gridMap)
    numberOfMoves = 0
    canvas.create_text(58, 25, text="Time remaining: " + str(1000 - numberOfMoves), tags="time_remaining")
    moveIt(canvas, window, registryActives, registryPassives, noOfBots, count, numberOfMoves, method)
    window.mainloop()
    return count.dirtCollected


result_list = []
variousProgram = False
if variousProgram:
    numberOfBots = 3
    typeOfMethod = ['Wandering', 'NearestGrid']
    numberOfIteration = numberOfBots + 1
    for i in range(1, numberOfBots + 1):
        for j in typeOfMethod:
            result_list.append([i, j, main(i, j)])
else:
    numberOfBots = 5
    typeOfMethod = 'NearestGrid'
    result_list.append([numberOfBots, typeOfMethod, main(numberOfBots, typeOfMethod)])

result_table = pd.DataFrame(result_list, columns=['Number of Robots', 'Method Used', 'Dirt Collected'])
print(result_table)
