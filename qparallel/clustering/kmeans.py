__author__ = 'Maria Khodorchenko'

from qparallel.clustering.base import Model
import numpy as np
from pathos.multiprocessing import ProcessPool as Pool

from qparallel.helpers import (
    split_data
)


class KMeans(Model):
    """
    Currently supports only 2d arrays
    """

    def __init__(self, k, cpu_count=-1, distance_metric='euclidean',
                 max_iter=300, n_iter=10, tol=1e-4, verbose=0):
        """
        :param k: number of clusters
        :param n_proc: number of cpu
        :param distance_metric: optional, only euclidean is implementedd
        :param max_iter: optional, maximum number of iterations
        :param n_iter: optional, number of iterations
        :param tol: optional, tolerance value
        :param verbose: optional, print information
        """
        super(KMeans, self).__init__(cpu_count=cpu_count)
        self.k = k
        self.distance_metric = distance_metric
        self.max_iter = max_iter
        self.n_iter = n_iter
        self.tol = 1e-4
        self.verbose = verbose

    def _check_x(self, x):
        # restrict number of dims if needed
        if isinstance(x, list):
            return np.asarray(x)
        elif isinstance(x, np.ndarray):
            return x
        else:
            raise TypeError

    def _clusters_init(self, x):
        # change to get centers from chunks
        inx = np.random.choice(range(x.shape[0]), self.k, replace=False)
        self.cluster_centers = x[inx]

    def _proc_run(self, chunk):
        chunk = np.array(chunk)
        C = np.array([np.argmin([np.dot(x_i - y_k, x_i - y_k) for y_k in self.cluster_centers]) for x_i in chunk])
        centroids = []
        for i in range(self.k):
            if chunk[C == i].size == 0:
                centroids.append([np.nan, np.nan])
            else:
                centroids += [chunk[C == i].mean(axis=0).tolist()]
        return centroids

    def fit(self, data):
        """
        :param data: np.array
        :return:
        example:
        >>> array = np.array([[2, 3], [9, 8], [4, 9], [5, 2]])
        >>> model = KMeans(2,4)
        >>> model.fit(array)
        >>> print(model.labels)
        """
        x = data
        self._check_x(x)
        self.random_state = None
        chunks = split_data(x[x[:, 0].argsort()], 2)
        self._clusters_init(x)
        for i in range(self.n_iter):
            with Pool(self.n_proc) as pool:
                arrays = pool.map(self._proc_run, chunks)
            arrays = np.array(arrays)
            self.cluster_centers = np.array(np.nanmean(arrays, axis=0).tolist())
        self.labels = []
        for i in x:
            tmp = []
            for y in self.cluster_centers:
                tmp += [np.dot(i - y, i - y)]
            self.labels += [tmp.index(min(tmp))]

        return self
