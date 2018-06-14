__author__ = 'Maria Khodorchenko'

def test_random():

    from qparallel.random_numbers import RandomGen

    gen = RandomGen(2)
    print(gen.n_proc)
    gen.generate_numbers(10, 1, 10)