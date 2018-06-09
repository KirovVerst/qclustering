__author__ = 'Maria Khodorchenko'

import numpy as np


def test_graph_alg():
    from qparallel.graph import Graph

    graph = Graph([[0, 1, 8], [0, 2, 5], [1, 0, 3], [2, 1, 2]], n_proc=4)
    graph.find_shortest_path()
    print(graph._I)
    assert graph._I == [[0., 7., 5.], [3., 0., 8.], [5., 2., 0.]]
