import sys
sys.path.insert(0, '../')
from Vessel import *
from unittest import *
from unittest.mock import *
import io
from Simulator import Simulator, Plant
from simulator_interface.lemonator import Lemonator
from Controller import Controller
from functools import wraps
import time


class PlantTest(TestCase):

    def setUp(self):
        self.lemonator = Lemonator()
        self.plant = Plant(self.lemonator, self.lemonator.lcd)

    def test_plant(self):
        self.assertEqual(self.plant._vessels['mix'].getFluidAmount(), 0)
        self.assertEqual(
            self.plant._vessels['a'].getFluidAmount(), full_vessel)
        self.assertEqual(
            self.plant._vessels['b'].getFluidAmount(), full_vessel)

        self.plant.update()
        with patch.object(self.plant._vessels['mix'], 'heat') as heater:
            self.plant._lemonator.heater.set(1)
            self.plant.update()
            heater.assert_called_once()

        self.plant._lemonator.sirup_pump.set(1)
        self.plant._lemonator.sirup_valve.set(0)
        self.plant.update()
        self.assertEqual(
            self.plant._vessels['a'].getFluidAmount(), full_vessel - flowRate)
        self.assertEqual(
            self.plant._vessels['mix'].getFluidAmount(), flowRate)
        self.plant._lemonator.sirup_pump.set(0)
        self.plant._lemonator.sirup_valve.set(1)
        self.plant.update()
        self.assertEqual(
            self.plant._vessels['a'].getFluidAmount(), full_vessel - flowRate)
        self.assertEqual(
            self.plant._vessels['mix'].getFluidAmount(), flowRate)

        self.plant._lemonator.water_pump.set(1)
        self.plant._lemonator.water_valve.set(0)
        self.plant.update()
        self.assertEqual(
            self.plant._vessels['b'].getFluidAmount(), full_vessel - flowRate)
        self.assertEqual(
            self.plant._vessels['mix'].getFluidAmount(), flowRate * 2)
        self.plant._lemonator.water_pump.set(0)
        self.plant._lemonator.water_valve.set(1)
        self.plant.update()
        self.assertEqual(
            self.plant._vessels['b'].getFluidAmount(), full_vessel - flowRate)
        self.assertEqual(
            self.plant._vessels['mix'].getFluidAmount(), flowRate * 2)
