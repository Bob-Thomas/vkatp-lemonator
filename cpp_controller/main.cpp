#include "lemonator_proxy.hpp"

enum class State  {START,NO_CUP,CUP_PRESENT,WAITING_FOR_INPUT,WAITING_FOR_CUP,MIXING,MIX_DONE };


static constexpr int full_cup = 55;
static constexpr int expected_fill = full_cup - 10;
static constexpr int empty_cup = 88;
static constexpr int diff_liquids = empty_cup - expected_fill;
static constexpr int full_vessel = full_cup*10;
static constexpr int required_percentage_sirup = 50;
static constexpr float required_sirup_in_mm = empty_cup - (int)expected_fill/100 * required_percentage_sirup;


class Controller {
    float temp_distance = empty_cup;
    State state = State::START;
    lemonator_proxy &lemonator;

    void change_state(State s) {
        state = s;
    }

    void update_display() {
        lemonator.lcd << "\t0000";
        for (int i = 0; i < 4; i++) {
            lemonator.lcd << "                    ";
            if( i < 3){
                lemonator.lcd << "\n";
            }
        }
        lemonator.lcd << "\t0000     Lemonator v1.0\n";

        if( state == State::WAITING_FOR_CUP){
            lemonator.lcd << "\r Please insert cup  ";
        }
        else if( state == State::CUP_PRESENT or state == State::WAITING_FOR_INPUT){
            lemonator.lcd << "\r Use keypad to start";
        }
        else if( state == State::MIXING){
            int distance = (int)(100/100)*(empty_cup-distance_filter()) /diff_liquids*100 || 0;
            lemonator.lcd << "\r      Mix starting  \n";
            lemonator.lcd << "\r              ";
            lemonator.lcd << distance;
            lemonator.lcd << "%";
        }
        else if( state == State::MIX_DONE){
            lemonator.lcd << "\t0103 Please take.";
            lemonator.lcd << "\t0203 And Enjoy! :3";
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
        if (temp_distance-value > 3) {
            return temp_distance;
        }
        temp_distance  = temp_distance * alpha + value * (1 - alpha);
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
        lemonator.water_pump.set(!v);
    }

public:
    Controller(lemonator_proxy& lemonator) : lemonator(lemonator)  {}

    void update() {
        if (state == State::START) {
            if (lemonator.p_reflex.get()) {
                change_state(State::CUP_PRESENT);
            } else {
                change_state(State::NO_CUP);
            }
        }

        if (state == State::MIXING && !lemonator.p_reflex.get()) {
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
            temp_distance = 88;
        }

        if (state == State::WAITING_FOR_CUP) {
            if (lemonator.p_reflex.get()) {
                change_state(State::CUP_PRESENT);
            }
        }

        if (state == State::WAITING_FOR_INPUT) {
            if (lemonator.p_reflex.get()) {
                change_state(State::CUP_PRESENT);
                return;
            }
            char value = lemonator.keypad.getc();
            if (value != '\0') {
                change_state(State::MIXING);
            }
        }

        if (state == State::MIXING) {
            update_display();
            if (distance_filter() < expected_fill) {
                disable_pumps();
                change_state(State::MIX_DONE);
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
    py::scoped_interpreter guard{};
   py::module sys = py::module::import("sys");
   py::object path = sys.attr("path");
   path.attr("insert")(0, "C:\\Users\\endargon\\school\\lemonator\\venv\\Lib\\site-packages");
   py::module dave = py::module::import("Simulator");
   py::object sim = dave.attr("Simulator");
   py::object test = py::module::import("lemonator").attr("lemonator")(4);
   Controller ctrl(*test.cast<lemonator_proxy *>());
   while(1) {
       ctrl.update();
   }
//    auto sims = sim(true, test, controller);
//    sims.attr("run");
}