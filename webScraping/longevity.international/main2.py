import requests
from bs4 import BeautifulSoup
import csv

# Path to the CSV file
csv_file_path = "/Users/asa/PycharmProjects/longevity.international/companies_info.csv"

# Specify the CSV file name for output
output_csv_file_name = 'company_details.csv'

# Open the output CSV file for writing outside the loop
with open(output_csv_file_name, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'Type', 'Description', 'Inventors', 'Technology', 'Industry', 'Headquarters',
                  'Founded Date', 'Employees Number', 'Funding Status', 'Investors Number',
                  'Total Funding', 'Estimated Revenue', 'Last Funding Date', 'Last Funding Type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Open the input CSV file for reading
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row

        # Iterate over each row in the CSV
        for row in reader:
            url = row[1]
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Successfully fetched {url}")
                soup = BeautifulSoup(response.content, 'html.parser')

                name = soup.find('h1', class_='h2').get_text(strip=True).split('\n')[0]

                description = soup.find('div', class_='text-justify').get_text(strip=True, separator=' ')

                # Investors
                investors_divs = soup.find_all('div', class_='firm_with_logo')
                investors = '; '.join(div.a.get_text(strip=True) for div in investors_divs)
                details_divs = soup.find_all('div', class_='border-light')
                details = {}

                for details_div in details_divs:
                    for detail_div in details_div.find_all('div'):
                        detail_name_span = detail_div.find('span', class_='gray')
                        detail_value_strong = detail_div.find('strong')

                        # Ensure both detail_name_span and detail_value_strong are found
                        if detail_name_span is not None and detail_value_strong is not None:
                            # Extract texts, clean them, and map them into the details dictionary
                            detail_name = detail_name_span.get_text(strip=True).rstrip(':')
                            detail_value = detail_value_strong.get_text(strip=True)
                            details[detail_name] = detail_value

                # Check if details were extracted
                if details:
                    print("Details extracted successfully:")
                    for key, value in details.items():
                        print(f"{key}: {value}")
                else:
                    print("No details extracted. Please check the HTML structure and selectors.")
                technology = details.get('Technology')
                type_ = details.get('Type')
                industry = details.get('Industry')
                headquarters = details.get('Headquarters')
                founded_date = details.get('Founded Date')
                employees_number = details.get('Employees Number')
                funding_status = details.get('Funding Status')
                investors_number = details.get('Investors Number')
                total_funding = details.get('Total Funding')
                estimated_revenue = details.get('Estimated Revenue')
                last_funding_date = details.get('Last Funding Date')
                last_funding_type = details.get('Last Funding Type')

                writer.writerow({
                    'Name': name,
                    'Type': type_,
                    'Description': description,
                    'Inventors': investors,
                    'Technology': technology,
                    'Industry': industry,
                    'Headquarters': headquarters,
                    'Founded Date': founded_date,
                    'Employees Number': employees_number,
                    'Funding Status': funding_status,
                    'Investors Number': investors_number,
                    'Total Funding': total_funding,
                    'Estimated Revenue': estimated_revenue,
                    'Last Funding Date': last_funding_date,
                    'Last Funding Type': last_funding_type
                })
            else:
                print(f"Failed to fetch {url}")

print(f"All company details have been successfully written to {output_csv_file_name}")
