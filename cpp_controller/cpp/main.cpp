#include "lemonator_proxy.hpp"
#include "simulator_lemonator_proxy.hpp"
#include "lemonator_controller.hpp"
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include <pybind11/pybind11.h>
#include <pybind11/eval.h>
#include <pybind11/embed.h>
#pragma GCC diagnostic pop
namespace py = pybind11;

PYBIND11_EMBEDDED_MODULE(controller_proxy, m)
{
    py::enum_<State>(m, "State")
        .value("START", State::START)
        .value("NO_CUP", State::NO_CUP)
        .value("CUP_PRESENT", State::CUP_PRESENT)
        .value("WAITING_FOR_INPUT", State::WAITING_FOR_INPUT)
        .value("WAITING_FOR_CUP", State::WAITING_FOR_CUP)
        .value("MIXING", State::MIXING)
        .value("MIX_DONE", State::MIX_DONE)
        .export_values();

    py::class_<lemonator_controller>(m, "Controller", py::dynamic_attr())
        .def(py::init<simulator_lemonator_proxy &>())
        //sensor proxies
        .def("get_lemonator", &lemonator_controller::get_lemonator, "")
        .def("disable_pumps", &lemonator_controller::disable_pumps)
        .def("set_water_pump", &lemonator_controller::set_water_pump, "",
             py::arg("v"))
        .def("set_sirup_pump", &lemonator_controller::set_sirup_pump, "",
             py::arg("v"))
        .def("update", &lemonator_controller::update)
        .def("update_display", &lemonator_controller::update_display)
        .def("change_state", &lemonator_controller::change_state, "",
             py::arg("v"))
        .def("distance_filter", &lemonator_controller::distance_filter);
}

PYBIND11_EMBEDDED_MODULE(simulator_proxy, m)
{
    py::enum_<hwlib::buffering>(m, "buffering")
        .value("unbuffered", hwlib::buffering::unbuffered)
        .value("buffered", hwlib::buffering::buffered)
        .export_values();

    py::class_<sim_output_proxy>(m, "sim_output_proxy", py::dynamic_attr())
        .def("set", &sim_output_proxy::set, "",

             py::arg("v"), py::arg("buffering") = hwlib::buffering::unbuffered)
        .def("get", &sim_output_proxy::get, "get pin state");

    py::class_<sim_keypad_proxy>(m, "sim_keypad_proxy", py::dynamic_attr())
        .def("readValue", &sim_keypad_proxy::readValue)
        .def("putc", &sim_keypad_proxy::putc, "",
             py::arg("v"))
        .def("update", &sim_sensor_proxy::update, "",
             py::arg("v"))
        .def("getc", &sim_keypad_proxy::getc, "");

    py::class_<sim_lcd_proxy>(m, "sim_lcd_proxy", py::dynamic_attr())
        .def("get_text", &sim_lcd_proxy::get_text, "")
        .def("putc", &sim_lcd_proxy::putc, "",
             py::arg("c"))
        .def("__lshift__", [](sim_lcd_proxy &stream, const char *s) {
            stream << s;
        },
             py::is_operator());

    py::class_<sim_sensor_proxy>(m, "sim_sensor_proxy", py::dynamic_attr())
        .def("update", &sim_sensor_proxy::update, "",
             py::arg("v"))
        .def("readValue", &sim_sensor_proxy::readValue)
        .def("read_mc", &sim_sensor_proxy::read_mc, "read temp in mili celsius")
        .def("read_mm", &sim_sensor_proxy::read_mm, "read mili meters")
        .def("read_rgb", &sim_sensor_proxy::read_rgb, "read rgb")
        .def("getc", &sim_sensor_proxy::getc, "Get character")
        .def("get", &sim_sensor_proxy::get, "Get pin",
             py::arg("buffering") = hwlib::buffering::unbuffered);

    py::class_<simulator_lemonator_proxy>(m, "lemonator", py::dynamic_attr())
        //sensor proxies
        .def(py::init<>())
        .def_readonly("lcd", &simulator_lemonator_proxy::lcd)
        .def_readonly("keypad", &simulator_lemonator_proxy::keypad)
        .def_readonly("distance", &simulator_lemonator_proxy::distance)
        .def_readonly("color", &simulator_lemonator_proxy::color)
        .def_readonly("temperature", &simulator_lemonator_proxy::temperature)
        .def_readonly("reflex", &simulator_lemonator_proxy::reflex)
        //output proxies
        .def_readonly("led_yellow", &simulator_lemonator_proxy::led_yellow)
        .def_readonly("led_green", &simulator_lemonator_proxy::led_green)
        .def_readonly("heater", &simulator_lemonator_proxy::heater)
        .def_readonly("sirup_pump", &simulator_lemonator_proxy::sirup_pump)
        .def_readonly("sirup_valve", &simulator_lemonator_proxy::sirup_valve)
        .def_readonly("water_pump", &simulator_lemonator_proxy::water_pump)
        .def_readonly("water_valve", &simulator_lemonator_proxy::water_valve);
}

