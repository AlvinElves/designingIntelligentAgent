import tkinter as tk

from Bot import *


def initialise(window):
    window.resizable(False, False)
    window.title('Robot')
    window_Width = window.winfo_screenwidth()
    window_Height = window.winfo_screenheight()
    app_Width = 1100
    app_Height = 850

    x = int((window_Width / 2) - (app_Width / 2))
    y = int((window_Height / 2) - (app_Height / 2)) - 40

    window.geometry("{}x{}+{}+{}".format(app_Width, app_Height, x, y))
    canvas = tk.Canvas(window, width=app_Width, height=app_Height)
    canvas.pack()
    return canvas


def register(canvas):
    registryActives = []
    registryPassives = []
    noOfBots = 3
    noOfLights = 1
    noOfCharger = 1
    noOfHeater = 5
    for i in range(0, noOfBots):
        bot = Bot("Bot" + str(i))
        registryActives.append(bot)
        bot.draw(canvas)
    for i in range(0, noOfLights):
        lamp = Lamp("Lamp" + str(i))
        registryPassives.append(lamp)
        lamp.draw(canvas, 'yellow')
    for i in range(0, noOfCharger):
        charger = Charger("Charger" + str(i))
        registryPassives.append(charger)
        charger.draw(canvas, 'black')
    for i in range(0, noOfHeater):
        heater = Heater("Heater" + str(i))
        registryPassives.append(heater)
        heater.draw(canvas, 'red')
    return registryActives, registryPassives


def moveIt(canvas, registryActives, registryPassives):
    for rr in registryActives:
        lightIntensityL, lightIntensityR = rr.senseLight(registryPassives)
        heatIntensityL, heatIntensityR = rr.senseHeat(registryPassives)
        rr.brain(lightIntensityL, lightIntensityR, heatIntensityL, heatIntensityR)
        rr.update(canvas, 1.0)
    canvas.after(50, moveIt, canvas, registryActives, registryPassives)


def main():
    window = tk.Tk()
    canvas = initialise(window)
    registryActives, registryPassives = register(canvas)
    moveIt(canvas, registryActives, registryPassives)
    window.mainloop()


main()
