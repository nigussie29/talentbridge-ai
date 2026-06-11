import pandas as pd
from pathlib import Path

# Find the main project folder
project_folder = Path(__file__).resolve().parent.parent

# Build the full path to the CSV file
csv_file = project_folder / "data" / "career_profiles.csv"

print("Looking for file here:")
print(csv_file)

# Load the dataset
df = pd.read_csv(csv_file)

# Show the first 5 rows
print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns)

print("\nBasic information:")
print(df.info())

print("\nTarget role counts:")
print(df["target_role"].value_counts())