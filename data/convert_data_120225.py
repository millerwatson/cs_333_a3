import pandas as pd
import re

INPUT_FILE = "oecd_hows_life_complete.csv"
OUTPUT_FILE = "oecd_hows_life_wide_2010_2024.csv"

# ------------------------------------------------------
# Helper: make D3-friendly IDs
# ------------------------------------------------------
def make_d3_id(name):
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s)
    s = s.strip("_")
    if re.match(r"^[0-9]", s):
        s = "v_" + s
    return s


# ------------------------------------------------------
# Load data (strings to avoid dtype issues)
# ------------------------------------------------------
df = pd.read_csv(INPUT_FILE, dtype=str)

# Normalize column names
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
)

# Drop duplicate columns (your file has many)
df = df.loc[:, ~df.columns.duplicated()]

# Required columns
required_cols = ["measure", "reference_area", "time_period", "obs_value"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

# Clean values
for col in required_cols:
    df[col] = df[col].astype(str).str.strip()

# Convert year to int
df["year"] = df["time_period"].astype(int)
df["country"] = df["reference_area"]

# ------------------------------------------------------
# Restrict to years 2010–2024
# ------------------------------------------------------
TARGET_YEARS = list(range(2010, 2025))
year_set = set(TARGET_YEARS)

df = df[df["year"].isin(TARGET_YEARS)]

# ------------------------------------------------------
# Identify variables with complete coverage for ALL years 2010–2024
# ------------------------------------------------------
years_by_measure = (
    df.groupby("measure")["year"]
      .apply(lambda s: set(s.dropna().unique()))
)

complete_vars = [
    m for m, yrs in years_by_measure.items()
    if yrs == year_set
]

print("Variables with complete coverage (2010–2024):")
for v in complete_vars:
    print(" •", v)

# Filter
df = df[df["measure"].isin(complete_vars)].copy()

# Create D3-friendly names
df["variable_id"] = df["measure"].apply(make_d3_id)
# ------------------------------------------------------
# Pivot wide (fixing duplicate rows by taking first)
# ------------------------------------------------------
wide = df.pivot_table(
    index=["country", "year"],
    columns="variable_id",
    values="obs_value",
    aggfunc="first"      # Prevents Pandas from trying mean on strings
).reset_index()

# Clean column names
wide.columns = [c if isinstance(c, str) else c[1] for c in wide.columns]

# Sort nicely
wide = wide.sort_values(["country", "year"])

# Save output
wide.to_csv(OUTPUT_FILE, index=False)

# ------------------------------------------------------
# Save output
# ------------------------------------------------------
wide.to_csv(OUTPUT_FILE, index=False)

print("\nSaved:", OUTPUT_FILE)
print("Number of variables retained:", len(complete_vars))
