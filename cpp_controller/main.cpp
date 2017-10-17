#include "lemonator_proxy.hpp"

enum class State  {START,NO_CUP,CUP_PRESENT,WAITING_FOR_INPUT,WAITING_FOR_CUP,MIXING,MIX_DONE };


static constexpr int full_cup = 55;
static constexpr int expected_fill = full_cup - 10;
static constexpr int empty_cup = 88;
static constexpr int diff_liquids = empty_cup - expected_fill;
static constexpr int full_vessel = full_cup*10;
static constexpr int required_percentage_sirup = 10;
static constexpr float required_sirup_in_mm = (float)empty_cup - (float)expected_fill/100.0 * (float)required_percentage_sirup;


class Controller {
    float temp_distance = empty_cup;
    lemonator_proxy &lemonator;
    State state = State::START;

    void change_state(State s) {
        state = s;
        update_display();
    }

    void update_display() {
        lemonator.lcd << "\t0002                    ";
        lemonator.lcd << "\t0003                    ";
        if( state == State::WAITING_FOR_CUP){
            lemonator.lcd << "\t0001Please insert cup   ";
        }
        else if( state == State::CUP_PRESENT || state == State::WAITING_FOR_INPUT){
            lemonator.lcd << "\t0001Use keypad to start ";
        }
        else if( state == State::MIXING){
            lemonator.lcd << "\t0001\r      Mix starting  \n";
            lemonator.lcd << "\r              \n";
            int distance = ((float)100/(float)100)*((float)empty_cup-distance_filter()) /(float)diff_liquids*(float)100;
            std::cout << distance << "\n";
            lemonator.lcd << distance;
            lemonator.lcd << "%";
        }
        else if( state == State::MIX_DONE){
            lemonator.lcd << "\t0001                   ";
            lemonator.lcd << "\t0002    Please take.   ";
            lemonator.lcd << "\t0003    And Enjoy! :3  ";
        }
    }

    float distance_filter() {
        float alpha = 0.7;
        int value = lemonator.distance.read_mm();
        if (value > empty_cup) {
            value = empty_cup;
        }
        if (value > temp_distance) {
            return temp_distance;
        }
        if (temp_distance-value > 5) {
            return temp_distance;
        }
        temp_distance  = temp_distance * alpha + (float)value * (1 - alpha);
        std::cout << "value: " << value << " EMA: " << temp_distance <<  "\n";
        return temp_distance;
    }

    void disable_pumps() {
        set_sirup_pump(0);
        set_water_pump(0);
    }

    void set_sirup_pump(int v) {
        lemonator.sirup_pump.set(v);
        lemonator.sirup_valve.set(!v);
    }

    void set_water_pump(int v) {
        lemonator.water_pump.set(v);
        lemonator.water_valve.set(!v);
    }

public:
    Controller(lemonator_proxy& lemonator) : lemonator(lemonator), state(State::START)  {
        lemonator.lcd << "\f   Lemonator v1.0\n";
    }

    void update() {
        distance_filter();
        if (state == State::START) {
            if (lemonator.p_reflex.get()) {
                change_state(State::CUP_PRESENT);
            } else {
                change_state(State::NO_CUP);
            }
        }

        if (!lemonator.p_reflex.get()) {
            change_state(State::NO_CUP);
        }

        if (state == State::CUP_PRESENT) {
            change_state(State::WAITING_FOR_INPUT);
            lemonator.led_green.set(1);
        }

        if (state == State::NO_CUP) {
            change_state(State::WAITING_FOR_CUP);
            lemonator.led_green.set(0);
            disable_pumps();
        }

        if (state == State::WAITING_FOR_CUP) {
            if (lemonator.p_reflex.get()) {
                change_state(State::CUP_PRESENT);
            }
        }

        if (state == State::WAITING_FOR_INPUT) {
            if (!lemonator.p_reflex.get()) {
                change_state(State::CUP_PRESENT);
                return;
            }
            char value = lemonator.keypad.getc();
            if (value != '\0') {
                temp_distance = lemonator.distance.read_mm();
                change_state(State::MIXING);
            }
        }

        if (state == State::MIXING) {
            update_display();
            if (distance_filter() < expected_fill) {
                change_state(State::MIX_DONE);
                disable_pumps();
                return;
            } else {
                if (distance_filter() > required_sirup_in_mm) {
                    set_water_pump(0);
                    set_sirup_pump(1);
                } else {
                    set_water_pump(1);
                    set_sirup_pump(0);
                }
            }

        }

    }
};

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include <pybind11/pybind11.h>
#include <pybind11/eval.h>
#include <pybind11/embed.h>
#pragma GCC diagnostic pop

namespace py = pybind11;

int main( void ){
    lemonator_proxy p(4, 0, 0);
    hwlib::wait_ms(2000);
    Controller ctrl(p);
    ctrl.update();
    // py::scoped_interpreter guard{};
//    py::module sys = py::module::import("sys");
//    py::object path = sys.attr("path");
//    path.attr("insert")(0, "C:\\Users\\endargon\\school\\lemonator\\venv\\Lib\\site-packages");
// //    py::module dave = py::module::import("Simulator");
// //    py::object sim = dave.attr("Simulator");
//    py::object test = py::module::import("lemonator").attr("lemonator")(4);
//    Controller ctrl(*test.cast<lemonator_proxy *>());
   while(1) {
       ctrl.update();
    //    hwlib::wait_ms(100);
   }
// //    auto sims = sim(true, test, controller);sou
// //    sims.attr("run");
}