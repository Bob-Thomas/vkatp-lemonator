
"""Constants for physical simulation"""
flowRate = 1         # the amount of water flowing (in ml) from the mixture vessel per second when tap is open
# the amount of heat increase (in degrees celsius) in mixture vessel when heater is on
heatRate = 1
# amount of temperature loss (in degrees celsius) in mixture vessel when heater is off
temperatureDecay = 0.1

# amount of seconds to build up enough pressure to make liquid flow from storage vessels
pressureRampUp = 3
# amount of time before liquid stops flowing after the air pump has been switched off
pressureRampDown = 20

# amount (in ml) of liquid that can maximally go into the containers (pi * 10 * 10 * 6.5; diameter 10cm, height ~6.5cm)
liquidMax = 45
environmentTemp = 20    # environmentalTemperature

# 0.00V = 0.0 degrees celsius; steps of 0.05V per degree celsius above 0
tempConversion = 0.05
levelConversion = 0.1     # V/cm; 0V is empty
# 0.00V = value 0 (pitch black) - 3.3 V = value 100 (bright white); value/lightness score (HSV)
colourConversion = 0.033

"""Set Points: these indicate the desired values for the dimensions of the resulting mixture"""
levelSetPoint = 44  # cm liquid (0.8 = 500ml)
colourSetPoint = 1.65  # % value
tempSetPoint = 2.0  # degrees celsius

"""Reaction difference: the amount of points of divergence allowed before the controller reacts"""
tempReaction = 0.05
levelReaction = 0.07
colourReaction = 0.05


full_cup = 55  # 44mm 25cl
expected_fill = full_cup - 10
empty_cup = 88
diff_liquids = empty_cup - expected_fill
full_vessel = full_cup * 10
required_percentage_sirup = 50
required_sirup_in_mm = empty_cup - \
    round((expected_fill / 100) * required_percentage_sirup)
