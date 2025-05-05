import fuzzywuzzy
from fuzzywuzzy import process, fuzz
import pandas as pd


df_investors = pd.read_csv('Investor.csv')

# Threshold for considering a match
threshold = 87


def find_matches(df, column='name', threshold=threshold):
    """
    Identifies and groups matching names based on fuzzy matching.

    Parameters:
    - df: DataFrame containing the names.
    - column: The column name in df that contains the names to match.
    - threshold: The minimum score to consider a match.

    Returns:
    - A dictionary where keys are standard names for each group and values are lists of names considered as matches.
    """
    unique_names = df[column].unique()
    matches = {}
    for name in unique_names:
        if not any(name in match_group for match_group in matches.values()):
            # Find matches for 'name' against all 'unique_names'
            close_matches = [n for n in unique_names if
                             process.fuzz.token_sort_ratio(name, n) >= threshold and n != name]
            # Group 'name' and its 'close_matches' together
            matches[name] = [name] + close_matches
    return matches


def standardize_names(df, matches, column='name'):
    """
    Updates the DataFrame to standardize names based on identified matches.

    Parameters:
    - df: DataFrame with names to standardize.
    - matches: Dictionary of matches to standardize names.
    - column: Column in df to apply standardization.
    """
    for standard_name, variations in matches.items():
        df[column] = df[column].replace(variations, standard_name)


# Identify matches
matches = find_matches(df_investors, 'Name', threshold)

# Standardize names in the DataFrame
standardize_names(df_investors, matches, 'Name')

# Convert the 'Name' column to a set to automatically remove duplicates
unique_names_set = set(df_investors['Name'])

# Convert the set back to a DataFrame to prepare for saving to CSV
df_unique_investors = pd.DataFrame(list(unique_names_set), columns=['Name'])

# Write the DataFrame with standardized names to a new CSV file
df_unique_investors.to_csv('updated_Investors.csv', index=False)

# Note: Adjust the threshold based on your accuracy needs. Higher is stricter.
