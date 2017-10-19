# uncompyle6 version 2.12.0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Nov 17 2016, 17:05:23)
# [GCC 5.4.0 20160609]
# Embedded file name: .\Controller.py
# Compiled at: 2017-08-29 16:53:26
# Size of source mod 2**32: 1554 bytes
import time
from enum import Enum
from typing import Dict

from Constants import diff_liquids, empty_cup, expected_fill, full_cup, required_sirup_in_mm


class States(Enum):
    START = 0
    NO_CUP = 1
    CUP_PRESENT = 2
    WAITING_FOR_INPUT = 3
    WAITING_FOR_CUP = 4
    MIXING = 5
    MIX_DONE = 6
    ERROR = 7


class Controller:
    temp_distance = empty_cup

    def __init__(self, lemonator):
        self.lemonator = lemonator
        self.changeState(States.START)

    def changeState(self, state: States):
        self.state = state
        self.update_display()

    def update_display(self):
        self.lemonator.lcd << "\t0000"
        for i in range(4):
            self.lemonator.lcd << ' '.join([''] * 20)
            if i < 3:
                self.lemonator.lcd << "\n"
        self.lemonator.lcd << "\t0000     Lemonator v1.0\n"

        if self.state == States.WAITING_FOR_CUP:
            self.lemonator.lcd << "\r Please insert cup  "
        elif self.state == States.CUP_PRESENT or self.state == States.WAITING_FOR_INPUT:
            self.lemonator.lcd << "\r Use keypad to start"
        elif self.state == States.MIXING:
            distance = round((100 / 100) * (empty_cup -
                                            self.distance_filter()) / diff_liquids * 100) or 0
            self.lemonator.lcd << "\r      Mix starting  \n"
            self.lemonator.lcd << "\r              " + str(distance) + "%"
        elif self.state == States.MIX_DONE:
            self.lemonator.lcd << "\t0103 Please take."
            self.lemonator.lcd << "\t0203 And Enjoy! :3"

    def update(self) -> None:
        if self.state == States.START:
            if self.lemonator.reflex.get():
                self.changeState(States.CUP_PRESENT)
            else:
                self.changeState(States.NO_CUP)

        if self.state == States.MIXING and not self.lemonator.reflex.get():
            self.changeState(States.NO_CUP)

        if self.state == States.CUP_PRESENT:
            self.changeState(States.WAITING_FOR_INPUT)
            self.lemonator.led_green.set(1)

        if self.state == States.NO_CUP:
            self.changeState(States.WAITING_FOR_CUP)
            self.lemonator.led_green.set(0)
            self.disable_pumps()
            self.temp_distance = 88

        if self.state == States.WAITING_FOR_CUP:
            if self.lemonator.reflex.get():
                self.changeState(States.CUP_PRESENT)

        if self.state == States.WAITING_FOR_INPUT:
            if not self.lemonator.reflex.get():
                self.changeState(States.NO_CUP)
                return
            value = self.lemonator.keypad.getc()
            if not value is '\0':
                self.changeState(States.MIXING)
                return

        if self.state == States.MIX_DONE:
            if not self.lemonator.reflex.get():
                self.changeState(States.START)

        if self.state == States.MIXING:
            self.update_display()
            if self.distance_filter() < expected_fill:
                self.disable_pumps()
                self.changeState(States.MIX_DONE)
                return
            else:
                if self.distance_filter() > required_sirup_in_mm:
                    self.set_water_pump(0)
                    self.set_sirup_pump(1)
                else:
                    self.set_water_pump(1)
                    self.set_sirup_pump(0)

    """
    Simple implementation of a exponential moving average
    with a alpha of 0.8
    """

    def distance_filter(self, alpha=0.8):
        value = float(self.lemonator.distance.read_mm())
        if value > empty_cup:
            value = empty_cup
        if value > self.temp_distance:
            return self.temp_distance
        if self.temp_distance - value > 3:
            return self.temp_distance
        self.temp_distance = self.temp_distance * alpha + value * (1 - alpha)
        return self.temp_distance

    def disable_pumps(self) -> None:
        self.set_sirup_pump(0)
        self.set_water_pump(0)

    def set_water_pump(self, v) -> None:
        self.lemonator.water_valve.set(not v)
        self.lemonator.water_pump.set(v)

    def set_sirup_pump(self, v) -> None:
        self.lemonator.sirup_valve.set(not v)
        self.lemonator.sirup_pump.set(v)

    def get_lemonator(self):
        return self.lemonator
