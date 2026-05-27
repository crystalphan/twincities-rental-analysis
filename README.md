# Twin Cities Rental Price Analysis

Analysis of rental price trends across the Minneapolis-St. Paul metro area using Zillow ZORI data (2015–2026) and HUD Fair Market Rents (FY2026).

## 📊 Live Dashboard
[View on Tableau Public](https://public.tableau.com/views/Rentdashboard_17799219557430/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## 🔍 Key Findings
- Average rent in the Twin Cities grew **77%** from $954 (2015) to $1,689 (2026)
- Most expensive zip code in 2025: **55410 Minneapolis** at $2,499/month
- Most affordable zip code in 2025: **55130 Saint Paul** at $1,169/month
- Regression model explains **69.5%** of rent variation (R² = 0.695)
- Hennepin County has the highest rents; Pierce County the most affordable

## 🛠️ Tools Used
| Tool | Purpose |
|---|---|
| Python | Data cleaning and joining datasets |
| SQL / SQLite | Data storage and querying |
| R / RStudio | EDA, visualization, regression model |
| Tableau Public | Interactive dashboard |

## 📁 Project Structure
```
twincities-rental-analysis/
│
├── clean_twincities.py        # Clean Zillow ZORI zip-level data
├── clean_hud_beginner.py      # Clean HUD Fair Market Rents
├── join_datasets.py           # Join Zillow + HUD by zip code
├── load_sqlite.py             # Load data into SQLite database
├── export_tableau.py          # Export data for Tableau
├── twincities_rental_analysis.Rmd   # R Markdown analysis
└── twincities_rental_analysis.html  # Final HTML report
```

## 📂 Data Sources
- [Zillow Research — ZORI (Smoothed)](https://www.zillow.com/research/data/)
- [HUD Fair Market Rents FY2026](https://www.huduser.gov/portal/datasets/fmr.html)

## 📈 Analysis Steps
1. Downloaded and cleaned Zillow zip-level rent data (80 Twin Cities zip codes)
2. Downloaded and cleaned HUD Fair Market Rents by bedroom size
3. Joined both datasets by zip code using pandas
4. Loaded into SQLite database for SQL querying
5. Performed EDA and built multiple linear regression in R
6. Built interactive Tableau dashboard

## 👩‍💻 Author
Crystal Phan — Data Analytics student at University of St. Thomas
