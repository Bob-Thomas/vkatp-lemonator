#include "lemonator_controller.hpp"

void lemonator_controller::change_state(State s)
{
    state = s;
}

void lemonator_controller::update_display()
{
    if (hwlib::now_us() - update_time > 1000000 * 2)
    {
        update_time = hwlib::now_us();
        lemonator.lcd << "\t0002                    ";
        lemonator.lcd << "\t0003                    ";
        if (state == State::WAITING_FOR_CUP)
        {
            lemonator.lcd << "\t0001Insert cup";
        }
        else if (state == State::CUP_PRESENT || state == State::WAITING_FOR_INPUT)
        {
            lemonator.lcd << "\t0001Use keypad to start ";
        }
        else if (state == State::MIXING)
        {
            lemonator.lcd << "\t0001\r      Mix starting  \n";
            lemonator.lcd << "\r              \n";
            int distance = ((float)100 / (float)100) * ((float)empty_cup - distance_filter()) / (float)diff_liquids * (float)100;
            lemonator.lcd << distance;
            lemonator.lcd << "%";
        }
        else if (state == State::MIX_DONE)
        {
            lemonator.lcd << "\t0001                   ";
            lemonator.lcd << "\t0002    Please take.   ";
            lemonator.lcd << "\t0003    And Enjoy! :3  ";
        }
    }
}

float lemonator_controller::distance_filter()
{
    float alpha = 0.7;
    int value = lemonator.distance.read_mm();
    if (value > empty_cup)
    {
        value = empty_cup;
    }
    // if (value < expected_fill)
    // {
    //     value = expected_fill;
    // }
    if (value > temp_distance)
    {
        return temp_distance;
    }
    if (temp_distance - value > 5)
    {
        return temp_distance;
    }
    temp_distance = temp_distance * alpha + (float)value * (1 - alpha);
    return temp_distance;
}

void lemonator_controller::disable_pumps()
{
    set_sirup_pump(0);
    set_water_pump(0);
}

void lemonator_controller::set_sirup_pump(int v)
{
    lemonator.sirup_pump.set(v);
    lemonator.sirup_valve.set(!v);
}

void lemonator_controller::set_water_pump(int v)
{
    lemonator.water_pump.set(v);
    lemonator.water_valve.set(!v);
}

lemonator_controller::lemonator_controller(lemonator_interface &lemonator) : lemonator(lemonator), state(State::START)
{
    lemonator.lcd << "\f   Lemonator v1.0\n";
}

void lemonator_controller::update()
{
    distance_filter();
    if (state == State::START)
    {
        if (lemonator.reflex.get())
        {
            change_state(State::CUP_PRESENT);
        }
        else
        {
            change_state(State::NO_CUP);
        }
    }

    if (!lemonator.reflex.get())
    {
        change_state(State::NO_CUP);
    }

    if (state == State::CUP_PRESENT)
    {
        change_state(State::WAITING_FOR_INPUT);
        lemonator.led_green.set(1);
    }

    if (state == State::NO_CUP)
    {
        change_state(State::WAITING_FOR_CUP);
        lemonator.led_green.set(0);
        disable_pumps();
    }

    if (state == State::WAITING_FOR_CUP)
    {
        if (lemonator.reflex.get())
        {
            change_state(State::CUP_PRESENT);
        }
    }

    if (state == State::WAITING_FOR_INPUT)
    {
        if (!lemonator.reflex.get())
        {
            change_state(State::CUP_PRESENT);
            return;
        }
        char value = lemonator.keypad.getc();
        if (value != '\0')
        {
            temp_distance = lemonator.distance.read_mm();
            change_state(State::MIXING);
        }
    }

    if (state == State::MIXING)
    {
        if (distance_filter() < expected_fill)
        {
            change_state(State::MIX_DONE);
            disable_pumps();
            return;
        }
        else
        {
            if (distance_filter() > required_sirup_in_mm)
            {
                set_water_pump(0);
                set_sirup_pump(1);
            }
            else
            {
                set_water_pump(1);
                set_sirup_pump(0);
            }
        }
    }
    update_display();
}

simulator_lemonator_proxy &lemonator_controller::get_lemonator()
{
    return (simulator_lemonator_proxy &)lemonator;
}