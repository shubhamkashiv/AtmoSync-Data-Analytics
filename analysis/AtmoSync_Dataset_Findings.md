# AtmoSync – Shipment Dataset Findings

## 1. Dataset Overview
The AtmoSync shipment dataset contains 14,398 records and 107 columns. It includes timestamp information, nine temperature sensor positions, shipment identifiers, temperature-related features and risk prediction labels.

## 2. Shipment Information
- Total shipments: 6
- Shipment IDs: S1, S2, S3, S4, S5 and S6
- Start date: 12 March 2019
- End date: 26 July 2019

## 3. Data Quality Analysis
- Total duplicate records: 0
- Columns containing missing values: 73
- Sensor readings contain missing values.
- Middle_Bottom has the highest number of missing readings (10,145).

## 4. Risk Level Distribution
- Risk level 0: 2,419 records
- Risk level 1: 104 records
- Risk level 2: 10,680 records
- Missing risk level: 1,195 records

## 5. Key Observations
1. The dataset contains shipment-level temperature monitoring information.
2. Nine sensor positions provide temperature readings from different locations.
3. Missing sensor values require further investigation before data cleaning.
4. Risk prediction fields are available for future analysis.
5. The dataset can support shipment temperature analysis and spoilage-risk research.

## 6. Conclusion
The initial inspection confirms that the dataset contains useful shipment monitoring and risk-related information. Further analysis will focus on missing-value patterns, temperature trends and risk-level distribution.