#include "lemonator_proxy.hpp"

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/pybind11.h"
#pragma GCC diagnostic pop

namespace py = pybind11;

PYBIND11_MODULE( lemonator, m ) {

    py::enum_< hwlib::buffering >( m, "buffering")
        .value( "unbuffered", hwlib::buffering::unbuffered )
        .value( "buffered", hwlib::buffering::buffered )
        .export_values();

    py::class_< output_proxy >( m, "output_proxy" )
        .def("set", &output_proxy::set, "",

            py::arg("v"), py::arg("buffering") = hwlib::buffering::unbuffered )
        .def("get", &output_proxy::get, "get pin state");

    py::class_< lcd_proxy >( m, "lcd_proxy" )
    .def( "putc", &lcd_proxy::putc, "",
        py::arg("c"))
    .def("__lshift__", [](lcd_proxy & stream, const char *s) {
        stream << s;
    }, py::is_operator());

    py::class_< sensor_proxy > (m, "sensor_proxy")
        .def("read_mc", &sensor_proxy::read_mc, "read temp in mili celsius")
        .def("read_mm", &sensor_proxy::read_mm, "read mili meters")
        .def("read_rgb", &sensor_proxy::read_rgb, "read rgb")
        .def("getc", &sensor_proxy::getc, "Get character")
        .def("get", &sensor_proxy::get, "Get pin",
            py::arg("buffering") = hwlib::buffering::unbuffered );



    py::class_< lemonator_proxy >(m, "lemonator" )
        .def( py::init< int >() )
        //sensor proxies
        .def_readonly("lcd", &lemonator_proxy::p_lcd)
        .def_readonly("keypad", &lemonator_proxy::p_keypad)
        .def_readonly("distance", &lemonator_proxy::p_distance)
        .def_readonly("color", &lemonator_proxy::p_color)
        .def_readonly("temperature", &lemonator_proxy::p_temperature)
        .def_readonly("reflex", &lemonator_proxy::p_reflex)
        //output proxies
        .def_readonly( "led_yellow", &lemonator_proxy::p_led_yellow )
        .def_readonly( "led_green", &lemonator_proxy::p_led_green )
        .def_readonly( "heater", &lemonator_proxy::p_heater )
        .def_readonly( "sirup_pump", &lemonator_proxy::p_sirup_pump )
        .def_readonly( "sirup_valve", &lemonator_proxy::p_sirup_valve )
        .def_readonly( "water_pump", &lemonator_proxy::p_water_pump )
        .def_readonly( "water_valve", &lemonator_proxy::p_water_valve );
}

