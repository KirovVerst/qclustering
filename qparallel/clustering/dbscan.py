__author__ = 'Azat Abubakirov'

import numpy as np

from pathos.multiprocessing import ProcessPool as Pool

from qparallel.clustering.base import Model
from qparallel.helpers import (
    get_available_cpu_count
)


class Point:
    def __init__(self, x, y, label=0, index=None):
        self.x = x
        self.y = y
        self.label = label
        self.index = index

    def __repr__(self):
        return 'Point(x={x}, y={y}, label={label})'.format(x=self.x, y=self.y, label=self.label)

    def to_list(self):
        return [self.x, self.y]

    def is_close(self, other, eps):
        return np.linalg.norm([other.x - self.x, other.y - self.y]) <= eps

    def __lt__(self, other):
        return self.x < other.x or self.x == other.x and self.y < other.y


class DBScan(Model):

    def __init__(self, eps=0.1, min_points=10, *args, **kwargs):
        super(DBScan, self).__init__(*args, **kwargs)
        self.eps = eps
        self.min_points = min_points

    def pre_process(self, data):
        """

        :param data:
        :return:
        """
        return list(sorted(map(lambda xy: Point(*xy), data)))

    def _get_neighbors(self, point, points):
        return list(filter(lambda other: point.is_close(other, self.eps), points))

    def _grow_cluster(self, point, points, neighbors, label):
        point.label = label
        i = 0
        while i < len(neighbors):
            neighbor = neighbors[i]
            if neighbor.label == -1:
                neighbor.label = label
            elif neighbor.label == 0:
                neighbor.label = label
                next_neighbors = self._get_neighbors(neighbor, points)

                if len(next_neighbors) >= self.min_points:
                    neighbors += next_neighbors

            i += 1

    def _clustering(self, points):
        """

        :param points: sorted list of Point objects
        :return:
        """
        label = 0
        for point in points:
            if not point.label != 0:
                continue

            neighbors = self._get_neighbors(point, points)

            if len(neighbors) < self.min_points:
                point.label = -1
            else:
                label += 1
                self._grow_cluster(point, points=points, neighbors=neighbors, label=label)
        return points

    def merge_two_clusters(self, cluster_1, cluster_2):
        """

        :param cluster_1: sorted list of Points objects
        :param cluster_2: sorted list of Points objects
        :return:
        """
        if len(cluster_1) == 0:
            return cluster_2

        if len(cluster_2) == 0:
            return cluster_1

        right_border = cluster_1[-1].x
        left_border = cluster_2[0].x

        right_points = list(filter(lambda p: abs(p.x - left_border) <= self.eps, cluster_1))
        left_points = list(filter(lambda p: abs(right_border - p.x) <= self.eps, cluster_2))

        for point in right_points:
            potential_neighbors = list(filter(lambda p: p.is_close(point, self.eps), left_points))
            for potential_neighbor in potential_neighbors:
                self.propagate_label(cluster_2, potential_neighbor.label, point.label)

        return cluster_1 + cluster_2

    @classmethod
    def propagate_label(cls, points, old_label, new_label):
        if old_label == new_label:
            return
        for point in points:
            if point.label == old_label:
                point.label = new_label

    def merge_clusters(self, clusters):
        if len(clusters) == 0:
            return clusters

        merged_clusters = clusters[0]

        for i in range(1, len(clusters)):
            merged_clusters = self.merge_two_clusters(merged_clusters, clusters[i])

        return merged_clusters

    def fit(self, data, cpu_count=-1, *args, **kwargs):
        """
        :param data: list of 2D-points. [[1,2], [3,4], ...]
        :param cpu_count:
        :param args:
        :param kwargs:
        :return:
        """
        data = self.pre_process(data)
        cpu_count = get_available_cpu_count(cpu_count)
        chunks = self.split_data(data, chunks=cpu_count)

        with Pool(cpu_count) as pool:
            clustered_chunks = pool.map(self._clustering, chunks)

        merged_clusters = self.merge_clusters(list(clustered_chunks))
        return merged_clusters
