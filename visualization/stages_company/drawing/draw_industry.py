import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np
import pandas as pd
from tqdm import tqdm
from fuzzywuzzy import process
import re
from collections import defaultdict
import os


info_investors = pd.read_csv('/Users/asa/PycharmProjects/stages_company/investor_data/updated_Investors.csv')
info_companies = pd.read_excel('/Users/asa/PycharmProjects/stages_company/company_data/company.xlsx')
info_technology = pd.read_csv('/Users/asa/PycharmProjects/stages_company/b-t/patent.csv')
info_science = pd.read_csv('/Users/asa/PycharmProjects/stages_company/t-s/literature.csv')

investors = {
    'name': info_investors['Name'],
    'coord_x': np.nan,
    'coord_y': np.nan
}
df_investors = pd.DataFrame(investors)

companies = {
    'co_name': info_companies['coname'],
    'investor_name': info_companies['Matched Inventors'],
    'stage_number': info_companies['cluster'],
    'coord_x': np.nan,
    'coord_y': np.nan
}
df_companies = pd.DataFrame(companies)
df_companies['investor_name'] = df_companies['investor_name'].to_string()

technologies = {
    'assignee': info_technology['assignee'],
    'patent_number': info_technology['patent number'],
    'stage_number': info_technology['cluster'],
    'coord_x': np.nan,
    'coord_y': np.nan
}
df_technology = pd.DataFrame(technologies)
df_technology['assignee'] = df_technology['assignee'].astype(str)

science = {
    'title': info_science['title'],
    'affiliation': info_science['affiliation'],
    'stage_number': info_science['type'],
    'coord_x': np.nan,
    'coord_y': np.nan
}
df_science = pd.DataFrame(science)
df_science['affiliation'] = df_science['affiliation'].astype(str)

fig = plt.figure(figsize=(100, 66))  # Adjust the figure size as needed
ax = fig.add_subplot(111, projection='3d')
ax.set_axis_off()
# Setting the axes properties (limits, labels, and title)
ax.set_xlim3d([0, 4])
ax.set_ylim3d([0, 4])
ax.set_zlim3d([-33, 14])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('')
def draw_planes():
    points_investor = np.array([[0, 0, 14], [0, 4, 14], [4, 4, 14], [4, 0, 14]])
    # Company layer
    points_company = np.array([[0, 0, 0], [0, 4, 0], [4, 4, 0], [4, 0, 0]])
    # Technology layer
    points_technology = np.array([[0, 0, -16], [0, 4, -16], [4, 4, -16], [4, 0, -16]])

    points_science = np.array([[0, 0, -33], [0, 4, -33], [4, 4, -33], [4, 0, -33]])


    # Draw the planes
    verts_investor = [list(points_investor)]
    verts_company = [list(points_company)]
    verts_technology =[list(points_technology)]
    verts_science = [list(points_science)]

    # Create the polygons for the planes and add them to the axis
    ax.add_collection3d(Poly3DCollection(verts_investor, facecolors='white', linewidths=1, edgecolors='black', alpha=.5))
    ax.add_collection3d(Poly3DCollection(verts_company, facecolors='white', linewidths=1, edgecolors='black', alpha=.5))
    ax.add_collection3d(Poly3DCollection(verts_technology, facecolors='white', linewidths=1, edgecolors='black', alpha=.5))
    ax.add_collection3d(Poly3DCollection(verts_science, facecolors='white', linewidths=1,edgecolors='black', alpha=.5  ))

    ax.set_box_aspect([1,1,2])
    # legend0 = ax.legend(fontsize=50, title='Investors Layer', title_fontsize='60',
    #                     loc='upper left', bbox_to_anchor=(-0.01, 0.9))
    # ax.add_artist(legend0)

