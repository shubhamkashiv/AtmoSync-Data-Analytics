"""
Validate the cleaned AtmoSync weather dataset without modifying it.

The script reports missing values and suspicious records, then writes all
identified suspicious rows to a separate CSV for review.
"""

import argparse
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "datasets" / "processed" / "cleaned_weather_data.csv"
DEFAULT_REPORT = PROJECT_ROOT / "reports" / "data_validation_report.txt"
DEFAULT_INVALID_OUTPUT = (
    PROJECT_ROOT / "datasets" / "processed" / "invalid_weather_records.csv"
)

REQUIRED_COLUMNS = [
    "City",
    "Country",
    "Elevation",
    "Timezone",
    "Coordinates",
    "DATE",
    "TMIN",
    "TAVG",
    "TMAX",
    "PRCP",
    "WSPD",
    "PRES",
]


def validate_weather_data(input_path: Path) -> tuple[pd.DataFrame, dict]:
    """Load and validate the cleaned weather dataset."""
    df = pd.read_csv(input_path)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    duplicate_mask = df.duplicated(keep=False)
    duplicate_count = int(df.duplicated().sum())

    reasons = pd.Series("", index=df.index, dtype="object")

    def add_reason(mask: pd.Series, reason: str) -> None:
        reasons.loc[mask] = reasons.loc[mask].apply(
            lambda existing: f"{existing}; {reason}" if existing else reason
        )

    add_reason(duplicate_mask, "Duplicate record")

    numeric_columns = ["TMIN", "TAVG", "TMAX", "PRCP", "WSPD"]
    invalid_numeric_counts = {column: 0 for column in numeric_columns}

    for column in numeric_columns:
        if column not in df.columns:
            continue

        original_non_empty = df[column].notna() & df[column].astype(str).str.strip().ne("")
        converted_values = pd.to_numeric(df[column], errors="coerce")
        invalid_numeric_mask = original_non_empty & converted_values.isna()

        invalid_numeric_counts[column] = int(invalid_numeric_mask.sum())
        add_reason(
            invalid_numeric_mask,
            f"Invalid numeric value in {column}",
        )
        df[column] = converted_values

    numeric_temperature_columns = ["TMIN", "TAVG", "TMAX"]
    temperature_mask = pd.Series(False, index=df.index)
    if all(column in df.columns for column in numeric_temperature_columns):
        temperature_mask = (
            df[numeric_temperature_columns].notna().all(axis=1)
            & (
                (df["TMIN"] > df["TAVG"])
                | (df["TAVG"] > df["TMAX"])
            )
        )
        add_reason(temperature_mask, "Invalid temperature logic (TMIN <= TAVG <= TMAX)")

    rainfall_mask = pd.Series(False, index=df.index)
    if "PRCP" in df.columns:
        rainfall_mask = df["PRCP"].notna() & (df["PRCP"] < 0)
        add_reason(rainfall_mask, "Negative rainfall")

    wind_mask = pd.Series(False, index=df.index)
    if "WSPD" in df.columns:
        wind_mask = df["WSPD"].notna() & (df["WSPD"] < 0)
        add_reason(wind_mask, "Negative wind speed")

    date_mask = pd.Series(False, index=df.index)
    if "DATE" in df.columns:
        parsed_dates = pd.to_datetime(df["DATE"], errors="coerce")
        date_mask = parsed_dates.isna()
        add_reason(date_mask, "Invalid or missing date")
        df["DATE"] = parsed_dates

    # Recalculate after numeric and date conversion so coerced values are counted
    # as missing values and invalid numeric values in the report.
    missing_values = df.isna().sum()
    missing_mask = pd.Series(False, index=df.index)
    for column in df.columns:
        column_missing_mask = df[column].isna()
        missing_mask |= column_missing_mask
        add_reason(column_missing_mask, f"Missing value in {column}")

    suspicious_mask = (
        missing_mask
        | duplicate_mask
        | temperature_mask
        | rainfall_mask
        | wind_mask
        | date_mask
    )

    invalid_df = df.loc[suspicious_mask].copy()
    invalid_df.insert(0, "VALIDATION_REASON", reasons.loc[suspicious_mask])

    results = {
        "total_records": len(df),
        "total_columns": len(df.columns),
        "missing_values": missing_values,
        "missing_columns": missing_columns,
        "invalid_numeric_counts": invalid_numeric_counts,
        "duplicate_count": duplicate_count,
        "invalid_temperature_count": int(temperature_mask.sum()),
        "invalid_rainfall_count": int(rainfall_mask.sum()),
        "invalid_wind_count": int(wind_mask.sum()),
        "invalid_date_count": int(date_mask.sum()),
        "suspicious_count": int(suspicious_mask.sum()),
        "invalid_df": invalid_df,
    }
    return df, results


