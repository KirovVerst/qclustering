__author__ = 'Azat Abubakirov'

import pytest

DEFAULT_CPU_COUNT = 4


@pytest.mark.parametrize('cpu_count, expected_cpu_count', [
    (-1, DEFAULT_CPU_COUNT),
    (10, DEFAULT_CPU_COUNT),
    (2, 2)
])
def test_get_available_cpu_count(monkeypatch, cpu_count, expected_cpu_count):
    monkeypatch.setattr('multiprocessing.cpu_count', lambda: DEFAULT_CPU_COUNT)

    from qparallel.helpers import get_available_cpu_count

    assert get_available_cpu_count(cpu_count) == expected_cpu_count
