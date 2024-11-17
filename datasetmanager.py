import os
import pandas as pd

# List of folder paths
folders = [
    "/Users/admin/Desktop/archive/repeated_values",
    "/Users/admin/Desktop/archive/gaussian",
    "/Users/admin/Desktop/archive/uniform",
    "/Users/admin/Desktop/archive/same_value",
    "/Users/admin/Desktop/archive/Combinations_of_ascending_and_descending_two_sub_arrays",
    "/Users/admin/Desktop/archive/reverse_ordered",
    "/Users/admin/Desktop/archive/ordered"
]

# Initialize lists to store data
paths = []
sizes = []
categories = []

# Traverse through each specified folder
for folder in folders:
    category = os.path.basename(folder)  # Get the name of the folder as the category
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            # Extract size from the file name assuming format: <name>-input-<size>.txt
            try:
                size = file_name.split('-input-')[1].replace('.txt', '')
            except IndexError:
                size = "Unknown"  # In case the file name does not match the expected format
            paths.append(file_path)
            sizes.append(size)
            categories.append(category)

# Create a DataFrame from the collected data
df = pd.DataFrame({
    'Path': paths,
    'Size': sizes,
    'Category': categories
})

# Define the output Excel file path
output_file = os.path.expanduser("~/Desktop/dataset_summary.xlsx")

# Write the DataFrame to an Excel file
df.to_excel(output_file, index=False)

print(f"Dataset summary saved to {output_file}")
