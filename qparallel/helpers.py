__author__ = 'Azat Abubakirov'

import multiprocessing


def get_available_cpu_count(cpu_count=-1):
    max_cpu_count = multiprocessing.cpu_count()
    return max_cpu_count if cpu_count == -1 or cpu_count > max_cpu_count else cpu_count
