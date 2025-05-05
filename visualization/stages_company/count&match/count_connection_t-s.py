import pandas as pd
import numpy as np
from fuzzywuzzy import process
from tqdm import tqdm
import re

info_technology = pd.read_csv('b-t/label.csv')
info_science = pd.read_csv('t-s/label_liter.csv')

technologies = {
    'assignee': info_technology['assignee'],
    'patent_number': info_technology['patent number'],
    'stage_number': info_technology['cluster'],
    'coord_x': np.nan,
    'coord_y': np.nan
}
df_technology = pd.DataFrame(technologies)
df_technology['assignee'] = df_technology['assignee'].astype(str)

science = {
    'title': info_science['title'],
    'affiliation': info_science['affiliation'],
    'stage_number': info_science['cluster'],
    'coord_x': np.nan,
    'coord_y': np.nan
}
df_science = pd.DataFrame(science)
df_science['affiliation'] = df_science['affiliation'].astype(str)

def normalize_terms(text, term_map):
    for old, new in term_map.items():
        # Regex pattern to match whole word with word boundaries
        pattern = r'\b' + re.escape(old) + r'\b'
        text = re.sub(pattern, new, text, flags=re.IGNORECASE)
    return text


def count_fuzzy_connections(df_science, df_technology, threshold,ignore_list=['\'to\'', 'inc.', 'inc', 'llc', 'ltd.','cera','anna university','cea','sana','one medical'],
                            term_map={'univ': 'university', 'inst': 'institute'}):
    connection_counter = 0  # Initialize a counter for the number of connections

    # Convert ignore_list to lowercase for consistency
    ignore_list = [word.lower() for word in ignore_list]

    for index, science in tqdm(df_science.iterrows(), total=df_science.shape[0], desc='Processing Science Entries'):
        # Normalize and prepare to iterate through each affiliation, ignoring 'nan', empty values, and ignore_list items
        affiliations = [normalize_terms(affil.lower().strip(), term_map) for affil in science['affiliation'].split(';')
                        if
                        affil.lower().strip() != 'nan' and affil.strip() != '' and affil.lower().strip() not in ignore_list]

        # Generate and normalize a list of all unique, cleaned, lowercased assignees from df_technology, ignoring ignore_list items
        all_assignees = set(
            normalize_terms(assignee.lower().strip(), term_map) for _, tech in df_technology.iterrows() for assignee in
            tech['assignee'].split(';') if
            assignee.lower().strip() != 'nan' and assignee.strip() != '' and assignee.lower().strip() not in ignore_list)

        for affiliation in affiliations:
            # Use fuzzy matching to find the best match for the current affiliation among all assignees
            best_match, score = process.extractOne(affiliation, list(all_assignees))

            # Check if best_match is not in ignore_list after normalization
            if score >= threshold and best_match not in [normalize_terms(word, term_map) for word in ignore_list]:
                connection_counter += 1  # Increment the connection counter

                # Print details of the connection
                print(
                    f"Connection #{connection_counter}: '{affiliation}' (Science) matched with '{best_match}' (Technology) with a score of {score}")

    return connection_counter


# Assuming df_science and df_technology are your DataFrames
# Example usage:
total_connections = count_fuzzy_connections(df_science, df_technology, 90)
print(f"Total fuzzy connections found: {total_connections}")
