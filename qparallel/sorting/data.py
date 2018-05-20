__author__ = 'Azat Abubakirov'

from random import random


def generate(size, path_to_file=None):
    if path_to_file:
        with open(path_to_file, 'w') as f:
            f.write(' '.join(map(lambda _: str(random()), range(size))))
    else:
        return [random() for _ in range(size)]
