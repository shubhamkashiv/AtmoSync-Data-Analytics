import pandas as pd

file_path = "datasets/raw/weather_data_asia_2024-03-25_2024-04-16.csv"

df = pd.read_csv(file_path)

# Convert date column
df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")

# Remove columns with 100% missing values
df = df.drop(columns=["SNOW", "WPGT", "TSUN"])
# Remove units and convert columns to numeric values

unit_columns = {
    "TMIN": "°C",
    "TAVG": "°C",
    "TMAX": "°C",
    "PRCP": "mm",
    "WSPD": "km/h",
    "PRES": "hPa"
}

for column, unit in unit_columns.items():
    df[column] = (
        df[column]
        .str.replace(unit, "", regex=False)
        .str.strip()
    )

    df[column] = pd.to_numeric(df[column], errors="coerce")

print("\nNumeric Conversion Completed!")
print(df[["TMIN", "TAVG", "TMAX", "PRCP", "WSPD", "PRES"]].dtypes)

print("Cleaning started successfully!")
print(df.head())
print("\nRemaining columns:")
print(df.columns.tolist())

# Check missing values after conversion
print("\nMissing Values After Conversion:")
print(df.isnull().sum())

# Save cleaned dataset
output_path = "datasets/processed/cleaned_weather_data.csv"

df.to_csv(output_path, index=False)

print("\nCleaned dataset saved successfully!")
print("Final Shape:", df.shape)