def draw_industry_connections():
    ratios = np.array([0.7, 1.4, 0.9, 1.6, 1.4])
    # Radii are proportional to the square root of the area
    radii = np.sqrt(ratios / np.pi)

    # Define the center points for each circle
    circle_centers = [(3.2, 0.8, 0), (0.9, 0.9, 0), (0.9, 3.1, 0), (2, 2, 0), (3.1, 3.1, 0)]
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
        handle, = ax.plot(x, y, z, color=colors, linewidth=4, label=label)
        plot_handles.append(handle)

    # scatter of the head layer
    for i in range(len(df_investors)):
        np.random.seed(19680801 + i)
        n = 1
        rng = np.random.default_rng()
        xs = rng.uniform(0, 4, n)
        ys = rng.uniform(0, 4, n)
        df_investors.loc[i, 'coord_x'] = xs
        df_investors.loc[i, 'coord_y'] = ys
        # Plot
        ax.scatter(xs, ys, 14, color='purple')

    # scatter of the bottom layer
    def generate_points_in_circle(center, radius, n):
        theta = np.random.uniform(0, 2 * np.pi, n)
        r = radius * np.sqrt(np.random.uniform(0, 1, n))
        x = center[0] + r * np.cos(theta)
        y = center[1] + r * np.sin(theta)
        return x, y

    stage_row_1 = df_companies[df_companies['stage_number'] == 0]
    for index, company in stage_row_1.iterrows():
        np.random.seed(19680101 + index)  # Make sure the seed changes each iteration
        xs1, ys1 = generate_points_in_circle(circle_centers[0], radii[0], 1)
        stage_row_1.loc[index, 'coord_x'] = xs1[0]  # Since xs1 is an array, we take the first element
        stage_row_1.loc[index, 'coord_y'] = ys1[0]  # Since ys1 is an array, we take the first element
        df_companies.loc[index, 'coord_x'] = xs1
        df_companies.loc[index, 'coord_y'] = ys1
        ax.scatter(xs1, ys1, 0, color='purple')

    stage_row_2 = df_companies[df_companies['stage_number'] == 1]
    for index, company in stage_row_2.iterrows():
        np.random.seed(13680101 + index)
        xs2, ys2 = generate_points_in_circle(circle_centers[1], radii[1], 1)
        stage_row_2.loc[index, 'coord_x'] = xs2
        stage_row_2.loc[index, 'coord_y'] = ys2
        df_companies.loc[index, 'coord_x'] = xs2
        df_companies.loc[index, 'coord_y'] = ys2
        ax.scatter(xs2, ys2, 0, color='#069AF3')

    stage_row_3 = df_companies[df_companies['stage_number'] == 2]
    for index, company in stage_row_3.iterrows():
        np.random.seed(19630101 + index)
        xs3, ys3 = generate_points_in_circle(circle_centers[2], radii[2], 1)
        stage_row_3.loc[index, 'coord_x'] = xs3
        stage_row_3.loc[index, 'coord_y'] = ys3
        df_companies.loc[index, 'coord_x'] = xs3
        df_companies.loc[index, 'coord_y'] = ys3
        ax.scatter(xs3, ys3, 0, color='red')

    stage_row_4 = df_companies[df_companies['stage_number'] == 3]
    for index, company in stage_row_4.iterrows():
        np.random.seed(19689101 + index)
        xs4, ys4 = generate_points_in_circle(circle_centers[3], radii[3], 1)
        stage_row_4.loc[index, 'coord_x'] = xs4
        stage_row_4.loc[index, 'coord_y'] = ys4
        df_companies.loc[index, 'coord_x'] = xs4
        df_companies.loc[index, 'coord_y'] = ys4
        ax.scatter(xs4, ys4, 0, color='green')

    stage_row_5 = df_companies[df_companies['stage_number'] == 4]
    for index, company in stage_row_5.iterrows():
        np.random.seed(19689101 + index)
        xs5, ys5 = generate_points_in_circle(circle_centers[4], radii[4], 1)
        stage_row_5.loc[index, 'coord_x'] = xs5
        stage_row_5.loc[index, 'coord_y'] = ys5
        df_companies.loc[index, 'coord_x'] = xs5
        df_companies.loc[index, 'coord_y'] = ys5
        ax.scatter(xs5, ys5, 0, color='orange')

    legend1 = ax.legend(handles=plot_handles, fontsize=50, title='Business Layer', title_fontsize='60',
                        loc='center left', bbox_to_anchor=(-0.01, 0.65))
    ax.add_artist(legend1)


    def draw_investment_connections(ax, df_investors, df_stage, color):
        for index, company in tqdm(df_stage.iterrows(), total=df_stage.shape[0], desc='Drawing Connections'):
            company_x, company_y = company['coord_x'], company['coord_y']
            # Split investor names and strip to remove leading/trailing whitespaces
            investors_list = [inv.strip() for inv in company['investor_name'].split(';')]

            # If more than five investors, randomly select five
            if len(investors_list) > 3:
                investors_list = random.sample(investors_list, 3)

            for investor in investors_list:
                # Find the investor in df_investors
                matched_investor = df_investors[df_investors['name'] == investor]
                if not matched_investor.empty:
                    # Assuming the investor DataFrame might have multiple matches, iterate through all
                    for _, inv in matched_investor.iterrows():
                        investor_x, investor_y = inv['coord_x'], inv['coord_y']
                        # Draw a line from company to investor
                        line = [[company_x, company_y, 0], [investor_x, investor_y, 14]]
                        ax.add_collection3d(Line3DCollection([line], colors=color, linewidths=2, linestyles=':', alpha=0.8))


    draw_investment_connections(ax, df_investors, stage_row_1, 'purple')
    draw_investment_connections(ax, df_investors, stage_row_2, '#069AF3')
    draw_investment_connections(ax, df_investors, stage_row_3, 'red')
    draw_investment_connections(ax, df_investors, stage_row_4, 'green')
    draw_investment_connections(ax, df_investors, stage_row_5, 'orange')

