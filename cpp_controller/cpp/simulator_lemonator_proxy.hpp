#ifndef _SIMULATOR_LEMONATOR_PROXY_H
#define _SIMULATOR_LEMONATOR_PROXY_H

#include "lemonator_interface.hpp"
#include <list>
#include <vector>
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include <pybind11/pybind11.h>
#include <pybind11/eval.h>
#include <pybind11/embed.h>
#pragma GCC diagnostic pop

namespace py = pybind11;
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"

class sim_output_proxy : public hwlib::pin_out
{
  private:
    py::object output;
    int _value;

  public:
    sim_output_proxy(py::object p) : output(p)
    {
    }

    void set(bool b, hwlib::buffering = hwlib::buffering::unbuffered)
    {
        output.attr("set")(b);
    }

    bool get()
    {
        return output.attr("get")().cast<int>();
    }
};

class sim_sensor_proxy : public hwlib::sensor_temperature,
                         public hwlib::sensor_distance,
                         public hwlib::sensor_rgb,
                         public hwlib::istream,
                         public hwlib::pin_in
{
  private:
    py::object output;
    int value;

  public:
    sim_sensor_proxy(py::object c) : output(c)
    {
    }

    int readValue()
    {
        return output("readValue")().cast<int>();
    }

    int read_mc() override
    {
        return output.attr("readValue")().cast<int>();
    }

    int read_mm() override
    {
        return output.attr("readValue")().cast<int>();
    }

    rgb read_rgb() override
    {
        return rgb(0, 0, 0);
    }

    char getc() override
    {
        return output.attr("readValue")().cast<int>();
    }

    void update(py::object c)
    {
        output.attr("update")(c);
    }

    bool get(
        hwlib::buffering buf = hwlib::buffering::unbuffered) override
    {
        return output.attr("readValue")().cast<int>();
    }
};

class sim_lcd_proxy : public hwlib::ostream
{
  private:
    py::object output;

  public:
    sim_lcd_proxy(py::object c) : output(c)
    {
    }

    void putc(char c)
    {
        output.attr("putc")(c);
    }

    py::list get_text()
    {
        return output.attr("get_text")();
    }

    friend sim_lcd_proxy & ::operator<<(sim_lcd_proxy &l, const char *s)
    {
        for (const char *p = s; *p != '\0'; p++)
        {
            l.putc(*p);
        }
        return l;
    }
};

class sim_keypad_proxy : public sim_sensor_proxy
{
    py::object output;

  public:
    sim_keypad_proxy(py::object c) : sim_sensor_proxy(c), output(c)
    {
    }

    void putc(char c)
    {
        output.attr("putc")(c);
    }

    char getc()
    {
        return output.attr("getc")().cast<char>();
    }

    void update(py::object c)
    {
        output.attr("update")(c);
    }

    int readValue()
    {
        return output("readValue")().cast<int>();
    }
};

class simulator_lemonator_proxy : public lemonator_interface
{
  public:
    sim_lcd_proxy lcd;
    sim_keypad_proxy keypad;
    sim_sensor_proxy distance;
    sim_sensor_proxy color;
    sim_sensor_proxy temperature;
    sim_sensor_proxy reflex;

    sim_output_proxy heater;
    sim_output_proxy sirup_pump;
    sim_output_proxy sirup_valve;
    sim_output_proxy water_pump;
    sim_output_proxy water_valve;
    sim_output_proxy led_green;
    sim_output_proxy led_yellow;

    simulator_lemonator_proxy() : lemonator_interface(
                                      lcd,
                                      keypad,
                                      distance,
                                      color,
                                      temperature,
                                      reflex,
                                      heater,
                                      sirup_pump,
                                      sirup_valve,
                                      water_pump,
                                      water_valve,
                                      led_green,
                                      led_yellow),
                                  lcd(py::module::import("python.simulator_interface.lemonator").attr("Lcd")()),
                                  keypad(py::module::import("python.simulator_interface.lemonator").attr("Keypad")()),
                                  distance(py::module::import("python.simulator_interface.sensor_proxies").attr("distance_sensor")()),
                                  color(py::module::import("python.simulator_interface.sensor_proxies").attr("color_sensor")()),
                                  temperature(py::module::import("python.simulator_interface.sensor_proxies").attr("temperature_sensor")()),
                                  reflex(py::module::import("python.simulator_interface.sensor_proxies").attr("sensor_proxy")()),

                                  heater(py::module::import("python.simulator_interface.output_proxies").attr("output_proxy")()),
                                  sirup_pump(py::module::import("python.simulator_interface.output_proxies").attr("output_proxy")()),
                                  sirup_valve(py::module::import("python.simulator_interface.output_proxies").attr("output_proxy")()),
                                  water_pump(py::module::import("python.simulator_interface.output_proxies").attr("output_proxy")()),
                                  water_valve(py::module::import("python.simulator_interface.output_proxies").attr("output_proxy")()),
                                  led_green(py::module::import("python.simulator_interface.output_proxies").attr("output_proxy")()),
                                  led_yellow(py::module::import("python.simulator_interface.output_proxies").attr("output_proxy")())
    {
    }
};

#pragma GCC diagnostic pop

#endif
