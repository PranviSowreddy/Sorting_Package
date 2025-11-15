"""
Implements the SortingFactory class for the sorting package.
(Fix for C0114: Missing module docstring)
"""

import sys  
from typing import Literal

from .sorting_algorithms import (
    SortingAlgorithm, BubbleSort, SelectionSort,
    QuickSort, MergeSort, ShellSort, IntList
)


class SortingFactory:
    """
    4. A class which calls these various algorithms based on a parameter.
    """
    ALGORITHMS = {
        'bubble': BubbleSort(),
        'selection': SelectionSort(),
        'quick': QuickSort(),
        'merge': MergeSort(),
        'shell': ShellSort(),
    }

    def sort_data(self,
                 
                  algorithm_name: Literal['bubble', 'selection', 'quick',
                                          'merge', 'shell'],
                  data: IntList,
                  order: Literal['asc', 'desc'],
                  list_size: int = None
                  ) -> IntList:
        """
        Sorts the input list using the specified algorithm and order.
        ...
        """
        if algorithm_name not in self.ALGORITHMS:
            supported = ", ".join(self.ALGORITHMS.keys())
            raise ValueError(
                f"Unknown algorithm: {algorithm_name}. "
                f"Choose from: {supported}"
            )

        # (Fix for W0613: Added validation to use the 'list_size' argument)
        if list_size is not None and list_size != len(data):
            raise ValueError(
                f"List size mismatch: provided {list_size}, got {len(data)}"
            )

        if not all(isinstance(x, int) for x in data):
            raise TypeError("Input list must only contain integer data types.")

        sorter: SortingAlgorithm = self.ALGORITHMS[algorithm_name]
        print(f"Sorting {len(data)} elements using "
              f"**{algorithm_name.upper()}** in "
              f"**{order.upper()}** order...", file=sys.stderr)

        return sorter.sort(data, order)

