import pandas as pd
from scipy.stats import chi2_contingency
import statsmodels.api as sm
df = pd.read_excel('/Users/asa/PycharmProjects/stages_company/b-t/chi.xlsx')
# # Create a contingency table
# contingency_table = pd.crosstab(df['Stage Number'], df['whether_have_patent'])
#
# # Perform the chi-square test
# chi2_stat, p_val, dof, ex = chi2_contingency(contingency_table)
#
# print("Chi-square statistic:", chi2_stat)
# print("p-value:", p_val)
# print("Degrees of freedom:", dof)
# print("Expected frequencies:", ex)

