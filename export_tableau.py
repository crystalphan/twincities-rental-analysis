# export_tableau.py
# Exports data from SQLite into a CSV for Tableau

import pandas as pd
import sqlite3

# Connect to the database
conn = sqlite3.connect("/Users/crystalphan/Desktop/Apartent rental project/twincities_rental.db")

# Export annual summary table
df = pd.read_sql("SELECT * FROM annual_summary", conn)

# Save to CSV
df.to_csv("/Users/crystalphan/Desktop/Apartent rental project/tableau_data.csv", index=False)

print(f"Done! Exported {len(df):,} rows to tableau_data.csv")
print(f"Columns: {list(df.columns)}")

conn.close()