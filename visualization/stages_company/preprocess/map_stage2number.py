import pandas as pd

# Define the mapping of stages to numbers
stage_mapping = {
    "Ideation to Seed Stage": 1,
    "Early Stage (Initial Traction and Product-Market Fit)": 2,
    "Growth Stage (Scaling and Expansion)": 3,
    "Maturity and Exit Stage": 4,
}

# Keywords for each stage
stage_keywords = {
    1: ["Angel", "Pre-seed", "Grants", "Grant", "Non-equity Assistance", "Equity Crowdfunding", "Seed", "Idea",
        "Product Crowdfunding"],
    2: ["Series A", "Convertible Note", "Corporate Rounds", "Debt Financing", "Early Stage Venture",
        "Venture - Series Unknown"],
    3: ["Series B", "Series C", "Late-stage Venture Capital", "Private Equity", "Secondary Market", "Debt Financing",
        "Startup Scaling"],
    4: ["Series D", "Series E", "Series F", "IPO", "M&A", "Post-IPO Equity", "Post-IPO Debt"],
}


def map_stage_to_number(stage):
    """Map a stage description to a stage number."""
    for number, keywords in stage_keywords.items():
        if any(keyword in stage for keyword in keywords):
            return number
    # Return None if no stage matches
    return None


def process_file(filename):
    # Read the file
    df = pd.read_csv(filename)

    # Map the 'Stage' column to the corresponding stage number
    df['Stage Number'] = df['Last Funding Type'].apply(lambda x: map_stage_to_number(x) if pd.notnull(x) else None)

    # Save the updated DataFrame to a new file
    new_filename = 'company_stage.csv'
    df.to_csv(new_filename, index=False)


# Example usage
file_path = '/Users/asa/PycharmProjects/stages_company/company_data/company_invested.csv'
process_file(file_path)
