import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np
import pandas as pd
from tqdm import tqdm
import random
import re

fig = plt.figure(figsize=(70, 50))  # Adjust the figure size as needed
ax = fig.add_subplot(111, projection='3d')
ax.set_axis_off()
# Setting the axes properties (limits, labels, and title)
ax.set_xlim3d([0, 4])
ax.set_ylim3d([0, 4])
ax.set_zlim3d([-14, 14])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('')
def draw_planes():
    points_company = np.array([[0, 0, 14], [0, 4, 14], [4, 4, 14], [4, 0, 14]])
    # Company layer
    points_technology = np.array([[0, 0, 0], [0, 4, 0], [4, 4, 0], [4, 0, 0]])
    # Technology layer
    points_science = np.array([[0, 0, -14], [0, 4, -14], [4, 4, -14], [4, 0, -14]])

    # Draw the planes
    verts_company = [list(points_company)]
    verts_technology =[list(points_technology)]
    verts_science = [list(points_science)]

    # Create the polygons for the planes and add them to the axis
    ax.add_collection3d(Poly3DCollection(verts_company, facecolors='white', linewidths=1, edgecolors='black', alpha=.3))
    ax.add_collection3d(Poly3DCollection(verts_technology, facecolors='white', linewidths=1, edgecolors='black', alpha=.3))
    ax.add_collection3d(Poly3DCollection(verts_science, facecolors='white', linewidths=1,edgecolors='black', alpha=.3))

    ax.set_box_aspect([1,1,2])

def draw_busines():
    ratios = np.array([0.8, 1.6, 1.2, 2, 1.6])
    # Radii are proportional to the square root of the area
    radii = np.sqrt(ratios / np.pi)

    # Define the center points for each circle
    circle_centers = [(2, 2, 14), (1.0, 1.0, 14), (3.1, 1.0, 14), (1.0, 3.0, 14), (3.1, 3.0, 14)]
    colors = [('purple'), ('#069AF3'), ('red'), ('green'), ('orange')]
    labels = ['AI and Robots', 'Telemedicine', 'Medical', 'Digital Wellness', 'Healthcare']
    plot_handles = []

    # Draw the circles on the lower plane
    for center, radius, colors, label in zip(circle_centers, radii, colors, labels):
        # Parametric equation of a circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        z = np.full_like(x, center[2])
        handle, = ax.plot(x, y, z, color=colors, linewidth=15, linestyle='--', label=label)
        plot_handles.append(handle)
        lines0 = [
            [(2, 2, 14), (2.3, 2.8, 0)],  # First line
            [(2, 2, 14), (0.9, 1.0, 0)],  # Second line
            [(2, 2, 14), (3.4, 2.8, 0)]  # Third line
        ]
        line_collection0 = Line3DCollection(lines0, colors='purple', linewidths=5, linestyles='--', alpha=0.5, zorder=1)
        lines1 = [
            [(1.0, 1.0, 14), (0.9, 1.0, 0)],  # Second line
            [(1.0, 1.0, 14), (2.0, 1.0, 0)]  # Third line
        ]
        line_collection1 = Line3DCollection(lines1, colors='#069AF3', linewidths=5, linestyles='--', alpha=0.5, zorder=1)
        lines2 = [
            [(3.1, 1.0, 14), (3.4, 2.8, 0)],  # First line
            [(3.1, 1.0, 14), (3.3, 1.0, 0)],  # Second line
            [(3.1, 1.0, 14), (2.0, 1.0, 0)]  # Third line
        ]
        line_collection2 = Line3DCollection(lines2, colors='red', linewidths=5, linestyles='--', alpha=0.5, zorder=1)
        lines3 = [
            [(1.0, 3.0, 14), (2.3, 2.8, 0)],  # First line
            [(1.0, 3.0, 14), (1.0, 2.8, 0)],  # Second line
        ]
        line_collection3 = Line3DCollection(lines3, colors='green', linewidths=5, linestyles='--', alpha=0.5, zorder=1)
        lines4 = [
            [(3.1, 3.0, 14), (1.0, 2.8, 0)],  # First line
            [(3.1, 3.0, 14), (3.3, 1.0, 0)],  # Second line
        ]
        line_collection4 = Line3DCollection(lines4, colors='orange', linewidths=5, linestyles='--', alpha=0.5, zorder=1)
        ax.add_collection3d(line_collection0)
        ax.add_collection3d(line_collection0)
        ax.add_collection3d(line_collection1)
        ax.add_collection3d(line_collection2)
        ax.add_collection3d(line_collection3)
        ax.add_collection3d(line_collection4)
    legend0 = ax.legend(handles=plot_handles, fontsize=50, title='Business Layer', title_fontsize='60',
                            loc='upper left', bbox_to_anchor=(-0.05,1))
    ax.add_artist(legend0)


