__author__ = 'Azat Abubakirov'

import os
from qparallel.experiments.sorting import (
    QuickSortingEvaluator,
    SortingRecord
)
from qparallel.experiments.logger import Logger
from scripts.config import RESULTS_DIR_PATH

if __name__ == '__main__':
    n = 100000
    data = list(range(n))

    configurations = [
        {'array': data.copy(), 'cpu_count': 1},
        {'array': data.copy(), 'cpu_count': 2},
        {'array': data.copy(), 'cpu_count': 4}
    ]

    iterations = 10
    evaluators = [
        QuickSortingEvaluator(ascending=False)
    ]
    logger = Logger(
        csv_file_path=os.path.join(RESULTS_DIR_PATH, 'sorting.csv'),
        evaluators=evaluators,
        configurations=configurations,
        field_names=SortingRecord.field_names(),
        iterations=iterations
    )

    logger.start()
