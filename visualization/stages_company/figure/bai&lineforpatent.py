import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# 数据
data = {
    'stages':['Ideation to Seed Stage', 'Early Stage', 'Growth Stage', 'Maturity and Exit Stage'],
    'Sensor systems': [38, 34, 58, 42],
    'IoT': [29, 26, 19, 23],
    'Hearing aid': [0, 5, 2, 35],
    'Medical': [6, 17, 34, 35],
    'Telemedicine': [28, 21, 39, 70],
    'AI and Robots': [10, 23, 35, 116],
    'averages': [0.21305182, 0.83443709, 1.66964286, 7.82926829],
    'Standard deviation': [1.31218494, 2.52304172, 5.04821509, 35.8231088]
}
indexes = np.arange(len(data['stages']))

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
bottoms = np.zeros(len(data['stages']))  # 初始的柱子底部高度为0
for i, key in enumerate(['Sensor systems', 'IoT', 'Hearing aid', 'Medical', 'Telemedicine', 'AI and Robots']):
    ax1.bar(indexes, data[key], bottom=bottoms, color=colors[i], label=key, width=0.4)
    bottoms += np.array(data[key])  # 更新底部高度

ax1.set_xlabel('Development Stages')
ax1.set_ylabel('Sum')
ax1.set_ylim(0,400)
ax1.set_xticks(indexes)
ax1.set_xticklabels(data['stages'])
ax1.legend(title='Technology field', bbox_to_anchor=(0, 1), loc='upper left')

# 添加第二个y轴显示方差
ax2 = ax1.twinx()
ax2.plot(indexes, data['Standard deviation'], label='Standard deviation', marker='x', color='g', linewidth=2)
ax2.set_ylabel('Standard deviation')
ax2.legend(loc='upper right', bbox_to_anchor=(1, 1))
ax2.set_ylim(0, 43)


# 添加第三个y轴显示平均值
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))  # 设置新轴的位置
ax3.plot(indexes, data['averages'], label='Average', marker='o', color='r', linewidth=2)
ax3.set_ylabel('Average')
ax3.set_ylim(0, 9)
ax3.legend(loc='upper right', bbox_to_anchor=(1, 0.95))

plt.title('The Sum , Average, and Standard deviation of Patents by Stage', fontsize=20)
plt.show()
