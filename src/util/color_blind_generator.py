from itertools import permutations
import json
from config import config

# Test other language
COLOR_TRANSLATIONS = {
        "EN": {
            "green": "green",
            "red": "red",
            "blue": "blue",
            "yellow": "yellow",
            "white": "white",
        },
        "EE": {
            "green": "roheline",
            "red": "punane",
            "blue": "sinine",
            "yellow": "kollane",
            "white": "valge",
        },
        "NL": {
            "green": "groen",
            "red": "rood",
            "blue": "blauw",
            "yellow": "geel",
            "white": "wit",
        },
        "PT": {
            "green": "verde",
            "red": "vermelho",
            "blue": "azul",
            "yellow": "amarelo",
            "white": "branco",
        },
        "HU": {
            "green": "zöld",
            "red": "piros",
            "blue": "kék",
            "yellow": "sárga",
            "white": "fehér",
        },
        "IT": {
            "green": "verde",
            "red": "rosso",
            "blue": "blu",
            "yellow": "giallo",
            "white": "bianco",
        },
        "RO": {
            "green": "verde",
            "red": "roșu",
            "blue": "albastru",
            "yellow": "galben",
            "white": "alb",
        },
        "PL": {
            "green": "zielony",
            "red": "czerwony",
            "blue": "niebieski",
            "yellow": "żółty",
            "white": "biały",
        },
        "FR": {
            "green": "vert",
            "red": "rouge",
            "blue": "bleu",
            "yellow": "jaune",
            "white": "blanc",
        },
        "IN": {
            "green": "hijau",
            "red": "merah",
            "blue": "biru",
            "yellow": "kuning",
            "white": "putih",
        }
}


def generate_combinations(coutry_code="EN"):
    """
    This script generates all possible combinations of
    text, text colors and background colors for the color blind game
    for a given language.
    """
    restult = {}
    all_colors = ['red', 'blue', 'green', 'yellow', 'white']

    for correct_color in all_colors:

        # the text color is the correct color (text_color = correct_color)
        remaining_colors = list(filter(lambda x: x != correct_color, all_colors))
        all_permutations = list(permutations(remaining_colors, 2))

        for permutation in all_permutations:

            text = COLOR_TRANSLATIONS[coutry_code][permutation[0]]
            background_color = permutation[1]

            if correct_color not in restult.keys():
                restult[correct_color] = []

            restult[correct_color].append([text.upper(), correct_color, background_color])
    return restult


if __name__ == "__main__":
    result = generate_combinations()
    with open(config.color_blind_file, 'w') as f:
        f.write(json.dumps(result))
