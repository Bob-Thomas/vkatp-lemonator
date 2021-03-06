# uncompyle6 version 2.12.0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Nov 17 2016, 17:05:23)
# [GCC 5.4.0 20160609]
# Embedded file name: .\Vessel.py
# Compiled at: 2017-08-29 15:46:48
# Size of source mod 2**32: 2437 bytes
from Constants import *


class Vessel:
    """ Class to describe containers of liquids;
    two types:
    - Storage vessels (generic type, attached with effectors, no sensors)
    - Mixture vessel (has a tap, attached with only heater effector, all types of sensors).
    """

    def __init__(self, amount=3000, max_liquid=full_vessel, colour=0, temperature=20, flowTo=None):
        self._amount = amount
        self._colour = colour
        self._temperature = temperature
        self._flowTo = flowTo
        self._max_liquid = max_liquid

    def getMax(self):
        return self._max_liquid

    def getFluidAmount(self):
        return self._amount

    def getColour(self):
        return self._colour

    def getTemperature(self):
        return self._temperature

    def flow(self):
        """Moves one (measurement defined in Constants) amount of liquid to the vessel connected to this vessel"""
        amount = flowRate
        if flowRate > self._amount:
            amount = self._amount
        self._amount -= amount
        if self._flowTo != None:
            self._flowTo.flowIn(amount, self._colour)

    def flowIn(self, amount, colour):
        if self._amount + flowRate > self._max_liquid:
            print('ERROR', 'overflow occuring in', type(self))
        else:
            self._colour = (self._colour * self._amount +
                            colour * amount) / (self._amount + amount)
            self._amount += amount

    def update(self):
        """Periodically called method to update the state of the vessel"""
        pass


class MixtureVessel(Vessel):
    """ Mixture extensions to Vessel
    - heat(True/False) (increases water temperature)
    """

    def __init__(self, amount=0, max_liquid=full_cup, colour=0, temperature=20):
        Vessel.__init__(self, amount, max_liquid, colour, temperature)
        self._heat = False
        self._present = 0

    def heat(self, state=False):
        # No more heat only lemonate
        pass

    def empty(self):
        self._present = not self._present
        self._amount = 0

    def update(self):
        """
        Updates the state of the mixture vessel depending on the state of the effectors.
        constants (flowRate, heatRate, temperatureDecay) defined in Constants.py
        """
        pass

        # No more heat only lemonate
        # if self._heat:
        #     self._temperature += heatRate
        # elif self._temperature > environmentTemp:
        #     self._temperature -= temperatureDecay
