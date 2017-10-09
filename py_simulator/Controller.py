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


class Controller:

    def __init__(self, lemonator):
        self.lemonator = lemonator

    def update(self) -> None:
        if self.lemonator.temperature.read_mc() + tempReaction < tempSetPoint:
            self.lemonator.heater.set(1)
        if self.lemonator.temperature.read_mc() + tempReaction > tempSetPoint:
            self.lemonator.heater.set(0)
        if self.lemonator.distance.read_mm() + levelReaction < levelSetPoint:
            if self.lemonator.color.read_rgb() < colourSetPoint:
                self.lemonator.sirup_pump.set(1)
            else:
                self.lemonator.water_pump.set(1)
        elif self.lemonator.distance.read_mm() + levelReaction > levelSetPoint:
            self.lemonator.water_pump.set(0)
            self.lemonator.sirup_pump.set(0)
