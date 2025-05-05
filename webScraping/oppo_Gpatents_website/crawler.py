import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def crawl_google_patent(url):
    # Make an HTTP GET request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    def get_text(tag, attrs):
        element = soup.find(tag, attrs)
        return element.text.strip() if element else None

    patent_name = get_text('h1', {'id': 'title'})
    abstract = get_text('div', {'class': 'abstract'})
    heading1 = get_text('heading', {'id': 'h-0001'})
    content1 = get_text('div', {'id': 'p-0002'})
    heading2 = get_text('heading', {'id': 'h-0002'})
    content2 = get_text('div', {'id': 'p-0003'})
    pub_id = get_text('h2', {'id': 'pubnum', 'class': 'style-scope patent-result'})

    return {
        'patent_name': patent_name,
        'abstract': abstract,
        'heading1': heading1,
        'content1': content1,
        'heading2': heading2,
        'content2': content2,
        'id': pub_id,
        'url': url
    }

def save_to_csv(data, filename):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if file.tell() == 0:  # Check if file is empty to write the header
            writer.writeheader()
        writer.writerow(data)

# Assuming you have a column 'PatentURL' in 'output.csv'
csv_file = 'output.csv'
df = pd.read_csv(csv_file)
i = 1
# Iterate over URLs and extract information
for index, row in df.iloc[1801:1803].iterrows():
    url = row['PatentURL']
    patent_data = crawl_google_patent(url)
    if patent_data:
        save_to_csv(patent_data, 'detail_international_patent2.csv')
        print(f'Success to retrieve data for {url}')
        print(i)
        i = i + 1  # Increment i on success
    else:
        print(f'Failed to retrieve data for {url}')
