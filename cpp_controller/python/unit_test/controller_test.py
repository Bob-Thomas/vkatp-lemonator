import sys
sys.path.insert(0, '../')
from Vessel import *
import unittest
import io
from Simulator import Simulator, Plant
from simulator_interface.lemonator import Lemonator
from Controller import Controller, States
from functools import wraps
import time


class ControllerTest(unittest.TestCase):

    def setUp(self):
        self.lemonator = Lemonator()
        self.lemonator.lcd << "\f"
        self.controller = Controller(self.lemonator)
        self.plant = Plant(self.controller.lemonator,
                           self.controller.lemonator.lcd)

    def test_init_controller(self):
        self.assertEqual(self.controller.state, States.START)
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         0]), '     Lemonator v1.0 ')
        self.assertEqual(self.controller.get_lemonator(), self.lemonator)

    def test_init_with_cup(self):
        self.controller = Controller(self.lemonator)
        self.controller.lemonator.reflex._value = 1
        self.controller.update()
        self.assertEqual(self.controller.state, States.CUP_PRESENT)
        self.controller.update()
        self.assertEqual(self.controller.state, States.WAITING_FOR_INPUT)
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         0]), '     Lemonator v1.0 ')
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         1]), 'Use keypad to start ')

    def test_init_without_cup(self):
        self.controller = Controller(self.lemonator)
        self.controller.lemonator.reflex._value = 0
        self.controller.update()
        self.assertEqual(self.controller.state, States.NO_CUP)
        self.controller.update()
        self.assertEqual(self.controller.lemonator.led_green.get(), False)
        self.assertEqual(self.controller.lemonator.water_pump.get(), False)
        self.assertEqual(self.controller.lemonator.water_valve.get(), True)
        self.assertEqual(self.controller.lemonator.sirup_pump.get(), False)
        self.assertEqual(self.controller.lemonator.sirup_valve.get(), True)
        self.assertEqual(self.controller.temp_distance, empty_cup)
        self.assertEqual(self.controller.state, States.WAITING_FOR_CUP)
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         0]), '     Lemonator v1.0 ')
        self.controller.update()
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         1]), 'Please insert cup   ')

    def test_insert_cup(self):
        self.controller = Controller(self.lemonator)
        self.controller.lemonator.reflex._value = 0
        self.controller.update()
        self.assertEqual(self.controller.state, States.NO_CUP)
        self.controller.update()
        self.assertEqual(self.controller.lemonator.led_green.get(), False)
        self.assertEqual(self.controller.lemonator.water_pump.get(), False)
        self.assertEqual(self.controller.lemonator.water_valve.get(), True)
        self.assertEqual(self.controller.lemonator.sirup_pump.get(), False)
        self.assertEqual(self.controller.lemonator.sirup_valve.get(), True)
        self.assertEqual(self.controller.temp_distance, empty_cup)
        self.assertEqual(self.controller.state, States.WAITING_FOR_CUP)
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         0]), '     Lemonator v1.0 ')
        self.controller.update()
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         1]), 'Please insert cup   ')

        self.controller.lemonator.reflex._value = 1
        self.controller.update()
        self.assertEqual(self.controller.state, States.CUP_PRESENT)
        self.controller.update()
        self.assertEqual(self.controller.state, States.WAITING_FOR_INPUT)
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         0]), '     Lemonator v1.0 ')
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         1]), 'Use keypad to start ')

    def test_wait_for_keypad_cup_removed(self):
        self.controller.lemonator.reflex._value = 1
        self.controller.update()
        self.controller.update()
        self.assertEqual(self.controller.state, States.WAITING_FOR_INPUT)
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         0]), '     Lemonator v1.0 ')
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         1]), 'Use keypad to start ')

        self.controller.lemonator.reflex._value = 0
        self.controller.update()
        self.assertEqual(self.controller.state, States.NO_CUP)

    def test_wait_for_keypad(self):
        self.controller.lemonator.reflex._value = 1
        self.controller.update()
        self.controller.update()
        self.assertEqual(self.controller.state, States.WAITING_FOR_INPUT)
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         0]), '     Lemonator v1.0 ')
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         1]), 'Use keypad to start ')
        self.controller.update()
        self.controller.update()
        self.controller.update()
        self.controller.lemonator.keypad.putc("a")
        self.controller.update()
        self.assertEqual(self.controller.state, States.MIXING)

    def test_mix_interupt(self):
        self.controller.lemonator.reflex._value = 1
        self.controller.changeState(States.MIXING)
        self.controller.update()
        self.controller.update()
        self.controller.update()
        self.controller.update()
        self.controller.lemonator.reflex._value = 0
        self.controller.update()
        self.assertEqual(self.controller.state, States.NO_CUP)

    def test_mixing_flow(self):
        self.controller = Controller(self.lemonator)
        self.plant._vessels['mix'].empty()
        self.plant.update()
        self.controller.update()
        self.controller.update()
        self.assertEqual(self.controller.state, States.WAITING_FOR_INPUT)
        self.controller.lemonator.keypad.putc('A')
        self.controller.update()
        self.assertEqual(self.controller.state, States.MIXING)
        while True:
            if self.controller.state == States.MIX_DONE:
                break
            self.controller.update()
            self.plant.update()
        self.assertAlmostEqual(
            self.plant._vessels['mix'].getFluidAmount(), expected_fill, delta=1)

        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         0]), '     Lemonator v1.0 ')
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
                         2]), ' Please take.       ')
        self.assertEqual(''.join(self.controller.lemonator.lcd.get_text()[
            3]), ' And Enjoy! :3      ')
        self.plant._vessels['mix'].empty()
        self.controller.update()
        self.plant.update()
        self.controller.update()
        self.assertEqual(self.controller.state, States.START)
