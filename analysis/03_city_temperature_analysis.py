import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("dataset/weather_data_cleaned.csv")

# Calculate average temperature city-wise
city_temperature = (
    df.groupby("City")["TAVG"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Temperature by City:")
print(city_temperature.round(2))

# Highest and lowest average temperature
print("\nCity with Highest Average Temperature:")
print(city_temperature.idxmax(), "-", round(city_temperature.max(), 2), "°C")

print("\nCity with Lowest Average Temperature:")
print(city_temperature.idxmin(), "-", round(city_temperature.min(), 2), "°C")

# Create bar chart
city_temperature.plot(kind="bar", figsize=(12, 6))

plt.title("City-wise Average Temperature")
plt.xlabel("City")
plt.ylabel("Average Temperature (°C)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig("analysis/city_wise_temperature.png")
plt.show()