def write_validation_report(report_path: Path, results: dict) -> None:
    """Write a clear human-readable validation report."""
    report_path.parent.mkdir(parents=True, exist_ok=True)

    has_missing_values = bool(results["missing_values"].gt(0).any())
    has_failures = (
        has_missing_values
        or bool(results["missing_columns"])
        or results["duplicate_count"] > 0
        or results["invalid_temperature_count"] > 0
        or results["invalid_rainfall_count"] > 0
        or results["invalid_wind_count"] > 0
        or results["invalid_date_count"] > 0
        or any(results["invalid_numeric_counts"].values())
    )
    overall_status = "FAIL" if has_failures else "PASS"

    lines = [
        "AtmoSync Weather Data Validation Report",
        "========================================",
        f"Total records: {results['total_records']}",
        f"Total columns: {results['total_columns']}",
        "",
        "Missing values per column:",
    ]

    if results["missing_values"].empty:
        lines.append("- None (dataset contains no columns)")
    else:
        for column, count in results["missing_values"].items():
            lines.append(f"- {column}: {int(count)}")

    lines.extend(
        [
            "",
            "Invalid numeric values per column:",
        ]
    )
    for column, count in results["invalid_numeric_counts"].items():
        lines.append(f"- {column}: {int(count)}")

    if results["missing_columns"]:
        lines.append("")
        lines.append("Missing required columns:")
        for column in results["missing_columns"]:
            lines.append(f"- {column}")

    lines.extend(
        [
            "",
            f"Duplicate count: {results['duplicate_count']}",
            f"Invalid temperature records: {results['invalid_temperature_count']}",
            f"Invalid rainfall records: {results['invalid_rainfall_count']}",
            f"Invalid wind speed records: {results['invalid_wind_count']}",
            f"Invalid date records: {results['invalid_date_count']}",
            f"Suspicious records identified: {results['suspicious_count']}",
            "",
            f"Overall validation status: {overall_status}",
        ]
    )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the cleaned AtmoSync weather data.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--invalid-output", type=Path, default=DEFAULT_INVALID_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input if args.input.is_absolute() else PROJECT_ROOT / args.input
    report_path = args.report if args.report.is_absolute() else PROJECT_ROOT / args.report
    invalid_output_path = (
        args.invalid_output
        if args.invalid_output.is_absolute()
        else PROJECT_ROOT / args.invalid_output
    )

    if not input_path.is_file():
        raise FileNotFoundError(f"Cleaned dataset not found: {input_path}")

    _, results = validate_weather_data(input_path)
    write_validation_report(report_path, results)

    invalid_df = results["invalid_df"]
    if not invalid_df.empty:
        invalid_output_path.parent.mkdir(parents=True, exist_ok=True)
        invalid_df.to_csv(invalid_output_path, index=False)
        print(
            f"Found {len(invalid_df)} suspicious record(s). "
            f"Saved them to: {invalid_output_path}"
        )
    else:
        if invalid_output_path.exists():
            invalid_output_path.unlink()
        print("No suspicious records found.")

    print(f"Validation report saved to: {report_path}")
    print(f"Overall validation status: "
          f"{'FAIL' if results['suspicious_count'] > 0 or results['missing_columns'] else 'PASS'}")


if __name__ == "__main__":
    main()
