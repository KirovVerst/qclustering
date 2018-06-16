__author__ = 'Maria Khodorchenko'


import os
from qparallel.experiments.graphs import (
    ColoringEvaluator,
    GraphRecord
)
from qparallel.experiments.logger import Logger
from scripts.config import RESULTS_DIR_PATH

from qparallel.helpers import (
    generate_full_graph
)

if __name__ == '__main__':
    cpus = 2
    graph = generate_full_graph(100)
    print(graph)
    configurations = [{'graph': graph, 'cpu_count': cpus}]
    iterations = 5
    evaluators = [ColoringEvaluator(graph, cpus)]
    logger = Logger(
        csv_file_path=os.path.join(RESULTS_DIR_PATH, 'graph_100_coloring_2.csv'),
        evaluators=evaluators,
        configurations=configurations,
        field_names=GraphRecord.field_names(),
        iterations=iterations
    )

    logger.start()
