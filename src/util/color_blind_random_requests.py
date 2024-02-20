import requests
from random import choice
import time

colors = ['red', 'blue', 'green', 'yellow', 'white']
# url = 'http://127.0.0.1:8080/notsober/'
url = 'https://gametable-xolpakqy5q-ez.a.run.app/notsober/'

while True:
    color = choice(colors)
    print(color)
    requests.get(f'{url}{color}')
    time.sleep(3)
