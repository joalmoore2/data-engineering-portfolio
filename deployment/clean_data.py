import pandas as pd

# Load cleaned dataset
df=pd.read_csv(r"C:\Users\joann\Documents\WGU\D602\task2\d602-deployment-task-2\cleaned_data.csv")

# Filter rows where 'ORG_AIRPORT' contains 'MIA' (Miami, Florida)
df = df[df['ORG_AIRPORT'].str.contains('MIA', na=False)]

print(df.head)

# CLean Data Again

# Remove duplicates
df = df.drop_duplicates()

# Add leading zeros to time columns to standardize column data to 4 digits
# List of columns to standardize
# Note: When opening in Excel default is to remove leading zeros. However zeros remain in .csv file
columns_to_standardize = ['SCHEDULED_DEPARTURE', 'DEPARTURE_TIME', 'SCHEDULED_ARRIVAL', 'ARRIVAL_TIME']

# Apply the zfill method to each column
for col in columns_to_standardize:
    # Convert to string, pad with leading zeros, then convert back to int
    df[col] = df[col].apply(lambda x: f'{int(x):04d}')

# Check result
print(df[columns_to_standardize].head())

# Save updates to cleaned file
df.to_csv('cleaned_data.csv', index=False)
