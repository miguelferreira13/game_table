"""
Quickly check if the buttons are working by lighting up the LEDs when the buttons are pressed.
"""
from button_led_pairs import ButtonLedPairs

button_led_pairs = ButtonLedPairs()
button_led_pairs.all_leds_low()

try:
    while button_led_pairs.keep_running():
        button_led_pairs.press_low_not_pressed_high()

finally:
    button_led_pairs.cleanup()
