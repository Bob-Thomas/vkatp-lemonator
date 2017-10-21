import sys
sys.path.insert(0, '../')

from Constants import *
from Vessel import Vessel, MixtureVessel
from math import pi
import random


class Sensor:
    def __init__(self):
        self._value = 0
        self._unitOfMeasure = ''

    def update(self, vessel):
        if vessel._present:
            self._value = 1
        else:
            self._value = 0

    def readValue(self) -> int:
        return round(self._value)


class sensor_proxy(Sensor):
    def __init__(self):
        Sensor.__init__(self)

    def read_mc(self):
        return self.readValue()

    def read_mm(self):
        return int(self.readValue())

    def read_rgb(self):
        return self.readValue()

    def getc(self):
        pass

    def get(self):
        return self.readValue()


class temperature_sensor(sensor_proxy):
    def __init__(self):
        sensor_proxy.__init__(self)
        self._unitOfMeasure = '°C'

    def update(self, vessel):
        pass
        # temperature = vessel.getTemperature()
        # self._value = int(temperature * tempConversion)


class color_sensor(sensor_proxy):
    def __init__(self):
        sensor_proxy.__init__(self)
        self._unitOfMeasure = '%'

    def update(self, vessel) -> None:
        pass


class distance_sensor(sensor_proxy):
    temp = 88

    def __init__(self):
        Sensor.__init__(self)
        self._unitOfMeasure = 'mm'

    def update(self, vessel) -> None:
        if random.randrange(9000) % 9 == 2:
            self._value = random.randint(
                round(self._value) - 20, round(self._value) + 20)
        else:
            self._value = 88 - vessel.getFluidAmount()
