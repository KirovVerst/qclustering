__author__ = 'Azat Abubakirov'


from qparallel.experiments.logger import AbstractEvaluator, Record
from qparallel.sorting import (
    AbstractSorting,
    MergeSorting,
    SelectSorting,
    QuickSorting
)


class SortingRecord(Record):
    def __init__(self, *args, **kwargs):
        self.merge_time = None  # datetime
        self.sort_time = None  # datetime
        super(Record, self).__init__(*args, **kwargs)

    @classmethod
    def field_names(cls):
        return Record.field_names() + ['sort_time', 'merge_time']


class AbstractSortingEvaluator(AbstractEvaluator, AbstractSorting):
    algorithm_name = 'abstract'
    record_class = SortingRecord

    def merge_sorted_arrays(self, sorted_arrays, cpu_count):
        merged_arrays = self._estimate_execution_time(super(AbstractSortingEvaluator, self),
                                                      'merge_sorted_arrays', 'merge_time',
                                                      sorted_arrays=sorted_arrays, cpu_count=cpu_count)
        return merged_arrays

    def sort_arrays(self, arrays, cpu_count):
        sorted_arrays = self._estimate_execution_time(super(AbstractSortingEvaluator, self),
                                                      'sort_arrays', 'sort_time',
                                                      arrays=arrays, cpu_count=cpu_count)
        return sorted_arrays

    def _execute(self, **configuration):
        array = configuration['array']
        cpu_count = configuration['cpu_count']

        self.record.algorithm_name = self.algorithm_name
        self.record.cpu_count = cpu_count
        self.record.data_size = len(array)

        return self._estimate_execution_time(self, 'sort', 'total_time', array=array, cpu_count=cpu_count)


class MergeSortingEvaluator(MergeSorting, AbstractSortingEvaluator):
    algorithm_name = 'merge_sorting'


class QuickSortingEvaluator(QuickSorting, AbstractSortingEvaluator):
    algorithm_name = 'quick_sorting'


class SelectSortingEvaluator(SelectSorting, AbstractSortingEvaluator):
    algorithm_name = 'select_sorting'
