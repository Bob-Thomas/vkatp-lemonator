from .sensor_proxies import *
from .output_proxies import *


class lcd_proxy():
    def __init__(self):
        pass

    def putc(self, c):
        pass


class Lemonator():
    def __init__(self):
        self.water_pump = Pump()
        self.water_valve = output_proxy()
        self.sirup_pump = Pump()
        self.sirup_valve = output_proxy()
        self.led_green = output_proxy()
        self.led_yellow = output_proxy()
        self.heater = Heater()

        self.keypad = sensor_proxy()
        self.distance = distance_sensor()
        self.color = color_sensor()
        self.temperature = temperature_sensor()
        self.reflex = sensor_proxy()

        self.lcd = lcd_proxy()
