import pandas as pd

df=pd.read_csv(r"C:\Users\joann\Documents\WGU\D602\task2\d602-deployment-task-2\T_ONTIME_REPORTING.csv")

# Show column names
print(df.columns)

# Show column datatypes
print(df.dtypes)

# See how many missing values are in each column
print(df.isnull().sum())

# Drop rows with missing values
df = df.dropna()

# Strip any leading or trailing spaces from column names to avoid errors
df.columns = df.columns.str.strip()

# Display cleaned column names
print(df.columns)

# Rename columns to match whats shown in poly_regressor file
df = df.rename(columns={
    'DAY_OF_MONTH': 'DAY',
    'ORIGIN': 'ORG_AIRPORT',
    'DEST': 'DEST_AIRPORT', 
    'CRS_DEP_TIME': 'SCHEDULED_DEPARTURE', 
    'DEP_TIME': 'DEPARTURE_TIME', 
    'DEP_DELAY': 'DEPARTURE_DELAY', 
    'CRS_ARR_TIME': 'SCHEDULED_ARRIVAL', 
    'ARR_TIME': 'ARRIVAL_TIME', 
    'ARR_DELAY': 'ARRIVAL_DELAY'
})

# Display cleaned column names
print(df.columns)

# Convert to integer
df[['DEPARTURE_TIME', 'DEPARTURE_DELAY', 'ARRIVAL_TIME', 'ARRIVAL_DELAY']] = df[['DEPARTURE_TIME', 'DEPARTURE_DELAY', 'ARRIVAL_TIME', 'ARRIVAL_DELAY']].astype('int64')

# check cleaned datatypes
print(df.dtypes)

# Save cleaned file
df.to_csv('cleaned_data.csv', index=False)
