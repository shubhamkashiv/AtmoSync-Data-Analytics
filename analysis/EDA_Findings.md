
# AtmoSync – Initial EDA Findings

## 1. Dataset Overview
- Total Records: 483
- Total Columns: 15
- Unique Cities: 21
- Unique Countries: 8
- Date Range: 25 March 2024 to 16 April 2024

## 2. Data Quality Findings
- No null values were detected using Pandas isnull().
- SNOW contains 483 placeholder values.
- WPGT contains 483 placeholder values.
- TSUN contains 483 placeholder values.
- Weather-related columns are stored as strings.

## 3. Initial Observations
- The dataset contains weather records from 21 Asian cities.
- The dataset covers 23 calendar days.
- Three columns contain only unavailable-value placeholders.
- Further data cleaning and type conversion are required before statistical analysis.

## 4. Next Steps
- Handle placeholder values.
- Convert weather measurements into numeric formats.
- Perform city-wise temperature analysis.
- Explore precipitation and wind patterns.
