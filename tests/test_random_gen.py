__author__ = 'Maria Khodorchenko'


def test_random():
    from qparallel.random_numbers import RandomGen
    gen = RandomGen(2)

    assert len(gen.generate_numbers(10, 1, 10)) == 10
