# if __name__ == "__main__":
#     """Only perform actions when invoked directly!"""
#     from Simulator import Simulator
#     #import the lemonator interface library...

#     simulator = Simulator(True) # use Simulator(False) to disable the GUI
#     simulator.run()

from lemonator import lemonator as hw_lemonator
from simulator_interface.lemonator import Lemonator as sw_lemonator
from Simulator import Simulator

Simulator(True, sw_lemonator()).run()
