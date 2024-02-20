from games.base_game import BaseGame
from button_led_pairs import ButtonLed, DEFAULT_DEBOUNCE_TIME
import time
import requests
from random import choice

LONG_PRESS_DURATION = 1
SPEED_INCREASE_RATE = 0.02
URL = 'https://gametable-xolpakqy5q-ez.a.run.app/notsober'


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

            request = requests.get(f'{URL}/{random_led.color}')
            request.raise_for_status()

            speed_decrease = round_number * SPEED_INCREASE_RATE
            if speed_decrease >= self.answer_time_limit:
                speed_decrease = 0.1

            # random_led.led_high() # We don't want to turn on the led, leaving for debugging purposes

            delay_while = time.time() + self.answer_time_limit - speed_decrease

            game_continues = False
            while delay_while > time.time() and self.pairs.keep_running():
                self.pairs.press_low_not_pressed_high()
                # If the button is pressed and it is an active player or is not an active player, the game continues
                if random_led.is_button_pressed():
                    game_continues = True
                    break

            time.sleep(delay_while - time.time() if delay_while > time.time() else 0)
            random_led.led_low()
            if not game_continues:
                self.loser = random_led
                self.defeat()
                raise Exception("Main menu requested")  # Avoid too many requests to the server
                # self.initialize()
                # round_number = 0
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
                    active_colors.update({color: active_colors.get(color, 0) + DEFAULT_DEBOUNCE_TIME})
            self.pairs.debounce()
        self.active_players = [self.pairs.led_button_combinations[color] for color in active_colors.keys()]

    def detect_long_press(self, active_colors: dict) -> bool:
        # If any color has been pressed more than once, we start the game
        return any([press_time > LONG_PRESS_DURATION for press_time in active_colors.values()])

    def defeat(self):
        self.pairs.all_leds_low()
        request = requests.get(f'{URL}/LOSER')
        request.raise_for_status()
        self.loser.blink(10, 0.1)

    def celebrate(self):
        self.pairs.blink_all_leds(10, 0.1)
