# ============================================================
# GOAL: Combine the Zillow and HUD datasets into one file
# INPUT:  twincities_clean.csv + minneapolis_fmr_2026_clean.csv
# OUTPUT: twincities_combined.csv
# ============================================================

import pandas as pd

# ── STEP 1: LOAD BOTH FILES ───────────────────────────────────

# Load the Zillow data (4,828 rows — one per zip per month)
zillow = pd.read_csv("/Users/crystalphan/Desktop/Apartent rental project/twincities_clean.csv")

print("Zillow loaded!")
print(f"  Rows: {len(zillow):,}")

# Load the HUD data (244 rows — one per zip code)
hud = pd.read_csv("/Users/crystalphan/Desktop/Apartent rental project/minneapolis_fmr_2026_clean.csv")

print("\nHUD loaded!")
print(f"  Rows: {len(hud)}")

# ── STEP 2: MAKE ZIP CODES THE SAME FORMAT IN BOTH FILES ─────

# Before joining, both files need zip codes in the same format
# If one has 55401 as a number and the other has "55401" as text
# Python will not recognize them as a match

# Convert both to text with exactly 5 digits
zillow["regionname"] = zillow["regionname"].astype(str).str.zfill(5)
hud["zip"]           = hud["zip"].astype(str).str.zfill(5)

# Check how many zip codes exist in both files
zillow_zips = set(zillow["regionname"].unique())
hud_zips    = set(hud["zip"].unique())
both        = zillow_zips & hud_zips  # & means "in both"

print(f"\nZip codes in Zillow:    {len(zillow_zips)}")
print(f"Zip codes in HUD:       {len(hud_zips)}")
print(f"Zip codes in BOTH:      {len(both)}")
# We want this to say 80 — meaning all Zillow zips found a match

# ── STEP 3: REMOVE UNNECESSARY COLUMN FROM HUD ───────────────

# The "hud_area" column just says the same thing for every row
# (Minneapolis-St. Paul-Bloomington...) — not useful
# Remove it to keep things clean

hud = hud.drop(columns=["hud_area"])

print(f"\nHUD columns kept: {list(hud.columns)}")

# ── STEP 4: JOIN THE TWO TABLES ───────────────────────────────

# A "join" combines two tables by matching on a shared column
# This is exactly like VLOOKUP in Excel
#
# Here we match on zip code:
#   Zillow calls it: "regionname"
#   HUD calls it:    "zip"
#
# how="left" means:
#   Keep all rows from Zillow
#   Add HUD columns where zip codes match

print("\nJoining Zillow + HUD on zip code...")

combined = zillow.merge(
    hud,
    left_on  = "regionname",  # zip column name in Zillow
    right_on = "zip",         # zip column name in HUD
    how      = "left"         # keep all Zillow rows
)

# After merging we have two zip columns (regionname AND zip)
# They have the same values so remove the duplicate
combined = combined.drop(columns=["zip"])

print(f"  Rows after join: {len(combined):,}")
print(f"  Should still be 4,828 — no rows lost!")

# ── STEP 5: CHECK FOR MISSING VALUES ─────────────────────────

# If any zip code had no match in HUD, those rent columns
# will be empty (NaN). Let's check.

print("\nChecking for missing values in rent columns:")
rent_cols = ["rent_studio", "rent_1br", "rent_2br", "rent_3br", "rent_4br"]
for col in rent_cols:
    missing = combined[col].isnull().sum()
    print(f"  {col}: {missing} missing")
# We want 0 missing for all columns

# ── STEP 6: REORDER COLUMNS ───────────────────────────────────

# Arrange columns in a logical order:
# location info → time info → Zillow rent → HUD bedroom rents

combined = combined[[
    "regionname",  # zip code
    "city",        # city name
    "countyname",  # county name
    "state",       # state
    "date",        # date of observation
    "year",        # year number
    "month",       # month number
    "rent_index",  # Zillow overall rent
    "rent_studio", # HUD studio rent
    "rent_1br",    # HUD 1 bedroom rent
    "rent_2br",    # HUD 2 bedroom rent
    "rent_3br",    # HUD 3 bedroom rent
    "rent_4br",    # HUD 4 bedroom rent
]]

# ── STEP 7: PREVIEW THE RESULT ───────────────────────────────

print("\nFirst 3 rows of combined data:")
print(combined.head(3).to_string(index=False))

# ── STEP 8: SAVE ─────────────────────────────────────────────

combined.to_csv("/Users/crystalphan/Desktop/Apartent rental project/twincities_combined.csv", index=False)

print("\n" + "=" * 40)
print("  DONE!")
print("=" * 40)
print(f"  Saved: twincities_combined.csv")
print(f"  Total rows:  {len(combined):,}")
print(f"  Zip codes:   {combined['regionname'].nunique()}")
print(f"  Date range:  {combined['date'].min()} → {combined['date'].max()}")
print()
print("  Next step: load into SQLite database")