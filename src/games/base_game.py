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
        pass

    def initialize(self):
        pass

    def defeat(self):
        pass
