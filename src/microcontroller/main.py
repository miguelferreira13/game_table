from button_led_pairs import ButtonLedPairs
from datetime import datetime
import time
from logger import logger

from games import (
    base_game,
    crocodile_dentist,
    whac_a_mole,
    stef_stunt_pilot,
    color_blind
)

GAMES_MAP = {
    "green": crocodile_dentist.CrocodileDentist(),
    "red": whac_a_mole.WhacAMole(),
    "yellow": base_game.BaseGame(),
    "blue": stef_stunt_pilot.StefStuntPilot(),
    "white": color_blind.ColorBlind()
}


class MainMenu:
    def __init__(self):
        self.pairs = ButtonLedPairs()

    def start(self):
        try:
            self._start()
        # except KeyboardInterrupt:
        #     return
        # except Exception as e:
        #     logger.exception(e)
        #     return
        finally:
            self.cleanup()
            return

    def _start(self):
        time.sleep(1)  # Wait for the user to release the button
        self.pairs.all_leds_low()
        self.pairs.blink_all_leds(5, 0.1)
        logger.info("Entering main menu")
        while self.pairs.keep_running():
            if datetime.now().second % 2:
                self.pairs.all_leds_high()
            else :
                self.pairs.all_leds_low()
            states = self.pairs.get_button_states()
            for color, state in states.items():
                game: base_game.BaseGame = GAMES_MAP[color]
                if state and game:
                    logger.info(f"Selected: {color.capitalize()} - {game.name}.")
                    self.execute_game(game)
                    return

    def execute_game(self, game):
        try:
            game.execute()
        except Exception as e:
            logger.exception(e)
            return
        finally:
            self.start()

    def cleanup(self):
        self.pairs.all_leds_low()
        self.pairs.cleanup()


if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.start()
