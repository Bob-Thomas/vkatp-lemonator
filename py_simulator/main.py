
# if __name__ == "__main__":
#     """Only perform actions when invoked directly!"""
#     from Simulator import Simulator
#     #import the lemonator interface library...

#     simulator = Simulator(True) # use Simulator(False) to disable the GUI
#     simulator.run()

from lemonator import lemonator as hw_lemonator
from simulator_interface.lemonator import Lemonator as sw_lemonator
from Simulator import Simulator
from Controller import Controller
import sys
import time

if __name__ == "__main__":
    sys.argv = sys.argv[1:]
    if len(sys.argv) < 1:
        print("Usage: python main.py [simulator|proxy]")
        sys.exit()
    if sys.argv[0] == 'simulator':
        Simulator(True, sw_lemonator()).run()
    elif sys.argv[0] == 'proxy':
        c = Controller(hw_lemonator(4))
        time.sleep(2)
        while True:
            c.update()
