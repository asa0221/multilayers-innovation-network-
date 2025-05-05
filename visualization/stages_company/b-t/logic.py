import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Load the data
df = pd.read_excel('/Users/asa/PycharmProjects/stages_company/b-t/logic.xlsx')

# Convert all columns to numeric and handle NaN values if any
df = df.apply(pd.to_numeric, errors='coerce')
df.dropna(inplace=True)  # Drop rows with NaNs

# The dependent variable (outcome)
y = df['whether_fund']

# The independent variables (predictors)
X = df[['whether_have_patent']]

# If you want to include other variables, uncomment the following lines
# Create the squared term for 'Stage Number'
df['Stage Number Squared'] = df['Stage Number'] ** 2
X = pd.concat([X, df[['Stage Number', 'Stage Number Squared']]], axis=1)

# Add a constant to the model (the intercept)
X = sm.add_constant(X)

# Check for multicollinearity
vif = pd.DataFrame()
vif['Variable'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print(vif)

# Build the logistic regression model
try:
    model = sm.Logit(y, X)
    result = model.fit(maxiter=100)  # Increase the maximum number of iterations

    # Save the result summary to a DataFrame
    result_summary = result.summary()

    # Convert the result summary to HTML format
    result_html = result_summary.tables[1].as_html()

    # Convert HTML to DataFrame
    result_df = pd.read_html(result_html, header=0, index_col=0)[0]

    # Collect additional performance metrics
    performance_metrics = {
        'Pseudo R-squared': [result.prsquared],
        'Log-Likelihood': [result.llf],
        'Converged': [result.mle_retvals['converged']],
        'LL-Null': [result.llnull],
        'LLR p-value': [result.llr_pvalue]
    }

    # Convert performance metrics to DataFrame
    performance_df = pd.DataFrame(performance_metrics)

    # Combine the result DataFrame and performance metrics DataFrame
    combined_df = pd.concat([result_df, performance_df], axis=1)

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv('logistic_regression_results.csv')

except Exception as e:
    print(e)
