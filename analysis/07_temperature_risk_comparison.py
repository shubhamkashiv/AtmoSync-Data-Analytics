


import duckdb

file_path = r"C:\Users\shrad\OneDrive\ドキュメント\Github\AtmoSync-Data-Analytics\dataset\w60_all.parquet"

risk_temperature = duckdb.query(f"""
    SELECT
        risk_level,
        COUNT(*) AS record_count,
        ROUND(AVG(W60_T_mean), 2) AS avg_temperature,
        ROUND(MIN(W60_T_mean), 2) AS min_temperature,
        ROUND(MAX(W60_T_mean), 2) AS max_temperature
    FROM read_parquet('{file_path}')
    WHERE risk_level IS NOT NULL
      AND W60_T_mean IS NOT NULL
    GROUP BY risk_level
    ORDER BY risk_level
""").df()

print("\nTEMPERATURE VS RISK LEVEL ANALYSIS")
print("-" * 55)
print(risk_temperature.to_string(index=False))


import matplotlib.pyplot as plt

plt.figure(figsize=(9, 5))

plt.bar(
    risk_temperature["risk_level"].astype(str),
    risk_temperature["avg_temperature"]
)

plt.title("Average Temperature by Risk Level")
plt.xlabel("Risk Level")
plt.ylabel("Average Temperature (°C)")

plt.tight_layout()
plt.savefig("AtmoSync-Data-Analytics/analysis/temperature_risk_comparison.png")
plt.show()
