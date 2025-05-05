import csv

# Paths to your files
first_file_path = 'Investor.csv'
second_file_path = 'unique_investor.csv'

def read_investor_names(file_path):
    """Read investor names from a CSV file and return as a set."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        names = {row[0].strip() for row in reader if row}  # Ensure no empty rows
    return names

# Read names from both files
first_file_names = read_investor_names(first_file_path)
second_file_names = read_investor_names(second_file_path)

# Find names in the second file but not in the first
new_names = second_file_names - first_file_names

# Append new names to the first file if there are any
if new_names:
    with open(first_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for name in new_names:
            writer.writerow([name])

print(f"Added {len(new_names)} new names to {first_file_path}.")
