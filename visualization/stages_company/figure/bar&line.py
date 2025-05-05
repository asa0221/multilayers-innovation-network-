import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Data
stages = ['Industry 0', 'Industry 1', 'Industry 2', 'Industry 3', 'Industry 4']
indexes = np.arange(len(stages))
sums = [930, 769, 362, 329, 780]
averages = [0.678832117, 0.561313869, 0.264233577, 0.240145985, 0.569343066]
variances = [3.797433259, 5.102519821, 1.762123773, 1.338197203, 6.290659174]


fig, ax1 = plt.subplots(figsize=(14, 8.75))

original_colors = ['purple', '#069AF3', 'red', 'green', 'orange']

# Function to adjust transparency of a color
def adjust_transparency(hex_color, alpha=0.5):
    # Convert hex to RGB, which is in [0,1] range
    rgb = mcolors.hex2color(hex_color)
    # Add the alpha channel
    return (rgb[0], rgb[1], rgb[2], alpha)

# Generate transparent colors
transparent_colors = [adjust_transparency(color, 0.5) for color in original_colors]

# Bar chart for sums with individual labels
bar_labels = ['AI and Robots', 'Telemedicine', 'Medical', 'Digital Wellness', 'Healthcare']
for i in range(len(sums)):
    ax1.bar(indexes[i], sums[i], width=0.4, color=transparent_colors[i], label=bar_labels[i])

ax1.set_xlabel('Industry')
ax1.set_ylabel('Sum')
ax1.set_xticks(indexes)
ax1.set_xticklabels(stages)
ax1.set_ylim(0, 1200)

# Create another axis for the variances
ax2 = ax1.twinx()

# Line chart for variances
ax2.plot(indexes, variances, label='Variance', marker='x', color='g')
ax2.set_ylabel('Variance')

# Create another axis for the averages with a range from 0 to 1
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))  # Offset this new spine
ax3.plot(indexes, averages, label='Average', marker='o', color='r')
ax3.set_ylabel('Average')
ax3.set_ylim(0, 1)  # Set the y-axis limits from 0 to 1

# Set legend positions
ax1.legend(loc='upper left')
ax2.legend(loc='upper right', bbox_to_anchor=(1, 0.95))
ax3.legend(loc='upper right')
ax2.set_ylim(0,8)

plt.title('The Sum, Average, and Variance of Investment by Industry', fontsize=20)
plt.show()
