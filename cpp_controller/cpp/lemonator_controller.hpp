#ifndef LEMONATOR_CONTROLLER_H
#define LEMAONTOR_CONTROLLER_H
#include "lemonator_proxy.hpp"
#include "simulator_lemonator_proxy.hpp"
#include "config.hpp"
enum class State
{
    START,
    NO_CUP,
    CUP_PRESENT,
    WAITING_FOR_INPUT,
    WAITING_FOR_CUP,
    MIXING,
    MIX_DONE
};

class lemonator_controller
{
  public:
    float temp_distance = empty_cup;
    lemonator_interface &lemonator;
    State state = State::START;
    uint64_t update_time = 0;

    lemonator_controller(lemonator_interface &lemonator);

    void change_state(State s);

    void update_display();

    float distance_filter();

    void disable_pumps();

    void set_sirup_pump(int v);

    void set_water_pump(int v);

    void update();

    simulator_lemonator_proxy &get_lemonator();
};

#endif