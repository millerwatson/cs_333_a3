import pandas as pd

orig = pd.read_csv("oecd_hows_life_complete.csv", dtype=str)

print("Unique values in Measure column:")
print(orig["Measure"].unique()[:200])   # print first 200 uniques
print("\nCount:", len(orig["Measure"].unique()))
