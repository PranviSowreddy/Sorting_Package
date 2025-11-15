"""
Unit tests for the sorting algorithms.

This test script uses the 'unittest' module to verify the correctness
of all sorting algorithms (Bubble, Selection, Quick, Merge) against
a variety of test cases.
"""

import unittest
import random
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

try:
    # Attempt to import all necessary classes
    from Sorting_Package.src.sorting_algorithms import (
        BubbleSort, SelectionSort, QuickSort, MergeSort, SortingAlgorithm
    )
except ImportError:
    print("\nError: Could not import sorting algorithms.", file=sys.stderr)
    print("Please ensure 'sorting_algorithms.py' exists in 'Sorting_Package/src/'", file=sys.stderr)
    print("And that your project structure matches the comments in 'test_sorting.py'.", file=sys.stderr)
    sys.exit(1)


class TestSortingAlgorithms(unittest.TestCase):
    """
    Tests the 4 sorting algorithms (Bubble, Selection, Quick, Merge)
    to check for correctness.
    """
    
    def setUp(self):
        """Set up test data and algorithms before each test."""
        
        # A comprehensive set of test cases
        self.test_lists = {
            'empty': [],
            'single': [10],
            'small_unsorted': [5, 2, 8, 1, 9, 3],
            'medium_unsorted': [42, 11, 7, 99, 101, 15, 20, 77, 33, 6],
            'already_sorted': [1, 2, 3, 4, 5],
            'reverse_sorted': [5, 4, 3, 2, 1],
            'all_duplicates': [2, 2, 2, 2],
            'with_duplicates': [5, 2, 8, 2, 5, 1, 1, 8],
            'negatives': [-5, -10, 0, 5, -2],
            # 1000 elements for a quick but effective large test
            'large_random': [random.randint(-10000, 10000) for _ in range(1000)]
        }
        
        # Dictionary of all algorithms to be tested
        self.algorithms = {
            'BubbleSort': BubbleSort(),
            'SelectionSort': SelectionSort(),
            'QuickSort': QuickSort(),
            'MergeSort': MergeSort(),
        }

    def _test_sort_helper(self, sorter: SortingAlgorithm, test_list: list, order: str, list_name: str):
        """
        Helper function to run and assert a single test case.
        This uses subTests to report all failures, not just the first one.
        """
        
        # Use Python's built-in sorted() as the "ground truth"
        if order == 'asc':
            expected_list = sorted(test_list)
        else:
            expected_list = sorted(test_list, reverse=True)
            
        # Use subtest to identify which combination failed
        with self.subTest(algorithm=sorter.__class__.__name__, list_name=list_name, order=order):
            
            # Pass a copy to ensure the original is not modified
            original_copy = test_list.copy() 
            
            # --- The actual sort call ---
            result = sorter.sort(original_copy, order)
            
            # 1. Test for correctness
            self.assertEqual(result, expected_list, 
                             f"Sort failed for {list_name} in {order} order.")
            
            # 2. Test that the original list was not modified (if applicable)
            # Your SortingAlgorithm ABC should return a new list, not sort in-place.
            self.assertEqual(test_list, original_copy, 
                             "The original list was modified (mutated)!")

    def test_all_algorithms_all_cases(self):
        """
        Iterates through every algorithm and every test list,
        testing both ascending and descending orders.
        """
        for algo_name, sorter in self.algorithms.items():
            for list_name, test_list in self.test_lists.items():
                # Test both ascending and descending
                self._test_sort_helper(sorter, test_list, 'asc', list_name)
                self._test_sort_helper(sorter, test_list, 'desc', list_name)

    def test_type_enforcement(self):
        """Tests that a TypeError is raised for non-integer data."""
        sorter = self.algorithms['BubbleSort'] # Just need one instance
        
        with self.subTest(data_type="strings"):
            with self.assertRaises(TypeError, msg="Did not raise TypeError for strings"):
                sorter.sort([1, 2, 'a', 4], 'asc')
                
        with self.subTest(data_type="floats"):
            with self.assertRaises(TypeError, msg="Did not raise TypeError for floats"):
                sorter.sort([1, 2, 3.14, 4], 'asc')

        with self.subTest(data_type="mixed"):
            with self.assertRaises(TypeError, msg="Did not raise TypeError for mixed list"):
                sorter.sort([10, 'hello', 2.5], 'desc')

if __name__ == '__main__':
    unittest.main()