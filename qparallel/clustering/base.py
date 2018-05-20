__author__ = 'Azat Abubakirov'

from qparallel.helpers import (
    split_data
)


class Model:
    def __init__(self, cpu_count=-1, *args, **kwargs):
        self.cpu_count = cpu_count

    def fit(self, data, *args, **kwargs):
        raise NotImplementedError

    def pre_process(self, data, *args, **kwargs):
        return data

    @classmethod
    def split_data(cls, data, chunks=None):
        return split_data(data, chunks)
