import pygame
from pygame import *
from Constants import *
from Vessel import Vessel
from Effector import Heater
from Sensor import Sensor
from time import sleep
from typing import *

class Keypad:
    def __init__(self):
        self.buttons = []
        self.buttons.append({'text' : '1', 'rect' : (680, 45, 30, 30), 'color' : (66, 134, 244), 'textPos' : (692, 50)})
        self.buttons.append({'text' : '2', 'rect' : (720, 45, 30, 30), 'color' : (66, 134, 244), 'textPos' : (732, 50)})
        self.buttons.append({'text' : '3', 'rect' : (760, 45, 30, 30), 'color' : (66, 134, 244), 'textPos' : (772, 50)})
        self.buttons.append({'text' : 'A', 'rect' : (800, 45, 30, 30), 'color' : (239, 36, 14), 'textPos' : (812, 50)})
        self.buttons.append({'text' : '4', 'rect' : (680, 85, 30, 30), 'color' : (66, 134, 244), 'textPos' : (692, 90)})
        self.buttons.append({'text' : '5', 'rect' : (720, 85, 30, 30), 'color' : (66, 134, 244), 'textPos' : (732, 90)})
        self.buttons.append({'text' : '6', 'rect' : (760, 85, 30, 30), 'color' : (66, 134, 244), 'textPos' : (772, 90)})
        self.buttons.append({'text' : 'B', 'rect' : (800, 85, 30, 30), 'color' : (239, 36, 14), 'textPos' : (812, 90)})
        self.buttons.append({'text' : '7', 'rect' : (680, 125, 30, 30), 'color' : (66, 134, 244), 'textPos' : (692, 130)})
        self.buttons.append({'text' : '8', 'rect' : (720, 125, 30, 30), 'color' : (66, 134, 244), 'textPos' : (732, 130)})
        self.buttons.append({'text' : '9', 'rect' : (760, 125, 30, 30), 'color' : (66, 134, 244), 'textPos' : (772, 130)})
        self.buttons.append({'text' : 'C', 'rect' : (800, 125, 30, 30), 'color' : (239, 36, 14), 'textPos' : (812, 130)})
        self.buttons.append({'text' : '*', 'rect' : (680, 165, 30, 30), 'color' : (239, 36, 14), 'textPos' : (692, 170)})
        self.buttons.append({'text' : '0', 'rect' : (720, 165, 30, 30), 'color' : (66, 134, 244), 'textPos' : (732, 170)})
        self.buttons.append({'text' : '#', 'rect' : (760, 165, 30, 30), 'color' : (239, 36, 14), 'textPos' : (772, 170)})
        self.buttons.append({'text' : 'D', 'rect' : (800, 165, 30, 30), 'color' : (239, 36, 14), 'textPos' : (812, 170)})

    def getButtons(self):
        return self.buttons

