import pandas as pd

# Load shipment dataset
file_path = "dataset/w60_all.parquet"
df = pd.read_parquet(file_path)

print("=" * 50)
print("ATMOSYNC - SHIPMENT DATASET OVERVIEW")
print("=" * 50)

print("\n1. Dataset Shape:")
print(df.shape)

print("\n2. Column Names:")
print(df.columns.tolist())

print("\n3. Data Types:")
print(df.dtypes)

print("\n4. Missing Values:")
print(df.isnull().sum())

print("\n5. Duplicate Records:")
print(df.duplicated().sum())

print("\n6. First 5 Records:")
print(df.head())

print("\n7. Date Range:")
print("Start:", df["Time"].min())
print("End:", df["Time"].max())

print("\n8. Number of Shipments:")
print(df["shipment_id"].nunique())

print("\n9. Shipment-wise Records:")
print(df["shipment_id"].value_counts())

print("\n10. Risk Level Distribution:")
print(df["risk_level"].value_counts(dropna=False))

print("\n11. Sensor-wise Missing Values:")
sensor_cols = [
    "Front_Top", "Front_Middle", "Front_Bottom",
    "Middle_Top", "Middle_Middle", "Middle_Bottom",
    "Rear_Top", "Rear_Middle", "Rear_Bottom"
]
print(df[sensor_cols].isnull().sum())

print("\n12. Columns with Missing Values:")
missing = df.isnull().sum()
print(missing[missing > 0].sort_values(ascending=False))