# ============================================================
# HUD Fair Market Rent Data Cleaning
# Goal: Filter the HUD dataset to Minneapolis zip codes only
# ============================================================

# pandas is a library that helps us work with data tables
# think of it like Excel, but in Python
import pandas as pd
import os

# Make sure we look for files in the same folder as this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# ============================================================
# STEP 1: LOAD THE FILE
# ============================================================

# Read the Excel file into a "DataFrame" (like a table)
# A DataFrame has rows and columns, just like a spreadsheet
df = pd.read_excel("fy2026_safmrs.xlsx")

# Let's see how big the table is (rows, columns)
print("Original data size:")
print(f"  Rows: {len(df)}")           # number of zip codes in the whole US
print(f"  Columns: {len(df.columns)}") # number of columns


# ============================================================
# STEP 2: FIX THE COLUMN NAMES
# ============================================================

# The column names in this file have hidden line breaks (\n)
# For example: "SAFMR\n0BR" instead of "SAFMR 0BR"
# We need to clean them so Python can read them properly

# .replace('\n', ' ') = swap line breaks with a space
# .strip()            = remove any extra spaces at start/end
df.columns = [col.replace("\n", " ").strip() for col in df.columns]

# Let's print the cleaned column names so we can see them
print("\nColumn names after cleaning:")
for col in df.columns:
    print(f"  {col}")


# ============================================================
# STEP 3: FILTER TO MINNEAPOLIS ONLY
# ============================================================

# The column "HUD Fair Market Rent Area Name" tells us which
# metro area each zip code belongs to.
# We only want Minneapolis-St. Paul zip codes.

# This is the exact name Minneapolis uses in the HUD dataset
minneapolis = "Minneapolis-St. Paul-Bloomington, MN-WI HUD Metro FMR Area"

# Keep only rows where the area name matches Minneapolis
# Think of this like filtering a column in Excel
df_mpls = df[df["HUD Fair Market Rent Area Name"] == minneapolis]

print(f"\nMinneapolis zip codes found: {len(df_mpls)}")


# ============================================================
# STEP 4: FIX ZIP CODE FORMAT
# ============================================================

# Zip codes are stored as numbers in this file
# For example: 55401 might be stored as 55401.0
# We need them as text (strings) with exactly 5 digits
# zfill(5) adds a leading zero if needed (e.g. 5401 -> 05401)

df_mpls = df_mpls.copy()  # make a fresh copy to avoid warnings
df_mpls["ZIP Code"] = df_mpls["ZIP Code"].astype(str).str.zfill(5)

print("\nSample zip codes after fixing:")
print(df_mpls["ZIP Code"].head(5).tolist())


# ============================================================
# STEP 5: KEEP ONLY THE COLUMNS WE NEED
# ============================================================

# The original file has 18 columns
# We only need 7 of them for our project:
#   - ZIP Code
#   - Studio rent (0BR = zero bedrooms = studio)
#   - 1 bedroom rent
#   - 2 bedroom rent
#   - 3 bedroom rent
#   - 4 bedroom rent
#   - Area name (good to keep for reference)

# We do NOT need the 90% and 110% payment standard columns
# Those are used for housing voucher programs, not our analysis

df_clean = df_mpls[[
    "ZIP Code",
    "HUD Fair Market Rent Area Name",
    "SAFMR 0BR",   # studio apartment
    "SAFMR 1BR",   # 1 bedroom apartment
    "SAFMR 2BR",   # 2 bedroom apartment
    "SAFMR 3BR",   # 3 bedroom apartment
    "SAFMR 4BR",   # 4 bedroom apartment
]]

print(f"\nColumns kept: {len(df_clean.columns)}")
print(f"Rows kept: {len(df_clean)}")


# ============================================================
# STEP 6: RENAME COLUMNS TO SIMPLER NAMES
# ============================================================

# The original column names are long and hard to type
# Let's rename them to something shorter and cleaner
# This makes it easier when we use this data in R later

df_clean = df_clean.rename(columns={
    "ZIP Code":                        "zip",
    "HUD Fair Market Rent Area Name":  "hud_area",
    "SAFMR 0BR":                       "rent_studio",
    "SAFMR 1BR":                       "rent_1br",
    "SAFMR 2BR":                       "rent_2br",
    "SAFMR 3BR":                       "rent_3br",
    "SAFMR 4BR":                       "rent_4br",
})

print("\nNew column names:")
for col in df_clean.columns:
    print(f"  {col}")


# ============================================================
# STEP 7: SORT BY ZIP CODE
# ============================================================

# Sort rows from smallest to largest zip code
# This makes the data easier to read and look up
df_clean = df_clean.sort_values("zip")

# Reset the row numbers (index) so they start from 0 again
# drop=True means don't keep the old row numbers as a column
df_clean = df_clean.reset_index(drop=True)


# ============================================================
# STEP 8: CHECK THE DATA LOOKS RIGHT
# ============================================================

print("\n--- PREVIEW OF CLEANED DATA ---")
print(df_clean.head(10))  # show first 10 rows

print("\n--- RENT STATISTICS ---")
# Show average rent for each bedroom size across all zips
rent_cols = ["rent_studio", "rent_1br", "rent_2br", "rent_3br", "rent_4br"]
for col in rent_cols:
    avg = df_clean[col].mean()
    mn  = df_clean[col].min()
    mx  = df_clean[col].max()
    print(f"  {col}: avg=${avg:,.0f}  min=${mn:,.0f}  max=${mx:,.0f}")


# ============================================================
# STEP 9: SAVE THE CLEANED DATA
# ============================================================

# Save as a CSV file (comma-separated values)
# index=False means don't save the row numbers as a column
output_file = "minneapolis_fmr_2026_clean.csv"
df_clean.to_csv(output_file, index=False)

print(f"\nDone! Saved {len(df_clean)} rows to '{output_file}'")
print("You can open this file in Excel or use it in R.")
