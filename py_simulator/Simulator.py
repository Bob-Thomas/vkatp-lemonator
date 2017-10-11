# uncompyle6 version 2.12.0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Nov 17 2016, 17:05:23)
# [GCC 5.4.0 20160609]
# Embedded file name: .\Simulator.py
# Compiled at: 2017-08-30 16:00:41
# Size of source mod 2**32: 3405 bytes
from Controller import Controller
from Vessel import Vessel, MixtureVessel
from Sensor import *
from Effector import *
from Constants import *
from Gui import GUI
from typing import Dict
import time

from simulator_interface.lemonator import Lemonator


class Plant:

    def __init__(self, effectors, sensors, display):
        self._vessels = {'mix': MixtureVessel(
            amount=0, temperature=0, colour=0)}
        self._vessels['a'] = Vessel(
            colour=0, amount=liquidMax, flowTo=self._vessels['mix'])
        self._vessels['b'] = Vessel(
            colour=100, amount=liquidMax, flowTo=self._vessels['mix'])

        self._display = display

        self._sensors = sensors
        self._effectors = effectors

    def update(self) -> None:
        for vessel in self._vessels.values():
            vessel.update()

        for sensor in self._sensors.values():
            sensor.update(self._vessels['mix'])

        self._effectors['heater'].update(self._vessels['mix'])

        self._effectors['water_pump'].update(self._vessels['a'])
        self._effectors['water_valve'].update(self._vessels['a'])

        self._effectors['sirup_pump'].update(self._vessels['b'])
        self._effectors['sirup_valve'].update(self._vessels['b'])

        self._effectors['led_yellow'].update()
        self._effectors['led_green'].update()


    def printState(self) -> None:
        for sensor in self._sensors.values():
            print('type:', type(sensor), 'value:',
                  sensor.readValue(), '->', sensor.measure())

        for effector in self._effectors.values():
            print('type:', type(effector), 'value:',
                  'on' if effector.isOn() else 'off')


class Simulator:

    def __init__(self, gui: bool=False, lemonator: Lemonator = None):
        self.__Simulator__lemonator = lemonator
        self.__Simulator__sensors = {
            'keypad': self.__Simulator__lemonator.keypad,
            'distance': self.__Simulator__lemonator.distance,
            'color': self.__Simulator__lemonator.color,
            'temperature': self.__Simulator__lemonator.temperature,
            'reflex': self.__Simulator__lemonator.reflex
        }

        self.__Simulator__effectors = {
            'water_pump': self.__Simulator__lemonator.water_pump,
            'water_valve': self.__Simulator__lemonator.water_valve,
            'sirup_pump': self.__Simulator__lemonator.sirup_pump,
            'sirup_valve': self.__Simulator__lemonator.sirup_valve,
            'led_green': self.__Simulator__lemonator.led_green,
            'led_yellow': self.__Simulator__lemonator.led_yellow,
            'heater': self.__Simulator__lemonator.heater,
        }

        self._Simulator__plant = Plant( self.__Simulator__effectors, self.__Simulator__sensors, self.__Simulator__lemonator.lcd)
        self._Simulator__controller = Controller(self.__Simulator__lemonator)
        self._Simulator__monitor = Monitor(
            self.__Simulator__sensors, self.__Simulator__effectors)
        if gui:
            self._Simulator__gui = GUI(
                self._Simulator__plant, self._Simulator__controller, self._Simulator__monitor)
        else:
            self._Simulator__gui = None

    def run(self) -> None:
        if self._Simulator__gui is None:
            timestamp = 0
            while True:
                timestamp += 1
                time.sleep(1)
                print(timestamp, '-' * 40)
                self._Simulator__plant.update()
                self._Simulator__controller.update()
                self._Simulator__plant.printState()

        else:
            self._Simulator__gui.run()


class Monitor:

    def __init__(self, sensors: Dict[str, Sensor],
                 effectors: Dict[str, Effector]):
        self._Monitor__sensors = sensors
        self._Monitor__effectors = effectors
        self._sensorReadings = {}
        self._effectorValues = {}
        for sensor in self._Monitor__sensors:
            self._sensorReadings[sensor] = []

        for effector in self._Monitor__effectors:
            self._effectorValues[effector] = []

    def update(self) -> None:
        for sensor in self._Monitor__sensors:
            self._sensorReadings[sensor].append(
                self._Monitor__sensors[sensor].readValue())

        for effector in self._Monitor__effectors:
            self._effectorValues[effector].append(
                self._Monitor__effectors[effector].isOn())


if __name__ == '__main__':
    simulator = Simulator(True)
    simulator.run()
