import pandas as pd

file_path = "datasets/raw/weather_data_asia_2024-03-25_2024-04-16.csv"

df = pd.read_csv(file_path)

print("First 5 Rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nDataset Information:")
df.info()


print("\nMissing Values:")
print(df.isin(["—", "-", ""]).sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())