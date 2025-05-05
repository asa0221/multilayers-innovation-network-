import pandas as pd
import numpy as np


info_companies = pd.read_csv('b-t/label_company.csv')
info_investors = pd.read_csv('updated_Investors.csv')
info_technology = pd.read_csv('b-t/label.csv')

investors = {
    'name': info_investors['Name'],
    'coord_x': np.nan,
    'coord_y': np.nan
}
df_investors = pd.DataFrame(investors)
import numpy as np

companies = {
    'co_name': info_companies['coname'],
    'investor_name': info_companies['invetsed'],
    'stage_number': info_companies['cluster'],
    'coord_x': np.nan,
    'coord_y': np.nan
}
df_companies = pd.DataFrame(companies)
df_companies['investor_name'] = df_companies['investor_name'].to_string()

technologies = {
    'assignee': info_technology['assignee'],
    'patent_number': info_technology['patent number'],
    'stage_number': info_technology['cluster'],
    'coord_x': np.nan,
    'coord_y': np.nan
}
df_technology = pd.DataFrame(technologies)
df_technology['assignee'] = df_technology['assignee'].astype(str)
def print_and_count_technology_connections(df_company, df_stage):
    connected_companies = set()  # Initialize a set to track connected companies
    line_count = 0  # Initialize a counter for the number of lines
    connections = []  # List to keep track of successful connections (company-technology pairs)

    for index, technology in df_stage.iterrows():
        # Split assignee names and strip to remove leading/trailing whitespaces
        company_list = [inv.strip() for inv in technology['assignee'].split(';')]

        for company in company_list:
            # Skip if the company has already been connected
            if company in connected_companies:
                continue

            # Find the company in df_company
            matched_company = df_company[df_company['co_name'] == company]
            if not matched_company.empty:
                # A line would be drawn here in the original function
                connected_companies.add(company)
                line_count += 1  # Increment the counter
                connections.append((company, technology['patent_number']))  # Add the connection
                break  # Skip to the next technology after the first match

    # Print the connections
    for connection in connections:
        print(f"Connection between company '{connection[0]}' and technology (patent number '{connection[1]}')")

    return line_count

# Example usage:
line_count = print_and_count_technology_connections(df_companies, df_technology)
print(f"Total lines that will be drawn: {line_count}")
