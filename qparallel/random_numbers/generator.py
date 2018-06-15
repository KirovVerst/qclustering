__author__ = 'Maria Khodorchenko'

from pathos.multiprocessing import ProcessPool as Pool
import os
import struct
import numpy as np


class RandomGen:

    def __init__(self, num_of_proc=1):
        self.n_proc = num_of_proc

    def _gen(self, num):

        results = [0] * num
        location = 0
        free = num
        for i in range(num):
            skip = int(free * int(str(struct.unpack("<L", os.urandom(4))[0])[5]) + 1)
            while skip > 0:
                location = (location % (num - 1)) + 1
                try:
                    results[location]
                except:
                    break
                if results[location] == 0:
                    skip -= 1
            results[location] = i
            free -= 1
        return [(max(results) - i)/(max(results) - min(results)) for i in results]

    def generate_numbers(self, n, low_border, high_border):
        self.high = high_border
        self.dry = low_border
        num_of_nums = [int(n / self.n_proc)] * self.n_proc
        if n > 1:
            num_of_nums[-1] += n - int(n / self.n_proc) * self.n_proc
        print(num_of_nums)
        with Pool(self.n_proc) as pool:
            res = list(pool.map(self._gen, num_of_nums))
        flat_list = [item for sublist in res for item in sublist]
        print(" ".join([str(i) for i in flat_list]))
