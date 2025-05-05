import pandas as pd
import numpy as np  # Import numpy for handling NaN values

# Load the opportunitiesALL.csv into a DataFrame
opportunities_all_df = pd.read_csv('opportunitiesALL1.csv')

# Initialize an empty list to keep track of processed subsets
processed_subsets = []

# List of subset file names
subset_files= ['AccelerateKY Connect. Inform. Inspire.csv','Aging2.0 Global Innovation Search 2022.csv',
               'Aging2.0 Global Innovation Search 2023.csv','AGING2.0 Main.csv','Aging2.0 | London, UK.csv',
               'Capital Connections.csv','CareTech Pitch 2023.csv','CEOc.csv','Derby City Angels.csv',
               'Healthcare Venture Challenge.csv','Kentucky.csv','Knoxville.csv','LEAP.csv','Lexington, KY.csv',
               'Louisville, KY.csv','Metals Innovation Initiative (MI2).csv','Northern Kentucky.csv',
               'Sheltowee Angel Network.csv','Sheltowee Business Network.csv','Sheltowee Network.csv','Sheltowee Venture Fund.csv',
               'University of Louisville.csv']
# Iterate through subset files
for subset_file in subset_files:
    if subset_file not in processed_subsets:
        # Load the subset file into a DataFrame
        subset_df = pd.read_csv(subset_file)

        # Merge the DataFrames based on the 'CoName' column with a left join
        opportunities_all_df = opportunities_all_df.merge(subset_df[['CoName', 'Network']], on='CoName', how='left')

        # Concatenate 'Network' and 'Network_subset' columns, separating with semicolons
        opportunities_all_df['Network'] = opportunities_all_df[['Network_x', 'Network_y']].astype(str).apply(lambda x: ';'.join(x), axis=1)

        # Drop the redundant columns
        opportunities_all_df.drop(['Network_x', 'Network_y'], axis=1, inplace=True)

        # Replace 'nan' with an empty string
        opportunities_all_df['Network'] = opportunities_all_df['Network'].replace('nan', '', regex=True)

        # Remove leading and trailing semicolons and extra consecutive semicolons
        opportunities_all_df['Network'] = opportunities_all_df['Network'].str.replace(r'^;+|;+$|;+(?=;)', '', regex=True)

        # Update the list of processed subsets
        processed_subsets.append(subset_file)

# Save the updated DataFrame back to a CSV file
opportunities_all_df.to_csv('opportunitiesALL_updated.csv', index=False)
