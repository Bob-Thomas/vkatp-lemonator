import sys
sys.path.insert(0, "../")
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


class output_proxy(Effector):
    def __init__(self):
        Effector.__init__(self)

    def set(self, v):
        Effector.switchOn(self) if v else Effector.switchOff(self)

    def get(self):
        return Effector.isOn(self)
