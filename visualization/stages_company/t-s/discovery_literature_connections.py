import pandas as pd
from collections import defaultdict
from fuzzywuzzy import process
from tqdm import tqdm
import re

def normalize_terms(text, term_map):
    for old, new in term_map.items():
        pattern = r'\b' + re.escape(old) + r'\b'
        text = re.sub(pattern, new, text, flags=re.IGNORECASE)
    return text

def process_data(df_science, df_technology, threshold=90,
                 ignore_list=['to', 'inc.', 'llc', 'ltd.', 'cera', 'anna university', 'cea', 'sana', 'one medical'],
                 term_map={'univ': 'university', 'inst': 'institute'}):
    ignore_list_normalized = set(normalize_terms(word.lower(), term_map) for word in ignore_list)

    # Extract and normalize science affiliations
    science_affiliations = defaultdict(int)
    for _, science in tqdm(df_science.iterrows(), total=df_science.shape[0], desc='Processing Science Data'):
        affiliations = set([normalize_terms(affil.lower().strip(), term_map) for affil in
                            str(science['affiliation']).split(';')
                            if affil.lower().strip() != 'nan' and affil.strip() != '' and
                            normalize_terms(affil.lower().strip(), term_map) not in ignore_list_normalized])
        for affil in affiliations:
            science_affiliations[affil] += 1

    # Extract and normalize technology assignees and count clusters
    technology_info = defaultdict(lambda: defaultdict(int))
    for _, tech in tqdm(df_technology.iterrows(), total=df_technology.shape[0], desc='Processing Technology Data'):
        assignees = set(
            normalize_terms(assignee.lower().strip(), term_map) for assignee in
            str(tech['assignee']).split(';')
            if assignee.lower().strip() != 'nan' and assignee.strip() != '' and
            normalize_terms(assignee.lower().strip(), term_map) not in ignore_list_normalized)
        for assignee in assignees:
            technology_info[assignee][tech['cluster']] += 1

    # Match science affiliations with technology assignees and count clusters
    results = []
    for affil, count in tqdm(science_affiliations.items(), desc='Matching Affiliations'):
        match_data = process.extractOne(affil, list(technology_info.keys()), score_cutoff=threshold)
        if match_data:
            best_match, score = match_data
            result = {
                'affiliation_name': affil,
                'time': count
            }
            cluster_counts = {f'Cluster{i}': technology_info[best_match][i] for i in range(6)}
            result.update(cluster_counts)
            results.append(result)

    return pd.DataFrame(results)



df_technology = pd.read_csv('/Users/asa/PycharmProjects/stages_company/b-t/patent.csv')
df_science = pd.read_csv('/Users/asa/PycharmProjects/stages_company/t-s/literature.csv')
df_science1 = df_science[df_science['type'] == 'b']

df_result = process_data(df_science1, df_technology)
print(df_result.head())
df_result.to_csv('literature_connections2.csv', index=False)