if __name__ == "__main__":
    """Only perform actions when invoked directly!"""
    from Simulator import Simulator
    #import the lemonator interface library...

    simulator = Simulator(True) # use Simulator(False) to disable the GUI
    simulator.run()