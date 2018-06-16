__author__ = 'Azat Abubakirov'


class TestDBScan:
    def test_point_class(self):
        from qparallel.clustering.dbscan import Point
        assert Point(x=0, y=0) < Point(x=1, y=0)
        assert Point(x=0, y=0) < Point(x=0, y=1)

    def test_merge_two_clusters(self):
        from qparallel.clustering.dbscan import DBScan, Point
        p_1_1 = Point(x=0, y=0, label=1)
        p_1_2 = Point(x=0, y=1, label=1)
        p_1_3 = Point(x=0, y=10, label=3)
        chunk_1 = [p_1_1, p_1_2, p_1_3]

        p_2_1 = Point(x=1, y=0, label=2)
        p_2_2 = Point(x=1, y=1, label=2)
        p_2_3 = Point(x=0, y=11, label=4)
        chunk_2 = [p_2_1, p_2_2, p_2_3]

        first_cluster = [p_1_1, p_1_2, p_2_1, p_2_2]
        second_cluster = [p_1_3, p_2_3]

        model = DBScan(eps=1)
        model.merge_two_clusters(chunk_1, chunk_2)

        assert set(map(lambda p: p.label, first_cluster)) == {1}
        assert set(map(lambda p: p.label, second_cluster)) == {3}
