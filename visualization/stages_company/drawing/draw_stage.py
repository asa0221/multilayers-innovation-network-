import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np
import pandas as pd
from tqdm import tqdm
import random
from fuzzywuzzy import process
import re



info_companies = pd.read_csv('/Users/asa/PycharmProjects/stages_company/company_data/updated_company_invested.csv')
info_investors = pd.read_csv('/Users/asa/PycharmProjects/stages_company/investor_data/updated_Investors.csv')
info_technology = pd.read_csv('/Users/asa/PycharmProjects/stages_company/b-t/patent.csv')

# Create a DataFrame from a dictionary
investors = {
    'name': info_investors['Name'],
    'coord_x': np.nan,
    'coord_y': np.nan
}
df_investors = pd.DataFrame(investors)

companies = {
    'co_name': info_companies['Name'],
    'investor_name': info_companies['Inventors'],
    'stage_number': info_companies['Stage Number'],
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

fig = plt.figure(figsize=(80, 46))  # Adjust the figure size as needed
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
    points_investor = np.array([[0, 0, 14], [0, 4, 14], [4, 4, 14], [4, 0, 14]])

    # Company layer
    points_company = np.array([[0, 0, 0], [0, 4, 0], [4, 4, 0], [4, 0, 0]])
    # Technology layer
    points_technology = np.array([[0, 0, -14], [0, 4, -14], [4, 4, -14], [4, 0, -14]])

    # Draw the planes
    verts_investor = [list(points_investor)]
    verts_company = [list(points_company)]
    verts_technology =[list(points_technology)]

    # Create the polygons for the planes and add them to the axis
    ax.add_collection3d(Poly3DCollection(verts_investor, facecolors='white', linewidths=1, edgecolors='black', alpha=.5))
    ax.add_collection3d(Poly3DCollection(verts_company, facecolors='white', linewidths=1, edgecolors='black', alpha=.5))
    ax.add_collection3d(Poly3DCollection(verts_technology, facecolors='white', linewidths=1, edgecolors='black', alpha=.5))

    ax.set_box_aspect([1,1,2])
    legend0 = ax.legend(fontsize=40, title='Investors Layer', title_fontsize='50',
                        loc='upper left', bbox_to_anchor=(-0.01, 0.95))
    ax.add_artist(legend0)
def draw_stage_connections():
    ratios = np.array([3.8, 1.6, 1.1, 0.4])
    radii = np.sqrt(ratios / np.pi)

    # Define the center points for each circle
    circle_centers = [(1.3, 1.6, 0), (3.2, 0.8, 0), (3.2, 2.2, 0), (3.2, 3.3, 0)]
    colors = [('#069AF3'), ('orange'), ('purple'), ('red')]
    labels = ['Ideation to Seed Stage', 'Early Stage', 'Growth Stage', 'Maturity and Exit Stage']
    plot_handles = []

    # Draw the circles on the lower plane
    for center, radius, colors, label in zip(circle_centers, radii, colors, labels):
        # Parametric equation of a circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        z = np.full_like(x, center[2])
        handle, = ax.plot(x, y, z, color=colors, linewidth=4, linestyle='--', label=label)
        plot_handles.append(handle)

    # scatter of the head layer
    for i in range(len(df_investors)):
        np.random.seed(19680801+i)
        n = 1
        rng = np.random.default_rng()
        xs = rng.uniform(0, 4, n)
        ys = rng.uniform(0, 4, n)
        df_investors.loc[i, 'coord_x'] = xs
        df_investors.loc[i, 'coord_y'] = ys
        # Plot
        ax.scatter(xs, ys, 14, color='blue')

    # scatter of the bottom layer
    def generate_points_in_circle(center, radius, n):
        theta = np.random.uniform(0, 2 * np.pi, n)
        r = radius * np.sqrt(np.random.uniform(0, 1, n))
        x = center[0] + r * np.cos(theta)
        y = center[1] + r * np.sin(theta)
        return x, y

    stage_row_1 = df_companies[df_companies['stage_number'] == 1]
    for index, company in stage_row_1.iterrows():
        np.random.seed(19680101 + index)  # Make sure the seed changes each iteration
        xs1, ys1 = generate_points_in_circle(circle_centers[0], radii[0], 1)
        stage_row_1.loc[index, 'coord_x'] = xs1[0]  # Since xs1 is an array, we take the first element
        stage_row_1.loc[index, 'coord_y'] = ys1[0]
        df_companies.loc[index, 'coord_x'] = xs1
        df_companies.loc[index, 'coord_y'] = ys1
        ax.scatter(xs1, ys1, 0, color='#069AF3')

    stage_row_2 = df_companies[df_companies['stage_number'] == 2]
    for index, company in stage_row_2.iterrows():
        np.random.seed(13680101 + index)
        xs2, ys2 = generate_points_in_circle(circle_centers[1], radii[1], 1)
        stage_row_2.loc[index, 'coord_x'] = xs2
        stage_row_2.loc[index, 'coord_y'] = ys2
        df_companies.loc[index, 'coord_x'] = xs2
        df_companies.loc[index, 'coord_y'] = ys2
        ax.scatter(xs2, ys2, 0, color='orange')

    stage_row_3 = df_companies[df_companies['stage_number'] == 3]
    for index, company in stage_row_3.iterrows():
        np.random.seed(19630101 + index)
        xs3, ys3 = generate_points_in_circle(circle_centers[2], radii[2], 1)
        stage_row_3.loc[index, 'coord_x'] = xs3
        stage_row_3.loc[index, 'coord_y'] = ys3
        df_companies.loc[index, 'coord_x'] = xs3
        df_companies.loc[index, 'coord_y'] = ys3
        ax.scatter(xs3, ys3, 0, color='purple')

    stage_row_4 = df_companies[df_companies['stage_number'] == 4]
    for index, company in stage_row_4.iterrows():
        np.random.seed(19689101 + index)
        xs4, ys4 = generate_points_in_circle(circle_centers[3], radii[3], 1)
        stage_row_4.loc[index, 'coord_x'] = xs4
        stage_row_4.loc[index, 'coord_y'] = ys4
        df_companies.loc[index, 'coord_x'] = xs4
        df_companies.loc[index, 'coord_y'] = ys4
        ax.scatter(xs4, ys4, 0, color='red')


    def draw_investment_connections(ax, df_investors, df_stage, color):
        for index, company in tqdm(df_stage.iterrows(), total=df_stage.shape[0], desc='Drawing Connections'):
            company_x, company_y = company['coord_x'], company['coord_y']
            # Split investor names and strip to remove leading/trailing whitespaces
            investors_list = [inv.strip() for inv in company['investor_name'].split(';')]

            # If more than five investors, randomly select five
            if len(investors_list) > 3:
                investors_list = random.sample(investors_list, 5)

            for investor in investors_list:
                # Find the investor in df_investors
                matched_investor = df_investors[df_investors['name'] == investor]
                if not matched_investor.empty:
                    # Assuming the investor DataFrame might have multiple matches, iterate through all
                    for _, inv in matched_investor.iterrows():
                        investor_x, investor_y = inv['coord_x'], inv['coord_y']
                        # Draw a line from company to investor
                        line = [[company_x, company_y, 0], [investor_x, investor_y, 14]]
                        ax.add_collection3d(Line3DCollection([line], colors=color, linewidths=2, linestyles=':'))

    draw_investment_connections(ax, df_investors, stage_row_1, '#069AF3')
    draw_investment_connections(ax, df_investors, stage_row_2, 'orange')
    draw_investment_connections(ax, df_investors, stage_row_3, 'purple')
    draw_investment_connections(ax, df_investors, stage_row_4, 'red')
    legend1 = ax.legend(handles=plot_handles, fontsize=40, title='Business Layer', title_fontsize='50',
                        loc='center left', bbox_to_anchor=(-0.05, 0.5))
    ax.add_artist(legend1)

def draw_technology_connections():
    ratios = np.array([1, 1.2, 0.6, 0.5, 1, 0.7])
    # Radii are proportional to the square root of the area
    radii = np.sqrt(ratios / np.pi)

    # Define the center points for each circle
    circle_centers = [(2.3, 2.8, -14), (1.0, 2.8, -14), (0.9, 1.0, -14), (3.4, 2.8, -14), (3.3, 1.0, -14), (2.0, 1.0, -14)]
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
        handle, = ax.plot(x, y, z, color=colors, linewidth=4, linestyle='--', label=label)
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
        stage_row_1.loc[index, 'coord_x'] = xs1
        stage_row_1.loc[index, 'coord_y'] = ys1
        df_technology.loc[index, 'coord_x'] = xs1
        df_technology.loc[index, 'coord_y'] = ys1
        ax.scatter(xs1, ys1, -14, color='orange')

    stage_row_2 = df_technology[df_technology['stage_number'] == 1]
    for index, technology in stage_row_2.iterrows():
        np.random.seed(13680101 + index)
        xs2, ys2 = generate_points_in_circle(circle_centers[1], radii[1], 1)
        stage_row_2.loc[index, 'coord_x'] = xs2
        stage_row_2.loc[index, 'coord_y'] = ys2
        df_technology.loc[index, 'coord_x'] = xs2
        df_technology.loc[index, 'coord_y'] = ys2
        ax.scatter(xs2, ys2, -14, color='#0000FF')

    stage_row_3 = df_technology[df_technology['stage_number'] == 2]
    for index, technology in stage_row_3.iterrows():
        np.random.seed(19630101 + index)
        xs3, ys3 = generate_points_in_circle(circle_centers[2], radii[2], 1)
        stage_row_3.loc[index, 'coord_x'] = xs3
        stage_row_3.loc[index, 'coord_y'] = ys3
        df_technology.loc[index, 'coord_x'] = xs3
        df_technology.loc[index, 'coord_y'] = ys3
        ax.scatter(xs3, ys3, -14, color='green')

    stage_row_4 = df_technology[df_technology['stage_number'] == 3]
    for index, technology in stage_row_4.iterrows():
        np.random.seed(19689101 + index)
        xs4, ys4 = generate_points_in_circle(circle_centers[3], radii[3], 1)
        stage_row_4.loc[index, 'coord_x'] = xs4
        stage_row_4.loc[index, 'coord_y'] = ys4
        df_technology.loc[index, 'coord_x'] = xs4
        df_technology.loc[index, 'coord_y'] = ys4
        ax.scatter(xs4, ys4, -14, color='red')

    stage_row_5 = df_technology[df_technology['stage_number'] == 4]
    for index, technology in stage_row_5.iterrows():
        np.random.seed(19689101 + index)
        xs5, ys5 = generate_points_in_circle(circle_centers[4], radii[4], 1)
        stage_row_5.loc[index, 'coord_x'] = xs5
        stage_row_5.loc[index, 'coord_y'] = ys5
        df_technology.loc[index, 'coord_x'] = xs5
        df_technology.loc[index, 'coord_y'] = ys5
        ax.scatter(xs5, ys5, -14, color='#069AF3')

    stage_row_6 = df_technology[df_technology['stage_number'] == 5]
    for index, technology in stage_row_6.iterrows():
        np.random.seed(19689101 + index)
        xs6, ys6 = generate_points_in_circle(circle_centers[5], radii[5], 1)
        stage_row_6.loc[index, 'coord_x'] = xs6
        stage_row_6.loc[index, 'coord_y'] = ys6
        df_technology.loc[index, 'coord_x'] = xs6
        df_technology.loc[index, 'coord_y'] = ys6
        ax.scatter(xs6, ys6, -14, color='purple')

    def normalize_terms(text, term_map):
        for old, new in term_map.items():
            pattern = r'\b' + re.escape(old) + r'\b'
            text = re.sub(pattern, new, text, flags=re.IGNORECASE)
        return text

    def draw_technology_connections(ax, df_company, df_stage, color, threshold=90,
                                    ignore_list=['to', 'inc.', 'llc', 'ltd.', 'Ware', 'roz', 'Elva', 'Akira', 'ripple',
                                                 'Sana', 'EEVE', 'Medical device'],
                                    term_map={'univ': 'university', 'inst': 'institute'}, output_csv='connections.csv'):
        # Initialize an empty DataFrame to record the connection information
        connections_record = pd.DataFrame()

        total_connections = 0  # Initialize total connections count

        for index, technology in tqdm(df_stage.iterrows(), total=df_stage.shape[0], desc='Drawing Connections'):
            technology_x, technology_y = technology['coord_x'], technology['coord_y']
            # Normalize, remove duplicates, and filter using ignore list for technology assignees
            company_list = set(
                [normalize_terms(inv.lower().strip(), term_map) for inv in technology['assignee'].split(';')
                 if normalize_terms(inv.lower().strip(), term_map) not in ignore_list and inv.strip() != ''])
            current_connected_companies = set()  # Initialize for each technology item

            all_companies_normalized = {normalize_terms(row['co_name'].lower().strip(), term_map): (
                row['co_name'], (row['coord_x'], row['coord_y']))
                for index, row in df_company.iterrows() if
                normalize_terms(row['co_name'].lower().strip(), term_map) not in ignore_list}

            for company in company_list:
                if company in current_connected_companies:
                    continue

                best_match, score = process.extractOne(company, all_companies_normalized.keys())
                if score >= threshold:
                    matched_company, (company_x, company_y) = all_companies_normalized[best_match]
                    current_connected_companies.add(matched_company)

                    # Record the connection in the DataFrame
                    connections_record.loc[company, matched_company] = connections_record.get(matched_company,
                                                                                              pd.Series(dtype=int)).get(
                        company, 0) + 1

                    print(f"Matched '{company}' with '{matched_company}' with a score of {score}")

                    line = [[company_x, company_y, 0], [technology_x, technology_y, -14]]
                    ax.add_collection3d(
                        Line3DCollection([line], colors=color, linewidths=2, linestyles=':', alpha=0.5, zorder=3))
                    total_connections += 1  # Increment total connections count

        print(f"Total connections found: {total_connections}")  # Output total connections found

    draw_technology_connections(ax, df_companies, stage_row_1, 'orange')
    draw_technology_connections(ax, df_companies, stage_row_2, '#0000FF')
    draw_technology_connections(ax, df_companies, stage_row_3, 'green')
    draw_technology_connections(ax, df_companies, stage_row_4, 'red')
    draw_technology_connections(ax, df_companies, stage_row_5, '#069AF3')
    draw_technology_connections(ax, df_companies, stage_row_6, 'purple')
    legend2 = ax.legend(handles=plot_handles, fontsize=40, title='Technology Layer', title_fontsize='50',
                        loc='lower left', bbox_to_anchor=(-0.02,0.05), fancybox=True)
    ax.add_artist(legend2)
# Call the function to draw the parallel planes
draw_planes()
draw_stage_connections()
draw_technology_connections()
plt.savefig('investment_connections.png')

