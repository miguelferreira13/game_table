import yaml
from logger import logger
import os

CONFIG_FILE = os.path.abspath("config.yaml")


class Config:
    def __init__(self):
        try:
            with open(CONFIG_FILE, "r") as file:
                self.config = yaml.safe_load(file)
                self.port = self.config["API"]["PORT"]
                self.url = self.config["API"]["URL"]
                self.ws = self.config["API"]["WS"]
                self.ws_type = self.config["API"]["WS_TYPE"]
                self.color_blind_file = self.config["APP"]["COLOR_BLIND_FILE"]
                self.speed_increase_rate = self.config["APP"]["SPEED_INCREASE_RATE"]
                self.default_debounce_time = self.config["APP"]["DEFAULT_DEBOUNCE_TIME"]
                self.cancel_press_duration = self.config["APP"]["CANCEL_PRESS_DURATION"]
                self.long_press_duration = self.config["APP"]["LONG_PRESS_DURATION"]
                self.colors = list(
                    self.config["APP"]["BUTTON_LED_COMBINATIONS"].keys()
                )
                # LED and Button Pins
                self.red_led_pin = self.config["APP"]["BUTTON_LED_COMBINATIONS"]["RED"]["LED_PIN"]
                self.red_button_pin = self.config["APP"]["BUTTON_LED_COMBINATIONS"]["RED"]["BUTTON_PIN"]
                self.green_led_pin = self.config["APP"]["BUTTON_LED_COMBINATIONS"]["GREEN"]["LED_PIN"]
                self.green_button_pin = self.config["APP"]["BUTTON_LED_COMBINATIONS"]["GREEN"]["BUTTON_PIN"]
                self.blue_led_pin = self.config["APP"]["BUTTON_LED_COMBINATIONS"]["BLUE"]["LED_PIN"]
                self.blue_button_pin = self.config["APP"]["BUTTON_LED_COMBINATIONS"]["BLUE"]["BUTTON_PIN"]
                self.yellow_led_pin = self.config["APP"]["BUTTON_LED_COMBINATIONS"]["YELLOW"]["LED_PIN"]
                self.yellow_button_pin = self.config["APP"]["BUTTON_LED_COMBINATIONS"]["YELLOW"]["BUTTON_PIN"]
                self.white_led_pin = self.config["APP"]["BUTTON_LED_COMBINATIONS"]["WHITE"]["LED_PIN"]
                self.white_button_pin = self.config["APP"]["BUTTON_LED_COMBINATIONS"]["WHITE"]["BUTTON_PIN"]

        except FileNotFoundError:
            logger.exception(f"File not found: {CONFIG_FILE}")
        except KeyError as e:
            logger.exception(f"Parameter missing in config file: {e}")
        except Exception as e:
            logger.exception(f"Config error: {e}")


config = Config()
