## AtmoSync – Initial EDA Findings

## 1. Dataset Overview

- Total Records: 483
- Total Columns: 15
- Unique Cities: 21
- Unique Countries: 8
- Date Range: 25 March 2024 to 16 April 2024

## 2. Data Quality Findings

- No null values were detected initially using Pandas `isnull()`.
- SNOW contains 483 placeholder values.
- WPGT contains 483 placeholder values.
- TSUN contains 483 placeholder values.
- Weather-related columns were initially stored as strings.

## 3. Initial Observations

- The dataset contains weather records from 21 Asian cities.
- The dataset covers 23 calendar days.
- Three columns contain only unavailable-value placeholders.
- Further data cleaning and type conversion were required and have now been completed.

## 4. Data Cleaning and Preprocessing

- Replaced unavailable placeholder values (—) with missing values.
- Removed measurement units from weather columns.
- Converted weather measurements into numeric data types.
- Converted the DATE column into datetime format.
- Preserved missing values in SNOW, WPGT and TSUN.
- Saved the cleaned dataset as `weather_data_cleaned.csv`.

## 5. Statistical Summary

- Total records processed: 483
- Average temperature (TAVG): 23.12°C
- Average precipitation (PRCP): 3.76 mm
- Average wind speed (WSPD): 10.70 km/h
- Maximum recorded precipitation: 97 mm
- Maximum recorded wind speed: 44 km/h

## 6. City-wise Temperature Analysis

- Average temperature was calculated for all 21 cities.
- Bangkok recorded the highest average temperature of 31.86°C.
- Busan recorded the lowest average temperature of 12.98°C.
- The temperature difference between the highest and lowest cities was 18.88°C.
- A bar chart was generated to compare average temperatures across cities.

### Key Observation

The analysis shows noticeable temperature variations across the selected Asian cities. Bangkok had the highest average temperature, while Busan had the lowest.

### Visualization

The city-wise average temperature chart is saved as:

`analysis/city_wise_temperature.png`