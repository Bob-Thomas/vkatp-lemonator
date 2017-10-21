import sys
sys.path.insert(0, '../')
from Vessel import *
from unittest import *
from unittest.mock import *
from Constants import *
import Simulator
import io


class VesselTest(TestCase):
    def setUp(self):
        self.mixer = MixtureVessel(amount=0, max_liquid=45)
        self.vessel = Vessel(colour=0, amount=full_vessel,
                             flowTo=self.mixer)

    # coverage life
    def test_getters(self):
        self.assertEqual(self.vessel.getMax(), full_vessel)
        self.assertEqual(self.vessel.getColour(), 0)
        self.assertEqual(self.vessel.getTemperature(), 20)
        self.assertEqual(self.vessel.getFluidAmount(), full_vessel)

    def test_vessel_flow(self):
        # flow into mixer
        self.assertEqual(self.vessel.getFluidAmount(), full_vessel)
        self.vessel.flow()
        self.assertEqual(self.vessel.getFluidAmount(), full_vessel - flowRate)
        self.assertEqual(self.mixer.getFluidAmount(), flowRate)

        # flow without vessel to flow to
        self.vessel = Vessel(colour=0, amount=full_vessel)
        self.vessel.flow()
        self.assertEqual(self.vessel.getFluidAmount(), full_vessel - flowRate)
        self.assertEqual(self.mixer.getFluidAmount(), flowRate)

        # empty vessel
        self.vessel = Vessel(colour=0, amount=0)
        self.vessel.flow()
        self.assertEqual(self.vessel.getFluidAmount(), 0)
        self.assertEqual(self.mixer.getFluidAmount(), flowRate)

    def test_mixer_flow_in(self):
        self.mixer = MixtureVessel(amount=0, max_liquid=1)
        self.vessel = Vessel(colour=0, amount=10,
                             flowTo=self.mixer)
        # flow into mixer
        self.assertEqual(self.vessel.getFluidAmount(), 10)
        with patch('sys.stdout', new=io.StringIO()) as fakeOutput:
            self.vessel.flow()
            self.vessel.flow()
            self.assertEqual(fakeOutput.getvalue().strip(),
                             'ERROR overflow occuring in %s' % str(type(self.mixer)))

    def test_empty_mixer(self):
        self.mixer = MixtureVessel(amount=40, max_liquid=50)
        self.assertEqual(self.mixer._present, 0)
        self.assertEqual(self.mixer.getFluidAmount(), 40)
        self.mixer.empty()
        self.assertEqual(self.mixer._present, 1)
        self.assertEqual(self.mixer.getFluidAmount(), 0)
