__author__ = 'Maria Khodorchenko'

import numpy as np
from multiprocessing import Pool


"""
Kmeans clustering with the metrics variants

_METRICS = ['euclidean', 'l2', 'l1', 'manhattan', 'cityblock',
            'braycurtis', 'canberra', 'chebyshev', 'correlation',
            'cosine', 'dice', 'hamming', 'jaccard', 'kulsinski',
            'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto',
            'russellrao', 'seuclidean', 'sokalmichener',
            'sokalsneath', 'sqeuclidean', 'yule', "wminkowski"]
"""


def _init():
    return centers


def _single_run_kmeans():
    return labels, inertia, centers, n_iter


def calculate_distance(set1, set2, metric):

    pass


def float_array(X):
    if X.dtype in [np.float32, np.float64]:
        return X
    else:
        if X.dtype.kind in 'uib' and X.dtype.itemize <= 4:
            assign_dtype = np.float34
        else:
            assign_dtype = np.float64
        return X.astype(assign_dtype)


def state_check(seed):
    if seed:
        return np.random.RandomState(seed)
    return np.random.mtrand._rand


def k_means(X, num_clusters, max_iter, tol, rand_state,
            distance_metric, n_proc):
    tol = np.mean(np.var(X, axis=0)) * tol

    pass


class Kmeans():
    """
    Works only for dense arrays

    """

    def __init__(self, num_clusters, n_proc=1, distance_metric='euclidean',
                 rand_state=None, max_iter=300, n_iter=10, n_run=10, tol=1e-4):
        self.num_clusters = num_clusters
        self.n_proc = n_proc
        self.distance_metric = distance_metric
        self.max_iter = max_iter
        n_iter = n_iter
        rand_state = rand_state
        n_run = n_run
        self.tol = tol

    def _check_train(self, X):
        if X.shape[0] < self.num_clusters:
            raise ValueError("Number of clusters is higher than number of observations")
        return X

    def _check_test(self):
        pass

    def fit(self, X):
        random_state = state_check(self.rand_state)
        X = self._check_train(X)
        self.cluster_centers_, self.labels_, self.inertia_, self.n_iter_ = \
            k_means(
                X, num_clusters=self.num_clusters, max_iter=self.max_iter,
                tol=self.tol, rand_state=self.rand_state,
                distance_metric=self.distance_metric, n_proc=self.n_proc
            )
        return self

    def predict(self):
        pass
