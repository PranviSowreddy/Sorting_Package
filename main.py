#!/usr/bin/env python3

"""
Main script to showcase the sorting package.

This script reads command-line arguments to determine which sorting
algorithm and order to use. It reads a list of space-separated integers
from standard input (stdin) and prints the sorted list to standard
output (stdout).

All log messages are printed to standard error (stderr).

Usage:
    python main.py <algorithm_name> <order> < input.txt > output.txt

Example:
    python main.py quick asc < input.txt > quick_asc_output.txt
    python main.py merge desc < input.txt > merge_desc_output.txt
"""

import sys
from src.sorting_factory import SortingFactory  # Assuming 'sorting_factory.py' in 'src'

def main():
    """Main execution function."""
    
    # 1. --- Argument Parsing ---
    if len(sys.argv) != 3:
        # Print usage instructions to stderr
        print("Usage: python main.py <algorithm> <order>", file=sys.stderr)
        print("  <algorithm>: quick, merge, bubble, selection", file=sys.stderr)
        print("  <order>: asc, desc", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print("  python main.py quick asc < input.txt > output.txt", file=sys.stderr)
        sys.exit(1)

    algorithm_name = sys.argv[1].lower()
    order = sys.argv[2].lower()

    if order not in ['asc', 'desc']:
        print(f"Error: Invalid order '{order}'. Must be 'asc' or 'desc'.", file=sys.stderr)
        sys.exit(1)

    # 2. --- Read from Standard Input (stdin) ---
    try:
        # Read the entire input, strip whitespace, and split into numbers
        input_line = sys.stdin.read().strip()
        if not input_line:
            print("Error: Input is empty.", file=sys.stderr)
            sys.exit(1)
            
        # 8. Ensure all data is integer
        input_list = [int(x) for x in input_line.split()]
        list_size = len(input_list)
        
    except ValueError:
        print("Error: Input must be space-separated integers only.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    # 5. Check constraints (logging to stderr)
    if list_size > 200000:
        print(f"Warning: List size ({list_size}) exceeds 2x1e5.", file=sys.stderr)

    # 3. --- Log Processing Info to stderr ---
    print("-" * 50, file=sys.stderr)
    print(f"Processing sort request...", file=sys.stderr)
    print(f"  Algorithm: {algorithm_name}", file=sys.stderr)
    print(f"  Order:     {order}", file=sys.stderr)
    print(f"  List Size: {list_size}", file=sys.stderr)
    print("-" * 50, file=sys.stderr)

    # 4. --- Call the Sorter Factory ---
    try:
        factory = SortingFactory()
        
        # 6. Call the sort function with all parameters
        sorted_list = factory.sort_data(
            algorithm_name=algorithm_name,
            data=input_list,
            order=order,
            list_size=list_size
        )
    except ValueError as e:
        # Catch errors from the factory (e.g., "Algorithm not found")
        print(f"Sorting Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
        
    output_str = " ".join(map(str, sorted_list))
    print(output_str)

if __name__ == "__main__":
    main()