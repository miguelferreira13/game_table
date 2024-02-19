import RPi.GPIO as GPIO
import time
from random import choice
from logger import logger

DEFAULT_DEBOUNCE_TIME = 0.1
CANCEL_PRESS_DURATION = 2.3

GPIO.setmode(GPIO.BCM)


class ButtonLed:
    def __init__(self, color, button_pin, led_pin):
        self.color = color
        self.button_pin = button_pin
        self.led_pin = led_pin

        GPIO.setup(self.button_pin, GPIO.IN)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def led_high(self, duration_seconds=None):
        if duration_seconds:
            GPIO.output(self.led_pin, GPIO.HIGH)
            time.sleep(duration_seconds)
            GPIO.output(self.led_pin, GPIO.LOW)
        else:
            GPIO.output(self.led_pin, GPIO.HIGH)

    def led_low(self, duration_seconds=None):
        if duration_seconds:
            GPIO.output(self.led_pin, GPIO.LOW)
            time.sleep(duration_seconds)
            GPIO.output(self.led_pin, GPIO.HIGH)
        else:
            GPIO.output(self.led_pin, GPIO.LOW)

    def blink(self, n=10, duration_seconds=0.2):
        for _ in range(n):
            self.led_high(duration_seconds)
            self.led_low(duration_seconds)

    def is_button_pressed(self) -> bool:
        return GPIO.input(self.button_pin) == GPIO.HIGH


class ButtonLedPairs:

    def __init__(self):
        self.red = ButtonLed(color="red", button_pin=17, led_pin=4)
        self.yellow = ButtonLed(color="yellow", button_pin=6, led_pin=5)
        self.blue = ButtonLed(color="blue", button_pin=23, led_pin=24)
        self.white = ButtonLed(color="white", button_pin=25, led_pin=16)
        self.green = ButtonLed(color="green", button_pin=20, led_pin=21)
        self.led_button_combinations = {
            "red": self.red,
            "yellow": self.yellow,
            "blue": self.blue,
            "white": self.white,
            "green": self.green
        }

        self.red_pressed_duration = 0

    def get_button_states(self):
        return {color: pair.is_button_pressed() for color, pair in self.led_button_combinations.items()}

    def press_buttons_leds_high(self, duration_seconds=None):
        states = self.get_button_states()
        for color, state in states.items():
            if state:
                self.led_button_combinations[color].led_high(duration_seconds)

    def not_press_buttons_leds_low(self, duration_seconds=None):
        states = self.get_button_states()
        for color, state in states.items():
            if not state:
                self.led_button_combinations[color].led_low(duration_seconds)

    def press_low_not_pressed_high(self, duration_seconds=None):
        self.press_buttons_leds_high(duration_seconds)
        self.not_press_buttons_leds_low(duration_seconds)

    def all_leds_high(self, duration_seconds=None):
        for _, pair in self.led_button_combinations.items():
            pair.led_high(duration_seconds)

    def all_leds_low(self, duration_seconds=None):
        for _, pair in self.led_button_combinations.items():
            pair.led_low(duration_seconds)

    def blink_all_leds(self, n=10, duration_seconds=0.5):
        for _ in range(n):
            self.all_leds_high()
            time.sleep(duration_seconds)
            self.all_leds_low()
            time.sleep(duration_seconds)

    def get_random_led(self):
        return choice(list(self.led_button_combinations.values()))

    def cleanup(self):
        GPIO.cleanup()

    def debounce(self):
        time.sleep(DEFAULT_DEBOUNCE_TIME)

    def update_red_pressed_duration(self):
        if self.red.is_button_pressed():
            self.red_pressed_duration = self.red_pressed_duration + DEFAULT_DEBOUNCE_TIME
        else:
            self.red_pressed_duration = 0

    def keep_running(self) -> bool:
        self.debounce()
        self.update_red_pressed_duration()
        if self.red_pressed_duration > CANCEL_PRESS_DURATION:
            logger.debug("Exiting...")
            return False
        return True
