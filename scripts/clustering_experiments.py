__author__ = 'Azat Abubakirov'

import os

from sklearn.datasets.samples_generator import make_blobs
from qparallel.experiments.clustering import DBScanEvaluator

from qparallel.experiments.logger import Logger
from scripts.config import RESULTS_DIR_PATH

if __name__ == '__main__':
    centers = [[1, 1], [-1, -1], [1, -1], [-1, 1]]
    X, labels_true = make_blobs(n_samples=1000, centers=centers, cluster_std=0.4, random_state=0)

    configurations = [{'data': X, 'cpu_count': cpu_count} for cpu_count in [1, 2, 4]]

    iterations = 3

    evaluators = [
        DBScanEvaluator(eps=0.3, min_points=10)
    ]

    logger = Logger(
        csv_file_path=os.path.join(RESULTS_DIR_PATH, 'clustering.csv'),
        evaluators=evaluators,
        configurations=configurations,
        iterations=iterations
    )
    logger.start()
