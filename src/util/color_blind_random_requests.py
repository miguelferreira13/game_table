import requests
from random import choice
import time
from logger import logger
from config import config

for _ in range(10):
    color = choice(config.colors)
    logger.info(f"Requesting color: {color}")
    requests.get(f'{config.url}/{color}')
    time.sleep(3)
