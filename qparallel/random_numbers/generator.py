__author__ = 'Maria Khodorchenko'

from pathos.multiprocessing import ProcessPool as Pool
import os
import struct


class RandomGen:

    def __init__(self, num_of_proc=1):
        self.n_proc = num_of_proc

    def _gen(self, num):

        results = [0] * num
        location = 1
        free = num
        for i in range(num):
            skip = free + struct.unpack("<L", os.urandom(4))[0] + 1
            print(skip)
            while skip > 0:
                location = (location % num)
                if results[location] == 0:
                    skip -= 1
            results[location] = i
            free -= 1
        return [(self.high - self.dry) * generated + self.dry for generated in results]

    def generate_numbers(self, n, low_border, high_border):
        self.high = high_border
        self.dry = low_border
        num_of_nums = [int(n / self.n_proc)] * self.n_proc
        num_of_nums[-1] += self.n_proc - int(n / self.n_proc) * self.n_proc
        with Pool(self.n_proc) as pool:
            res = list(pool.map(self._gen, num_of_nums))
        flat_list = [item for sublist in res for item in sublist]
        print(" ".join([map(str, flat_list)]))
