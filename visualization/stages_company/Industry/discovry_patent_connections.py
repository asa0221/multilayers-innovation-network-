import pandas as pd
from tqdm import tqdm
from fuzzywuzzy import process, fuzz

def update_patent_counts(company_csv, patent_csv, output_csv,
                         ignore_list=['to', 'inc.', 'llc', 'ltd.', 'Ware', 'roz', 'Elva', 'Akira', 'ripple', 'Sana', 'EEVE'],
                         term_map={'univ': 'university', 'inst': 'institute'}, threshold=90):
    df_companies = pd.read_csv(company_csv)
    df_patents = pd.read_csv(patent_csv)

    # 初始化公司列的专利计数
    for col in ['Cluster0', 'Cluster1', 'Cluster2', 'Cluster3', 'Cluster4', 'Cluster5']:
        if col not in df_companies.columns:
            df_companies[col] = 0

    ignore_list_normalized = [normalize_terms(term.lower(), term_map) for term in ignore_list]
    df_companies['Normalized Name'] = df_companies['Name'].apply(lambda x: normalize_terms(x.lower(), term_map))
    df_companies = df_companies[~df_companies['Normalized Name'].isin(ignore_list_normalized)]

    print("Starting to process patents...")

    # 遍历每个专利，查找匹配的公司并更新计数
    for index, patent in tqdm(df_patents.iterrows(), total=df_patents.shape[0], desc='Processing patents'):
        # Normalize and deduplicate assignees
        assignees = set([normalize_terms(assignee.lower().strip(), term_map) for assignee in patent['assignee'].split(';')
                         if normalize_terms(assignee.lower().strip(), term_map) not in ignore_list_normalized])
        cluster = 'Cluster' + str(patent['cluster'])  # 假设cluster列直接记录数字0-5

        for assignee_normalized in assignees:
            if assignee_normalized:
                # 使用模糊匹配找到最佳匹配的公司名称
                match = process.extractOne(assignee_normalized, df_companies['Normalized Name'], scorer=fuzz.WRatio, score_cutoff=threshold)
                if match:
                    best_match, score = match[0], match[1]
                    if score >= threshold:
                        matched_company = df_companies[df_companies['Normalized Name'] == best_match]['Name'].iloc[0]
                        matched_idx = df_companies[df_companies['Name'] == matched_company].index
                        df_companies.loc[matched_idx, cluster] += 1
                        print(f"Assignee '{assignee_normalized}' matched with company '{matched_company}' with score {score}")

    print("Finished processing patents.")
    print("Saving updated company information...")

    # 保存更新后的公司信息
    df_companies.to_csv(output_csv, index=False)
    print(f"Updated company information has been saved to {output_csv}")


def normalize_terms(term, term_map):
    for key, value in term_map.items():
        term = term.replace(key, value)
    return term


update_patent_counts('/Users/asa/PycharmProjects/stages_company/b-t/updated_company_invested.csv', '/Users/asa/PycharmProjects/stages_company/b-t/patent.csv', 'updated_company_info.csv')
