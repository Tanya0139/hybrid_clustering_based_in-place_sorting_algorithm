import pandas as pd
import time
import copy
import matplotlib.pyplot as plt
import os

# Helper function to check if an array is sorted
def is_sorted(arr):
    """Check if the array is sorted in non-decreasing order."""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

# In-Place Interleaved Cluster Sort with Shell Sort
def in_place_interleaved_cluster_sort_shell(arr, num_clusters=10):
    """In-place interleaved cluster sort using Shell Sort for sorting within clusters."""
    n = len(arr)
    if n == 0:
        return arr

    min_value = min(arr)
    max_value = max(arr)
    if max_value == min_value:
        return arr  

    cluster_size = (max_value - min_value) / num_clusters
    clusters = [[] for _ in range(int(num_clusters))]

    for value in arr:
        cluster_index = min(int((value - min_value) / cluster_size), num_clusters - 1)
        clusters[cluster_index].append(value)

    for cluster in clusters:
        if cluster:
            shell_sort(cluster)

    index = 0
    for cluster in clusters:
        for value in cluster:
            arr[index] = value
            index += 1

    return arr

# In-Place Interleaved Cluster Sort with Comb Sort
def in_place_interleaved_cluster_sort_comb(arr, num_clusters=10):
    """In-place interleaved cluster sort using Comb Sort for sorting within clusters."""
    n = len(arr)
    if n == 0:
        return arr

    min_value = min(arr)
    max_value = max(arr)
    if max_value == min_value:
        return arr

    cluster_size = (max_value - min_value) / num_clusters
    clusters = [[] for _ in range(int(num_clusters))]

    for value in arr:
        cluster_index = min(int((value - min_value) / cluster_size), num_clusters - 1)
        clusters[cluster_index].append(value)

    for cluster in clusters:
        if cluster:
            comb_sort(cluster)

    index = 0
    for cluster in clusters:
        for value in cluster:
            arr[index] = value
            index += 1

    return arr

# Optimized Shell Sort
def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

# Optimized Comb Sort
def comb_sort(arr):
    gap = len(arr)
    shrink_factor = 1.3
    sorted = False
    while not sorted:
        gap = int(gap / shrink_factor)
        if gap <= 1:
            gap = 1
            sorted = True
        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
    return arr

# Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Heap Sort
def heap_sort(arr):
    n = len(arr)

    # Build a maxheap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]   # swap
        heapify(arr, i, 0)
    
    return arr  # Return the sorted array

def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    left = 2 * i + 1
    right = 2 * i + 2

    # See if left child of root exists and is greater than root
    if left < n and arr[i] < arr[left]:
        largest = left

    # See if right child of root exists and is greater than root
    if right < n and arr[largest] < arr[right]:
        largest = right

    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
        heapify(arr, n, largest)

# Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Function for sorting time measurement and sorted check
def measure_sort_time(sort_func, arr, repetitions=10):
    total_time = 0.0
    correctly_sorted = True
    for _ in range(repetitions):
        copied_array = copy.deepcopy(arr)
        start_time = time.perf_counter()
        sorted_array = sort_func(copied_array)
        end_time = time.perf_counter()
        total_time += end_time - start_time
        correctly_sorted &= is_sorted(sorted_array)
    average_time = total_time / repetitions
    return round(average_time, 12), correctly_sorted

# Load the dataset from Excel sheet
input_file = r"C:\Users\mohit\Desktop\dsupdate - Copy.xlsx"
df = pd.read_excel(input_file)

# Create output folder
output_folder = r"C:\Users\mohit\Desktop\interleaved\result"
os.makedirs(output_folder, exist_ok=True)

# Iterate over each datatype (category)
datatypes = df['Category'].unique()
file_counter = 0

for datatype in datatypes:
    print(f"Processing datatype: {datatype}")
    datatype_df = df[df['Category'] == datatype]

    # Initialize a list to store individual file results
    results = []

    # Process each file in the datatype category
    for index, row in datatype_df.iterrows():
        file_path = row['Path']
        size = row['Size']
        category = row['Category']

        try:
            with open(file_path, "r") as file:
                array = [float(x) for x in file.read().split()]
        except FileNotFoundError:
            print(f"File not found: {file_path}. Skipping this entry.")
            continue
        except Exception as e:
            print(f"Error reading {file_path}: {e}. Skipping this entry.")
            continue

        # Measure sorting time and check if sorted
        time_cluster_shell, sorted_cluster_shell = measure_sort_time(in_place_interleaved_cluster_sort_shell, array)
        time_cluster_comb, sorted_cluster_comb = measure_sort_time(in_place_interleaved_cluster_sort_comb, array)
        time_merge_sort, sorted_merge_sort = measure_sort_time(merge_sort, array)
        time_quick_sort, sorted_quick_sort = measure_sort_time(quick_sort, array)
        time_heap_sort, sorted_heap_sort = measure_sort_time(heap_sort, array)

        # Append results for each file
        results.append({
            'Size': size,
            'Cluster Sort (Shell) Time': time_cluster_shell,
            'Cluster Sort (Shell) Sorted': sorted_cluster_shell,
            'Cluster Sort (Comb) Time': time_cluster_comb,
            'Cluster Sort (Comb) Sorted': sorted_cluster_comb,
            'Merge Sort Time': time_merge_sort,
            'Merge Sort Sorted': sorted_merge_sort,
            'Quick Sort Time': time_quick_sort,
            'Quick Sort Sorted': sorted_quick_sort,
            'Heap Sort Time': time_heap_sort,
            'Heap Sort Sorted': sorted_heap_sort
        })

        file_counter += 1
        print(f"{file_counter} files processed")

    # Convert the results to a DataFrame
    results_df = pd.DataFrame(results)

    # Group by 'Size' and calculate average times and sorted flags
    averaged_results = results_df.groupby('Size').agg({
        'Cluster Sort (Shell) Time': 'mean',
        'Cluster Sort (Shell) Sorted': 'all',
        'Cluster Sort (Comb) Time': 'mean',
        'Cluster Sort (Comb) Sorted': 'all',
        'Merge Sort Time': 'mean',
        'Merge Sort Sorted': 'all',
        'Quick Sort Time': 'mean',
        'Quick Sort Sorted': 'all',
        'Heap Sort Time': 'mean',
        'Heap Sort Sorted': 'all'
    }).reset_index()

    # Save averaged results to Excel
    output_file = os.path.join(output_folder, f"averaged_result_sort_{datatype}.xlsx")
    averaged_results.to_excel(output_file, index=False)

    # Plot the averaged sorting times on a logarithmic scale
    plt.figure(figsize=(10, 6))
    sizes = averaged_results['Size']
    plt.plot(sizes, averaged_results['Cluster Sort (Shell) Time'], label='Cluster Sort (Shell)', marker='o')
    plt.plot(sizes, averaged_results['Cluster Sort (Comb) Time'], label='Cluster Sort (Comb)', marker='o')
    plt.plot(sizes, averaged_results['Merge Sort Time'], label='Merge Sort', marker='o')
    plt.plot(sizes, averaged_results['Quick Sort Time'], label='Quick Sort', marker='o')
    plt.plot(sizes, averaged_results['Heap Sort Time'], label='Heap Sort', marker='o')

    plt.xlabel("Array Size")
    plt.ylabel("Average Time (s)")
    plt.yscale("log")  # Set y-axis to logarithmic scale
    plt.title(f"Average Sorting Algorithm Comparison - {datatype}")
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(output_folder, f"averaged_log_plot_sort_{datatype}.png"))
    plt.close()
