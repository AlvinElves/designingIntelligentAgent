import random


class Lamp:
    def __init__(self, namep):
        self.centreX = random.randint(100, 1000)
        self.centreY = random.randint(100, 750)
        self.name = namep

    def draw(self, canvas):
        body = canvas.create_oval(self.centreX - 10, self.centreY - 10,
                                  self.centreX + 10, self.centreY + 10,
                                  fill="yellow", tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY
