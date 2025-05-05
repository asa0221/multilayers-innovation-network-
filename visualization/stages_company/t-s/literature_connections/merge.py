import pandas as pd

# 假设文件名分别为 file1.csv 到 file6.csv，你可以根据实际情况修改文件名和路径
filenames = ['literature_connections1.csv', 'literature_connections2.csv', 'literature_connections3.csv', 'literature_connections4.csv', 'literature_connections5.csv', 'literature_connections6.csv', 'literature_connections7.csv']
dataframes = []

for i, filename in enumerate(filenames):
    # 读取每个文件
    df = pd.read_csv(filename)
    # 将 'time' 列重命名为对应的 'a' 到 'g'
    df.rename(columns={'time': chr(97 + i)}, inplace=True)
    # 将修改后的 DataFrame 添加到列表中
    dataframes.append(df)

# 使用 reduce 函数和 merge 来合并所有 DataFrame
from functools import reduce

# 合并所有的 DataFrame，基于 'affiliation_name' 和所有 'Cluster' 列
merged_df = reduce(lambda left, right: pd.merge(left, right, on=['affiliation_name', 'Cluster0', 'Cluster1', 'Cluster2', 'Cluster3', 'Cluster4', 'Cluster5'], how='outer'), dataframes)

# 输出合并后的 DataFrame，查看结果
print(merged_df.head())

# 如果需要将合并后的结果保存到新的 CSV 文件
merged_df.to_csv('merged_file.csv', index=False)
