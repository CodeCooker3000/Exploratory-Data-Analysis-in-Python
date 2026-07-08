import pandas as pd
import numpy as np
import pygal
from scipy import stats
from pygal.style import Style

# --- 1. DATA LOADING ---
filename = 'USA_Housing.csv'

try:
    df = pd.read_csv(filename)
    # Mapping CSV headers to easier variables
    income = df['Avg. Area Income']
    house_age = df['Avg. Area House Age']
    rooms = df['Avg. Area Number of Rooms']
    bedrooms = df['Avg. Area Number of Bedrooms']
    population = df['Area Population']
    price = df['Price']
    print(f"Dataset loaded: {df.shape[0]} rows found.\n")
except FileNotFoundError:
    print(f"Error: {filename} not found. Ensure it is in the same directory.")
    exit()

# --- 2. HYPOTHESIS TESTING (One-Sample T-Test) ---
# Question: Is the average area income significantly different from $70,000?
null_mean = 70000
t_stat, p_two_sided = stats.ttest_1samp(income, null_mean)

# One-sided tests
# alternative='greater' -> Right Tail
p_right = stats.ttest_1samp(income, null_mean, alternative='greater').pvalue
# alternative='less' -> Left Tail
p_left = stats.ttest_1samp(income, null_mean, alternative='less').pvalue

print("--- Hypothesis Testing (Income vs $70,000) ---")
print(f"Two-Sided P-value: {p_two_sided:.10f}")
print(f"Right-Tail P-value (Mean > 70k): {p_right:.10f}")
print(f"Left-Tail P-value  (Mean < 70k): {p_left:.10f}\n")

# --- 3. 2x2 CONTINGENCY TABLE ---
# Categorizing Income and Price based on their medians to create 2x2 bins
df['income_bin'] = np.where(income > income.median(), 'High Income', 'Low Income')
df['price_bin'] = np.where(price > price.median(), 'High Price', 'Low Price')

contingency_table = pd.crosstab(df['income_bin'], df['price_bin'])
chi2, p_chi, dof, expected = stats.chi2_contingency(contingency_table)

print("--- 2x2 Contingency Table (Income Level vs Price Level) ---")
print(contingency_table, "\n")
print(f"\nChi-Square Statistic: {chi2:.4f}")
print(f"P-value for Independence: {p_chi:.10f}")

# Determination of correlation
if p_chi < 0.05:
    print("Result: Statistically Significant. The variables are correlated.\n")
else:
    print("Result: Not Significant. The variables are independent.\n")
    

# --- 4. LINEAR REGRESSION ---
# Modeling Price (dependent) based on Area Income (independent)
slope, intercept, r_value, p_reg, std_err = stats.linregress(income, price)

print("--- Linear Regression Results (Price ~ Income) ---")
print(f"Slope: {slope:.4f}")
print(f"Intercept: {intercept:.4f}")
print(f"R-squared: {r_value**2:.4f}\n")

# --- 5. VISUALIZATIONS WITH PYGAL ---

# Regression Visualization: Scatter Plot + Trendline
reg_style = Style(colors=('#E8537A', '#1C3144'))
reg_chart = pygal.XY(
    stroke=False, 
    title='Linear Regression: Income vs Price', 
    x_title='Avg Area Income', 
    y_title='Price',
    style=reg_style
)

# Adding a sample of 200 points for performance/clarity in the SVG
scatter_data = [tuple(x) for x in df[['Avg. Area Income', 'Price']].values[:200]]
reg_chart.add('Actual Data (Sample)', scatter_data)

# Adding the Regression Line
x_min, x_max = income.min(), income.max()
reg_chart.add('Trendline', [
    (x_min, slope * x_min + intercept), 
    (x_max, slope * x_max + intercept)
], stroke=True, show_dots=False)

reg_chart.render_to_file('housing_regression.svg')

# Contingency Table Visualization: Dot Chart
dot_chart = pygal.Dot(title='Contingency Table Frequencies', x_title='Price Category', y_title='Income Category')
dot_chart.x_labels = ['High Price', 'Low Price']
dot_chart.add('High Income', [contingency_table.loc['High Income', 'High Price'], 
                               contingency_table.loc['High Income', 'Low Price']])
dot_chart.add('Low Income', [contingency_table.loc['Low Income', 'High Price'], 
                              contingency_table.loc['Low Income', 'Low Price']])

dot_chart.render_to_file('contingency_dot_chart.svg')

print("Charts saved as 'housing_regression.svg' and 'contingency_dot_chart.svg'.")
