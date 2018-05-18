__author__ = 'Azat Abubakirov'


from qparallel.clustering.base import Model


class DBScan(Model):
    def __init__(self, eps=0.1, *args, **kwargs):
        super(DBScan, self).__init__(*args, **kwargs)
        self.eps = eps

    def pre_process(self, data):
        """

        :param data:
        :return:
        """
        pass

    def fit(self, data, cpu_count=-1, *args, **kwargs):
        """
        :param data: list of 2D-points. [[1,2], [3,4], ...]
        :param cpu_count:
        :param args:
        :param kwargs:
        :return:
        """
        pass