class GUI:
    def __init__(self, plant = None, controller = None, monitor = None):
        self.__plant = plant
        self.__controller = controller
        self.__monitor = monitor
        self.__timestamp = 0
        self.__run = False
        self.__tap = False
        self.__keypad = Keypad()
        # Initialise PyGame
        pygame.init()
        pygame.font.init()
        self.__font = pygame.font.Font('font/OpenSans-Regular.ttf', 12)
        self.__big_font = pygame.font.Font('font/OpenSans-Regular.ttf', 26)
        # Define a screen
        self.__screen = pygame.display.set_mode((940, 400))
        pygame.display.set_caption('Liquid Mixer Simulator GUI')
        pygame.mouse.set_visible(True)

        # Create components
        self.__icons = {}
        self.__icons["a"] = VesselIcon(self.__screen, 100, 50, self.__plant._vessels["a"])
        self.__icons["b"] = VesselIcon(self.__screen, 300, 50, self.__plant._vessels["b"])
        self.__icons["mix"] = VesselIcon(self.__screen, 200, 125, self.__plant._vessels["mix"])
        self.__icons["heater"] = HeaterIcon(self.__screen, 200, 185, self.__plant._effectors["heater"].get)
        self.__icons["temperature"] = SensorIcon(self.__screen, 275, 125, self.__plant._sensors["temperature"].read_mc, "°C",  "Temperature")
        self.__icons["distance"] = SensorIcon(self.__screen, 275, 150, self.__plant._sensors["distance"].read_mm, "ml", "distance")
        self.__icons["color"] = SensorIcon(self.__screen, 275, 175, self.__plant._sensors["color"].read_rgb, "%", "Colour")

        # Draw
        self.step()

    def drawPipes(self) -> None:
        pygame.draw.lines(self.__screen, (0, 0, 0), False,
                          [(135, 55), (135, 35), (215, 35), (215, 140)], 5)
        pygame.draw.lines(self.__screen, (0, 0, 0), False,
                          [(235, 140), (235, 35), (315, 35), (315, 55)], 5)

    def drawButtons(self) -> None:
        pygame.draw.rect(self.__screen, (240, 120, 0), [500, 10, 60, 30])
        if self.__run:
            pygame.draw.rect(self.__screen, (240, 240, 240), [517, 15, 10, 20])
            pygame.draw.rect(self.__screen, (240, 240, 240), [532, 15, 10, 20])
        else:
            pygame.draw.polygon(self.__screen, (240, 240, 240), [(527, 15), (527, 35), (543, 25)])
        pygame.draw.rect(self.__screen, (240, 120, 0), [570, 10, 60, 30])
        pygame.draw.polygon(self.__screen, (240, 240, 240), [(585, 15), (585, 35), (600, 25)])
        pygame.draw.rect(self.__screen, (240, 240, 240), [605, 15, 10, 20])
        pygame.draw.rect(self.__screen, (240, 120, 0), [500, 50, 130, 30])

        #KEYPAD
        for keyPadButton in self.__keypad.getButtons():
            pygame.draw.rect(self.__screen, keyPadButton['color'], keyPadButton['rect'])
            label = self.__font.render(keyPadButton['text'], False, (255, 255, 255))
            self.__screen.blit(label, keyPadButton['textPos'])

        #LCD LED
        pygame.draw.rect(self.__screen, (52, 191, 30), [680, 215, 145, 50])
        #for each lcd letter, print
        for idx,text in enumerate(self.__plant._display.get_text(), start=0):
            label = self.__font.render(''.join(text), False, (0, 0, 0))
            self.__screen.blit(label, [685, 215+(idx*12)])


        water_pump = "water pump: "+("on " if self.__plant._effectors["water_pump"].get() else "off")
        label = self.__font.render(water_pump, False, (240, 240, 240))
        self.__screen.blit(label, [530, 55])
        pygame.draw.rect(self.__screen, (240, 120, 0), [500, 90, 130, 30])
        sirup_pump = "sirup pump: "+("on " if self.__plant._effectors["sirup_pump"].get() else "off")
        label = self.__font.render(sirup_pump, False, (240, 240, 240))
        self.__screen.blit(label, [530, 95])
        pygame.draw.rect(self.__screen, (240, 120, 0), [500, 130, 130, 30])
        heater = "Heater: "+("on " if self.__plant._effectors["heater"].get() else "off")
        label = self.__font.render(heater, False, (240, 240, 240))
        self.__screen.blit(label, [530, 135])
        pygame.draw.rect(self.__screen, (240, 120, 0), [500, 170, 130, 30])
        tap = "Tap: "+("on " if self.__tap else "off")
        label = self.__font.render(tap, False, (240, 240, 240))
        self.__screen.blit(label, [530, 175])

        self.add_cup = pygame.draw.rect(self.__screen, (240, 120, 0), [160, 0, 130, 30])
        self.__screen.blit(
            self.__font.render("%s" % ("Remove cup" if self.__plant._sensors["reflex"].get() else "Insert cup"), False, (240, 240, 240)),
        [200, 0])

        pygame.draw.circle(self.__screen, (0, 255, 0), (226,90), 7, 0) if self.__plant._effectors['led_green'].get() else pygame.draw.circle(self.__screen, (0, 0, 0), (226,90), 7, 0)

        pygame.draw.circle(self.__screen, (255, 255, 0), (226,70), 7, 0) if self.__plant._effectors['led_yellow'].get() else pygame.draw.circle(self.__screen, (0, 0, 0), (226,70), 7, 0)

    def drawGraphs(self) -> None:
        scale = 140 / 3.3
        # Temperature
        pygame.draw.lines(self.__screen, (0, 0, 0), False, [(30, 240), (30, 380), (200, 380)])
        label = self.__font.render("0", False, (0, 0, 0))
        self.__screen.blit(label, [20, 380])
        label = self.__font.render("3.3", False, (0, 0, 0))
        self.__screen.blit(label, [10, 230])
        x0 = 30
        y0 = 380
        pygame.draw.line(self.__screen, (240, 120, 0), [x0, y0 - (tempSetPoint * scale)], [x0 + 170, y0 - tempSetPoint * scale])
        label = self.__font.render(str(tempSetPoint), False, (240, 120, 0))
        self.__screen.blit(label, [5, y0 - (tempSetPoint * scale) - 10])

        if len(self.__monitor._sensorReadings["temperature"]) < 170:
            x, y = x0, y0
        else:
            x = x0
            y = y0 - self.__monitor._sensorReadings["temperature"][-170] * scale
        for reading in self.__monitor._sensorReadings["temperature"][-170:]:
            prevX, prevY = x, y
            x += 1
            y = y0 - (reading * scale)
            pygame.draw.line(self.__screen, (240, 0, 0), [prevX, prevY], [x, y], 2)
        x, y = x0, y0
        for value in self.__monitor._effectorValues["heater"][-170:]:
            x += 1
            y = y0-20 if value else y0
            pygame.draw.line(self.__screen, (120, 120, 0), [x, y0], [x, y])
        label = self.__font.render("Temperature", False, (0, 0, 0))
        self.__screen.blit(label, [80, 225])

        # distance
        pygame.draw.lines(self.__screen, (0, 0, 0), False, [(240, 240), (240, 380), (410, 380)])
        label = self.__font.render("0", False, (0, 0, 0))
        self.__screen.blit(label, [230, 380])
        label = self.__font.render("3.3", False, (0, 0, 0))
        self.__screen.blit(label, [220, 230])
        x0 = 240
        pygame.draw.line(self.__screen, (240, 120, 0), [x0, y0 - (levelSetPoint * scale)], [x0 + 170, y0 - levelSetPoint * scale])
        label = self.__font.render(str(levelSetPoint), False, (240, 120, 0))
        self.__screen.blit(label, [210, y0 - (levelSetPoint * scale) - 10])

        if len(self.__monitor._sensorReadings["distance"]) < 170:
            x, y = x0, y0
        else:
            x = x0
            y = y0 - self.__monitor._sensorReadings["distance"][-170] * scale
        for reading in self.__monitor._sensorReadings["distance"][-170:]:
            prevX, prevY = x, y
            x += 1
            y = y0 - (reading * scale)
            pygame.draw.line(self.__screen, (0, 240, 0), [prevX, prevY], [x, y], 2)
        x, y = x0, y0
        for value1, value2 in zip(self.__monitor._effectorValues["water_pump"][-170:], self.__monitor._effectorValues["sirup_pump"][-170:]):
            x += 1
            y = y0-15 if value1 else y0
            pygame.draw.line(self.__screen, (120, 0, 120), [x, y0], [x, y])
            y = y0-7 if value2 else y0
            pygame.draw.line(self.__screen, (0, 120, 120), [x, y0], [x, y])
        label = self.__font.render("distance", False, (0, 0, 0))
        self.__screen.blit(label, [280, 225])

        # Colour
        pygame.draw.lines(self.__screen, (0, 0, 0), False, [(450, 240), (450, 380), (620, 380)])
        label = self.__font.render("0", False, (0, 0, 0))
        self.__screen.blit(label, [440, 380])
        label = self.__font.render("3.3", False, (0, 0, 0))
        self.__screen.blit(label, [430, 230])
        x0 = 450
        pygame.draw.line(self.__screen, (240, 120, 0), [x0, y0 - (colourSetPoint * scale)], [x0 + 170, y0 - colourSetPoint * scale])
        label = self.__font.render(str(colourSetPoint), False, (240, 120, 0))
        self.__screen.blit(label, [420, y0 - (colourSetPoint * scale) - 10])

        if len(self.__monitor._sensorReadings["color"]) < 170:
            x, y = x0, y0
        else:
            x = x0
            y = y0 - self.__monitor._sensorReadings["color"][-170] * scale
        for reading in self.__monitor._sensorReadings["color"][-170:]:
            prevX, prevY = x, y
            x += 1
            y = y0 - (reading * scale)
            pygame.draw.line(self.__screen, (0, 0, 240), [prevX, prevY], [x, y], 2)
        label = self.__font.render("Colour", False, (0, 0, 0))
        self.__screen.blit(label, [480, 225])


    def update(self) -> None:
        self.__screen.fill((250, 250, 250))
        for (name, icon) in self.__icons.items():
            if not (name == 'mix' and not self.__plant._sensors['reflex'].get()):
                icon.draw()
        self.drawPipes()

        self.drawButtons()
        self.drawGraphs()

        label = self.__font.render(str(self.__timestamp), True, (0, 0, 0))
        self.__screen.blit(label, [10, 10])

        pygame.display.update()

    def step(self) -> None:
        self.__timestamp += 1
        self.__plant.update()
        self.__controller.update()
        self.__monitor.update()
        if self.__tap:
            self.__plant._vessels["mix"].flow()

    def run(self) -> None:
        while True:
            if self.__run:
                self.step()

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 500 < pos[0] <= 630:
                        if 10 < pos[1] <= 40 and pos[0] < 560:
                            self.__run = False if self.__run else True
                        elif 10 < pos[1] <= 40 and pos[0] > 560:
                            if not self.__run:
                                self.step()
                        elif 50 < pos[1] <= 80:
                            if self.__plant._effectors["water_pump"].get():
                                self.__plant._effectors["water_pump"].set(0)
                            else:
                                self.__plant._effectors["water_pump"].set(1)
                        elif 90 < pos[1] <= 120:
                            if self.__plant._effectors["sirup_pump"].get():
                                self.__plant._effectors["sirup_pump"].set(0)
                            else:
                                self.__plant._effectors["sirup_pump"].set(1)
                        elif 130 < pos[1] <= 160:
                            if self.__plant._effectors["heater"].get():
                                self.__plant._effectors["heater"].set(0)
                            else:
                                self.__plant._effectors["heater"].set(1)
                        elif 170 < pos[1] <= 200:
                            self.__tap = False if self.__tap else True
                    print(pos)
                    #keypad
                    for keypadButton in self.__keypad.getButtons():
                        if pygame.Rect(keypadButton['rect']).collidepoint(pos):
                            self.__plant._sensors['keypad'].putc(keypadButton['text'])
                    if pygame.Rect(self.add_cup).collidepoint(pos):
                        self.__plant._sensors['reflex']._value = not self.__plant._sensors['reflex']._value
                        self.__plant._vessels['mix'].empty()

            self.update()
            sleep(0.1)


