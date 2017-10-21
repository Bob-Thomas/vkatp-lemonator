> Bob Thomas and Robbie Valkenburg
# Lemonator
----

This is the readme file of the repository belonging to my school project.
This project is made to teach us how to work with a hardware project that isn't widely available to test on.

So our project was to build a simulator in python that resembled the real world application as seen below.
![Imgur](https://i.imgur.com/KRZMe8E.jpg)

So we need a simulator that could hold 2 containers of liquids,
A pump and valve system and a cup detector.
Previous homework already supplied us with a Simulator working with a pygame GUI.
So we decided to repurpose it and tweak it to work with our needs
> hindsight it took so much more effort to tweak than to actually build our own

### Simulator
![Imgur](https://i.imgur.com/wllw8ei.png)

### Proxy
The teacher prepared a proxy interface to use the same interface as the hardware used but instead of setting pins it would send a command over the serial port to the arduino listening to it.

```
    hw.green_led.set(1) would equal to '1g' over serial
```
That interface was however written in c++ and we needed to use it in our python environment so we used pybind11 to create python modules from our c++ classes

The first implementation of creating a pyd file to use in python is found here ->
[Pybind11 module binding to pyd](https://github.com/Bob-Thomas/vkatp-lemonator/blob/master/pc_python/lemonator.cpp)

So that was our first assesment after that we needed to write a control system that would mix our 2 liquids together with a set amount of (lemonade and water) -> [Python controller](https://github.com/Bob-Thomas/vkatp-lemonator/blob/master/cpp_controller/python/Controller.py)  

This controller needed to work conform the proxy interface so it can be used in our simulator and with the actual hardware interface.

After that was working nicely we wrote the tests for it -> [Tests](https://github.com/Bob-Thomas/vkatp-lemonator/tree/master/cpp_controller/python/unit_test)  

![coverage](https://i.imgur.com/m1ag9el.png)

So our prototype was working on our simulator and on the actual hardware.

### C++ controller
Now we needed to implement the same python controller into a c++ version->
[C++ Controller](https://github.com/Bob-Thomas/vkatp-lemonator/blob/master/cpp_controller/cpp/lemonator_controller.hpp)
That went quite easy without any real big troubles until we needed to also make our c++ controller call the actuall python simulator.

I struggled for a while to make this work but in the end I got it to play nicely.
To make our c++ controller work with the simulator we needed to make a proxy for the actual python proxy interface so it would work both ways.
[c++ python proxy](https://github.com/Bob-Thomas/vkatp-lemonator/blob/master/cpp_controller/cpp/simulator_lemonator_proxy.hpp) This proxy inherits from the lemonator_interface and instead of setting pins or sending serial commands it would call the underlying python object functions.

In the example below the pythonobject resembles an instance of
[output_proxy](https://github.com/Bob-Thomas/vkatp-lemonator/blob/master/cpp_controller/python/simulator_interface/output_proxies.py)
```
  lemonator.led_green.set(1) would call interface.pythonobject.set(1)
```

After creating the back and forth proxies for the lemonator_interface and the [c++ controller](https://github.com/Bob-Thomas/vkatp-lemonator/blob/master/cpp_controller/cpp/main.cpp#L12)


### Calling python from c++
We could actually pass our c++ controller into the python simulator like this
```
        Py_Initialize();
        py::object l = py::module::import("simulator_proxy").attr("lemonator")();
        py::object c = py::module::import("controller_proxy").attr("Controller")(l.cast<simulator_lemonator_proxy &>());
        py::object sim = py::module::import("python.Simulator").attr("Simulator")(true, c).attr("run")();
```

Some problems arose because I installed pygame into my virtualenv and pybind11 didn't want to include it.
So I just added my venv path to the packages like this
```
        py::module sys = py::module::import("sys");
        py::object path = sys.attr("path");
        path.attr("insert")(0, "C:\\Users\\endargon\\school\\lemonator\\venv\\Lib\\site-packages");
        path.attr("insert")(0, "python");
```

After that my simulator would start up without any trouble


# FIN
