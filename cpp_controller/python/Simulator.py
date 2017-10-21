# uncompyle6 version 2.12.0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Nov 17 2016, 17:05:23)
# [GCC 5.4.0 20160609]
# Embedded file name: .\Simulator.py
# Compiled at: 2017-08-30 16:00:41
# Size of source mod 2**32: 3405 bytes
from Vessel import Vessel, MixtureVessel
from Constants import *
from Gui import GUI
from typing import Dict
import time

from simulator_interface.lemonator import Lemonator


class Plant:

    def __init__(self, lemonator, display):
        self._vessels = {'mix': MixtureVessel(
            amount=0, temperature=0, colour=0)}
        self._vessels['a'] = Vessel(
            colour=100, amount=full_vessel, flowTo=self._vessels['mix'])
        self._vessels['b'] = Vessel(
            colour=0, amount=full_vessel, flowTo=self._vessels['mix'])

        self._display = display
        self._lemonator = lemonator

    def update(self) -> None:
        for vessel in self._vessels.values():
            vessel.update()

        self._lemonator.keypad.update(self._vessels['mix'])
        self._lemonator.distance.update(self._vessels['mix'])
        self._lemonator.color.update(self._vessels['mix'])
        self._lemonator.temperature.update(self._vessels['mix'])
        self._lemonator.reflex.update(self._vessels['mix'])

        if self._lemonator.heater.get():
            self._vessels['mix'].heat()

        if self._lemonator.sirup_pump.get() and not self._lemonator.sirup_valve.get():
            self._vessels['a'].flow()

        if self._lemonator.water_pump.get() and not self._lemonator.water_valve.get():
            self._vessels['b'].flow()


class Simulator:

    def __init__(self, gui: bool=False, controller=None):
        self.__Simulator__controller = controller
        self.__Simulator__lemonator = controller.get_lemonator()
        self.test = self.__Simulator__lemonator.keypad

        self._Simulator__plant = Plant(
            self.__Simulator__lemonator, self.__Simulator__lemonator.lcd)
        self._Simulator__monitor = Monitor(
            self.__Simulator__controller, self.__Simulator__lemonator)
        if gui:
            self._Simulator__gui = GUI(
                self._Simulator__plant, self.__Simulator__controller, self._Simulator__monitor)
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
                self.__Simulator__controller.update()
                self._Simulator__monitor.update()

        else:
            self._Simulator__gui.run()

    def step(self) -> None:
        self._Simulator__plant.update()
        self.__Simulator__controller.update()
        self._Simulator__plant.printState()
        self._Simulator__monitor.update()


class Monitor:

    def __init__(self,
                 controller,
                 lemonator: Lemonator):
        self._Monitor_controller = controller
        self._Monitor_lemonator = lemonator
        self._sensorReadings = {}
        self._effectorValues = {}
        self._sensorReadings['distance'] = []
        self._effectorValues['water_pump'] = []
        self._effectorValues['sirup_pump'] = []

    def update(self) -> None:
        self._sensorReadings['distance'].append(
            self._Monitor_controller.distance_filter()
        )

        self._effectorValues['water_pump'].append(
            self._Monitor_lemonator.water_pump.get()
        )
        self._effectorValues['sirup_pump'].append(
            self._Monitor_lemonator.sirup_pump.get()
        )
        self.print_state()

    def print_state(self) -> None:
        mergy = {**self._effectorValues, **self._sensorReadings}
        for i in range(len(self._sensorReadings['distance'])):
            print('%s -> %d | %s -> %d | %s -> %d' % (
                "Distance", self._sensorReadings['distance'][i],
                "Water pump", self._effectorValues['water_pump'][i],
                'Sirup pump', self._effectorValues['sirup_pump'][i])
            )
