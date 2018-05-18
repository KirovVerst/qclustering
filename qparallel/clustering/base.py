__author__ = 'Azat Abubakirov'

from qparallel.helpers import get_available_cpu_count


class Model:
    def __init__(self, cpu_count=-1, *args, **kwargs):
        self.cpu_count = cpu_count

    def fit(self, data, *args, **kwargs):
        raise NotImplementedError

    def pre_process(self, data, *args, **kwargs):
        return data

    @classmethod
    def split_data(cls, data, chunks_count=None):
        if chunks_count is None:
            chunks_count = get_available_cpu_count()

        data_size = len(data)
        chunk_size = int(data_size / chunks_count)
        rest = data_size % chunks_count
        left_border = 0
        chunks = []

        for i in range(chunks_count):
            current_chunk_size = chunk_size
            if rest > 0:
                current_chunk_size += 1
                rest -= 1

            chunks.append(data[left_border:left_border + current_chunk_size])
            left_border += current_chunk_size

        return chunks
