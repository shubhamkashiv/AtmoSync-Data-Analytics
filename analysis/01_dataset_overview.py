
import pandas as pd
from pathlib import Path

# Load weather dataset
file_path = Path(__file__).parent.parent / "dataset" / "weather_data_asia_2024-03-25_2024-04-16.csv"

df = pd.read_csv(file_path)

# Display dataset overview
print("ATMoSync - Weather Dataset Analysis")
print("-----------------------------------")

print("\n1. Dataset Shape:")
print(df.shape)

print("\n2. Column Names:")
print(df.columns.tolist())

print("\n3. Dataset Information:")
df.info()

print("\n4. Missing Values:")
print(df.isnull().sum())

print("\n5. Descriptive Statistics:")
print(df.describe(include="all"))

print("\n6. First 5 Records:")
print(df.head())


# 7. Check placeholder values
print("\n7. Placeholder Values:")
for column in df.columns:
    count = (df[column].astype(str).str.strip() == "—").sum()
    if count > 0:
        print(f"{column}: {count} placeholder values")

# 8. Date Range
df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")

print("\n8. Date Range:")
print("Start Date:", df["DATE"].min())
print("End Date:", df["DATE"].max())

# 9. Unique Cities and Countries
print("\n9. Unique Cities:", df["City"].nunique())
print("Unique Countries:", df["Country"].nunique())
