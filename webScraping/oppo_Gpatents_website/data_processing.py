import pandas as pd

# Function to convert patent ID to URL
def convert_to_url(patent_id):
    base_url = "https://patents.google.com/patent/"
    return f"{base_url}{patent_id.replace(' ', '')}/en"

# Read the CSV file
file_path = "/Users/asa/Desktop/2asa/PycharmProjects/oppo_Gpatents_website/filtered_internation_patent.csv"  # Change this to the path of your input CSV file
df = pd.read_csv(file_path)

# Assuming the patent IDs are in a column named 'PatentID'
# Convert each patent ID in the 'PatentID' column to its corresponding URL
df['PatentURL'] = df['PN'].apply(convert_to_url)

# Output to a new CSV file
output_file_path = "output.csv"  # Change this to your desired output file path
df.to_csv(output_file_path, index=False)

print(f"Processed file saved to {output_file_path}")
