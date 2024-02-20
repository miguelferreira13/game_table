from button_led_pairs import ButtonLedPairs
from logger import logger


class BaseGame:
    def __init__(self):
        self.pairs: ButtonLedPairs = ButtonLedPairs()
        self.name: str = "Base Game"

    def execute(self):
        logger.info(f"Playing {self.name}")
        self.play()
        logger.info(f"{self.name} finished")

    def play(self):
        self.pairs.all_leds_low()

        while self.pairs.keep_running():
            self.pairs.press_low_not_pressed_high()

    def initialize(self):
        pass

    def defeat(self):
        pass
