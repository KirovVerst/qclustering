__author__ = 'Maria Khodorchenko'

from pathos.multiprocessing import ProcessPool as Pool
import numpy as np

from qparallel.helpers import (
    get_available_cpu_count,
    split_data
)

"""
graph should be passed as list of weighted edges
in the form [node1, node2, weight]
nodes are counted from 0
"""


class Graph:

    def __init__(self, x, n_proc=1):
        self.data = np.array(x)
        self.n_proc = n_proc
        self._calculate_adjacency_matrix()
        self._I = self._adjacency_matrix.copy()
        self._I[self._I == 0] = np.inf
        for i in range(len(self._I)):
            self._I[i, i] = 0


    def _calculate_adjacency_matrix(self):
        i, j, w = self.data[:, 0], self.data[:, 1], self.data[:, 2]
        self.num_nodes = max(max(set(i)), max(set(j))) + 1
        a = np.zeros(shape=(self.num_nodes, self.num_nodes))
        for i, j, w in zip(i, j, w):
            a[i, j] = w
        for i in range(self.num_nodes):
            a[i, i] = 0
        self._adjacency_matrix = a

    def process_distances(self):
        raise NotImplementedError

    def _shortest(self, ind, k):
        print(ind, k)
        tmp_array = [[0 for i in range(self.num_nodes)] for j in range(len(ind))]
        #tmp_array = np.zeros(shape=(len(ind), self.num_nodes))
        for i in range(len(ind)):
            for j in range(self.num_nodes):
                if (self._I[ind[i]][k] != np.inf and self._I[k][j] != np.inf):
                    tmp_array[i][j] = min(self._I[ind[i], j], self._I[ind[i], k] + self._I[k, j])
        return tmp_array

    def _parallel(self, k):
        k = [k] * (self.n_proc - 1)
        ind_list = [i for i in range(self.num_nodes + 1)]
        ind = split_data(ind_list, self.n_proc)
        with Pool(self.n_proc) as pool:
            res = list(pool.map(self._shortest, ind, k))
        print('SELF', res)
        return self

    def find_shortest_path(self):
        """
        Parallel Floyd's algorithm
        """
        for k in range(self.num_nodes):
            self._parallel(k)

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
