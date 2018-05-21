import numpy as np
from pathos.multiprocessing import ProcessPool as Pool
from qparallel.helpers import (
    get_available_cpu_count
)
from random import randint

# to add number of mertics
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import squareform

"""
Kmeans clustering with the metrics variants

"""

_METRICS = ['euclidean', 'l2', 'l1', 'manhattan', 'cityblock',
            'braycurtis', 'canberra', 'chebyshev', 'correlation',
            'cosine', 'dice', 'hamming', 'jaccard', 'kulsinski',
            'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto',
            'russellrao', 'seuclidean', 'sokalmichener',
            'sokalsneath', 'sqeuclidean', 'yule', "wminkowski"]


def squareform_2(X):
    if np.asarray(X, order='c').dtype != np.double:
        X = np.asarray(X, order='c').astype(np.double)
    else:
        X = np.asarray(X, order='c')
    s = X.shape
    d = s[0]
    v = np.zeros((d * (d - 1)) // 2, dtype=np.double)


def compute_matrix(X, y=None, metric='euclidean'):
    distances = pairwise_distances(X, y, metric)
    return squareform(distances)


def _k_init(X, num_clusters, random_state, metric):
    n_samples, n_features = X.shape
    centers = np.empty((num_clusters, n_features), dtype=X.dtype)
    n_local_trials = 2 + int(np.log(num_clusters))
    center_id = random_state.randint(n_samples)
    centers[0] = X[center_id]
    closest_dist_sq = compute_matrix(centers[0, np.newaxis], X, metric)
    current_pot = closest_dist_sq.sum()
    for c in range(1, num_clusters):
        rand_vals = random_state.random_sample(n_local_trials) * current_pot
        candidate_ids = np.searchsorted(np.cumsum(closest_dist_sq, axis=None, dtype=np.float64),
                                        rand_vals)
        distance_to_candidates = compute_matrix(X[candidate_ids], X, metric)
        best_candidate = None
        best_pot = None
        best_dist_sq = None
        for trial in range(n_local_trials):
            new_dist_sq = np.minimum(closest_dist_sq,
                                     distance_to_candidates[trial])
            new_pot = new_dist_sq.sum()
            if (best_candidate is None) or (new_pot < best_pot):
                best_candidate = candidate_ids[trial]
                best_pot = new_pot
                best_dist_sq = new_dist_sq
        centers[c] = X[best_candidate]
        current_pot = best_pot
        closest_dist_sq = best_dist_sq
    return centers


def state_check(seed):
    if seed:
        return np.random.RandomState(seed)
    return np.random.mtrand._rand


def _init_centroids(X, k, init, rand_state, x_squared_norms, metric, init_size=None):
    rand_state = state_check(rand_state)
    n_samples = X.shape[0]
    centers = _k_init(X, k, rand_state=rand_state, metric=metric)
    return centers


def _centers(X, labels, num_clusters, distances):
    n_samples = X.shape[0]
    n_features = X.shape[1]
    centers = np.zeros((num_clusters, n_features), dtype=np.float64)
    s_clust = np.bincount(labels, minlength=num_clusters)
    empty = np.where(s_clust == 0)[0]
    if len(empty):
        far = distances.argsort()[::-1]
        for i, ind in enumerate(empty):
            new_center = X[far[i]]
            centers[ind] = new_center
            s_clust[ind] = 1
    for i in range(n_samples):
        for j in range(n_features):
            centers[labels[i], j] += X[i, j]
    centers /= s_clust[:, np.newaxis]
    return centers


def _labels_inertia(X, x_squared_norms, centers, distances=None):
    store_distances = 0
    inertia = 0
    n_samples = X.shape[0]
    n_features = X.shape[1]
    n_clusters = centers.shape[0]
    labels = -np.ones(n_samples, np.int32)
    x_stride = X.strides[1]
    center_stride = centers.strides[1]
    center_squared_norms = np.zeros(n_clusters, dtype=np.float32)
    for center_idx in range(n_clusters):
        center_squared_norms[center_idx] = n_features * centers[center_idx, 0] * \
                                           center_stride * centers[center_idx, 0] *center_stride
    for sample_idx in range(n_samples):
        min_dist = -1
        for center_idx in range(n_clusters):
            dist = 0
            dist += (n_features*X[sample_idx,0],x_stride,
                     centers[center_idx,0],center_stride)
        dist *= -2
        dist += center_squared_norms[center_idx]
        dist += x_squared_norms[sample_idx]
        if min_dist == -1 or dist < min_dist:
            min_dist = dist
            labels[sample_idx] = center_idx
        if store_distances:
            distances[sample_idx] = min_dist
        inertia += min_dist

    return labels, inertia


def _single_run_kmeans(X, num_clusters, max_iter, n_run, tol, x_squared_norms, rand_state, metric):
    rand_state = state_check(rand_state)
    best_labels, best_inertia, best_centers = None, None, None
    centers = _init_centroids(X, num_clusters, n_run, random_state=rand_state,
                              x_squared_norms=x_squared_norms, metric=metric)
    distances = np.zeros(shape=(X.shape[0],), dtype=X.dtype)
    for i in range(max_iter):
        centers_old = centers.copy()
        labels, inertia = \
            _labels_inertia(X, x_squared_norms, centers,
                            distances=distances)

        centers = _centers(X, labels, num_clusters, distances)
        if best_inertia is None or inertia < best_inertia:
            best_labels = labels.copy()
            best_centers = centers.copy()
            best_inertia = inertia
        # may be a bug
        shift = centers_old - centers
        shift = np.ravel(shift, order='K')
        center_shift_total = np.dot(shift, shift)
        if center_shift_total <= tol:
            break
    if center_shift_total > 0:
        best_labels, best_inertia = \
            _labels_inertia(X, x_squared_norms, best_centers,
                            distances=distances)

    return best_labels, best_inertia, best_centers, i + 1


def float_array(X):
    if X.dtype in [np.float32, np.float64]:
        return X
    else:
        if X.dtype.kind in 'uib' and X.dtype.itemize <= 4:
            assign_dtype = np.float34
        else:
            assign_dtype = np.float64
        return X.astype(assign_dtype)


def k_means(X, num_clusters, n_run, max_iter, tol,
            rand_state, distance_metric, n_proc):
    tol = np.mean(np.var(X, axis=0)) * tol
    n_samples = X.shape[0]
    distances = (num_clusters * n_samples) < 12e6
    X_mean = X.mean(axis=0)
    #X -= X_mean
    norms = np.einsum('ij,ij->i', X, X)
    best_labels, best_inertia, best_centers = None, None, None
    if n_proc == 1:
        for i in range(n_run):
            labels, inertia, centers = _single_run_kmeans(
                X, num_clusters, max_iter=max_iter, n_run=n_run, distances=distances,
                tol=tol, x_squared_norms=norms, random_state=rand_state, metric=distance_metric
            )
            if best_inertia is None or inertia < best_inertia:
                best_labels = labels.copy()
                best_centers = centers.copy()
                best_inertia = inertia
    else:
        seeds = np.random.mtrand._rand.randint(np.iinfo(np.int32).max, size=n_run)
        with Pool(n_proc) as pool:
            results = list(pool.map(_single_run_kmeans, n_run=n_run, X=X, num_clusters=num_clusters,
                                    max_iter=max_iter, distances=distances,tol=tol,
                                    x_squared_norms=norms, random_state=rand_state, metric=distance_metric
                ))
        labels, inertia, centers, n_iters = zip(*results)
        best = np.argmin(inertia)
        best_labels = labels[best]
        best_inertia = inertia[best]
        best_centers = centers[best]
        best_n_iter = n_iters[best]
    X += X_mean
    best_centers += X_mean
    return best_centers, best_labels, best_inertia

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
        self.n_iter = n_iter
        self.rand_state = rand_state
        self.n_run = n_run
        self.tol = tol

    def fit(self, X):
        random_state = state_check(self.rand_state)
        self.cluster_centers_, self.labels_, self.inertia_, self.n_iter_ = \
            k_means(
                X, num_clusters=self.num_clusters, n_run=self.n_run, max_iter=self.max_iter,
                tol=self.tol, rand_state=self.rand_state,
                distance_metric=self.distance_metric, n_proc=self.n_proc
            )
        return self

    def predict(self):
        pass

    def transform(self):
        pass


X = np.array([[1, 2], [1, 4], [1, 0],[4, 2], [4, 4], [4, 0]])
kmeans = Kmeans(num_clusters=2, n_proc=2, rand_state=0).fit(X)
kmeans.labels_