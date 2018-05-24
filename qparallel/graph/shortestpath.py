__author__ = 'Maria Khodorchenko'

from pathos.multiprocessing import ProcessPool as Pool
import numpy as np

from qparallel.helpers import (
    get_available_cpu_count,
    split_data
)

"""
graph should be passed as list of unweighted edges
nodes are counted from 0
"""


def chunks_with_indixes(data, n_proc):
    inx = [i for i in range(len(data))]
    inx = split_data(inx, n_proc)
    chunks = split_data(data, n_proc)
    for i in range(len(chunks)):
        tmp = np.zeros(shape=(len(data)))
        for j in inx[i]:
            tmp[j] = 1
        chunks[i] = np.append(chunks[i], [tmp], axis=0)
        print(chunks[1])
    return chunks


class Graph:

    def __init__(self, x, n_proc=1):
        self.data = np.array(x)
        self.n_proc = n_proc
        self._calculate_adjacency_matrix()

    def _calculate_adjacency_matrix(self):
        i, j = self.data[:, 0], self.data[:, 1]
        self.num_nodes = max(max(set(i)), max(set(j))) + 1
        a = np.zeros(shape=(self.num_nodes, self.num_nodes))
        for i, j in zip(i, j):
            a[i, j] = 1
        self._adjacency_matrix = a

    def process_distances(self):
        raise NotImplementedError

    def find_shortest_path(self):
        """
        Parallel Floyd's algorithm
        """
        self._I = np.zeros(shape=(self.num_nodes, self.num_nodes))
        chunks = split_data(self._adjacency_matrix, self.n_proc)
        chunks = chunks_with_indixes(self._adjacency_matrix, self.n_proc)
        print(chunks)
        with Pool(self.n_proc) as pool:
            pass

    # for k in range(n_proc-1):
    #     for i in range()
    # pass

    def color_graph(self):
        raise NotImplementedError


graph = Graph([[0, 5], [1, 2], [2, 3], [3, 4]], n_proc=5)
print(graph._adjacency_matrix)
graph.find_shortest_path()
