import math
import numpy as np
import time

from Lamp import *
from Charger import *
from Heater import *


class Bot:

    def __init__(self, namep):
        self.x = random.randint(100, 1000)
        self.y = random.randint(100, 750)
        self.theta = random.uniform(0.0, 2.0 * math.pi)
        # self.theta = 0
        self.name = namep
        self.ll = 60  # axle width
        self.vl = 0.0
        self.vr = 0.0

        # Random Walk
        self.movement_time = time.time()
        self.movement = "move"
        self.move_timer = random.randint(1, 10)
        self.turn_left = True

        # Towards and Away Light
        self.light_difference = 0
        self.initial_direction = ""
        self.current_direction = ""
        self.previousLightL = 0
        self.previousLightR = 0

        # Battery
        self.initial = True
        self.robot_mode = "lamp"
        self.maxBatteryLevel = 1000
        self.batteryLevel = self.maxBatteryLevel

        # modify this to change the robot's behaviour

    def brain(self, lightL, lightR, heatL, heatR):
        # self.random_walk()

        if (heatL + heatR) < 150:
            self.towards_light(lightL, lightR)
        else:
            self.away_light(heatL, heatR)

    # Move towards the light, attracted to light
    def towards_light(self, lightL, lightR):
        tolerance = (lightL + lightR) / 2
        speed = 10 / tolerance
        if speed > 5:
            speed = 5
        elif speed < -5:
            speed = -5
        elif 0 < speed < 1:
            speed = 1
        elif 0 > speed > -1:
            speed = -1

        if self.previousLightL > lightL + 15 and self.previousLightR > lightR + 15:
            self.vl = 0.0
            self.vr = 0.0
            # print("Stop Moving")
            if self.robot_mode == "charger":
                self.robot_mode = "charging"
        else:
            if (lightL - lightR) > self.light_difference:
                self.vl = 0.0
                self.vr = speed
                # print("Turn Left")
                self.current_direction = "left"
                self.previousLightL = lightL
                self.previousLightR = lightR

                if self.initial:
                    self.initial = False
                    self.initial_direction = "left"
                if self.initial_direction != self.current_direction:
                    self.light_difference = tolerance / 15

            elif (lightR - lightL) > self.light_difference:
                self.vl = speed
                self.vr = 0.0
                # print("Turn Right")
                self.current_direction = "right"
                self.previousLightL = lightL
                self.previousLightR = lightR

                if self.initial:
                    self.initial = False
                    self.initial_direction = "right"
                if self.initial_direction != self.current_direction:
                    self.light_difference = tolerance / 15

            else:
                self.vl = speed
                self.vr = speed
                # print("Move Straight")
                #if self.initial:
                #    self.light_difference = 0
                #else:
                #    self.light_difference = tolerance / 15
                self.light_difference = tolerance / 15
                self.previousLightL = lightL
                self.previousLightR = lightR

    # Move away from light, scare of light
    def away_light(self, lightL, lightR):
        tolerance = (lightL + lightR) / 2
        speed = 10 / tolerance
        if speed > 5:
            speed = 5
        elif speed < -5:
            speed = -5
        elif 0 < speed < 1:
            speed = 1
        elif 0 > speed > -1:
            speed = -1

        if (lightL - lightR) > self.light_difference:
            self.vl = speed
            self.vr = 0.0
            # print("Turn Left")
            self.current_direction = "left"

            if self.initial:
                self.initial = False
                self.initial_direction = "left"
            if self.initial_direction != self.current_direction:
                self.light_difference = tolerance / 15

        elif (lightR - lightL) > self.light_difference:
            self.vl = 0.0
            self.vr = speed
            # print("Turn Right")
            self.current_direction = "right"

            if self.initial:
                self.initial = False
                self.initial_direction = "right"
            if self.initial_direction != self.current_direction:
                self.light_difference = tolerance / 15

        else:
            self.vl = speed
            self.vr = speed
            # print("Move Straight")
            self.light_difference = tolerance / 15

    # Random walking behaviour using time
    def random_walk(self):
        current_time = time.time()
        if self.movement == "move":
            if (current_time - self.movement_time) < self.move_timer:
                self.vl = 1.0
                self.vr = 1.0
                # print("Move straight for " + str(self.move_timer) + " seconds")
            else:
                self.movement = "turn"
                self.movement_time = time.time()
                self.move_timer = random.randint(1, 10)
                self.turn_left = bool(random.getrandbits(1))

        elif self.movement == "turn":
            if (current_time - self.movement_time) < self.move_timer:
                if self.turn_left:
                    self.vl = 0.0
                    self.vr = 1.0
                    # print("Turn left for " + str(self.move_timer) + " seconds")
                else:
                    self.vl = 1.0
                    self.vr = 0.0
                    # print("Turn right for " + str(self.move_timer) + " seconds")
            else:
                self.movement = "move"
                self.movement_time = time.time()
                self.move_timer = random.randint(1, 10)

    # what happens at each timestep
    def update(self, canvas, dt):
        # for now, the only thing that changes is that the robot moves
        #   (using the current settings of self.vl and self.vr)
        battery_threshold = 600
        if self.batteryLevel < battery_threshold:
            if self.robot_mode != "charging" and self.robot_mode != "charger":
                self.robot_mode = "charger"
                self.previousLightL = 0
                self.previousLightR = 0
                self.light_difference = 0

        if self.robot_mode == "charging":
            self.batteryLevel += 1
            if self.batteryLevel >= self.maxBatteryLevel:
                self.robot_mode = "lamp"
                self.previousLightL = 0
                self.previousLightR = 0
                self.light_difference = 0
                print(self.light_difference)
                self.initial = True
        else:
            self.batteryLevel -= 1
        if self.batteryLevel > 0:
            self.move(canvas, dt)
        # print(self.batteryLevel)

    # draws the robot at its current position
    def draw(self, canvas):
        points = [(self.x + 30 * math.sin(self.theta)) - 30 * math.sin((math.pi / 2.0) - self.theta),
                  (self.y - 30 * math.cos(self.theta)) - 30 * math.cos((math.pi / 2.0) - self.theta),
                  (self.x - 30 * math.sin(self.theta)) - 30 * math.sin((math.pi / 2.0) - self.theta),
                  (self.y + 30 * math.cos(self.theta)) - 30 * math.cos((math.pi / 2.0) - self.theta),
                  (self.x - 30 * math.sin(self.theta)) + 30 * math.sin((math.pi / 2.0) - self.theta),
                  (self.y + 30 * math.cos(self.theta)) + 30 * math.cos((math.pi / 2.0) - self.theta),
                  (self.x + 30 * math.sin(self.theta)) + 30 * math.sin((math.pi / 2.0) - self.theta),
                  (self.y - 30 * math.cos(self.theta)) + 30 * math.cos((math.pi / 2.0) - self.theta)
                  ]
        canvas.create_polygon(points, fill="blue", tags=self.name)

        self.sensorPositions = [(self.x + 20 * math.sin(self.theta)) + 30 * math.sin((math.pi / 2.0) - self.theta),
                                (self.y - 20 * math.cos(self.theta)) + 30 * math.cos((math.pi / 2.0) - self.theta),
                                (self.x - 20 * math.sin(self.theta)) + 30 * math.sin((math.pi / 2.0) - self.theta),
                                (self.y + 20 * math.cos(self.theta)) + 30 * math.cos((math.pi / 2.0) - self.theta)
                                ]

        centre1PosX = self.x
        centre1PosY = self.y
        canvas.create_oval(centre1PosX - 15, centre1PosY - 15,
                           centre1PosX + 15, centre1PosY + 15,
                           fill="gold", tags=self.name)

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
        canvas.create_text(self.x, self.y, text=str(self.batteryLevel), tags=self.name)

    # handles the physics of the movement
    # cf. Dudek and Jenkin, Computational Principles of Mobile Robotics
    def move(self, canvas, dt):
        app_Width = 1100
        app_Height = 850

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

        # Make the robot go around the window when it is off the screen
        if self.x > app_Width - 1:
            self.x = 1
        elif self.x < 1:
            self.x = app_Width - 1

        if self.y > app_Height - 1:
            self.y = 1
        elif self.y < 1:
            self.y = app_Height - 1

        canvas.delete(self.name)
        self.draw(canvas)

    # returns the output from polling the light sensors
    def senseLight(self, registryPassives):
        lightL = 0.00
        lightR = 0.00
        for pp in registryPassives:
            if self.robot_mode == "lamp":
                if isinstance(pp, Lamp):
                    lx, ly = pp.getLocation()
                    distanceL = math.sqrt((lx - self.sensorPositions[0]) * (lx - self.sensorPositions[0]) +
                                          (ly - self.sensorPositions[1]) * (ly - self.sensorPositions[1]))
                    distanceR = math.sqrt((lx - self.sensorPositions[2]) * (lx - self.sensorPositions[2]) +
                                          (ly - self.sensorPositions[3]) * (ly - self.sensorPositions[3]))
                    lightL += 200000 / (distanceL * distanceL)
                    lightR += 200000 / (distanceR * distanceR)
            elif self.robot_mode == "charger":
                if isinstance(pp, Charger):
                    lx, ly = pp.getLocation()
                    distanceL = math.sqrt((lx - self.sensorPositions[0]) * (lx - self.sensorPositions[0]) +
                                          (ly - self.sensorPositions[1]) * (ly - self.sensorPositions[1]))
                    distanceR = math.sqrt((lx - self.sensorPositions[2]) * (lx - self.sensorPositions[2]) +
                                          (ly - self.sensorPositions[3]) * (ly - self.sensorPositions[3]))
                    lightL += 200000 / (distanceL * distanceL)
                    lightR += 200000 / (distanceR * distanceR)
            else:
                lightL = 0.01
                lightR = 0.01

        return lightL, lightR

    # returns the output from polling the heat sensors
    def senseHeat(self, registryPassives):
        heatL = 0.00
        heatR = 0.00
        for pp in registryPassives:
            if isinstance(pp, Heater):
                lx, ly = pp.getLocation()
                distanceL = math.sqrt((lx - self.sensorPositions[0]) * (lx - self.sensorPositions[0]) +
                                      (ly - self.sensorPositions[1]) * (ly - self.sensorPositions[1]))
                distanceR = math.sqrt((lx - self.sensorPositions[2]) * (lx - self.sensorPositions[2]) +
                                      (ly - self.sensorPositions[3]) * (ly - self.sensorPositions[3]))
                heatL += 200000 / (distanceL * distanceL)
                heatR += 200000 / (distanceR * distanceR)

        return heatL, heatR