class Icon:
    def __init__(self, screen: pygame.display, x: int = 0, y: int = 0):
        self._x = x
        self._y = y
        self._screen = screen
        self._font = pygame.font.Font('font/OpenSans-Regular.ttf', 12)

    def draw(self) -> None:
        text = self._font.render("?", False, (0,0,0))
        self._screen.blit(text, [self._x, self._y])


class VesselIcon(Icon):
    def __init__(self, screen: pygame.display, x: int, y: int, vessel: Vessel) -> None:
        Icon.__init__(self, screen, x, y)
        self._vessel = vessel

    def draw(self) -> None:
        max_liquid = self._vessel.getMax()
        color = self._vessel.getColour()
        distance = (50/100)*(self._vessel.getFluidAmount() / (max_liquid/100))
        pygame.draw.rect(self._screen, (color*2.55, 0, 255-color*2.55), [self._x, self._y+51-distance, 50, distance])
        pygame.draw.lines(self._screen, (0, 0, 0), False, [(self._x, self._y), (self._x, self._y+50), (self._x+50, self._y+50), (self._x+50, self._y)],2)


class HeaterIcon(Icon):
    def __init__(self, screen: pygame.display, x: int, y: int, heater: callable) -> None:
        Icon.__init__(self, screen, x, y)
        self._heater = heater

    def draw(self) -> None:
        pygame.draw.line(self._screen, (0, 0, 0), [self._x, self._y], [self._x+50, self._y], 4)
        if self._heater():
            x = self._x + 2
            for i in range(6):
                pygame.draw.lines(self._screen, (0,0,0), True, [(x, self._y-2), (x+3, self._y-6), (x+6, self._y-2)], 2)
                x += 8


class SensorIcon(Icon):
    def __init__(self, screen: pygame.display, x: int, y: int, readValue: Callable, unit: str, name: str) -> None:
        Icon.__init__(self, screen, x, y)
        self._name = name
        self.readValue = readValue
        self.unit = unit

    def draw(self) -> None:
        name = self._name + ":"
        value = str(self.readValue()) + " / " + self.unit
        nameLabel = self._font.render(name, False, (0,0,0))
        self._screen.blit(nameLabel, [self._x, self._y])
        valueLabel = self._font.render(value, False, (0,0,0))
        self._screen.blit(valueLabel, [self._x+85, self._y])
