import requests
from bs4 import BeautifulSoup
import csv

# The target URL
url = "https://mindmaps.aginganalytics.com/reports/162/details/investors"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all divs with the class 'mt-1 mb-1 li_div'
    divs = soup.find_all('div', class_='mt-1 mb-1 li_div')

    # Initialize a list to hold the company info
    companies_info = []

    # Loop through each div to extract the company URL and name
    for div in divs:
        # Find the <a> tag within the div
        a_tag = div.find('a')
        if a_tag:
            # Extract the href attribute (URL) and the text (company name)
            company_url = a_tag['href']
            company_name = a_tag.text

            # Append the extracted info to the companies_info list
            companies_info.append((company_name, company_url))

    # Specify the CSV file name
    csv_file_name = 'inventor_info.csv'

    # Open the CSV file for writing
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        # Create a CSV writer object
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['Company Name', 'URL'])

        # Write the company info rows
        for company in companies_info:
            writer.writerow(company)

    print(f"Data has been successfully written to {csv_file_name}")
else:
    print("Failed to retrieve the webpage")
