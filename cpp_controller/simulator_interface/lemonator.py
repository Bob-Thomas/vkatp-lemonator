from .sensor_proxies import *
from .output_proxies import *


class lcd_proxy():
    def __init__(self):
        pass

    def putc(self, c):
        pass

class Lcd(lcd_proxy):
    _text  = ['                    '] * 4
    index = [0,0]
    position_state = False
    def __init__(self):
        lcd_proxy.__init__(self)

    def putc(self, c):
        if self.position_state == 'x':
            self.index[0] = c
            self.position_state = 'xx'
            return
        if self.position_state == 'xx':
            self.index[0] = int(str(self.index[0]) + c)
            self.position_state = 'y'
            return
        if self.position_state == 'y':
            self.index[1] = c
            self.position_state = 'yy'
            return
        if self.position_state == 'yy':
            self.index[1] = int(str(self.index[1]) + c)
            self.position_state = False
            print(self.index)
            return
        if c == '\f':
            self._text = ['                    '] * 4
            self.index = [0,0]
            return
        if c == '\n':
            self.index = [self.index[0]+1,0]
            return
        if c == '\r':
            self.index = [self.index[0], 0]
            return
        if c == '\t':
            self.position_state = 'x'
            return
        if c:
            new_text = list(self._text[self.index[0]])
            new_text[self.index[1]]  = c
            try:
                self.index[1] += 1
                self._text[self.index[0]] = new_text
            except IndexError as e:
                print("index out of range")



    def __lshift__(self, other):
        for i in other:
            self.putc(i)

    def get_text(self):
        return self._text

class Keypad(sensor_proxy):
    _input = "\0"
    def __init__(self):
        sensor_proxy.__init__(self)

    def getc(self):
        v = self._input
        self._input = "\0"
        return v

    def putc(self, v):
        self._input = v


class Lemonator():
    def __init__(self):
        self.water_pump = output_proxy()
        self.water_valve = output_proxy()
        self.sirup_pump = output_proxy()
        self.sirup_valve = output_proxy()
        self.led_green = output_proxy()
        self.led_yellow = output_proxy()
        self.heater = output_proxy()

        self.keypad = Keypad()
        self.distance = distance_sensor()
        self.color = color_sensor()
        self.temperature = temperature_sensor()
        self.reflex = sensor_proxy()

        self.lcd = Lcd()
