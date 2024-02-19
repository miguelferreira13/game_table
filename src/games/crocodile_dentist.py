from button_led_pairs import ButtonLedPairs
import time


class CrocodileDentist:
    def __init__(self):
        self.pairs = ButtonLedPairs()
        self.sore_led = None  # We have sore leds instead of sore teeth :)

    def play(self):

        print("Playing Crocodile Dentist")
        self.initialize()

        while self.pairs.keep_running():
            self.pairs.press_buttons_leds_high()
            if self.pairs.get_button_states()[self.sore_led]:
                self.defeat()
                self.initialize()

    def initialize(self):
        print("Initializing Crocodile Dentist")
        time.sleep(1)
        self.pairs.all_leds_low()
        self.refresh_sore_led()

    def refresh_sore_led(self):
        self.sore_led = self.pairs.get_random_color()
        print(f"Sore led is {self.sore_led}")

    def defeat(self):
        print("You lost!")
        self.pairs.all_leds_low()
        self.pairs.pairs[self.sore_led].blink()
