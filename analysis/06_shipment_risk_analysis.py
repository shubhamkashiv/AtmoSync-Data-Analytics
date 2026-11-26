import duckdb

file_path = "dataset/w60_all.parquet"

risk_analysis = duckdb.query(f"""
    SELECT
        shipment_id,
        risk_level,
        COUNT(*) AS record_count
    FROM read_parquet('{file_path}')
    GROUP BY shipment_id, risk_level
    ORDER BY shipment_id, risk_level
""").df()

print("\nSHIPMENT-WISE RISK LEVEL ANALYSIS")
print("-" * 50)
print(risk_analysis)

missing_analysis = duckdb.query(f"""
    SELECT
        shipment_id,
        COUNT(*) AS total_records,
        COUNT(risk_level) AS available_risk_records,
        COUNT(*) - COUNT(risk_level) AS missing_risk_records
    FROM read_parquet('{file_path}')
    GROUP BY shipment_id
    ORDER BY shipment_id
""").df()

print("\nSHIPMENT-WISE MISSING RISK ANALYSIS")
print("-" * 50)
print(missing_analysis)

import matplotlib.pyplot as plt

risk_pivot = risk_analysis.pivot(
    index="shipment_id",
    columns="risk_level",
    values="record_count"
).fillna(0)

risk_pivot = risk_pivot.drop(columns=[float("nan")], errors="ignore")

risk_pivot.plot(kind="bar", figsize=(10, 6))

plt.title("Shipment-wise Risk Level Distribution")
plt.xlabel("Shipment ID")
plt.ylabel("Number of Records")
plt.xticks(rotation=0)
plt.legend(title="Risk Level")
plt.tight_layout()

plt.savefig("analysis/shipment_risk_distribution.png")
plt.show()