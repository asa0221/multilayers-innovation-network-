import pandas as pd
from fuzzywuzzy import process


df_current = pd.read_csv('/Users/asa/PycharmProjects/stages_company/b-t/updated_company_info.csv')  # 如果是从CSV文件读取
df_company = pd.read_csv('/Users/asa/PycharmProjects/stages_company/b-t/industry_type.csv')  # 如果是从CSV文件读取

# 函数用于找到最佳匹配项
def get_closest_match(x, choices, cutoff=85):
    """返回最佳匹配项，只有当匹配得分超过cutoff时"""
    best_match = process.extractOne(x, choices, score_cutoff=cutoff)
    return best_match[0] if best_match else None

# 将公司名称的标准化处理放在匹配函数之前进行
df_current['Name'] = df_current['Name'].str.lower().str.strip().str.replace(r'[^\w\s]', '', regex=True)
df_company['coname'] = df_company['coname'].str.lower().str.strip().str.replace(r'[^\w\s]', '', regex=True)

# 创建一个字典，将公司名映射到cluster
company_to_cluster = dict(zip(df_company['coname'], df_company['cluster']))

# 获取所有可能的公司名称选项
choices = df_company['coname'].tolist()

# 对df_current中每个公司名称应用匹配函数并映射到cluster
df_current['matched_name'] = df_current['Name'].apply(lambda x: get_closest_match(x, choices))
df_current['cluster'] = df_current['matched_name'].map(company_to_cluster)

# 删除不需要的临时列
df_current.drop(columns=['matched_name'], inplace=True)

# 打印结果查看
print(df_current.head())

# 保存合并后的数据框到新的CSV文件，如果需要
df_current.to_csv('updated_current_file.csv', index=False)
