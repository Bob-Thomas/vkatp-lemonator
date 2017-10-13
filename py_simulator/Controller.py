# uncompyle6 version 2.12.0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Nov 17 2016, 17:05:23)
# [GCC 5.4.0 20160609]
# Embedded file name: .\Controller.py
# Compiled at: 2017-08-29 16:53:26
# Size of source mod 2**32: 1554 bytes
from Effector import Effector
from Sensor import Sensor, TemperatureSensor, LevelSensor, ColourSensor
from Constants import *
from typing import Dict
import time
from enum import Enum
class States(Enum):
    START = 0
    NO_CUP = 1
    CUP_PRESENT = 2
    WAITING_FOR_INPUT = 3
    WAITING_FOR_CUP = 4
    STARTING_MIX = 5
    MIXING = 6
    MIX_DONE = 7
    ERROR = 8
from ctypes import cdll, c_char_p
class Controller:

    def __init__(self, lemonator):
        self.lemonator = lemonator
        self.state = States.START
        penis = "      Lemonator V1.0\n\n"
        self.lemonator.lcd << penis

    def update(self) -> None:
        if self.state == States.START:
            self.clear_display()
            if self.lemonator.reflex.get():
                self.state = States.CUP_PRESENT
            else:
                self.state = States.NO_CUP

        if self.state == States.MIXING and not self.lemonator.reflex.get():
            self.state = States.NO_CUP

        if self.state == States.CUP_PRESENT:
            self.lemonator.lcd << "\r Use keypad to start"
            self.lemonator.led_green.set(1)
            self.state = States.WAITING_FOR_INPUT
        if self.state == States.NO_CUP:
            self.lemonator.lcd << "\r Please insert cup  "
            self.lemonator.led_green.set(0)
            self.state = States.WAITING_FOR_CUP

        if self.state == States.WAITING_FOR_CUP:
            if self.lemonator.reflex.get():
                self.state = States.CUP_PRESENT

        if self.state == States.WAITING_FOR_INPUT:
            if not self.lemonator.reflex.get():
                self.state = States.NO_CUP
                return
            value = self.lemonator.keypad.getc()
            if not value is '\0':
                print('beep boop')
                self.state = States.STARTING_MIX
                return

        if self.state == States.STARTING_MIX:
            self.lemonator.lcd << "\r      Mix starting  \n"
            self.state = States.MIXING

        if self.state == States.MIX_DONE:
            self.lemonator.lcd << "\r" + ''.join([" " for x in range(1, 21)])
            self.lemonator.lcd << "\t0103 Please take cup."
            self.lemonator.lcd << "\t0203 Enjoy!"
            if not self.lemonator.reflex.get():
                self.state = States.START

        if self.state == States.MIXING:
            if self.lemonator.distance.read_mm() > full_cup-10:
                self.disable_pumps()
                self.state = States.MIX_DONE
                return
            else:
                if self.lemonator.distance.read_mm() < required_sirup_in_mm:
                    self.set_water_pump(0)
                    self.set_sirup_pump(1)
                else:
                    self.set_water_pump(1)
                    self.set_sirup_pump(0)
            distance = round((20/100)*(self.lemonator.distance.read_mm() / ((full_cup - 10)/100)))
            print(distance)
            self.lemonator.lcd << "\r" + ''.join([str('#') for x in range(1, distance)])

    def disable_pumps(self) -> None:
        self.set_sirup_pump(0)
        self.set_water_pump(0)

    def set_water_pump(self, v) -> None:
        self.lemonator.water_valve.set(not v)
        self.lemonator.water_pump.set(v)

    def set_sirup_pump(self, v) -> None:
        self.lemonator.sirup_valve.set(not v)
        self.lemonator.sirup_pump.set(v)

    def clear_display(self):
        self.lemonator.lcd << "\f      Lemonator V1.0\n\n"
