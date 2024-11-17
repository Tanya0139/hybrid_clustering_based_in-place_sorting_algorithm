import pandas as pd
import os

# Dictionary of dataset paths
datasets = {
    'uniform': r"C:\Users\mohit\Desktop\interleaved\result\averaged_result_sort_uniform.xlsx",
    'gaussian': r"C:\Users\mohit\Desktop\interleaved\result\averaged_result_sort_gaussian.xlsx",
    'ordered': r"C:\Users\mohit\Desktop\interleaved\result\averaged_result_sort_ordered.xlsx",
    'repeated_values': r"C:\Users\mohit\Desktop\interleaved\result\averaged_result_sort_repeated_values.xlsx",
    'reverse_ordered': r"C:\Users\mohit\Desktop\interleaved\result\averaged_result_sort_reverse_ordered.xlsx",
    'same_value': r"C:\Users\mohit\Desktop\interleaved\result\averaged_result_sort_same_value.xlsx"
}

# Analyze and compare sorting algorithms
def analyze_sort_performance(df):
    performance_comparison = []

    # Expected algorithm column names (focused on "Time" columns only)
    algo_list = [
        'Cluster Sort (Comb) Time', 'Cluster Sort (Shell) Time', 
        'Quick Sort Time', 'Merge Sort Time', 'Heap Sort Time'
    ]
    
    # Clean column names to avoid errors (strip whitespaces and replace spaces with underscores)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(' ', '_')
    
    # Adjust algo_list to match modified column names
    algo_list_cleaned = [algo.replace(' ', '_') for algo in algo_list]

    try:
        # Calculate mean for algorithms
        mean_times = df[algo_list_cleaned].mean()
    except KeyError as e:
        print(f"KeyError: {e}. Some columns are missing. Please check the column names.")
        return pd.DataFrame()

    # Create comparisons for each algorithm against each other
    for algo_base in algo_list_cleaned:
        comparisons = {'Algorithm': algo_base}
        for algo_compare in algo_list_cleaned:
            if algo_base != algo_compare:
                # Calculate the percentage difference
                comparisons[f'vs {algo_compare} (%)'] = (
                    (mean_times[algo_compare] - mean_times[algo_base]) / mean_times[algo_compare] * 100
                ) if mean_times[algo_base] < mean_times[algo_compare] else ''
        
        performance_comparison.append(comparisons)

    return pd.DataFrame(performance_comparison)

# Folder to save analysis results
output_folder = r"C:\Users\mohit\Desktop\interleaved\analysis"
os.makedirs(output_folder, exist_ok=True)

# Iterate over each dataset
for dataset_name, input_file in datasets.items():
    print(f"Processing dataset: {dataset_name}")

    # Load dataset from Excel file
    df = pd.read_excel(input_file)

    # Perform analysis
    comparison_df = analyze_sort_performance(df)
    
    # Store all results in one Excel sheet for each dataset
    output_file = os.path.join(output_folder, f"analysis_{dataset_name}.xlsx")
    if not comparison_df.empty:
        with pd.ExcelWriter(output_file) as writer:
            comparison_df.to_excel(writer, sheet_name='Performance Comparison', index=False)

    print(f"Analysis saved for {dataset_name} at {output_file}")

print("All datasets processed.")
