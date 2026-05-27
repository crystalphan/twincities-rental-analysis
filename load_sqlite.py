# ============================================================
# GOAL: Load our combined dataset into a SQLite database
# INPUT:  twincities_combined.csv
# OUTPUT: twincities_rental.db
# ============================================================

# pandas helps us work with data tables
import pandas as pd

# sqlite3 is built into Python — no installation needed!
import sqlite3

# os helps us check if files exist
import os

# ── STEP 1: LOAD THE COMBINED CSV ────────────────────────────

# Read the combined file we created in the last step
df = pd.read_csv("/Users/crystalphan/Desktop/Apartent rental project/twincities_combined.csv")

print("Combined file loaded!")
print(f"  Rows:    {len(df):,}")
print(f"  Columns: {list(df.columns)}")

# ── STEP 2: CONNECT TO SQLITE ────────────────────────────────

# This creates a new database file called twincities_rental.db
# If the file already exists, it just opens it
# Think of this like creating a new Excel workbook

db_path = "/Users/crystalphan/Desktop/Apartent rental project/twincities_rental.db"
conn = sqlite3.connect(db_path)

print(f"\nDatabase created: twincities_rental.db")

# ── STEP 3: SAVE DATA INTO THE DATABASE ──────────────────────

# This saves our DataFrame as a table called "rentals" in the database
# if_exists="replace" means: if the table already exists, overwrite it
# index=False means: don't save the row numbers as a column

df.to_sql("rentals", conn, if_exists="replace", index=False)

print(f"  Table 'rentals' saved with {len(df):,} rows")

# ── STEP 4: CREATE A SUMMARY TABLE ───────────────────────────

# This creates a second table with annual averages per zip code
# It will be useful for Tableau and the regression in R
# We use SQL language to create it

summary_sql = """
CREATE TABLE IF NOT EXISTS annual_summary AS
SELECT
    regionname,                        -- zip code
    city,                              -- city name
    countyname,                        -- county name
    state,                             -- state
    year,                              -- year
    ROUND(AVG(rent_index), 2)  AS avg_rent,       -- average Zillow rent
    ROUND(MIN(rent_index), 2)  AS min_rent,       -- lowest rent that year
    ROUND(MAX(rent_index), 2)  AS max_rent,       -- highest rent that year
    COUNT(*)                   AS months_of_data, -- how many months recorded
    rent_studio,               -- HUD studio rent
    rent_1br,                  -- HUD 1 bedroom rent
    rent_2br,                  -- HUD 2 bedroom rent
    rent_3br,                  -- HUD 3 bedroom rent
    rent_4br                   -- HUD 4 bedroom rent
FROM rentals
GROUP BY regionname, year      -- one row per zip per year
ORDER BY regionname, year
"""

# Drop the table first if it already exists, then recreate it
conn.execute("DROP TABLE IF EXISTS annual_summary")
conn.execute(summary_sql)
conn.commit()

# Check how many rows the summary table has
row_count = conn.execute("SELECT COUNT(*) FROM annual_summary").fetchone()[0]
print(f"  Table 'annual_summary' saved with {row_count:,} rows")

# ── STEP 5: TEST WITH SOME SQL QUERIES ───────────────────────

# Let's run a few queries to confirm the data looks right
# This is us actually USING SQL to ask questions about our data

print("\n--- TEST QUERY 1: How many zip codes per county? ---")
query1 = """
SELECT countyname, COUNT(DISTINCT regionname) AS zip_count
FROM rentals
GROUP BY countyname
ORDER BY zip_count DESC
"""
result1 = pd.read_sql(query1, conn)
print(result1.to_string(index=False))

print("\n--- TEST QUERY 2: Top 5 most expensive zip codes (2025) ---")
query2 = """
SELECT regionname, city, ROUND(avg_rent, 0) AS avg_rent
FROM annual_summary
WHERE year = 2025
ORDER BY avg_rent DESC
LIMIT 5
"""
result2 = pd.read_sql(query2, conn)
print(result2.to_string(index=False))

print("\n--- TEST QUERY 3: Top 5 most affordable zip codes (2025) ---")
query3 = """
SELECT regionname, city, ROUND(avg_rent, 0) AS avg_rent
FROM annual_summary
WHERE year = 2025
ORDER BY avg_rent ASC
LIMIT 5
"""
result3 = pd.read_sql(query3, conn)
print(result3.to_string(index=False))

print("\n--- TEST QUERY 4: Average rent by year (all Twin Cities) ---")
query4 = """
SELECT year, ROUND(AVG(avg_rent), 0) AS metro_avg_rent
FROM annual_summary
GROUP BY year
ORDER BY year
"""
result4 = pd.read_sql(query4, conn)
print(result4.to_string(index=False))

# ── STEP 6: CLOSE THE CONNECTION ─────────────────────────────

# Always close the connection when you're done
# Like closing a file after you finish reading it
conn.close()

print("\n" + "=" * 40)
print("  DONE!")
print("=" * 40)
print(f"  Database saved: twincities_rental.db")
print(f"  Tables created:")
print(f"    rentals        — full monthly data (4,828 rows)")
print(f"    annual_summary — yearly averages per zip")
print()
print("  Next step: open R and connect to this database!")
print("  conn <- dbConnect(SQLite(), 'twincities_rental.db')")