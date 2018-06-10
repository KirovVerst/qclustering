__author__ = 'Maria Khodorchenko'

from pathos.multiprocessing import ProcessPool as Pool
import numpy as np
import random

from qparallel.helpers import (
    get_available_cpu_count,
    split_data
)

"""
Graph should be passed as list of weighted edges
in the form [node1, node2, weight]
Nodes numbering should begin from 0
"""


class AbstractGraphAlg:
    def __init__(self):
        self.data = None


class Graph:

    def __init__(self, x, n_proc=1):
        self.data = np.array(x)
        self.n_proc = n_proc
        self._calculate_adjacency_matrix()
        self._I = self._adjacency_matrix.copy()
        self._I[self._I == 0] = np.inf
        for i in range(len(self._I)):
            self._I[i, i] = 0

    def init_for_coloring(self):
        random.seed(42)
        elems = random.sample(range(10 * self.num_nodes), 10)
        self._neigh_dict = {}
        self._node_color_dict = {}
        for i in self.data:
            if i[0] in self._neigh_dict:
                self._neigh_dict[i[0]].append(i[1])
            else:
                self._node_color_dict[i[0]] = [elems[i[0]], 0]
                self._neigh_dict[i[0]] = [i[1]]

    def _calculate_adjacency_matrix(self):
        i, j, w = self.data[:, 0], self.data[:, 1], self.data[:, 2]
        self.num_nodes = max(max(set(i)), max(set(j))) + 1
        a = np.zeros(shape=(self.num_nodes, self.num_nodes))
        for i, j, w in zip(i, j, w):
            a[i, j] = w
        for i in range(self.num_nodes):
            a[i, i] = 0
        self._adjacency_matrix = a

    def _shortest(self, ind, k):
        tmp_array = [[0 for i in range(self.num_nodes)] for j in range(len(ind))]
        for i in range(len(ind)):
            for j in range(self.num_nodes):
                tmp_array[i][j] = min(self._I[ind[i], j], self._I[ind[i], k] + self._I[k, j])
        return tmp_array

    def _parallel(self, k):
        ind_list = [i for i in range(self.num_nodes)]
        ind = split_data(ind_list, self.n_proc)
        k = [k] * (len(ind) - 1)
        with Pool(self.n_proc) as pool:
            res = list(pool.map(self._shortest, ind, k))
        counter = 0
        for i in res:
            for j in i:
                self._I[counter] = j
                counter += 1
        return self

    def find_shortest_path(self):
        """
        Parallel Floyd's algorithm
        """
        for k in range(self.num_nodes):
            self._parallel(k)

    def _coloring(self, nodes):
        colored_nodes = []
        for node in nodes:
            # uncolored node
            flag = True
            neigh_nodes = self._neigh_dict[node]
            node_num = self._node_color_dict[node][0]
            for nnode in neigh_nodes:
                if self._node_color_dict[nnode][1] == 0:
                    if self._node_color_dict[nnode][0] > node_num:
                        flag = False
            if flag:
                colored_nodes.append(node)
        return colored_nodes

    def color_graph(self):
        """

        Jones-Plassmann Coloring

        Only for undirected graphs
        :return: list of lists [node, color]
        """
        self.init_for_coloring()
        u = self._neigh_dict.keys()
        color = 1
        while self._neigh_dict != {}:
            u = self._neigh_dict.keys()
            nodes_to_proc = split_data(list(u), self.n_proc)
            with Pool(self.n_proc) as pool:
                res = list(pool.map(self._coloring, nodes_to_proc))
            for i in res:
                if i != []:
                    self._node_color_dict[i[0]][1] = color
                    del self._neigh_dict[i[0]]
            color += 1
        coloring = {}
        for i in self._node_color_dict:
            coloring[i] = self._node_color_dict[i][1]
        return coloring
