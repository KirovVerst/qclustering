__author__ = 'Azat Abubakirov'

import csv
import datetime


class Record:
    def __init__(self, algorithm_name=None, cpu_count=None, data_size=None, total_time=None):
        self.algorithm_name = algorithm_name
        self.cpu_count = cpu_count
        self.data_size = data_size
        self.total_time = total_time

    @classmethod
    def field_names(cls):
        return ['algorithm_name', 'data_size', 'cpu_count', 'total_time']

    def to_list(self):
        return [getattr(self, field_name) for field_name in self.field_names()]


class AbstractEvaluator:
    record_class = Record

    def _execute(self, **kwargs):
        raise NotImplementedError

    def run(self, **configuration):
        self.record = self.record_class()
        self._execute(**configuration)
        return self.record.to_list()

    def _estimate_execution_time(self, obj, function_name, record_field, **arguments):
        start_time = datetime.datetime.now()
        result = getattr(obj, function_name)(**arguments)
        finish_time = datetime.datetime.now()
        setattr(self.record, record_field, finish_time - start_time)
        return result


class Logger:
    def __init__(self, csv_file_path, field_names, iterations, configurations, evaluators):
        """

        :param csv_file_path:
        :param field_names: ['algorithm', 'cpu_count', 'data_size', 'execution_time']
        :param iterations:
        :param configurations: [{'data': [1,2,3], 'cpu_count': 1, ...}]
        """
        self.path = csv_file_path
        self.field_names = field_names
        self.iterations = iterations
        self.configurations = configurations
        self.evaluators = evaluators

    def init_csv_file(self):
        with open(self.path, 'w') as fp:
            writer = csv.writer(fp, delimiter=',')
            writer.writerow(self.field_names)

    def write_records(self, records):
        with open(self.path, 'a') as fp:
            writer = csv.writer(fp, delimiter=',')
            for record in records:
                writer.writerow(record)

    def start(self, iteration_step_print=1):
        self.init_csv_file()
        for k, evaluator in enumerate(self.evaluators):
            print(evaluator.algorithm_name, '{}/{}'.format(k + 1, len(self.evaluators)))
            for i, configuration in enumerate(self.configurations):
                print('\tconfiguration: {}/{}'.format(i + 1, len(self.configurations)))
                records = []

                for j in range(self.iterations):
                    if j % iteration_step_print == 0:
                        print('\t\titeration: {}/{}'.format(j + 1, self.iterations))
                    records.append(evaluator.run(**configuration))

                self.write_records(records)