PYBIND11_MODULE(python_proxy, m)
{

    py::enum_<hwlib::buffering>(m, "buffering")
        .value("unbuffered", hwlib::buffering::unbuffered)
        .value("buffered", hwlib::buffering::buffered)
        .export_values();

    py::class_<output_proxy>(m, "output_proxy")
        .def("set", &output_proxy::set, "",

             py::arg("v"), py::arg("buffering") = hwlib::buffering::unbuffered)
        .def("get", &output_proxy::get, "get pin state");

    py::class_<lcd_proxy>(m, "lcd_proxy")
        .def("putc", &lcd_proxy::putc, "",
             py::arg("c"))
        .def("__lshift__", [](lcd_proxy &stream, const char *s) {
            stream << s;
        },
             py::is_operator());

    py::class_<sensor_proxy>(m, "sensor_proxy")
        .def("read_mc", &sensor_proxy::read_mc, "read temp in mili celsius")
        .def("read_mm", &sensor_proxy::read_mm, "read mili meters")
        .def("read_rgb", &sensor_proxy::read_rgb, "read rgb")
        .def("getc", &sensor_proxy::getc, "Get character")
        .def("get", &sensor_proxy::get, "Get pin",
             py::arg("buffering") = hwlib::buffering::unbuffered);

    py::class_<lemonator_proxy>(m, "lemonator")
        .def(py::init<int>())
        //sensor proxies
        .def_readonly("lcd", &lemonator_proxy::p_lcd)
        .def_readonly("keypad", &lemonator_proxy::p_keypad)
        .def_readonly("distance", &lemonator_proxy::p_distance)
        .def_readonly("color", &lemonator_proxy::p_color)
        .def_readonly("temperature", &lemonator_proxy::p_temperature)
        .def_readonly("reflex", &lemonator_proxy::p_reflex)
        //output proxies
        .def_readonly("led_yellow", &lemonator_proxy::p_led_yellow)
        .def_readonly("led_green", &lemonator_proxy::p_led_green)
        .def_readonly("heater", &lemonator_proxy::p_heater)
        .def_readonly("sirup_pump", &lemonator_proxy::p_sirup_pump)
        .def_readonly("sirup_valve", &lemonator_proxy::p_sirup_valve)
        .def_readonly("water_pump", &lemonator_proxy::p_water_pump)
        .def_readonly("water_valve", &lemonator_proxy::p_water_valve);
}

int main(int argc, char *argv[])
{
    // Check the number of parameters
    if (argc < 2)
    {
        // Tell the user how to run the program
        std::cerr << "Usage: main.exe "
                  << " Simulator | Proxy" << std::endl;
        /* "Usage messages" are a conventional way of telling the user
         * how to run a program if they enter the command incorrectly.
         */
        return 1;
    }
    if (strcmp(argv[1], "Simulator") == 0)
    {
        Py_Initialize();

        //include my venv pygame and the python folder with all the lemonator modules
        py::module sys = py::module::import("sys");
        py::object path = sys.attr("path");
        path.attr("insert")(0, "C:\\Users\\endargon\\school\\lemonator\\venv\\Lib\\site-packages");
        path.attr("insert")(0, "python");

        py::object l = py::module::import("simulator_proxy").attr("lemonator")();
        py::object c = py::module::import("controller_proxy").attr("Controller")(l.cast<simulator_lemonator_proxy &>());
        py::object dave = py::module::import("python.Simulator").attr("Simulator")(true, c).attr("run")();
    }
    else if (strcmp(argv[1], "Proxy") == 0)
    {
        lemonator_proxy prox(4);
        hwlib::wait_ms(2000);
        lemonator_controller lem(prox);
        while (1)
        {
            lem.update();
        }
    }
    return 0;
}