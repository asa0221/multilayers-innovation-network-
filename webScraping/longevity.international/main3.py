import requests
from bs4 import BeautifulSoup
import csv

# Path to the CSV file
csv_file_path = "/Users/asa/PycharmProjects/longevity.international/inventor_info.csv"

# Specify the CSV file name for output
output_csv_file_name = 'inventor_details3.csv'

# Open the output CSV file for writing outside the loop
with open(output_csv_file_name, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'Type', 'Description', 'Invests Into', 'Industry', 'Headquarters', 'Zip',
                  'Founded Date', 'Employees Number', 'Investor Type', 'Investment Stage', 'Number Of Exits',
                  'Investors Number', 'Acquisition Number',
                  'Total Funding', 'Estimated Revenue', 'Last Funding Date', 'Last Funding Type', 'Visit Website']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Open the input CSV file for reading
    start_from_row = 548  # Define the row number from which to start processing

    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row

        for i, row in enumerate(reader, start=1):  # Start enumeration from 1 since we skipped the header
            if i < start_from_row:
                continue  # Skip rows until we reach the starting row
            url = row[1]
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Successfully fetched {url}")
                soup = BeautifulSoup(response.content, 'html.parser')

                name = soup.find('h1', class_='h2').get_text(strip=True).split('\n')[0]

                description = soup.find('div', class_='text-justify').get_text(strip=True, separator=' ')

                # Invests into
                investors_divs = soup.find_all('div', class_='firm_with_logo')
                invests_into = '; '.join(div.a.get_text(strip=True) for div in investors_divs)
                print(invests_into)
                details_divs = soup.find_all('div', class_='border-light')
                details = {}
                # Using a case-insensitive search for more flexibility
                visit_website_link = soup.find('a', text=lambda text: text and "visit website" in text.lower())

                # Check if the <a> tag was found before trying to access the 'href'
                if visit_website_link:
                    visit_website = visit_website_link['href']
                    print(visit_website)
                else:
                    print("The 'Visit Website' link could not be found.")
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
                type_ = details.get('Type')
                industry = details.get('Industry')
                headquarters = details.get('Headquarters')
                zip = details.get('Zip')
                founded_date = details.get('Founded Date')
                employees_number = details.get('Employees Number')
                investor_type = details.get('Investor Type')
                investment_stage = details.get('Investment Stage')
                number_of_exits = details.get('Number Of Exits')
                acquisition_number = details.get('Acquisition Number')
                investors_number = details.get('Investors Number')
                total_funding = details.get('Total Funding')
                estimated_revenue = details.get('Estimated Revenue')
                last_funding_date = details.get('Last Funding Date')
                last_funding_type = details.get('Last Funding Type')

                writer.writerow({
                    'Name': name,
                    'Type': type_,
                    'Description': description,
                    'Invests Into': invests_into,
                    'Industry': industry,
                    'Headquarters': headquarters,
                    'Zip': zip,
                    'Founded Date': founded_date,
                    'Employees Number': employees_number,
                    'Investor Type': investor_type,
                    'Investment Stage': investment_stage,
                    'Number Of Exits': number_of_exits,
                    'Acquisition Number': acquisition_number,
                    'Investors Number': investors_number,
                    'Total Funding': total_funding,
                    'Estimated Revenue': estimated_revenue,
                    'Last Funding Date': last_funding_date,
                    'Last Funding Type': last_funding_type,
                    'Visit Website': visit_website
                })
            else:
                print(f"Failed to fetch {url}")

print(f"All company details have been successfully written to {output_csv_file_name}")
