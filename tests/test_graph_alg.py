__author__ = 'Maria Khodorchenko'


def test_graph_alg():
    from qparallel.graph import Graph

    graph = Graph([[0, 1, 8], [0, 2, 5], [2, 0, 4], [1, 0, 3], [2, 1, 2], [1, 2, 3], [2, 3, 1], [3, 2, 2]], n_proc=3)
    graph.find_shortest_path()
    print(graph._I)
    # assert graph._I.tolist() == [[0., 7., 5.], [3., 0., 8.], [5., 2., 0.]]
    print(graph.color_graph())
