import multiprocessing
import numpy as np


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

def kmeans():
    pass

def calculate_distance(set1, set2, metric):
    pass

class Kmeans():

    def __init__(self, num_clusters, n_proc=1, metric='eucl',max_iter=300, n_iter=10,
           n_run=10, tol=1e-4):

        """


        :param num_clusters:
        :param n_proc:
        :param metric:
        :param max_iter:
        :param n_iter:
        :param n_run:
        :param tol:
        """

        self.num_clusters = num_clusters
        self.max_iter = 300
        self.tol = tol
        self.n_proc = n_proc

    def fit(self):
        pass

    def predict(self):
        pass
