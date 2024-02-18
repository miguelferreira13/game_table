from button_led_pairs import ButtonLedPairs
from crocodile_dentist import CrocodileDentist
from datetime import datetime

GAMES_MAP = {
    "green": CrocodileDentist(),
    "red": None,
    "yellow": None,
    "blue": None,
    "white": None
}


class MainMenu:
    def __init__(self):
        self.pairs = ButtonLedPairs()

    def start(self):
        print("Starting main menu")
        game_selected = False
        while self.pairs.keep_running() or not game_selected:
            if datetime.now().second % 2:
                self.pairs.all_leds_high()
            else :
                self.pairs.all_leds_low()
            states = self.pairs.get_button_states()
            for color, state in states.items():
                if state and GAMES_MAP[color]:
                    print(f"Selected game color {color}")
                    self.play_game(GAMES_MAP[color])
                    game_selected = True
                    break

    def play_game(self, game):
        try:
            print("Game starting from main menu")
            game.play()
            print("Game finished")
        finally:
            self.start()

    def cleanup(self):
        self.paris.cleanup()


if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.start()
    main_menu.cleanup()
