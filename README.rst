===========
QParallel
===========

Library of popular algorithms implemented in a parallel way

|travis| |coveralls| |license|

------------
Requirements
------------

Python 3.6

-------
Install
-------

.. code:: bash

    (venv)$ pip install -r requirements.txt

--------
Examples
--------
**Sorting algorithms** 

.. code:: python
    
    from random import random
    from qparallel.sorting import MergeSorting
    
    array = [random() for _ in range(100)]
    
    assert MergeSorting(ascending=True).sort(array, cpu_count=2) == sorted(array)
    assert MergeSorting(ascending=False).sort(array, cpu_count=2) == sorted(array, reverse=True)


----
Test
----

.. code:: bash

    (venv)$ flake8
    (venv)$ py.test

---------
Licensing
---------

The code in this project is licensed under MIT license.

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
    :target: https://raw.githubusercontent.com/kirovverst/qparallel/master/LICENSE
    :alt: Package license
.. |travis| image:: https://travis-ci.com/KirovVerst/qparallel.svg?branch=master
    :target: https://travis-ci.com/KirovVerst/qparallel
    :alt: CI status
.. |coveralls| image:: https://coveralls.io/repos/github/KirovVerst/qparallel/badge.svg?branch=master
    :target: https://coveralls.io/github/KirovVerst/qparallel?branch=master
