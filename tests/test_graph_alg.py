__author__ = 'Maria Khodorchenko'


def test_split_data():
    from qparallel.graph import Graph

    graph = Graph([[0, 5], [1, 2], [2, 3], [3, 4]], n_proc=5)
    print(graph._adjacency_matrix)
    graph.find_shortest_path()
