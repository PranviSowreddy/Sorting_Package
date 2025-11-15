# sorting_factory.py
import sys  
from typing import Literal
from .sorting_algorithms import SortingAlgorithm, BubbleSort, SelectionSort, QuickSort, MergeSort, IntList

class SortingFactory:
    """
    4. A class which calls these various algorithms based on a parameter.
    """
    ALGORITHMS = {
        'bubble': BubbleSort(),
        'selection': SelectionSort(),
        'quick': QuickSort(),
        'merge': MergeSort(),
    }

    def sort_data(self,
                  algorithm_name: Literal['bubble', 'selection', 'quick', 'merge'],
                  data: IntList,
                  order: Literal['asc', 'desc'],
                  list_size: int = None
                  ) -> IntList:
        """
        Sorts the input list using the specified algorithm and order.
        ...
        """
        if algorithm_name not in self.ALGORITHMS:
            raise ValueError(f"Unknown algorithm: {algorithm_name}. Choose from: {', '.join(self.ALGORITHMS.keys())}")

        if not all(isinstance(x, int) for x in data):
            raise TypeError("Input list must only contain integer data types.")

        sorter: SortingAlgorithm = self.ALGORITHMS[algorithm_name]
      
        print(f"Sorting {len(data)} elements using **{algorithm_name.upper()}** in **{order.upper()}** order...", file=sys.stderr)

        return sorter.sort(data, order)