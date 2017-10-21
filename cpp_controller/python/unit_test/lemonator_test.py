__author__ = 'robbie'
import sys
sys.path.insert(0, '../')
from Vessel import *
import unittest
import unittest.mock
from simulator_interface import output_proxies, lemonator, sensor_proxies
import io
from contextlib import redirect_stdout


class LemonatorInterfaceTest(unittest.TestCase):

    def setUp(self):
        self.lemonator = lemonator.Lemonator()
        self.vessel = MixtureVessel(amount=45, max_liquid=45)

    def tearDown(self):
        self.lemonator = None
        self.vessel = None

    def test_sensor(self):
        sensor = lemonator.Sensor()
        sensor._value = 20
        self.assertEqual(sensor.readValue(), 20,
                         "Read value should return _value")

    def test_sensor_proxy(self):
        sensor = lemonator.sensor_proxy()
        sensor._value = 20
        self.assertEqual(sensor.read_mc(), 20,
                         "Read value should return _value")
        self.assertEqual(sensor.read_mm(), 20,
                         "Read value should return _value")
        self.assertEqual(sensor.read_rgb(), 20,
                         "Read value should return _value")

    def test_output_proxies(self):
        # Get all the output proxies in list.
        self.outputProxies = filter(lambda x: isinstance(
            x, output_proxies.output_proxy), vars(self.lemonator).values())
        # Test all output proxies.
        for output_proxy in self.outputProxies:
            # Set signal on.
            output_proxy.set(1)
            # Check if signal turned on.
            self.assertEqual(1, output_proxy.get())
            # Set signal off.
            output_proxy.set(0)
            # Check if signal turned off.
            self.assertEqual(0, output_proxy.get())

    def test_keypad(self):
        # Get the keypad instance from Lemonator.
        self.keypad = self.lemonator.keypad
        # Check default return value (zero terminator).
        self.assertEqual('\0', self.keypad.getc())
        # Put character to keyboard.
        self.keypad.putc('1')
        # Get character from keyboard.
        self.assertEqual('1', self.keypad.getc())

    @unittest.mock.patch('random.randrange', lambda x: 0)
    def test_distance_sensor_no_spike(self):
        # Get the distance (sensor) from Lemonator.
        self.distance_sensor = self.lemonator.distance
        # Check for default value.
        self.assertEqual(0, self.distance_sensor.read_mm())
        # Update once with a vessel object that contains 45 mm liquid.
        self.distance_sensor.update(self.vessel)
        # Check if distance sensor read succesfully.
        # 88 mm is the space between distance sensor and cup.
        # 45 mm is the amount of liquid in the cup.
        self.assertEqual(88 - 45, self.distance_sensor.read_mm())

    @unittest.mock.patch('random.randrange', lambda x: 2)
    @unittest.mock.patch('random.randint', lambda x, y: 666)
    def test_distance_sensor_with_spike(self):
        # Get the distance (sensor) from Lemonator.
        self.distance_sensor = self.lemonator.distance
        # Check for default value.
        self.assertEqual(0, self.distance_sensor.read_mm())
        # Update once with a vessel object that contains 45 mm liquid.
        self.distance_sensor.update(self.vessel)
        # Check if distance sensor read succesfully.
        # 88 mm is the space between distance sensor and cup.
        # 45 mm is the amount of liquid in the cup.
        self.assertEqual(666, self.distance_sensor.read_mm())

    def test_reflex_sensor(self):
        # Get the instance of the reflex sensor.
        self.reflex_sensor = self.lemonator.reflex
        # Check default value.
        self.assertEqual(0, self.reflex_sensor.get())
        # Update once with a vessel object.
        self.reflex_sensor.update(self.vessel)

        self.vessel._present = True

        self.reflex_sensor.update(self.vessel)

        self.assertEqual(1, self.reflex_sensor.get())

    def test_lcd_hello_world(self):
        # Get the LCD instance.
        lcd = self.lemonator.lcd
        # Check if the string stored in the lcd object
        lcd << "\rHello world. Hello w"
        self.assertEqual(
            ''.join(lcd.get_text()[
                0]), "Hello world. Hello w")
        # Lets create a overflow in the LCD. Check if the terminal print the "Out of range message."
        self.out = io.StringIO()
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fakeOutput:
            lcd << "\rHello world. Hello dd"
            self.assertEqual(fakeOutput.getvalue().strip(),
                             'Index out of range')

    def test_lcd_overflow(self):
        # Get the LCD instance.
        lcd = self.lemonator.lcd
        # Check if the string stored in the lcd object
        # Lets create a overflow in the LCD. Check if the terminal print the "Out of range message."
        self.out = io.StringIO()
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fakeOutput:
            lcd << "\rHello world. Hello dd"
            self.assertEqual(fakeOutput.getvalue().strip(),
                             'Index out of range')

    def test_lcd_position(self):
        # Get the LCD instance.
        lcd = self.lemonator.lcd

        lcd << "\t0101dave"
        self.assertEqual(''.join(lcd.get_text()[
                         1]), ' dave               ')

        lcd << "\t0002dave"
        self.assertEqual(''.join(lcd.get_text()[
                         2]), 'dave                ')

    def test_lcd_flush(self):
        # Get the LCD instance.
        lcd = self.lemonator.lcd
        lcd << "dave dave dave"
        self.assertEqual(''.join(lcd.get_text()[
                         0]), 'dave dave dave      ')
        lcd << "\f"

        self.assertEqual(lcd.get_text(), ['                    '] * 4)

    def test_lcd_home(self):
        # Get the LCD instance.
        lcd = self.lemonator.lcd
        lcd << "\fdave dave dave"
        self.assertEqual(''.join(lcd.get_text()[
                         0]), 'dave dave dave      ')
        lcd << "\rbob  bob  bob     "

        self.assertEqual(''.join(lcd.get_text()[
                         0]), 'bob  bob  bob       ')

    def test_lcd_newline(self):
            # Get the LCD instance.
        lcd = self.lemonator.lcd
        lcd << "\fdave dave dave"
        self.assertEqual(''.join(lcd.get_text()[
            0]), 'dave dave dave      ')
        lcd << "\nbob  bob  bob     "

        self.assertEqual(''.join(lcd.get_text()[
            1]), 'bob  bob  bob       ')
