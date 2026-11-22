import pandas as pd
from pathlib import Path

# Load original dataset
base_path = Path(__file__).parent.parent
file_path = base_path / "dataset" / "weather_data_asia_2024-03-25_2024-04-16.csv"

df = pd.read_csv(file_path)

print("ATmoSync - Data Cleaning")
print("------------------------")

# Replace unavailable placeholders with missing values
df = df.replace("—", pd.NA)

# Remove extra spaces from text columns
for column in df.select_dtypes(include="object").columns:
    df[column] = df[column].str.strip()

# Convert date column
df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")

# Convert weather measurement columns into numeric format
weather_columns = ["TMIN", "TAVG", "TMAX", "PRCP", "SNOW", "WSPD", "WPGT", "PRES", "TSUN"]

for column in weather_columns:
    df[column] = (
        df[column]
        .astype("string")
        .str.extract(r"([-+]?\d*\.?\d+)")[0]
    )
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Check cleaned data
print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nUpdated data types:")
print(df.dtypes)

# Save cleaned dataset separately
output_path = base_path / "dataset" / "weather_data_cleaned.csv"
df.to_csv(output_path, index=False)

print("\nCleaned dataset saved successfully!")
print("Output:", output_path)