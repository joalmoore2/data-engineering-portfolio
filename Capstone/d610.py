import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv(r"C:\Users\joann\Documents\WGU\D610\911_Calls_For_Service_2024.csv")

# Display basic info and a sample
print(df.info())
print(df.head())

# Convert callDateTime to datetime format
df['callDateTime'] = pd.to_datetime(df['callDateTime'], errors='coerce')

# Drop rows with invalid or missing callDateTime
df = df.dropna(subset=['callDateTime'])

# Extract the hour from the datetime
df['callHour'] = df['callDateTime'].dt.hour

# Normalize neighborhood names to avoid casing issues
df['Neighborhood'] = df['Neighborhood'].str.strip().str.title()

# Filter for just Canton and Druid Heights
df_filtered = df[df['Neighborhood'].isin(['Canton', 'Druid Heights'])]

# Check how many records we have for each neighborhood
print(df_filtered['Neighborhood'].value_counts())

# Optional: Save the cleaned and filtered dataset
df_filtered.to_csv('filtered_911_calls_canton_druid.csv', index=False)

plt.figure(figsize=(12, 6))
sns.histplot(data=df_filtered, x='callHour', hue='Neighborhood', multiple='dodge', bins=24, kde=False)
plt.title('911 Call Volume by Hour: Canton vs Druid Heights')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Calls')
plt.xticks(range(0, 24))
plt.grid(True)
plt.show()

# Group by Neighborhood and calculate descriptive stats
grouped_stats = df_filtered.groupby('Neighborhood')['callHour'].agg(['mean', 'median', pd.Series.mode])

# Reset index for cleaner display
grouped_stats = grouped_stats.reset_index()
grouped_stats.columns = ['Neighborhood', 'Mean Call Hour', 'Median Call Hour', 'Mode Call Hour']

print(grouped_stats)

plt.figure(figsize=(10, 6))
sns.boxplot(data=df_filtered, x='Neighborhood', y='callHour', hue='Neighborhood', palette='Set2', legend=False)
plt.title('Distribution of 911 Call Times by Neighborhood')
plt.ylabel('Hour of Day (0–23)')
plt.xlabel('Neighborhood')
plt.grid(True)
plt.show()

df_filtered = df_filtered.copy()
df_filtered['TimeBin'] = df_filtered['callHour'].apply(categorize_time)

# Add binned times
def categorize_time(hour):
    if 0 <= hour < 6:
        return 'Night'
    elif 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 18:
        return 'Afternoon'
    else:
        return 'Evening'

# Apply the categorization to the 'callHour' column
df_filtered.loc[:, 'TimeBin'] = df_filtered['callHour'].apply(categorize_time)

# Create contingency table
contingency_table = pd.crosstab(df_filtered['Neighborhood'], df_filtered['TimeBin'])
print(contingency_table)

from scipy.stats import chi2_contingency

# Perform the chi-squared test
chi2, p, dof, expected = chi2_contingency(contingency_table)

# Output results
print(f"Chi-squared: {chi2:.2f}, p-value: {p:.4f}")
