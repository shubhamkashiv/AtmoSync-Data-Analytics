
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
- Further data cleaning and type conversion were required and have now been completed.

## 4. Data Cleaning and Preprocessing

- Replaced unavailable placeholder values (—) with missing values.
- Removed measurement units from weather columns.
- Converted weather measurements into numeric data types.
- Converted DATE column into datetime format.
- Preserved missing values in SNOW, WPGT and TSUN.
- Saved the cleaned dataset as weather_data_cleaned.csv.

## 5. Statistical Summary

- Total records processed: 483
- Average temperature (TAVG): 23.12°C
- Average precipitation (PRCP): 3.76 mm
- Average wind speed (WSPD): 10.70 km/h
- Maximum recorded precipitation: 97 mm
- Maximum recorded wind speed: 44 km/h

## 6. Next Steps

- Perform city-wise temperature analysis.
- Analyze precipitation patterns.
- Explore wind speed patterns.
- Create visualizations to identify weather trends.