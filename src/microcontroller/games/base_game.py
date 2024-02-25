from microcontroller.button_led_pairs import ButtonLedPairs
from logger import logger

MAIN_MENU_REQUESTED = "Main menu requested"


class BaseGame:
    def __init__(self):
        self.pairs: ButtonLedPairs = ButtonLedPairs()
        self.name: str = "Base Game"

    def execute(self):
        logger.info(f"Playing {self.name}")
        try:
            self.play()
        except Exception as e:
            if str(e) != MAIN_MENU_REQUESTED:
                logger.exception(e)
            return
        logger.info(f"{self.name} finished")

    def play(self):
        self.pairs.all_leds_low()

        while self.pairs.keep_running():
            self.pairs.press_low_not_pressed_high()

    def initialize(self):
        pass

    def defeat(self):
        pass
