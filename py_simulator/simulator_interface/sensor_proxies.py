from Constants import *
from Vessel import Vessel, MixtureVessel
from math import pi
import random

class Sensor:
    def __init__(self):
        self._value = 0
        self._unitOfMeasure = ''

    def update(self, vessel=None) -> None:
        pass

    def readValue(self) -> float:
        return round(self._value, 2)

    def measure(self) -> str:
        return str(self._convertToValue()) + self._unitOfMeasure

    def _convertToValue(self) -> float:
        return round(self._value, 2)


class sensor_proxy(Sensor):
    def __init__(self):
        Sensor.__init__(self)

    def read_mc(self):
        return self.readValue()

    def read_mm(self):
        return self.readValue()

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
        temperature = vessel.getTemperature()
        self._value = temperature * tempConversion

    def _convertToValue(self) -> float:
        return round(self._value / tempConversion, 2)


class color_sensor(sensor_proxy):
    def __init__(self):
        sensor_proxy.__init__(self)
        self._unitOfMeasure = '%'

    def update(self, vessel) -> None:
        if type(vessel) != None:
            colour = vessel.getColour()
            self._value = colour * colourConversion

    def _convertToValue(self) -> float:
        return round(self._value / colourConversion, 2)


class distance_sensor(sensor_proxy):
    temp = 88
    def __init__(self):
        Sensor.__init__(self)
        self._unitOfMeasure = 'mm'

    def update(self, vessel) -> None:
        if type(vessel) != None:
            if random.randrange(9000) % 9 == 2:
                self._value = random.randint(round(self._value)-200, round(self._value)+200)
            else:
              self._value = 88-vessel.getFluidAmount()

    def _convertToValue(self) -> float:
        return round(self._value / levelConversion * pi * 10 * 10, 2)