def draw_technology():
    ratios = np.array([1, 1.2, 0.6, 0.5, 1, 0.7])
    # Radii are proportional to the square root of the area
    radii = np.sqrt(ratios / np.pi)

    # Define the center points for each circle
    circle_centers = [(2.3, 2.8, 0), (1.0, 2.8, 0), (0.9, 1.0, 0), (3.4, 2.8, 0), (3.3, 1.0, 0), (2.0, 1.0, 0)]
    colors = [('orange'), ('#0000FF'), ('green'), ('red'), ('#069AF3'),('purple')]
    labels1 = ['Sensor Systems', 'IoT', 'Hearing aid', 'Medical', 'Telemedicine', 'AI and Robots']
    plot_handles = []

    # Draw the circles on the lower plane
    for center, radius, colors, label in zip(circle_centers, radii, colors, labels1):
        # Parametric equation of a circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        z = np.full_like(x, center[2])
        handle, = ax.plot(x, y, z, color=colors, linewidth=15, linestyle='--', label=label)
        plot_handles.append(handle)
        lines0 = [
            [(2.3, 2.8, 0), (1.0, 0.9, -14)],  # First line
            [(2.3, 2.8, 0), (2.6, 3.4, -14)],  # Second line
        ]
        line_collection0 = Line3DCollection(lines0, colors='orange', linewidths=5, linestyles='--', alpha=0.5,
                                            zorder=1)
        lines1 = [
            [(1.0, 2.8, 0), (1.3, 2.9, -14)],  # Second line
            [(1.0, 2.8, 0), (2.5, 0.5, -14)],  # Third line
            [(1.0, 2.8, 0), (3.4, 2.5, -14)]  # Third line
        ]
        line_collection1 = Line3DCollection(lines1, colors='#0000FF', linewidths=5, linestyles='--', alpha=0.5,
                                            zorder=1)
        lines2 = [
            [(0.9, 1.0, 0), (1.0, 0.9, -14)],  # First line
            [(0.9, 1.0, 0), (2.5, 0.5, -14)],  # Second line
            [(0.9, 1.0, 0), (3.4, 1.2, -14)]  # Third line
        ]
        line_collection2 = Line3DCollection(lines2, colors='green', linewidths=5, linestyles='--', alpha=0.5, zorder=1)
        lines3 = [
            [(3.4, 2.8, 0), (1.0, 0.9, -14)],  # First line
            [(3.4, 2.8, 0), (2.6, 3.4, -14)],# Second line
            [(3.4, 2.8, 0), (3.4, 1.2, -14)]
        ]
        line_collection3 = Line3DCollection(lines3, colors='red', linewidths=5, linestyles='--', alpha=0.5, zorder=1)
        lines4 = [
            [(3.3, 1.0, 0), (2.6, 3.4, -14)],  # First line
            [(3.3, 1.0, 0), (2.2, 1.7, -14)],  # Second line
        ]
        line_collection4 = Line3DCollection(lines4, colors='#069AF3', linewidths=5, linestyles='--', alpha=0.5, zorder=1)
        lines5 = [
            [(2.0, 1.0, 0), (2.2, 1.7, -14)],  # First line
            [(2.0, 1.0, 0), (3.4, 2.5, -14)],  # Second line
        ]
        line_collection5 = Line3DCollection(lines5, colors='purple', linewidths=5, linestyles='--', alpha=0.5, zorder=1)
        ax.add_collection3d(line_collection0)
        ax.add_collection3d(line_collection0)
        ax.add_collection3d(line_collection1)
        ax.add_collection3d(line_collection2)
        ax.add_collection3d(line_collection3)
        ax.add_collection3d(line_collection4)
        ax.add_collection3d(line_collection5)
    legend1 = ax.legend(handles=plot_handles, fontsize=50, title='Technology Layer', title_fontsize='60',
                        loc='center left', bbox_to_anchor=(-0.05,0.5), fancybox=True)
    ax.add_artist(legend1)
def draw_science():
    ratios = np.array([0.7, 0.5, 2, 0.8, 0.4, 0.4, 0.6])
    # Radii are proportional to the square root of the area
    radii = np.sqrt(ratios / np.pi)

    # Define the center points for each circle
    circle_centers = [(1.0, 0.9, -14),  (2.6, 3.4, -14), (1.3, 2.9, -14), (2.2, 1.7, -14), (2.5, 0.5, -14), (3.4, 1.2, -14), (3.4, 2.5, -14)]
    colors = [('#069AF3'), ('green'), ('#0000FF'), ('red'), ('orange'),('purple'),("#6C733D")]
    labels = ['Monitoring systems ', 'Rehabilitation', 'Dementia', 'Surgery and Cancer', 'Infectious diseases', 'AI', 'Chronic diseases']
    plot_handles = []

    # Draw the circles on the lower plane
    for center, radius, colors,label in zip(circle_centers, radii, colors, labels):
        # Parametric equation of a circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        z = np.full_like(x, center[2])
        ax.plot(x, y, z, color=colors, linewidth=15, linestyle='--')
        handle, = ax.plot(x, y, z, color=colors, linewidth=15, linestyle='--', label=label)
        plot_handles.append(handle)
    legend2 = ax.legend(handles=plot_handles, fontsize=50, title='Science Layer', title_fontsize='60',
                        loc='lower left', bbox_to_anchor=(-0.05,0.05), fancybox=True)
    ax.add_artist(legend2)

draw_planes()
draw_busines()
draw_technology()
draw_science()
plt.savefig('industry_connections.png')
