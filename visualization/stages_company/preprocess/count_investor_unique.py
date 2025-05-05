import csv
from collections import OrderedDict

input_file_path = 'updated_company_invested.csv'
output_file_path = 'updated1_company_invested.csv'
unique_companies_file_path = 'unique_companies.csv'

# Step 1: Read the CSV and process the data
unique_companies = OrderedDict()

with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile, \
        open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        # Split the company names and count them
        companies = [company.strip() for company in row[1].split(';') if company.strip()]
        company_count = len(companies)
        row.append(company_count)
        writer.writerow(row)
        # Add companies to the unique list
        for company in companies:
            unique_companies[company] = None  # Using None as a placeholder value

# Step 2: Save the unique companies to a new CSV
with open(unique_companies_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for company in unique_companies.keys():
        writer.writerow([company])

print("Processing complete. Check the output and unique companies files.")
