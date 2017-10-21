#ifndef CONFIG_H
#define CONFIG_H
namespace config
{
constexpr int full_cup = 55;
constexpr int expected_fill = full_cup - 10;
constexpr int empty_cup = 88;
constexpr int diff_liquids = empty_cup - expected_fill;
constexpr int full_vessel = full_cup * 10;
constexpr int required_percentage_sirup = 10;
constexpr float required_sirup_in_mm = (float)empty_cup - (float)expected_fill / 100.0 * (float)required_percentage_sirup;
}
#endif