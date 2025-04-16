import pandas as pd

# Path to your CSV file
file_path = 'c:/Users/Karthik/Downloads/tree.csv'

# Load the data from the CSV file
data = pd.read_csv(file_path, sep=';')

# Specify the output Excel file path
output_file_path = 'c:/Users/Karthik/Downloads/tree_out.xlsx'

# Save the data to an Excel file
data.to_excel(output_file_path, index=False)

print(f"Excel file created successfully at {output_file_path}")

