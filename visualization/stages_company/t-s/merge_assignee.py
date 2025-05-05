import pandas as pd
from fuzzywuzzy import process

# 读取CSV文件
df_csv = pd.read_csv('/Users/asa/PycharmProjects/stages_company/company_data/company_details_row.csv')

# 读取Excel文件
df_excel = pd.read_excel('/Users/asa/PycharmProjects/stages_company/company_data/company.xlsx')

# 预处理Company Name列，去除空格和大小写统一化
df_csv['Company Name'] = df_csv['Company Name'].str.strip().str.lower()
df_excel['coname'] = df_excel['coname'].str.strip().str.lower()

# 创建一个新列用于存放匹配的Inventors数据
df_excel['Matched Inventors'] = ""

# 进行匹配并将Inventors数据放入对应行的新列中
for index, row in df_excel.iterrows():
    match = process.extractOne(row['coname'], df_csv['Company Name'])
    if match[1] >= 90:  # 设置阈值，确保匹配准确性
        matched_row = df_csv.loc[match[2]]
        df_excel.at[index, 'Matched Inventors'] = matched_row['Inventors']

# 保存更新后的Excel文件
df_excel.to_excel('merge_assignee.xlsx', index=False)

# 读取数据
df_csv = pd.read_csv('/Users/asa/PycharmProjects/stages_company/company_data/company_details_row.csv')
df_excel = pd.read_excel('/Users/asa/PycharmProjects/stages_company/company_data/company.xlsx')


# 读取CSV文件
df_csv = pd.read_csv('company_details_row.csv')

# 读取Excel文件
df_excel = pd.read_excel('company.xlsx')

# 预处理Company Name列，去除空格和大小写统一化
df_csv['Company Name'] = df_csv['Company Name'].str.strip().str.lower()
df_excel['coname'] = df_excel['coname'].str.strip().str.lower()

# 创建一个新列用于存放匹配的Inventors数据
df_excel['Matched Inventors'] = ""

# 进行匹配并将Inventors数据放入对应行的新列中
for index, row in df_excel.iterrows():
    match = process.extractOne(row['coname'], df_csv['Company Name'])
    if match[1] >= 90:  # 设置阈值，确保匹配准确性
        matched_row = df_csv.loc[match[2]]
        df_excel.at[index, 'Matched Inventors'] = matched_row['Inventors']

# 保存更新后的Excel文件
df_excel.to_excel('merge_assignee.xlsx', index=False)
