import random
import string

def str_sequence():
    return random.sample(string.ascii_letters, 9)

def int_sequence():
    digits = []
    for digit in range(5):
        digits.append(str(random.randint(0,50)))
    return digits


sequence = (str_sequence() + int_sequence())

def create_sequence():
    random.shuffle(sequence)
    return "".join(sequence)
