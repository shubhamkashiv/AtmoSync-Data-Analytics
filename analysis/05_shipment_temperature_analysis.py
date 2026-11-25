import duckdb

# Load and analyse shipment data
file_path = "dataset/w60_all.parquet"

shipment_analysis = duckdb.query(f"""
    SELECT
        shipment_id,
        COUNT(W60_T_mean) AS count,
        ROUND(AVG(W60_T_mean), 2) AS mean,
        ROUND(MIN(W60_T_mean), 2) AS min,
        ROUND(MAX(W60_T_mean), 2) AS max,
        ROUND(STDDEV_SAMP(W60_T_mean), 2) AS std
    FROM read_parquet('{file_path}')
    GROUP BY shipment_id
    ORDER BY shipment_id
""").df()

print("\nSHIPMENT-WISE TEMPERATURE ANALYSIS")
print("-" * 55)
print(shipment_analysis)

import matplotlib.pyplot as plt

plt.figure(figsize=(9, 5))

plt.bar(
    shipment_analysis["shipment_id"],
    shipment_analysis["mean"]
)

plt.title("Average Temperature by Shipment")
plt.xlabel("Shipment ID")
plt.ylabel("Average Temperature (°C)")

plt.tight_layout()
plt.savefig("analysis/shipment_temperature_comparison.png")

plt.show()