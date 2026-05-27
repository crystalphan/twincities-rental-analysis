# ============================================================
# GOAL: Filter the Zillow dataset to Twin Cities zip codes only
# INPUT:  Zip_zori_uc_sfrcondomfr_sm_month.csv (downloaded from Zillow)
# OUTPUT: twincities_clean.csv
# ============================================================

# pandas helps us work with data tables (like Excel but in Python)
import pandas as pd

# ── STEP 1: LOAD THE FILE ────────────────────────────────────

# Read the Zillow CSV file into a table called "df"
# df is short for "DataFrame" — just means a table with rows and columns
df = pd.read_csv("/Users/crystalphan/Desktop/Apartent rental project/Zip_zori_uc_sfrcondomfr_sm_month.csv")

# Print how many rows and columns we loaded
print("Zillow file loaded!")
print(f"  Total zip codes in the US: {len(df):,}")
print(f"  Total columns: {len(df.columns)}")

# ── STEP 2: FILTER TO TWIN CITIES ONLY ───────────────────────

# The "Metro" column tells us which city each zip code belongs to
# We only want zip codes in the Minneapolis-St. Paul area
# This is the exact text used in the Metro column for Twin Cities
twin_cities = "Minneapolis-St. Paul-Bloomington, MN-WI"

# Keep only rows where Metro equals twin_cities
# This is like using a filter in Excel
df_tc = df[df["Metro"] == twin_cities].copy()

print(f"\nAfter filtering to Twin Cities:")
print(f"  Zip codes found: {len(df_tc)}")

# ── STEP 3: FIND THE DATE COLUMNS ────────────────────────────

# Zillow stores rent for each month as a separate column
# For example: "2015-01-31", "2015-02-28", "2015-03-31" ...
# These are called "date columns"

# The non-date columns are info about the zip code (city, state, etc.)
info_cols = ["RegionID", "SizeRank", "RegionName", "RegionType",
             "StateName", "State", "City", "Metro", "CountyName"]

# Find all date columns — they look like "2015-01-31" (10 characters, with dashes)
date_cols = [c for c in df.columns if len(c) == 10 and c[4] == "-" and c[7] == "-"]

print(f"\nDate columns found: {len(date_cols)}")
print(f"  First month: {date_cols[0]}")
print(f"  Last month:  {date_cols[-1]}")

# ── STEP 4: REMOVE ZIPS WITH NOT ENOUGH DATA ─────────────────

# Some zip codes only have a few months of rent data
# We need at least 24 months (2 years) for meaningful analysis
# Count how many months are MISSING for each zip code
missing_months   = df_tc[date_cols].isnull().sum(axis=1)

# Calculate how many months ARE available
months_available = len(date_cols) - missing_months

# Keep only zip codes with 24 or more months of data
before = len(df_tc)
df_tc  = df_tc[months_available >= 24].copy()

print(f"\nRemoving zips with less than 24 months of data:")
print(f"  Kept:    {len(df_tc)} zips")
print(f"  Removed: {before - len(df_tc)} zips")

# ── STEP 5: RESHAPE FROM WIDE TO LONG FORMAT ─────────────────

# Right now the table is "wide":
#   zip | city | 2015-01-31 | 2015-02-28 | 2015-03-31 | ...
#
# We need it to be "long" (one row per zip per month):
#   zip | city | date       | rent
#   55401 | Minneapolis | 2015-01-31 | 1200
#   55401 | Minneapolis | 2015-02-28 | 1210
#   ...
#
# This is called "melting" the table
# It makes it much easier to work with in R and SQL

print("\nReshaping table from wide to long format...")

df_long = df_tc.melt(
    id_vars    = info_cols,    # columns to keep as-is
    value_vars = date_cols,    # columns to turn into rows
    var_name   = "date",       # name for the new date column
    value_name = "rent_index"  # name for the new rent column
)

print(f"  Rows after reshape: {len(df_long):,}")

# ── STEP 6: CLEAN UP THE COLUMNS ─────────────────────────────

# Convert the date column from text to a real date
df_long["date"] = pd.to_datetime(df_long["date"])

# Add separate year and month columns (useful for grouping later)
df_long["year"]  = df_long["date"].dt.year
df_long["month"] = df_long["date"].dt.month

# Make sure rent is stored as a number, not text
df_long["rent_index"] = pd.to_numeric(df_long["rent_index"], errors="coerce")

# Make zip codes exactly 5 digits (add leading zero if needed)
# Example: 5401 becomes 05401
df_long["RegionName"] = df_long["RegionName"].astype(str).str.zfill(5)

# Make all column names lowercase with underscores (easier to type)
# Example: "RegionName" becomes "regionname"
df_long.columns = df_long.columns.str.lower().str.replace(" ", "_")

# ── STEP 7: REMOVE ROWS WITH NO RENT VALUE ───────────────────

# Some rows have no rent data at all — remove those
before  = len(df_long)
df_long = df_long.dropna(subset=["rent_index"])

print(f"\nRemoving rows with no rent data:")
print(f"  Removed: {before - len(df_long):,} rows")
print(f"  Kept:    {len(df_long):,} rows")

# ── STEP 8: KEEP ONLY THE COLUMNS WE NEED ────────────────────

# We only need these 9 columns for our project
df_long = df_long[[
    "regionname",   # zip code
    "city",         # city name
    "countyname",   # county name
    "metro",        # metro area name
    "state",        # state (MN or WI)
    "date",         # date of rent observation
    "year",         # year number
    "month",        # month number
    "rent_index",   # rent value from Zillow
]]

# Sort by zip code and date so it's easy to read
df_long = df_long.sort_values(["regionname", "date"]).reset_index(drop=True)

# ── STEP 9: SAVE THE CLEANED FILE ────────────────────────────

df_long.to_csv("/Users/crystalphan/Desktop/Apartent rental project/twincities_clean.csv", index=False)

print("\n" + "=" * 40)
print("  DONE!")
print("=" * 40)
print(f"  Saved: twincities_clean.csv")
print(f"  Zip codes:  {df_long['regionname'].nunique()}")
print(f"  Cities:     {df_long['city'].nunique()}")
print(f"  Date range: {df_long['date'].min().date()} → {df_long['date'].max().date()}")
print(f"  Total rows: {len(df_long):,}")