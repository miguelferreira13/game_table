from games.base_game import BaseGame
from microcontroller.button_led_pairs import ButtonLed
from logger import logger
import time
import requests
from random import choice
from config import config


# The color of the text is the correct color
class ColorBlind(BaseGame):
    def __init__(self):
        super().__init__()
        self.name = "Color Blind"
        self.answer_time_limit = 2.3  # Time allowed to press the button in seconds
        self.loser: ButtonLed = None

    def play(self):
        self.initialize()
        time.sleep(1)  # Wait for the user to release the button
        all_leds = list(self.pairs.led_button_combinations.values())
        round_number = 0

        while self.pairs.keep_running():

            random_led: ButtonLed = choice([led for led in all_leds])
            logger.debug(f"Winning color: {random_led.color}")

            request = requests.get(f"{config.url}/game_table/{random_led.color}")
            request.raise_for_status()

            if (round_number * config.speed_increase_rate) < self.answer_time_limit:
                speed_decrease = round_number * config.speed_increase_rate

            # random_led.led_high() # We don't want to turn on the led, leaving for debugging purposes

            delay_while = time.time() + self.answer_time_limit - speed_decrease

            game_continues = False
            while delay_while > time.time() and self.pairs.keep_running():
                self.pairs.press_low_not_pressed_high()
                for led in self.pairs.led_button_combinations.values():
                    if led.button_state() and led != random_led:
                        self.loser = led
                        self.defeat()
                        self.initialize()
                        round_number = 0
                        time.sleep(0.5)
                        break
                # If the button is pressed and it is an active player or is not an active player, the game continues
                if random_led.button_state():
                    game_continues = True
                    time.sleep(0.5)
                    break

            random_led.led_low()
            if not game_continues:
                self.loser = random_led
                self.defeat()
                # Press the defeated button for next another game
                while not self.loser.button_state() and self.pairs.keep_running():
                    # raise Exception(MAIN_MENU_REQUESTED)  # Avoid too many requests to the server
                    self.pairs.debounce()
                self.initialize()
                round_number = 0
            round_number += 1

    def initialize(self):
        time.sleep(0.5)  # Wait for the user to release the button
        self.pairs.all_leds_low()

    def get_active_palyers_colors(self):
        active_colors: dict = {}
        while not self.detect_long_press(active_colors):
            states = self.pairs.get_button_states()
            for color, state in states.items():
                if state:
                    self.pairs.led_button_combinations[color].led_high()
                    active_colors.update({color: active_colors.get(color, 0) + config.default_debounce_time})
            self.pairs.debounce()
        self.active_players = [self.pairs.led_button_combinations[color] for color in active_colors.keys()]

    def detect_long_press(self, active_colors: dict) -> bool:
        # If any color has been pressed more than once, we start the game
        return any([press_time > config.long_press_duration for press_time in active_colors.values()])

    def defeat(self):
        self.pairs.all_leds_low()
        request = requests.get(f'{config.url}/game_table/loser')
        request.raise_for_status()
        self.loser.blink(10, 0.1)

    def celebrate(self):
        self.pairs.blink_all_leds(10, 0.1)
