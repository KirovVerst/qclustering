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

    def _shortest(self, chunk):
        for k in range(chunk.shape[0]):
            for i in range(chunk.shape[0]):
                for j in range(self.num_nodes):
                    chunk[i, j] = min(chunk[i, j], chunk[i, k] + chunk[k, j])
        return np.array(chunk)

    def find_shortest_path(self):
        """
        Parallel Floyd's algorithm
        """
        I = self._adjacency_matrix.copy()
        I[I == 0] = np.inf
        ind = np.array([i for i in range(self.num_nodes)])
        ind = split_data(ind, self.n_proc)
        chunks = split_data(I, self.n_proc)
        with Pool(self.n_proc) as pool:
            res = list(pool.map(self._shortest, chunks))
        com_res = res[0]
        for i in range(1,len(res)):
            com_res = np.append(com_res, res[i],axis=0)
        return com_res

    def _coloring(self):
        pass

    def color_graph(self):
        """
        Jones-Plassmann Coloring
        """
        rand_assign = {}
        nodes = self.data.flatten()
        # len_nodes
        # for i in range(len(set(nodes))):
        #     random_assign[i] =


if __name__ == "__main__":
    graph = Graph([[0, 5], [1, 2], [2, 3], [3, 4], [5, 0], [2, 1], [3, 2], [4, 3], [3, 0], [0, 3]], n_proc=2)
    print(graph._adjacency_matrix)
    print(graph.find_shortest_path())
    print(graph.color_graph())

