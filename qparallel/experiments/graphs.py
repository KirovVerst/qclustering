__author__ = 'Maria Khodorchenko'

from qparallel.experiments.logger import AbstractEvaluator, Record
from qparallel.graph import (
    Graph
)


class GraphRecord(Record):
    def __init__(self, *args, **kwargs):
        self.shortest_time = None
        self.coloring_time = None
        super(Record, self).__init__(*args, **kwargs)

    @classmethod
    def field_names(cls):
        return Record.field_names() + ['shortest_time', 'coloring_time']


class AbstractGraphAlgEvaluator(AbstractEvaluator, Graph):
    algorithm_name = 'abstract'
    record_class = GraphRecord

    def _execute(self, **configuration):
        graph = configuration['graph']
        cpu_count = configuration['cpu_count']

        self.record.algorithm_name = self.algorithm_name
        self.record.cpu_count = cpu_count
        self.record.data_size = len(graph)

        return self._estimate_execution_time(self, 'color_graph', 'total_time')


class ShortestPathEvaluator(AbstractGraphAlgEvaluator, Graph):
    algorithm_name = 'shortest_path'


class ColoringEvaluator(AbstractGraphAlgEvaluator, Graph):
    algorithm_name = 'coloring'
