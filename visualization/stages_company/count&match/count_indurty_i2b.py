import pandas as pd

# 加载公司信息
df_companies = pd.read_csv('/Users/asa/PycharmProjects/stages_company/Industry/b2t1.csv')  # 假设字段是通过制表符分隔的

# 加载投资者信息
df_investors = pd.read_csv('/Users/asa/PycharmProjects/stages_company/investor_data/updated_Investors.csv')

# 扩展'Matched Inventors'列中的多个投资者为多行
df_expanded = df_companies.set_index(['coname', 'industry'])['Matched Inventors'].str.split(';', expand=True)
df_expanded = df_expanded.stack().reset_index().drop('level_2', axis=1)
df_expanded.columns = ['coname', 'industry', 'Investor']

# 确保投资者名称没有前后空格
df_expanded['Investor'] = df_expanded['Investor'].str.strip()

# 创建需要的列名列表
columns_needed = [f'Industry{i}' for i in range(5)] + ['Total']  # 现在是Industry0到Industry4


# 重新计算每个投资者在不同行业的投资数量并重新映射列
investor_industry_counts = df_expanded.groupby(['Investor', 'industry']).size().unstack(fill_value=0)

# 添加行业投资总数
# 重新计算每个投资者在不同行业的投资数量并重新映射列

# 重命名列以匹配预期格式
investor_industry_counts.columns = ['Industry' + str(i) for i in investor_industry_counts.columns]

# 添加行业投资总数
investor_industry_counts['Total'] = investor_industry_counts.sum(axis=1)

# 确保所有需要的列都存在，且未出现的行业列填充为0
columns_needed = ['Industry0', 'Industry1', 'Industry2', 'Industry3', 'Industry4', 'Total']
investor_industry_counts = investor_industry_counts.reindex(columns=columns_needed, fill_value=0)
print(investor_industry_counts.head)

# 输出到CSV文件
investor_industry_counts.to_csv('investor_industry_counts.csv')
