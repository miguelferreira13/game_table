from itertools import permutations
import json


def generate_all_combinations():
    """
    This script generates all possible combinations of
    text, text colors and background colors for the color blind game.
    """
    restult = {}
    all_colors = ['red', 'blue', 'green', 'yellow', 'white']

    for correct_color in all_colors:

        # the text color is the correct color (text_color = correct_color)
        remaining_colors = list(filter(lambda x: x != correct_color, all_colors))
        all_permutations = list(permutations(remaining_colors, 2))

        for permutation in all_permutations:

            text = permutation[0]
            background_color = permutation[1]

            if correct_color not in restult.keys():
                restult[correct_color] = []

            restult[correct_color].append([text.upper(), correct_color, background_color])

    with open('color_blind_combinations.json', 'w') as f:
        f.write(json.dumps(restult))


if __name__ == "__main__":
    generate_all_combinations()
