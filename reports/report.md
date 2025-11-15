# Q3 Design and Test Case Report

This report details the code design for the Python sorting package and the rationale behind the test cases used to verify its correctness.

## 1. Code Design

The code is designed using the **Strategy Pattern**, which allows the main application to select a specific sorting algorithm at runtime. This design is clean, maintainable, and easily extensible.

### The Interface (Abstract Base Class)

As required by the prompt, a parent abstract base class (ABC) named `SortingAlgorithm` is the core of the design.

* **File:** `src/sorting_algorithms.py`
* **Purpose:** It defines a common "contract" or interface that all concrete sorting algorithms *must* follow.
* **Method:** It declares a single abstract method: `sort(self, data: list, order: str) -> list`.
    * `data`: The list of integers to sort.
    * `order`: A string ('asc' or 'desc') specifying the sort direction.
    * `Returns`: A **new** sorted list.

### Concrete Strategies (The Algorithms)

Each sorting algorithm (`BubbleSort`, `SelectionSort`, `QuickSort`, `MergeSort`) is implemented as a separate class.

* **Inheritance:** Each of these classes inherits from the `SortingAlgorithm` ABC.
* **Implementation:** Each class provides its own concrete implementation of the `sort()` method, fulfilling the contract.
* **Key Design Choice (Immutability):** A critical design decision, also verified by the test suite, is that the `sort()` method is **non-destructive**. It does not modify (mutate) the original list passed to it. Instead, it operates on a copy (e.g., `new_list = data.copy()`) and returns a *new* sorted list. This prevents unexpected side effects in the calling code.

### The Caller Class (Factory)

To fulfill item 4 of the prompt ("A class which calls these various algorithms"), a central `SortingFactory` class is used.

* **Purpose:** This class acts as the single entry point for the user. It holds a mapping (e.g., a dictionary) of algorithm names (like "bubble" or "quick") to their corresponding strategy class instances.
* **Method:** It has one main public method, `sort_data(...)`, which is responsible for:
    1.  **Validation:** Checking that the algorithm name is valid and that the list contains *only* integers (Requirement 8).
    2.  **Delegation:** Selecting the correct strategy object from its dictionary.
    3.  **Execution:** Calling that object's `sort()` method and returning the result to the user.

## 2. Test Case Rationale (using `unittest`)

The test script `test/test_sorting.py` uses Python's built-in `unittest` module to ensure all algorithms are correct and robust. The test cases were "reached" by considering all possible inputs, edge cases, and constraints.

### Test Structure

The test class `TestSortingAlgorithms` is structured for comprehensive coverage:

1.  **`setUp(self)`**: This method runs before each test. It initializes a "fresh" set of test lists (`self.test_lists`) and instances of all sorting algorithms (`self.algorithms`). This ensures that tests are independent.
2.  **`_test_sort_helper(self, ...)`**: This helper function contains the core test logic. It's called for every combination of algorithm, list, and order.
3.  **`subTest`**: The helper uses `self.subTest(...)` to run each combination as a distinct case. This is crucial: if one test fails (e.g., Bubble Sort on the 'reverse_sorted' list), the test run *continues*, and all other failures are reported at the end.

### How the Test Cases Were Reached

The `self.test_lists` dictionary was designed to cover all significant scenarios. The "ground truth" for correctness is always established by comparing the algorithm's output to Python's built-in `sorted()` function.

1.  **Edge Cases:**
    * `'empty': []`
    * `'single': [10]`
    * **Rationale:** These are the most basic cases. They test for `IndexError` or off-by-one errors that can occur in loops that don't correctly handle lists of length 0 or 1.

2.  **Best/Worst-Case Scenarios:**
    * `'already_sorted': [1, 2, 3, 4, 5]`
    * `'reverse_sorted': [5, 4, 3, 2, 1]`
    * **Rationale:** These test the algorithm's performance and correctness under extreme conditions. `'already_sorted'` is the best-case for an optimized Bubble Sort, while `'reverse_sorted'` is the worst-case for many, including naive Quick Sort.

3.  **Data-Specific Cases:**
    * `'all_duplicates': [2, 2, 2, 2]`
    * `'with_duplicates': [5, 2, 8, 2, 5, 1, 1, 8]`
    * `'negatives': [-5, -10, 0, 5, -2]`
    * **Rationale:** These cases ensure the comparison logic is sound. They verify that the algorithms are stable (if applicable), handle duplicates correctly, and can sort negative numbers and zero.


