__author__ = 'Azat Abubakirov'

import pytest

ASCENDING = True
DECREASING = False
ARRAYS = [
    range(10),
    range(10, -1, -1),
    [],
    [3, 4, 1, 5, 2, 6, 8, 2, 3, 4]
]
DEFAULT_CPU_COUNT = 2

SORTING_CLASS_NAMES = ['MergeSorting', 'SelectSorting', 'QuickSorting', 'BlockSorting']


@pytest.mark.parametrize('array_1, array_2, ascending, result', [
    (range(5), range(5, 10), ASCENDING, list(range(10))),
    (range(5, -1, -1), range(9, 5, -1), DECREASING, list(range(9, -1, -1))),
    (range(0, 10, 2), range(1, 10, 2), ASCENDING, list(range(10)))
])
def test_merge_two_sorted_arrays(array_1, array_2, ascending, result):
    from qparallel.sorting.algorithms import AbstractSorting

    sorting = AbstractSorting(ascending=ascending)

    assert sorting.merge_two_sorted_arrays(array_1, array_2) == result


def run_sort_one_array(sorting_class, array, ascending):
    sorting = sorting_class(ascending=ascending)
    assert sorting.sort_one_array(array=array) == sorted(array, reverse=not ascending)


def run_sort_array(sorting_class, array, ascending):
    sorting = sorting_class(ascending=ascending)
    assert sorting.sort(array=array) == sorted(array, reverse=not ascending)


@pytest.mark.parametrize('array', ARRAYS)
@pytest.mark.parametrize('ascending', [ASCENDING, DECREASING])
@pytest.mark.parametrize('sorting_class_name', SORTING_CLASS_NAMES)
def test_sorting(array, ascending, sorting_class_name, monkeypatch):
    monkeypatch.setattr('multiprocessing.cpu_count', lambda: DEFAULT_CPU_COUNT)

    import qparallel.sorting

    sorting_class = getattr(qparallel.sorting, sorting_class_name)
    run_sort_one_array(sorting_class, array, ascending)
    run_sort_array(sorting_class, array, ascending)


@pytest.mark.parametrize('array, step, arrays', [
    ([1, 2, 11, 12], 10, [[1, 2], [11, 12]]),
    ([1, 1, 1, 1, 3], 1, [[1, 1, 1, 1], [], [3]])
])
def test_block_sort_split_data(array, step, arrays):
    from qparallel.sorting.algorithms import BlockSorting
    assert BlockSorting._split_array(array=array, step=step) == arrays
