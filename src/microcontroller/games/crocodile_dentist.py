from games.base_game import BaseGame
from microcontroller.button_led_pairs import ButtonLed
import time
from logger import logger


class CrocodileDentist(BaseGame):
    def __init__(self):
        super().__init__()
        self.name = "Crocodile Dentist"
        self.sore_led: ButtonLed = None  # We have sore leds instead of sore teeth :)

    def play(self):
        self.initialize()
        while self.pairs.keep_running():
            self.pairs.press_buttons_leds_high()
            pairs = self.pairs.get_led_states()
            if self.sore_led.button_state():
                # If it's the last buttom pressed, celebrate, otherwise, defeat
                if all([led_state for led_state in pairs.values()]):
                    self.celebrate()
                else:
                    self.defeat()
                self.initialize()

    def initialize(self):
        time.sleep(0.5)  # Wait for the user to release the button
        self.pairs.all_leds_low()
        self.refresh_sore_led()
        logger.debug(f"Sore led: {self.sore_led.color}")

    def refresh_sore_led(self):
        self.sore_led = self.pairs.get_random_led()

    def defeat(self):
        self.pairs.all_leds_low()
        self.sore_led.blink()

    def celebrate(self):
        self.pairs.all_leds_low()
        self.pairs.blink_all_leds(5)