def draw_technology_connections():
    ratios = np.array([1, 1.2, 0.6, 0.5, 1, 0.7])
    # Radii are proportional to the square root of the area
    radii = np.sqrt(ratios / np.pi)

    # Define the center points for each circle
    circle_centers = [(2.3, 2.8, -16), (1.0, 2.8, -16), (0.9, 1.0, -16), (3.4, 2.8, -16), (3.3, 1.0, -16), (2.0, 1.0, -16)]
    colors = [('orange'), ('#0000FF'), ('green'), ('red'), ('#069AF3'), ('purple')]
    labels = ['Sensor Systems', 'IoT', 'Hearing aid', 'Medical', 'Telemedicine', 'AI and Robots']
    plot_handles = []

    # Draw the circles on the lower plane
    for center, radius, colors, label in zip(circle_centers, radii, colors, labels):
        # Parametric equation of a circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        z = np.full_like(x, center[2])
        handle, = ax.plot(x, y, z, color=colors, linewidth=4, label=label)
        plot_handles.append(handle)

    # scatter of the bottom layer
    def generate_points_in_circle(center, radius, n):
        theta = np.random.uniform(0, 2 * np.pi, n)
        r = radius * np.sqrt(np.random.uniform(0, 1, n))
        x = center[0] + r * np.cos(theta)
        y = center[1] + r * np.sin(theta)
        return x, y

    stage_row_1 = df_technology[df_technology['stage_number'] == 0]
    for index, technology in stage_row_1.iterrows():
        np.random.seed(19680101 + index)
        xs1, ys1 = generate_points_in_circle(circle_centers[0], radii[0], 1)
        stage_row_1.loc[index, 'coord_x'] = xs1[0]
        stage_row_1.loc[index, 'coord_y'] = ys1[0]
        df_technology.loc[index, 'coord_x'] = xs1
        df_technology.loc[index, 'coord_y'] = ys1
        ax.scatter(xs1, ys1, -16, color='orange')

    stage_row_2 = df_technology[df_technology['stage_number'] == 1]
    for index, technology in stage_row_2.iterrows():
        np.random.seed(13680101 + index)
        xs2, ys2 = generate_points_in_circle(circle_centers[1], radii[1], 1)
        stage_row_2.loc[index, 'coord_x'] = xs2
        stage_row_2.loc[index, 'coord_y'] = ys2
        df_technology.loc[index, 'coord_x'] = xs2
        df_technology.loc[index, 'coord_y'] = ys2
        ax.scatter(xs2, ys2, -16, color='#0000FF')

    stage_row_3 = df_technology[df_technology['stage_number'] == 2]
    for index, technology in stage_row_3.iterrows():
        np.random.seed(19630101 + index)
        xs3, ys3 = generate_points_in_circle(circle_centers[2], radii[2], 1)
        stage_row_3.loc[index, 'coord_x'] = xs3
        stage_row_3.loc[index, 'coord_y'] = ys3
        df_technology.loc[index, 'coord_x'] = xs3
        df_technology.loc[index, 'coord_y'] = ys3
        ax.scatter(xs3, ys3, -16, color='green')

    stage_row_4 = df_technology[df_technology['stage_number'] == 3]
    for index, technology in stage_row_4.iterrows():
        np.random.seed(19689101 + index)
        xs4, ys4 = generate_points_in_circle(circle_centers[3], radii[3], 1)
        stage_row_4.loc[index, 'coord_x'] = xs4
        stage_row_4.loc[index, 'coord_y'] = ys4
        df_technology.loc[index, 'coord_x'] = xs4
        df_technology.loc[index, 'coord_y'] = ys4
        ax.scatter(xs4, ys4, -16, color='red')

    stage_row_5 = df_technology[df_technology['stage_number'] == 4]
    for index, technology in stage_row_5.iterrows():
        np.random.seed(19689101 + index)
        xs5, ys5 = generate_points_in_circle(circle_centers[4], radii[4], 1)
        stage_row_5.loc[index, 'coord_x'] = xs5
        stage_row_5.loc[index, 'coord_y'] = ys5
        df_technology.loc[index, 'coord_x'] = xs5
        df_technology.loc[index, 'coord_y'] = ys5
        ax.scatter(xs5, ys5, -16, color='#069AF3')

    stage_row_6 = df_technology[df_technology['stage_number'] == 5]
    for index, technology in stage_row_6.iterrows():
        np.random.seed(19689101 + index)
        xs6, ys6 = generate_points_in_circle(circle_centers[5], radii[5], 1)
        stage_row_6.loc[index, 'coord_x'] = xs6
        stage_row_6.loc[index, 'coord_y'] = ys6
        df_technology.loc[index, 'coord_x'] = xs6
        df_technology.loc[index, 'coord_y'] = ys6
        ax.scatter(xs6, ys6, -16, color='purple')
    #
    legend2 = ax.legend(handles=plot_handles, fontsize=50, title='Technology Layer', title_fontsize='60',
                        loc='lower left', bbox_to_anchor=(-0.01, 0.33), fancybox=True)
    ax.add_artist(legend2)

    def normalize_terms(text, term_map):
        for old, new in term_map.items():
            pattern = r'\b' + re.escape(old) + r'\b'
            text = re.sub(pattern, new, text, flags=re.IGNORECASE)
        return text

    def contains_ignore_word(name, ignore_list):
        for word in ignore_list:
            if word in name:
                return True
        return False

    def draw_technology_connections(ax, df_company, df_stage, color, threshold=90,
                                    ignore_list=['to', 'inc.', 'llc', 'ltd.', 'ware', 'roz', 'elva', 'akira', 'ripple',
                                                 'sana', 'eeve', 'medical device'],
                                    term_map={'univ': 'university', 'inst': 'institute'}, output_csv='connections.csv'):
        connections_record = pd.DataFrame()

        total_connections = 0  # 初始化总连接数

        all_companies_normalized = {}
        for index, row in df_company.iterrows():
            normalized_name = normalize_terms(row['co_name'].lower().strip(), term_map)
            if not contains_ignore_word(normalized_name, ignore_list):
                all_companies_normalized[normalized_name] = (row['co_name'], (row['coord_x'], row['coord_y']))

        for index, technology in tqdm(df_stage.iterrows(), total=df_stage.shape[0], desc='Drawing Connections'):
            technology_x, technology_y = technology['coord_x'], technology['coord_y']
            # Normalize, remove duplicates, and filter using ignore list for technology assignees
            company_list = set(
                [normalize_terms(inv.lower().strip(), term_map) for inv in technology['assignee'].split(';')
                 if not contains_ignore_word(normalize_terms(inv.lower().strip(), term_map),
                                             ignore_list) and inv.strip() != ''])
            current_connected_companies = set()

            for company in company_list:
                normalized_company = normalize_terms(company, term_map)
                if normalized_company in current_connected_companies:
                    continue

                best_match, score = process.extractOne(normalized_company, all_companies_normalized.keys())
                if score >= threshold and not contains_ignore_word(best_match, ignore_list):
                    matched_company, (company_x, company_y) = all_companies_normalized[best_match]
                    current_connected_companies.add(matched_company)

                    connections_record.loc[company, matched_company] = connections_record.get(matched_company,
                                                                                              pd.Series(dtype=int)).get(
                        company, 0) + 1

                    print(f"Matched '{company}' with '{matched_company}' with a score of {score}")

                    line = [[company_x, company_y, 0], [technology_x, technology_y, -16]]
                    ax.add_collection3d(
                        Line3DCollection([line], colors=color, linewidths=2, linestyles=':', alpha=0.5, zorder=3))
                    total_connections += 1

        print(f"Total connections found: {total_connections}")

    draw_technology_connections(ax, df_companies, stage_row_1, 'orange')
    draw_technology_connections(ax, df_companies, stage_row_2, '#0000FF')
    draw_technology_connections(ax, df_companies, stage_row_3, 'green')
    draw_technology_connections(ax, df_companies, stage_row_4, 'red')
    draw_technology_connections(ax, df_companies, stage_row_5, '#069AF3')
    draw_technology_connections(ax, df_companies, stage_row_6, 'purple')

