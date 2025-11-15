import abc
from typing import List, Literal, TypeVar

# Define a type variable constrained to int for type hinting
IntList = List[int]

class SortingAlgorithm(abc.ABC):
    """
    1. A parent abstract base class for sorting algorithms.
    """
    @abc.abstractmethod
    def sort(self, data: IntList, order: Literal['asc', 'desc']) -> IntList:
        """
        Sorts the input list of integers.

        Args:
            data: The list of integers to sort.
            order: 'asc' for ascending, 'desc' for descending.

        Returns:
            A new, sorted list.
        """
        pass

    def _swap(self, data: IntList, i: int, j: int) -> None:
        """Helper for swapping elements."""
        data[i], data[j] = data[j], data[i]

    def _is_valid_input(self, data: List) -> None:
        """Checks if the input is a list of integers."""
        if not all(isinstance(x, int) for x in data):
            raise TypeError("Input list must only contain integer data types.")


class BubbleSort(SortingAlgorithm):
    """2. Implements Bubble Sort."""
    def sort(self, data: IntList, order: Literal['asc', 'desc']) -> IntList:
        self._is_valid_input(data)
        n = len(data)
        # Work on a copy to avoid modifying the original list
        arr = data[:]

        # Helper function for comparison
        def compare(a, b):
            if order == 'asc':
                return a > b
            else: # 'desc'
                return a < b

        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                # Compare adjacent elements
                if compare(arr[j], arr[j+1]):
                    self._swap(arr, j, j+1)
                    swapped = True
            if not swapped:
                break # Optimization for already sorted arrays
        return arr


class SelectionSort(SortingAlgorithm):
    """2. Implements Selection Sort."""
    def sort(self, data: IntList, order: Literal['asc', 'desc']) -> IntList:
        self._is_valid_input(data)
        n = len(data)
        arr = data[:]

        # Helper function for comparison
        def compare(a, b):
            if order == 'asc':
                return a < b # Find minimum
            else: # 'desc'
                return a > b # Find maximum

        for i in range(n):
            # Assume the current index is the minimum/maximum
            extreme_idx = i
            for j in range(i + 1, n):
                # Check if we found a new minimum/maximum
                if compare(arr[j], arr[extreme_idx]):
                    extreme_idx = j

            # Swap the found minimum/maximum element with the element at position i
            self._swap(arr, i, extreme_idx)
        return arr


class QuickSort(SortingAlgorithm):
    """2. Implements Quick Sort."""
    def sort(self, data: IntList, order: Literal['asc', 'desc']) -> IntList:
        self._is_valid_input(data)
        arr = data[:] # Use a copy
        self._quick_sort_recursive(arr, 0, len(arr) - 1, order)
        return arr

    def _partition(self, arr: IntList, low: int, high: int, order: str) -> int:
        pivot = arr[high]
        i = low - 1 # Index of smaller element

        # Helper function for comparison
        def compare(a, b):
            if order == 'asc':
                return a <= b
            else: # 'desc'
                return a >= b

        for j in range(low, high):
            # If current element is smaller/greater than or equal to pivot
            if compare(arr[j], pivot):
                i = i + 1
                self._swap(arr, i, j)

        self._swap(arr, i + 1, high)
        return i + 1

    def _quick_sort_recursive(self, arr: IntList, low: int, high: int, order: str) -> None:
        if low < high:
            # pi is partitioning index, arr[pi] is now at right place
            pi = self._partition(arr, low, high, order)

            # Separately sort elements before partition and after partition
            self._quick_sort_recursive(arr, low, pi - 1, order)
            self._quick_sort_recursive(arr, pi + 1, high, order)


class MergeSort(SortingAlgorithm):
    """2. Implements Merge Sort."""
    def sort(self, data: IntList, order: Literal['asc', 'desc']) -> IntList:
        self._is_valid_input(data)
        arr = data[:] # Use a copy
        self._merge_sort_recursive(arr, 0, len(arr) - 1, order)
        return arr

    def _merge(self, arr: IntList, l: int, m: int, r: int, order: str) -> None:
        n1 = m - l + 1
        n2 = r - m

        # Create temporary arrays
        L = arr[l : l + n1]
        R = arr[m + 1 : m + 1 + n2]

        i = j = 0  # Initial index of first and second subarrays
        k = l      # Initial index of merged subarray

        # Helper function for comparison
        def compare(a, b):
            if order == 'asc':
                return a <= b
            else: # 'desc'
                return a >= b

        while i < n1 and j < n2:
            if compare(L[i], R[j]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Copy the remaining elements of L[], if any
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1

        # Copy the remaining elements of R[], if any
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1


    def _merge_sort_recursive(self, arr: IntList, l: int, r: int, order: str) -> None:
        if l < r:
            # Same as (l+r)//2, but avoids overflow for large l and r
            m = l + (r - l) // 2

            # Sort first and second halves
            self._merge_sort_recursive(arr, l, m, order)
            self._merge_sort_recursive(arr, m + 1, r, order)
            self._merge(arr, l, m, r, order)