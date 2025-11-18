import pandas as pd

def clean_oecd_large_csv(path, out="oecd_clean.csv"):
    """
    Cleans large OECD SDMX CSVs while preserving all substantive columns.
    Handles multiple countries, many measures, and large file sizes.
    """

    # 1. Load (low_memory=False handles mixed data types)
    df = pd.read_csv(path, low_memory=False)

    # 2. Normalize column names (easier to work with programmatically)
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # 3. Identify the actual observation/value column
    # OECD SDMX files vary in naming conventions
    value_candidates = [
        "obs_value",
        "observation_value",
        "observationvalue",
        "value"
    ]

    value_col = None
    for col in value_candidates:
        if col in df.columns:
            value_col = col
            break

    if value_col is None:
        raise ValueError("Could not find the observation value column.")

    # 4. Create a consistent "value" column
    df["value"] = df[value_col]

    # 5. Drop only useless columns — keep all substantive metadata
    # SDMX metadata columns that are safe to drop
    drop_cols = [
        "structure",               # structural metadata
        "structure_id",
        "structure_name",
        "action",                  # SDMX action flags
        "unit_mult",               # often repeats "unit_multiplier"
        "unit_multiplier",
        "decimals",
        "base_per",
        "base_period"
    ]

    keep_cols = [c for c in df.columns if c not in drop_cols]

    clean = df[keep_cols]

    # 6. Output to CSV
    clean.to_csv(out, index=False)

    print(f"Saved cleaned dataset to: {out}")
    print("Resulting columns:", list(clean.columns))

    return clean

def main():
    clean_df = clean_oecd_large_csv(
    "input_well-being_data.csv",
    out="OECD_clean_large.csv"
)

main()