def draw_science_connections():
    ratios = np.array([1, 0.6, 2.7, 1.1, 0.7, 0.4, 0.8])
    # Radii are proportional to the square root of the area
    radii = np.sqrt(ratios / np.pi)

    # Define the center points for each circle
    circle_centers = [(0.9, 0.8, -33), (2.2, 0.7, -33), (1.0, 2.9, -33), (2.9, 3.0, -33), (2.2, 1.8, -33), (3.3, 0.6, -33), (3.4, 1.8, -33)]

    colors = [('#069AF3'), ('green'), ('#0000FF'), ('red'), ('orange'),('purple'),("#6C733D")]
    labels = ['Monitoring systems ', 'Rehabilitation', 'Dementia', 'Surgery and Cancer', 'Infectious diseases', 'AI', 'Chronic diseases']
    plot_handles = []

    # Draw the circles on the lower plane
    for center, radius, colors, label in zip(circle_centers, radii, colors, labels):
        # Parametric equation of a circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        z = np.full_like(x, center[2])
        handle, = ax.plot(x, y, z, color=colors, linewidth=4, label=label)
        plot_handles.append(handle)


    # scatter of the bottom layer
    def generate_points_in_circle(center, radius, n):
        theta = np.random.uniform(0, 2 * np.pi, n)
        r = radius * np.sqrt(np.random.uniform(0, 1, n))
        x = center[0] + r * np.cos(theta)
        y = center[1] + r * np.sin(theta)
        return x, y

    stage_row_1 = df_science[df_science['stage_number'] == 'a']
    for index, science in stage_row_1.iterrows():
        np.random.seed(19680101 + index)
        xs1, ys1 = generate_points_in_circle(circle_centers[0], radii[0], 1)
        stage_row_1.loc[index, 'coord_x'] = xs1[0]
        stage_row_1.loc[index, 'coord_y'] = ys1[0]
        df_science.loc[index, 'coord_x'] = xs1
        df_science.loc[index, 'coord_y'] = ys1
        ax.scatter(xs1, ys1, -33, color='#069AF3')

    stage_row_2 = df_science[df_science['stage_number'] == 'b']
    for index, science in stage_row_2.iterrows():
        np.random.seed(13680101 + index)
        xs2, ys2 = generate_points_in_circle(circle_centers[1], radii[1], 1)
        stage_row_2.loc[index, 'coord_x'] = xs2
        stage_row_2.loc[index, 'coord_y'] = ys2
        df_science.loc[index, 'coord_x'] = xs2
        df_science.loc[index, 'coord_y'] = ys2
        ax.scatter(xs2, ys2, -33, color='green')

    stage_row_3 = df_science[df_science['stage_number'] == 'c']
    for index, science in stage_row_3.iterrows():
        np.random.seed(19630101 + index)
        xs3, ys3 = generate_points_in_circle(circle_centers[2], radii[2], 1)
        stage_row_3.loc[index, 'coord_x'] = xs3
        stage_row_3.loc[index, 'coord_y'] = ys3
        df_science.loc[index, 'coord_x'] = xs3
        df_science.loc[index, 'coord_y'] = ys3
        ax.scatter(xs3, ys3, -33, color='#0000FF')

    stage_row_4 = df_science[df_science['stage_number'] == 'd']
    for index, science in stage_row_4.iterrows():
        np.random.seed(19689101 + index)
        xs4, ys4 = generate_points_in_circle(circle_centers[3], radii[3], 1)
        stage_row_4.loc[index, 'coord_x'] = xs4
        stage_row_4.loc[index, 'coord_y'] = ys4
        df_science.loc[index, 'coord_x'] = xs4
        df_science.loc[index, 'coord_y'] = ys4
        ax.scatter(xs4, ys4, -33, color='red')

    stage_row_5 = df_science[df_science['stage_number'] == 'e']
    for index, science in stage_row_5.iterrows():
        np.random.seed(19689101 + index)
        xs5, ys5 = generate_points_in_circle(circle_centers[4], radii[4], 1)
        stage_row_5.loc[index, 'coord_x'] = xs5
        stage_row_5.loc[index, 'coord_y'] = ys5
        df_science.loc[index, 'coord_x'] = xs5
        df_science.loc[index, 'coord_y'] = ys5
        ax.scatter(xs5, ys5, -33, color='orange')

    stage_row_6 = df_science[df_science['stage_number'] == 'f']
    for index, science in stage_row_6.iterrows():
        np.random.seed(19689101 + index)
        xs6, ys6 = generate_points_in_circle(circle_centers[5], radii[5], 1)
        stage_row_6.loc[index, 'coord_x'] = xs6
        stage_row_6.loc[index, 'coord_y'] = ys6
        df_science.loc[index, 'coord_x'] = xs6
        df_science.loc[index, 'coord_y'] = ys6
        ax.scatter(xs6, ys6, -33, color='purple')

    stage_row_7 = df_science[df_science['stage_number'] == 'g']
    for index, science in stage_row_7.iterrows():
        np.random.seed(19689101 + index)
        xs7, ys7 = generate_points_in_circle(circle_centers[6], radii[6], 1)
        stage_row_7.loc[index, 'coord_x'] = xs7
        stage_row_7.loc[index, 'coord_y'] = ys7
        df_science.loc[index, 'coord_x'] = xs7
        df_science.loc[index, 'coord_y'] = ys7
        ax.scatter(xs7, ys7, -33, color='#6C733D')
    #
    legend3 = ax.legend(handles=plot_handles, fontsize=50, title='Science Layer', title_fontsize='60',
                        loc='lower left', bbox_to_anchor=(-0.01, 0.05), fancybox=True)
    ax.add_artist(legend3)

    def normalize_terms(text, term_map):
        for old, new in term_map.items():
            pattern = r'\b' + re.escape(old) + r'\b'
            text = re.sub(pattern, new, text, flags=re.IGNORECASE)
        return text


    def draw_science_technology_connections(ax, df_science, df_technology, color, threshold=90,
                                            ignore_list=['to', 'inc.', 'llc', 'ltd.', 'cera', 'anna university', 'cea',
                                                         'sana', 'one medical'],
                                            term_map={'univ': 'university', 'inst': 'institute'}):
        connection_counter = 0
        ignore_list_normalized = [normalize_terms(word.lower(), term_map) for word in ignore_list]

        for index, science in tqdm(df_science.iterrows(), total=df_science.shape[0], desc='Drawing Connections'):
            science_x, science_y = science['coord_x'], science['coord_y']
            # Normalize, remove duplicates, and filter using ignore list for science affiliations
            affiliations = set([normalize_terms(affil.lower().strip(), term_map) for affil in
                                science['affiliation'].split(';') if
                                affil.lower().strip() != 'nan' and affil.strip() != '' and normalize_terms(
                                    affil.lower().strip(), term_map) not in ignore_list_normalized])

            technology_info = {}
            for _, tech in df_technology.iterrows():
                # Normalize, remove duplicates, and filter using ignore list for technology assignees
                assignees = set(
                    [normalize_terms(assignee.lower().strip(), term_map) for assignee in tech['assignee'].split(';')
                     if assignee.lower().strip() != 'nan' and assignee.strip() != '' and normalize_terms(
                        assignee.lower().strip(), term_map) not in ignore_list_normalized])
                for normalized_assignee in assignees:
                    if normalized_assignee not in technology_info:
                        technology_info[normalized_assignee] = []
                    technology_info[normalized_assignee].append((tech['coord_x'], tech['coord_y']))

            for affiliation in affiliations:
                best_match, score = process.extractOne(affiliation, list(technology_info.keys()))
                if score >= threshold and best_match in technology_info and best_match not in ignore_list_normalized:
                    for tech_x, tech_y in technology_info[best_match]:
                        connection_counter += 1
                        print(
                            f"Connection #{connection_counter}: '{affiliation}' (Science) at ({science_x}, {science_y}) connected to '{best_match}' (Technology) at ({tech_x}, {tech_y}) with score {score}")
                        line = [[science_x, science_y, -33], [tech_x, tech_y, -16]]
                        ax.add_collection3d(
                            Line3DCollection([line], colors=color, linewidths=2, linestyles=':', alpha=1, zorder=5))

        print(f"Total connections made: {connection_counter}")

    draw_science_technology_connections(ax, stage_row_1, df_technology,'#069AF3')
    draw_science_technology_connections(ax, stage_row_2, df_technology, 'green')
    draw_science_technology_connections(ax, stage_row_3, df_technology, '#0000FF')
    draw_science_technology_connections(ax, stage_row_4, df_technology, 'red')
    draw_science_technology_connections(ax, stage_row_5, df_technology, 'orange')
    draw_science_technology_connections(ax, stage_row_6, df_technology, 'purple')
    draw_science_technology_connections(ax, stage_row_7, df_technology, '#6C733D')


draw_planes()
# draw_industry_connections()
# draw_technology_connections()
# draw_science_connections()
plt.savefig('plane.png')
