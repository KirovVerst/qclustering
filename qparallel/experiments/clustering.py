__author__ = 'Azat Abubakirov'

from qparallel.experiments.logger import AbstractEvaluator
from qparallel.clustering.dbscan import DBScan


class DBScanEvaluator(DBScan, AbstractEvaluator):
    algorithm_name = 'db_scan'

    def _execute(self, **configuration):
        data = configuration['data']
        cpu_count = configuration['cpu_count']

        super(DBScanEvaluator, self)._execute(cpu_count=cpu_count, data_size=len(data))

        return self._estimate_execution_time(
            super(DBScanEvaluator, self),
            'fit', 'total_time',
            data=data, cpu_count=cpu_count
        )
