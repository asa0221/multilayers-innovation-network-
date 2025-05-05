import pandas as pd


def count_investors(input_csv, column_name, output_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv)

    # Ensure the column exists
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the input CSV.")

    # Split the investor names and flatten the list
    investors = df[column_name].str.split(';').explode().str.strip()

    # Count unique investors
    investor_count = investors.value_counts().reset_index()
    investor_count.columns = ['Investor', 'Count']

    # Write to a new CSV file
    investor_count.to_csv(output_csv, index=False)
    print(f"Output saved to {output_csv}")

def count_stages_per_investor(investors_csv, data_csv, output_csv):
    # Load the list of investors
    investors_df = pd.read_csv(investors_csv, header=None)
    investors = investors_df.iloc[:, 0].unique()

    # Load the data CSV, specifying only the necessary columns
    data_df = pd.read_csv(data_csv, usecols=[1, 6], header=None)
    data_df.columns = ['Invested', 'industry']

    # Initialize an empty list to hold the output data
    output_data = []

    # Define the range for clusters (adjust as needed for your data)
    cluster_range = range(0, 4)  # Assuming clusters go from 0 to 5

    # Iterate over each unique investor
    for investor in investors:
        # Initialize the count of each cluster for this investor
        clusters_count = {f'Cluster {cluster}': 0 for cluster in cluster_range}

        # Iterate over each row in the data DataFrame
        for _, row in data_df.iterrows():
            # Check if the current investor is in this row's list of investors
            if investor.strip() in [inv.strip() for inv in str(row['Matched Inventors']).split(';')]:
                # Increment the count for this row's cluster
                cluster_key = f'Cluster {int(row["industry"])}'
                if cluster_key in clusters_count:  # Safe check to ensure the cluster key exists
                    clusters_count[cluster_key] += 1

        # Sum the cluster counts to get the total number of clusters for this investor
        total_clusters = sum(clusters_count.values())

        # Prepare the row for this investor
        investor_row = [investor] + list(clusters_count.values()) + [total_clusters]
        output_data.append(investor_row)

    # Column headers including the total count
    columns = ['Investor'] + [f'Cluster {cluster}' for cluster in cluster_range] + ['Total Clusters']

    # Create the output DataFrame
    output_df = pd.DataFrame(output_data, columns=columns)

    # Write the results to the output CSV file
    output_df.to_csv(output_csv, index=False)
    print(f"Output saved to {output_csv}")



count_stages_per_investor('/Users/asa/PycharmProjects/stages_company/investor_data/updated_Investors.csv', '/Users/asa/PycharmProjects/stages_company/Industry/b2t1.csv', 'output1.csv')
