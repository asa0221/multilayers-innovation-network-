import plotly.graph_objects as go

# 标签
labels = [
    'Investors',
    'AI and Robots', 'Telemedicine', 'Medical', 'Digital Wellness', 'Healthcare',
    'Sensor systems', 'IoT', 'Hearing aid', 'Medical', 'Telemedicine', 'AI and Robots'
]

# 颜色配置
colors = [
    'rgba(234, 4, 162, 0.3)',  # 投资颜色
    'rgba(128, 0, 128, 0.3)', 'rgba(6, 154, 243, 0.3)', 'rgba(255, 0, 0, 0.3)', 'rgba(0, 128, 0, 0.3)', 'rgba(255, 165, 0, 0.3)',
    'rgba(255, 165, 0, 0.3)', 'rgba(0, 0, 255, 0.3)', 'rgba(0, 128, 0, 0.3)', 'rgba(255, 0, 0, 0.3)',
    'rgba(6, 154, 243, 0.3)', 'rgba(128, 0, 128, 0.3)'  # 技术阶段颜色
]


# 数据配置
investments = [930, 769, 362, 329, 780]
total_investment = sum(investments)
company_amounts = [141, 256, 191, 307, 259]
clusters = [
    [58, 47, 42, 1, 89, 163],
    [11, 7, 1, 8, 20, 7],
    [126, 12, 5, 119, 41, 10],
    [30, 12, 5, 6, 17, 9],
    [126, 37, 250, 15, 72, 14]
]

source = []
target = []
value = []

# 投资总额连接到业务阶段，使用投资金额的百分比
for i in range(5):
    source.append(0)
    target.append(1 + i)
    value.append((investments[i] / total_investment) * 100)

# 业务阶段到技术阶段的连接，使用每个群组中的比例
for i in range(5):
    total_patents = sum(clusters[i])  # 计算每个阶段的总专利数
    for j in range(6):
        if clusters[i][j] > 0:
            source.append(1 + i)
            target.append(6 + j)
            value.append((clusters[i][j] / total_patents) * 100)

# 创建 Sankey 图
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=colors
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=[colors[t] for t in target]  # 使用目标节点的颜色为连接线颜色
    )
)])

fig.update_layout(title_text="Sankey Diagram: Investment -> Company Industry Fields -> Technology Fields(ratio relationship)", font_size=12)
fig.show()
