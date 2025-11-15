"""
Implements a collection of sorting algorithms based on an abstract base class.

This module provides an abstract base class `SortingAlgorithm` and
several concrete implementations:
- BubbleSort
- SelectionSort
- QuickSort
- MergeSort
- ShellSort
"""

import abc
from typing import List, Literal

# Type alias for a list of integers
IntList = List[int]

class SortingAlgorithm(abc.ABC):
    """A parent abstract base class for sorting algorithms."""
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

    @staticmethod
    def _swap(data: IntList, i: int, j: int) -> None:
        """Helper for swapping elements."""
        data[i], data[j] = data[j], data[i]

    @staticmethod
    def _is_valid_input(data: List) -> None:
        """Checks if the input is a list of integers."""
        if not all(isinstance(x, int) for x in data):
            raise TypeError("Input list must only contain integer data types.")


class BubbleSort(SortingAlgorithm):
    """Implements the Bubble Sort algorithm."""
    def sort(self, data: IntList, order: Literal['asc', 'desc']) -> IntList:
        self._is_valid_input(data)
        num_items = len(data)
        # Work on a copy to avoid modifying the original list
        arr = data[:]

        def compare(a_val: int, b_val: int) -> bool:
            """Compares two values based on sort order."""
            if order == 'asc':
                return a_val > b_val
            # 'desc'
            return a_val < b_val

        for i in range(num_items):
            swapped = False
            for j in range(0, num_items - i - 1):
                # Compare adjacent elements
                if compare(arr[j], arr[j+1]):
                    self._swap(arr, j, j+1)
                    swapped = True
            if not swapped:
                break # Optimization for already sorted arrays
        return arr


class SelectionSort(SortingAlgorithm):
    """Implements the Selection Sort algorithm."""
    def sort(self, data: IntList, order: Literal['asc', 'desc']) -> IntList:
        self._is_valid_input(data)
        num_items = len(data)
        arr = data[:]

        def compare(a_val: int, b_val: int) -> bool:
            """Checks if a is the new extreme (min/max) value."""
            if order == 'asc':
                return a_val < b_val # Find minimum
            # 'desc'
            return a_val > b_val # Find maximum

        for i in range(num_items):
            # Assume the current index is the minimum/maximum
            extreme_idx = i
            for j in range(i + 1, num_items):
                # Check if we found a new minimum/maximum
                if compare(arr[j], arr[extreme_idx]):
                    extreme_idx = j

            # Swap the found minimum/maximum element with the element at position i
            self._swap(arr, i, extreme_idx)
        return arr


class QuickSort(SortingAlgorithm):
    """Implements the Quick Sort algorithm."""
    def sort(self, data: IntList, order: Literal['asc', 'desc']) -> IntList:
        self._is_valid_input(data)
        arr = data[:] # Use a copy
        self._quick_sort_recursive(arr, 0, len(arr) - 1, order)
        return arr

    def _partition(self, arr: IntList, low: int, high: int, order: str) -> int:
        pivot = arr[high]
        i = low - 1 # Index of smaller element

        def compare(a_val: int, b_val: int) -> bool:
            """Checks if element should be on the 'left' side of pivot."""
            if order == 'asc':
                return a_val <= b_val
            # 'desc'
            return a_val >= b_val

        for j in range(low, high):
            # If current element is smaller/greater than or equal to pivot
            if compare(arr[j], pivot):
                i = i + 1
                self._swap(arr, i, j)

        self._swap(arr, i + 1, high)
        return i + 1

    # Pylint is correct that this has many args, but they are all
    # necessary for the recursion. We disable the check.
    # pylint: disable=too-many-arguments
    def _quick_sort_recursive(self, arr: IntList, low: int, high: int, order: str) -> None:
        if low < high:
            # partition_index is partitioning index, arr[pi] is now at right place
            partition_index = self._partition(arr, low, high, order)

            # Separately sort elements before partition and after partition
            self._quick_sort_recursive(arr, low, partition_index - 1, order)
            self._quick_sort_recursive(arr, partition_index + 1, high, order)


class MergeSort(SortingAlgorithm):
    """Implements the Merge Sort algorithm."""
    def sort(self, data: IntList, order: Literal['asc', 'desc']) -> IntList:
        self._is_valid_input(data)
        arr = data[:] # Use a copy
        self._merge_sort_recursive(arr, 0, len(arr) - 1, order)
        return arr

    # Pylint is correct that this has many args, but they are all
    # necessary for the algorithm. We disable the check.
    # pylint: disable=too-many-arguments
    def _merge(self, arr: IntList, left: int, mid: int, right: int, order: str) -> None:
        left_size = mid - left + 1
        right_size = right - mid

        # Create temporary arrays
        left_half = arr[left : left + left_size]
        right_half = arr[mid + 1 : mid + 1 + right_size]

        left_idx = right_idx = 0  # Initial index of first and second subarrays
        merged_idx = left         # Initial index of merged subarray

        def compare(a_val: int, b_val: int) -> bool:
            """Checks if left-half value should be merged first."""
            if order == 'asc':
                return a_val <= b_val
            # 'desc'
            return a_val >= b_val

        while left_idx < left_size and right_idx < right_size:
            if compare(left_half[left_idx], right_half[right_idx]):
                arr[merged_idx] = left_half[left_idx]
                left_idx += 1
            else:
                arr[merged_idx] = right_half[right_idx]
                right_idx += 1
            merged_idx += 1

        # Copy the remaining elements of left_half[], if any
        while left_idx < left_size:
            arr[merged_idx] = left_half[left_idx]
            left_idx += 1
            merged_idx += 1

        # Copy the remaining elements of right_half[], if any
        while right_idx < right_size:
            arr[merged_idx] = right_half[right_idx]
            right_idx += 1
            merged_idx += 1

    # Pylint is correct that this has many args, but they are all
    # necessary for the recursion. We disable the check.
    # pylint: disable=too-many-arguments
    def _merge_sort_recursive(self, arr: IntList, left: int, right: int, order: str) -> None:
        if left < right:
            # Same as (left+right)//2, but avoids overflow
            mid = left + (right - left) // 2

            # Sort first and second halves
            self._merge_sort_recursive(arr, left, mid, order)
            self._merge_sort_recursive(arr, mid + 1, right, order)
            self._merge(arr, left, mid, right, order)

# --- NEWLY ADDED ALGORITHM ---

class ShellSort(SortingAlgorithm):
    """Implements the Shell Sort algorithm."""
    def sort(self, data: IntList, order: Literal['asc', 'desc']) -> IntList:
        self._is_valid_input(data)
        num_items = len(data)
        arr = data[:]
        gap = num_items // 2

        while gap > 0:
            for i in range(gap, num_items):
                # Add arr[i] to the elements that have been gap sorted
                temp = arr[i]
                j = i
                
                # --- Comparison Logic ---
                # Shift earlier gap-sorted elements up until the correct location
                # for arr[i] is found.
                if order == 'asc':
                    while j >= gap and arr[j - gap] > temp:
                        arr[j] = arr[j - gap]
                        j -= gap
                else: # 'desc'
                    while j >= gap and arr[j - gap] < temp:
                        arr[j] = arr[j - gap]
                        j -= gap
                # --- End Comparison ---

                # Put temp (the original arr[i]) in its correct location
                arr[j] = temp
            
            gap //= 2
            
        return arr