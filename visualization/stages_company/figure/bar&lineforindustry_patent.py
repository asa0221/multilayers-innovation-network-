import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.font_manager as fm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC']  # 使用 Noto Sans CJK SC 字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 数据
data = {
    'industry': ['人工智能与机器人', '远程医疗', '医疗与疾病诊断', '数字健康', '生活辅助'],
    '传感器': [58, 11, 126, 30, 126],
    '物联网': [47, 7, 12, 12, 37],
    '听觉辅助': [42, 1, 5, 5, 250],
    '医疗科技': [1, 8, 119, 6, 15],
    '远程医疗': [89, 20, 41, 17, 72],
    '人工智能': [163, 7, 10, 9, 14],
    'averages': [2.877697842, 0.2109375, 1.638743455, 0.260726073, 1.984555985],
    'Standard deviation': [19.02799632, 0.731931034, 10.76594859, 1.276899494, 17.37657898]
}
indexes = np.arange(len(data['industry']))

fig, ax1 = plt.subplots(figsize=(14, 8.75))

# 设置不同的颜色代表不同的Cluster
colors = ['orange', '#0000FF', 'green', 'red', '#069AF3', 'purple']

# Function to adjust transparency of a color
def adjust_transparency(hex_color, alpha=0.5):
    # Convert hex to RGB, which is in [0,1] range
    rgb = mcolors.hex2color(hex_color)
    # Return the RGBA tuple with the specified alpha
    return (rgb[0], rgb[1], rgb[2], alpha)

# Adjusting the transparency and saturation of each color
colors = [adjust_transparency(color, 0.5) for color in colors]  # 透明度调整为0.5以减少饱和度

# 绘制堆叠柱状图
bottoms = np.zeros(len(data['industry']))  # 初始的柱子底部高度为0
for i, key in enumerate(['传感器', '物联网', '听觉辅助', '医疗科技', '远程医疗', '人工智能']):
    ax1.bar(indexes, data[key], bottom=bottoms, color=colors[i], label=key, width=0.4)
    bottoms += np.array(data[key])  # 更新底部高度

ax1.set_xlabel('产业类型')
ax1.set_ylabel('总数')
ax1.set_ylim(0, 700)
ax1.set_xticks(indexes)
ax1.set_xticklabels(data['industry'])
ax1.legend(title='技术领域', bbox_to_anchor=(0, 1), loc='upper left')

# 添加第二个y轴显示方差
ax2 = ax1.twinx()
ax2.plot(indexes, data['Standard deviation'], label='标准差', marker='x', color='g', linewidth=2)
ax2.set_ylabel('标准差')
ax2.legend(loc='upper right', bbox_to_anchor=(1, 1))
ax2.set_ylim(0, 25)

# 添加第三个y轴显示平均值
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))  # 设置新轴的位置
ax3.plot(indexes, data['averages'], label='均值', marker='o', color='r', linewidth=2)
ax3.set_ylabel('均值')
ax3.set_ylim(0, 4)
ax3.legend(loc='upper right', bbox_to_anchor=(1, 0.95))

plt.title('不同产业申请专利的数量，均值，与标准差', fontsize=20)
plt.show()
