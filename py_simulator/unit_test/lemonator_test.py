__author__ = 'robbie'

from Vessel import *
from unittest import *
from simulator_interface import output_proxies, lemonator, sensor_proxies
import io
from contextlib import redirect_stdout

class LemonatorInterfaceTest(TestCase):

    def test_output_proxies(self):
        # Get all the output proxies in list.
        self.outputProxies = filter(lambda x: isinstance(x, output_proxies.output_proxy), vars(lemonator.Lemonator()).values())
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
        self.keypad = lemonator.Lemonator().keypad
        # Check default return value (zero terminator).
        self.assertEqual('\0', self.keypad.getc())
        # Put character to keyboard.
        self.keypad.putc('1')
        # Get character from keyboard.
        self.assertEqual('1', self.keypad.getc())

    def test_distance_sensor(self):
        # Get the distance (sensor) from Lemonator.
        self.distance_sensor = lemonator.Lemonator().distance
        # Check for default value.
        self.assertEqual(0, self.distance_sensor.read_mm())
        # Update once with a vessel object that contains 45 mm liquid.
        self.distance_sensor.update(Vessel(amount=45, max_liquid=45))
        # Check if distance sensor read succesfully.
        # 88 mm is the space between distance sensor and cup
        # 45 mm is the amount of liquid in the cup
        self.assertEqual(88 - 45, self.distance_sensor.read_mm())

    def test_distance_sensor(self):
        # Get the distance (sensor) from Lemonator.
        self.distance_sensor = lemonator.Lemonator().distance
        # Check for default value.
        self.assertEqual(0, self.distance_sensor.read_mm())
        # Update once with a vessel object that contains 45 mm liquid.
        self.distance_sensor.update(Vessel(amount=45, max_liquid=45))
        # Check if distance sensor read succesfully.
        # 88 mm is the space between distance sensor and cup.
        # 45 mm is the amount of liquid in the cup.
        self.assertEqual(88 - 45, self.distance_sensor.read_mm())

    def test_reflex_sensor(self):
        # Get the instance of the reflex sensor.
        self.reflex_sensor = lemonator.Lemonator().reflex
        # Check default value.
        self.assertEqual(0, self.reflex_sensor.get())
        # Update once with a vessel object.
        self.reflex_sensor.update(Vessel(amount=45,max_liquid=45))

    def test_lcd(self):
        # Get the LCD instance.
        self.lcd = lemonator.Lemonator().lcd
        # Check if the string stored in the lcd object
        self.lcd << "\rHello world. Hello w"
        self.assertEqual(''.join(self.lcd.get_text()[0]), "\rHello world. Hello w")
        # Lets create a overflow in the LCD. Check if the terminal print the "Out of range message."
        self.out = io.StringIO()
        with redirect_stdout(self.out):
            self.lcd << "\rHello world. Hello we"
        output = self.out.getvalue()
        self.assertEqual(output, "out of range")

sit = LemonatorInterfaceTest()
suite = TestLoader().loadTestsFromModule(sit)
TextTestRunner().run(suite)