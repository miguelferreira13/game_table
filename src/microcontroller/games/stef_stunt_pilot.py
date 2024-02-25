from games.base_game import BaseGame, MAIN_MENU_REQUESTED
from microcontroller.button_led_pairs import ButtonLed
import time
from typing import List
from config import config


class StefStuntPilot(BaseGame):
    def __init__(self):
        super().__init__()
        self.name = "Stef Stunt Pilot"
        self.initial_speed = 1.3  # Initial speed of the game in seconds
        self.active_players: List[ButtonLed] = []
        self.loser: ButtonLed = None

    def play(self):
        self.initialize()
        time.sleep(1)  # Wait for the user to release the button
        round_number = 0
        all_leds = list(self.pairs.led_button_combinations.values())
        led_iterator = (led for _ in range(500) for led in all_leds)

        while self.pairs.keep_running():
            # Make sure no one is pressing the button in the beginning of the round
            for led in self.active_players:
                if led.button_state():
                    if led.color == "red":  # If the red button is pressed, assume we want main menu
                        time.sleep(0.5)  # Wait for the user to release the button
                        if led.button_state():
                            raise Exception(MAIN_MENU_REQUESTED)
                    self.loser = led
                    self.defeat()
                    self.initialize()
                    round_number = 0
                    break
            game_continues = False

            next_led = next(led_iterator)

            if (round_number * config.speed_increase_rate) < self.initial_speed:
                speed_decrease = round_number * config.speed_increase_rate

            next_led.led_high()
            delay_while = time.time() + self.initial_speed - speed_decrease
            while delay_while > time.time() and self.pairs.keep_running():
                for led in self.active_players:
                    if led.button_state() and led != next_led:
                        self.loser = led
                        self.defeat()
                        self.initialize()
                        round_number = 0
                        break
                # If the button is pressed and it is an active player or is not an active player, the game continues
                if (next_led.button_state() and
                    next_led in self.active_players) or \
                        next_led not in self.active_players:
                    game_continues = True

            next_led.led_low()
            if not game_continues:
                self.loser = next_led
                self.defeat()
                self.initialize()
                round_number = 0
            round_number += 1

    def initialize(self):
        time.sleep(0.5)  # Wait for the user to release the button
        self.pairs.all_leds_low()
        self.get_active_palyers_colors()
        self.pairs.all_leds_low()
        time.sleep(1)  # Wait for the user to release the button

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
        self.loser.blink(10, 0.1)

    def celebrate(self):
        self.pairs.blink_all_leds(10, 0.1)
