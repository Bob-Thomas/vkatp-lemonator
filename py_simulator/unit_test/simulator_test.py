__author__ = 'robbie'

from Vessel import *
from unittest import *
import Simulator
import io

class SimulatorInterfaceTest(object):
    def test_function(self):
        pass

sit = SimulatorInterfaceTest()
suite = TestLoader().loadTestsFromModule(sit)
TextTestRunner().run(suite)