__author__ = 'Azat Abubakirov'

from pathos.multiprocessing import ProcessPool as Pool

from qparallel.helpers import (
    get_available_cpu_count,
    split_data
)


class AbstractSorting:
    def __init__(self, **kwargs):
        self.ascending = kwargs.get('ascending', True)

        def ascending_comp(x, y):
            return x < y

        def decreasing_comp(x, y):
            return x > y

        self.comparator = ascending_comp if self.ascending else decreasing_comp

    def _sort_one_array(self, array):
        raise NotImplementedError

    def merge_sorted_arrays(self, sorted_arrays, cpu_count):
        while len(sorted_arrays) > 1:
            if len(sorted_arrays) % 2 == 1:
                sorted_arrays.append([])

            arrays_pairs = list(map(lambda i: (sorted_arrays[i], sorted_arrays[i + 1]),
                                    range(0, len(sorted_arrays), 2)))

            with Pool(cpu_count) as pool:
                sorted_arrays = list(pool.map(self.merge_two_sorted_arrays, arrays_pairs))

        return sorted_arrays

    def merge_two_sorted_arrays(self, arrays):
        array_1, array_2 = arrays[0], arrays[1]

        merged_array = []

        index_1 = 0
        index_2 = 0

        size_1 = len(array_1)
        size_2 = len(array_2)

        while index_1 < size_1 and index_2 < size_2:
            if self.comparator(array_1[index_1], array_2[index_2]):
                merged_array.append(array_1[index_1])
                index_1 += 1
            else:
                merged_array.append(array_2[index_2])
                index_2 += 1

        while index_1 < size_1:
            merged_array.append(array_1[index_1])
            index_1 += 1

        while index_2 < size_2:
            merged_array.append(array_2[index_2])
            index_2 += 1

        return merged_array

    def sort_one_array(self, array):
        array = list(array)
        return self._sort_one_array(array)

    def sort_arrays(self, arrays, cpu_count):
        with Pool(cpu_count) as pool:
            sorted_arrays = pool.map(self._sort_one_array, arrays)

        return sorted_arrays

    def sort(self, array, cpu_count=-1):
        array = list(array)
        cpu_count = get_available_cpu_count(cpu_count)
        arrays = split_data(array, cpu_count)

        sorted_arrays = self.sort_arrays(arrays, cpu_count)

        merged_arrays = self.merge_sorted_arrays(sorted_arrays, cpu_count)

        return merged_arrays[0]


class MergeSorting(AbstractSorting):
    def _sort_one_array(self, array):
        array = list(array)

        array_size = len(array)

        if len(array) <= 1:
            return array

        array_1 = self._sort_one_array(array[:array_size // 2])
        array_2 = self._sort_one_array(array[array_size // 2:])

        return self.merge_two_sorted_arrays((array_1, array_2))


class SelectSorting(AbstractSorting):
    def _sort_one_array(self, array):
        array = list(array)

        selector = min if self.ascending else max

        for i in range(len(array)):
            index = i + array[i:].index(selector(array[i:]))
            array[index], array[i] = array[i], array[index]

        return array


class QuickSorting(AbstractSorting):
    def _partition(self, array, left, right):
        value = array[(left + right) // 2]

        while left <= right:
            while self.comparator(array[left], value):
                left += 1

            while self.comparator(value, array[right]):
                right -= 1

            if left <= right:
                array[left], array[right] = array[right], array[left]
                left += 1
                right -= 1

        return left

    def _quicksort(self, array, left, right):
        if len(array) <= 1:
            return array

        if left < right:
            index = self._partition(array, left, right)
            self._quicksort(array, left, index - 1)
            self._quicksort(array, index, right)

    def _sort_one_array(self, array):
        array = list(array)

        self._quicksort(array, 0, len(array) - 1)
        return array
