from Vessel import Vessel, MixtureVessel
from Constants import *

class Effector:
    def __init__(self):
        self._value = False

    def switchOn(self) -> None:
        self._value = True

    def switchOff(self) -> None:
        self._value = False

    def isOn(self) -> float:
        return self._value

    def update(self, vessel=None) -> None:
        pass

class output_proxy(Effector):
    def __init__(self):
        Effector.__init__(self)

    def set(self, v):
        Effector.switchOn(self) if v else Effector.switchOff(self)

    def get(self):
        return self._value



class Pump(output_proxy):
    def __init__(self):
        output_proxy.__init__(self)
        self._pressure = 0

    def update(self, vessel):
        if self._pressure > 100 and vessel != None:
            vessel.flow()
        if self.get():
            self._pressure = min(self._pressure + 100 / pressureRampUp, 100)
            if self._pressure == 100:
                self._pressure = 200
        else:
            self._pressure = max(self._pressure - 100 / pressureRampDown, 0)


class Heater(output_proxy):
    def update(self, vessel) -> None:
        if self.get():
            vessel.heat(True)
        else:
            vessel.heat(False)
