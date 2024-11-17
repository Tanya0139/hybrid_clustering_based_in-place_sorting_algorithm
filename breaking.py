import pandas as pd
import time
import tracemalloc  # To measure space complexity
import copy  # To deep copy arrays
import csv  # Import CSV to handle CSV files

# Optimized Grouped Insertion Sort with Advanced Shell Sort Enhancements
def grouped_insertion_sort_shell_optimized(arr):
    n = len(arr)

    if n < 2:
        return arr  # Early exit for small arrays

    # Reverse ordered optimization: Detect if array is fully reversed and reverse it in O(n)
    if arr == sorted(arr, reverse=True):
        arr.reverse()
        return arr

    # Repeated values optimization: Handle blocks of repeated values more efficiently
    freq_map = {}
    for num in arr:
        freq_map[num] = freq_map.get(num, 0) + 1

    # If array is largely made up of a few repeated values, sort them once and skip further checks
    if max(freq_map.values()) > n // 2:
        unique_sorted_values = sorted(set(arr))
        i = 0
        for value in unique_sorted_values:
            count = freq_map[value]
            arr[i:i + count] = [value] * count
            i += count
        return arr

    # Use Sedgewick Gap Sequence for better optimization
    gaps = []
    k = 0
    while True:
        gap = 9 * 4 * k - 9 * 2 * k + 1
        if gap > n:
            break
        gaps.insert(0, gap)  # Insert gap into the list from largest to smallest
        k += 1

    # Perform Shell Sort with the Sedgewick gap sequence
    for gap in gaps:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            # Shift earlier gap-sorted elements up until the correct location for arr[i] is found
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp

    # Final pass to group duplicate values after Shell Sort
    # This groups blocks of repeated values together more efficiently
    i = 0
    while i < n - 1:
        if arr[i] == arr[i + 1]:
            j = i + 1
            # Move to the end of the block of duplicates
            while j < n and arr[j] == arr[i]:
                j += 1
            # If found a block, continue sorting within this group
            i = j
        else:
            i += 1

    return arr

# Standard Shell Sort Function
def shell_sort(arr):
    n = len(arr)
    gap = n // 2

    # Start with a large gap, then reduce the gap
    while gap > 0:
        # Perform a gapped insertion sort for this gap size
        for i in range(gap, n):
            temp = arr[i]
            j = i
            # Shift elements of arr[0..i-gap] that are greater than temp
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap = gap // 2  # Reduce the gap for the next iteration

    return arr

# Utility function for timing sorting in microseconds
def measure_sort_time(sort_func, arr):
    start_time = time.perf_counter()
    sort_func(arr)
    end_time = time.perf_counter()
    total_time = (end_time - start_time) * 1e6  # Convert to microseconds
    return round(total_time, 6)  # Return in microseconds

# Utility function for measuring memory usage
def measure_memory_usage(sort_func, arr):
    tracemalloc.start()  # Start memory tracking
    sort_func(arr)  # Run the sort
    current, peak = tracemalloc.get_traced_memory()  # Get memory usage
    tracemalloc.stop()  # Stop memory tracking
    return peak  # Return peak memory usage in bytes

# Load the transactional dataset
input_file = r"C:\Users\mohit\Desktop\good day\transactional_T10I4D100K (1).csv"

def load_transactional_data(file_path):
    array = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            array.extend(map(float, row))  # Convert each element to float
    return array

# Function to test at increasing data sizes
def test_with_increasing_size(array, sort_func, step=100000, max_size=None, time_limit=5.0, memory_limit=500e6):
    results = []
    counter = 0
    n = len(array)
    
    # Loop over progressively larger sizes
    for size in range(step, n + 1, step):
        if max_size and size > max_size:
            break
        subset = array[:size]  # Create a progressively larger subset of the data

        # Measure time
        sort_time = measure_sort_time(sort_func, subset)
        
        # Measure memory
        memory_usage = measure_memory_usage(sort_func, subset)
        
        # Record the results
        results.append({
            'Dataset Size': size,
            'Sort Time (µs)': sort_time,
            'Memory Usage (bytes)': memory_usage
        })

        print(f"Processed dataset of size {size}: Time = {sort_time} µs, Memory = {memory_usage} bytes")

        # Breaking condition: if time or memory exceeds the limits, break
        if sort_time > time_limit * 1e6:
            print(f"Breaking due to time limit at dataset size {size}")
            break
        if memory_usage > memory_limit:
            print(f"Breaking due to memory limit at dataset size {size}")
            break

    return results

# Load the dataset and run the tests
array = load_transactional_data(input_file)

# Run the test for grouped insertion sort and shell sort
grouped_results = test_with_increasing_size(array, grouped_insertion_sort_shell_optimized, step=100000, time_limit=5, memory_limit=500e6)
shell_results = test_with_increasing_size(array, shell_sort, step=100000, time_limit=5, memory_limit=500e6)

# Save the results to an Excel file
output_file = r"C:\Users\mohit\Desktop\good day\breaking_point_analysis.xlsx"
grouped_df = pd.DataFrame(grouped_results)
shell_df = pd.DataFrame(shell_results)
with pd.ExcelWriter(output_file) as writer:
    grouped_df.to_excel(writer, sheet_name='Grouped Insertion Sort', index=False)
    shell_df.to_excel(writer, sheet_name='Shell Sort', index=False)

print("Breaking point analysis saved to Excel.")
