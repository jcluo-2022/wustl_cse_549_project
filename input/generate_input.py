import os
from random import randint


def generate_input(exp):

    input_size = 2 ** int(exp)
    file_name = str(input_size) + ".txt"

    if os.path.exists("./input/" + file_name):

        return

    input_array = [randint(0, input_size) for x in range(0, input_size)]
    with open("./input/" + file_name, "w") as file:
        for num in input_array:
            file.write(str(num) + "\n")
