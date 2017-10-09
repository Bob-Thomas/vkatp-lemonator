import lemonator
import time

print( "Python interface demo running" )
hw = lemonator.lemonator( 2 )

class led_yellow():
    def __init__(self, led):
        self.led = led
    def set(self, v):
        self.led.set(v)

h = heater(hw.heater)

while 1:
    yellow.set(1)
    time.sleep(1)
    yellow.set(0)
    time.sleep(1)
