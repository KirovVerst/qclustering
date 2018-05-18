__author__ = 'Azat Abubakirov'


def test_split_data():
    from qparallel.clustering import Model
    data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    chunks = Model.split_data(data, 2)
    assert chunks[0] == [0, 1, 2, 3, 4]
    assert chunks[1] == [5, 6, 7, 8, 9]

    chunks = Model.split_data(data, 3)
    assert chunks[0] == [0, 1, 2, 3]
    assert chunks[1] == [4, 5, 6]
    assert chunks[2] == [7, 8, 9]
