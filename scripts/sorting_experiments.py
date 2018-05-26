__author__ = 'Azat Abubakirov'

import os
from qparallel.experiments.sorting import (
    BlockSortingEvaluator,
    MergeSortingEvaluator,
    SelectSortingEvaluator,
    SortingRecord
)
from qparallel.experiments.logger import Logger
from scripts.config import RESULTS_DIR_PATH

if __name__ == '__main__':
    configurations = [{'array': list(range(10000)), 'cpu_count': 2}]
    iterations = 10
    evaluators = [
        BlockSortingEvaluator(ascending=False),
        SelectSortingEvaluator(ascending=False),
        MergeSortingEvaluator(ascending=False)
    ]
    logger = Logger(
        csv_file_path=os.path.join(RESULTS_DIR_PATH, 'sorting.csv'),
        evaluators=evaluators,
        configurations=configurations,
        field_names=SortingRecord.field_names(),
        iterations=iterations
    )

    logger.start()
