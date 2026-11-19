from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw/pvdaq/2023-solar-data-prize/system-2107")

for path in sorted(DATA_DIR.glob("*.csv")):
    print("\n" + "=" * 85)
    print(f"FILE: {path.name}")

    df = pd.read_csv(path, parse_dates=["measured_on"], low_memory=False)

    timestamps = df["measured_on"].dropna().sort_values()
    intervals = timestamps.diff().dropna()

    print(f"Shape:              {df.shape}")
    print(f"Rows:               {len(df):,}")
    print(f"Columns:            {len(df.columns)}")
    print(f"First timestamp:    {timestamps.min()}")
    print(f"Last timestamp:     {timestamps.max()}")
    print(f"Duplicate times:    {df['measured_on'].duplicated().sum():,}")
    print(f"Missing timestamps: {df['measured_on'].isna().sum():,}")

    print("\nMost common sampling intervals:")
    print(intervals.value_counts().head(8).to_string())

    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    print("\nColumns with missing values:")
    print(
        (missing / len(df) * 100).round(2).astype(str).add("%").to_string()
        if not missing.empty else "None"
    )

    print("\nNumeric summary:")
    print(df.select_dtypes(include="number").describe().round(2).to_string())

    print("\nColumn names:")
    for column in df.columns:
        print(f"  {column}")
