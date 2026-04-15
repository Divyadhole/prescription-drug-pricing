"""
src/drug_data.py
Prescription drug pricing data.

Sources:
  CMS Medicare Part D Drug Spending Dashboard:
    https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug
  OECD Health Statistics — pharmaceutical spending
  ASPE: "Comparison of U.S. and International Prices for Top Medicare Part B Drugs"
  FDA Orange Book — generic approvals
"""

import pandas as pd
import sqlite3
from pathlib import Path

Path("data/processed").mkdir(parents=True, exist_ok=True)


# ── Top Medicare Part D Drugs by Spending 2022 ────────────────────────────
# Source: CMS Medicare Part D Drug Spending Dashboard
# https://data.cms.gov/summary-statistics-on-use-and-payments
MEDICARE_PART_D_TOP = [
    # drug_name, manufacturer, drug_class, total_spending_2022_M, total_spending_2021_M,
    # avg_cost_per_claim_2022, total_claims_M, beneficiaries_M, generic_available
    ("Eliquis",       "Bristol-Myers Squibb", "Anticoagulant",      17024, 16154, 566, 30.1,  9.4,  False),
    ("Jardiance",     "Boehringer Ingelheim", "Diabetes/CV",         8142,  6418, 591, 13.8,  4.2,  False),
    ("Ozempic",       "Novo Nordisk",         "GLP-1/Diabetes",      7983,  4231, 892,  8.9,  2.8,  False),
    ("Xarelto",       "Janssen",              "Anticoagulant",       6908,  7312, 497, 13.9,  4.6,  False),
    ("Trulicity",     "Eli Lilly",            "GLP-1/Diabetes",      6321,  5841, 764,  8.3,  2.7,  False),
    ("Symbicort",     "AstraZeneca",          "Respiratory",         5124,  5412, 344, 14.9,  5.8,  False),
    ("Revlimid",      "Bristol-Myers Squibb", "Cancer",              5019,  5881,20441,  0.25, 0.09, False),
    ("Stelara",       "Janssen",              "Immunology",          4987,  4212,36298,  0.14, 0.08, False),
    ("Humira",        "AbbVie",               "Immunology",          4832,  5614,28741,  0.17, 0.09, False),
    ("Entresto",      "Novartis",             "Heart Failure",       4218,  3384, 614,  6.9,  2.3,  False),
    ("Dupixent",      "Regeneron/Sanofi",     "Immunology",          4104,  2841,33812,  0.12, 0.07, False),
    ("Farxiga",       "AstraZeneca",          "Diabetes/CV",         3921,  2814, 512,  7.7,  2.4,  False),
    ("Rybelsus",      "Novo Nordisk",         "GLP-1/Diabetes",      3418,  1984, 712,  4.8,  1.7,  False),
    ("Invokana",      "Janssen",              "Diabetes",            1842,  2118, 448,  4.1,  1.4,  False),
    ("Lantus",        "Sanofi",               "Insulin",             4122,  4521, 284, 14.5,  5.1,  True),
    ("Atorvastatin",  "Generic",              "Statin",              1841,  1921,  12,153.4, 48.2,  True),
    ("Lisinopril",    "Generic",              "ACE Inhibitor",        421,   448,   4,105.2, 38.4,  True),
    ("Metformin",     "Generic",              "Diabetes",             312,   334,   3, 98.4, 32.1,  True),
    ("Amlodipine",    "Generic",              "Calcium Channel",      284,   301,   4, 71.2, 25.6,  True),
    ("Metoprolol",    "Generic",              "Beta Blocker",         218,   231,   3, 72.8, 26.4,  True),
]

# ── Spending Trend 2013-2022 ──────────────────────────────────────────────
# Source: CMS NHE (National Health Expenditure) Accounts
SPENDING_TREND = {
    2013: {"total_B": 374.3, "per_capita": 1187, "retail_B": 325.1, "hospital_B":  49.2},
    2014: {"total_B": 400.6, "per_capita": 1261, "retail_B": 347.4, "hospital_B":  53.2},
    2015: {"total_B": 458.1, "per_capita": 1431, "retail_B": 394.8, "hospital_B":  63.3},
    2016: {"total_B": 476.5, "per_capita": 1477, "retail_B": 409.7, "hospital_B":  66.8},
    2017: {"total_B": 489.8, "per_capita": 1502, "retail_B": 420.4, "hospital_B":  69.4},
    2018: {"total_B": 510.8, "per_capita": 1553, "retail_B": 435.8, "hospital_B":  75.0},
    2019: {"total_B": 533.7, "per_capita": 1614, "retail_B": 453.8, "hospital_B":  79.9},
    2020: {"total_B": 553.4, "per_capita": 1664, "retail_B": 468.2, "hospital_B":  85.2},
    2021: {"total_B": 576.2, "per_capita": 1729, "retail_B": 487.9, "hospital_B":  88.3},
    2022: {"total_B": 616.7, "per_capita": 1844, "retail_B": 520.6, "hospital_B":  96.1},
}

# ── International Price Comparison ───────────────────────────────────────
# Source: ASPE 2021 report + OECD Health Statistics
# Monthly cost in USD (standardized dosing)
INTERNATIONAL_PRICES = [
    # drug_name, us_price_usd, canada_price_usd, germany_price_usd, uk_price_usd, france_price_usd
    ("Humira (adalimumab)",     1363,  408, 158, 213, 185),
    ("Eliquis (apixaban)",       466,  124,  89, 105,  97),
    ("Xarelto (rivaroxaban)",    441,   98,  76,  92,  84),
    ("Ozempic (semaglutide)",    892,  208, 156, 184, 171),
    ("Lantus (insulin glargine", 292,   28,  21,  26,  23),
    ("Jardiance (empagliflozin", 591,  138,  94, 118, 108),
    ("Trulicity (dulaglutide)",  764,  198, 141, 172, 158),
    ("Entresto (sacubitril)",    614,  142,  98, 124, 114),
    ("Revlimid (lenalidomide)", 4248, 1284, 786,1021, 912),
    ("Dupixent (dupilumab)",    2818,  798, 484, 624, 572),
    ("Keytruda (pembrolizumab)",8248, 2484,1521,1984,1812),
    ("Ozempic (injection)",      892,  208, 156, 184, 171),
    ("Skyrizi (risankizumab)",  3241,  921, 548, 714, 648),
    ("Ibrance (palbociclib)",   4321, 1214, 721, 948, 852),
    ("Imbruvica (ibrutinib)",   9812, 2948,1812,2384,2148),
]

# ── Generic vs Brand Comparison ───────────────────────────────────────────
# Source: FDA, AAM (Association for Accessible Medicines)
GENERIC_VS_BRAND = [
    # drug_name, brand_name, generic_name, brand_avg_cost, generic_avg_cost,
    # medicare_brand_claims_M, years_since_generic_entry
    ("Lipitor/Atorvastatin",    "Lipitor",    "Atorvastatin",    318,  12, 4.2, 12),
    ("Plavix/Clopidogrel",      "Plavix",     "Clopidogrel",     284,   8, 3.8, 12),
    ("Zocor/Simvastatin",       "Zocor",      "Simvastatin",     198,   6, 5.1, 14),
    ("Prilosec/Omeprazole",     "Prilosec",   "Omeprazole",      168,   8, 8.4, 17),
    ("Glucophage/Metformin",    "Glucophage", "Metformin",        98,   3, 9.8, 22),
    ("Zestril/Lisinopril",      "Zestril",    "Lisinopril",       84,   4,10.5, 20),
    ("Norvasc/Amlodipine",      "Norvasc",    "Amlodipine",      112,   4, 7.1, 21),
    ("Toprol/Metoprolol",       "Toprol XL",  "Metoprolol",       98,   3, 7.3, 16),
    ("Zoloft/Sertraline",       "Zoloft",     "Sertraline",      128,   6, 6.2, 19),
    ("Prozac/Fluoxetine",       "Prozac",     "Fluoxetine",      118,   5, 5.8, 27),
]

# ── OECD Per Capita Drug Spending ─────────────────────────────────────────
# Source: OECD Health Statistics 2023
OECD_PER_CAPITA = [
    ("United States",    1844, 100.0),
    ("Switzerland",      1021,  55.4),
    ("Germany",           871,  47.2),
    ("Canada",            818,  44.4),
    ("Japan",             812,  44.0),
    ("France",            762,  41.3),
    ("Austria",           724,  39.3),
    ("Belgium",           718,  38.9),
    ("Ireland",           698,  37.9),
    ("Italy",             618,  33.5),
    ("United Kingdom",    612,  33.2),
    ("Australia",         584,  31.7),
    ("Spain",             548,  29.7),
    ("South Korea",       484,  26.2),
    ("OECD Average",      720,  39.0),
]

# ── Patent Cliff Data ────────────────────────────────────────────────────
# Price index at brand launch = 100, tracks price after generic entry
PATENT_CLIFF = {
    "years_after_generic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
    "brand_price_index":   [100, 105, 108, 111, 114, 116, 118, 119, 120, 121],
    "generic_price_index": [100,  70,  42,  28,  22,  19,  17,  16,  15,  14],
    "generic_market_share_pct": [0, 32, 58, 72, 81, 87, 91, 93, 95, 96],
}


def build_database():
    db_path = "data/drug_pricing.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Medicare Part D top drugs
    c.execute("""CREATE TABLE IF NOT EXISTS medicare_part_d_top (
        drug_name TEXT PRIMARY KEY,
        manufacturer TEXT,
        drug_class TEXT,
        total_spending_2022_M REAL,
        total_spending_2021_M REAL,
        avg_cost_per_claim_2022 INTEGER,
        total_claims_M REAL,
        beneficiaries_M REAL,
        generic_available INTEGER
    )""")
    for row in MEDICARE_PART_D_TOP:
        c.execute("INSERT OR REPLACE INTO medicare_part_d_top VALUES (?,?,?,?,?,?,?,?,?)",
                  (*row[:8], 1 if row[8] else 0))

    # Spending trend
    c.execute("""CREATE TABLE IF NOT EXISTS spending_trend (
        year INTEGER PRIMARY KEY,
        total_B REAL,
        per_capita INTEGER,
        retail_B REAL,
        hospital_B REAL
    )""")
    for yr, d in SPENDING_TREND.items():
        c.execute("INSERT OR REPLACE INTO spending_trend VALUES (?,?,?,?,?)",
                  (yr, d["total_B"], d["per_capita"], d["retail_B"], d["hospital_B"]))

    # International prices
    c.execute("""CREATE TABLE IF NOT EXISTS international_prices (
        drug_name TEXT PRIMARY KEY,
        us_price_usd INTEGER,
        canada_price_usd INTEGER,
        germany_price_usd INTEGER,
        uk_price_usd INTEGER,
        france_price_usd INTEGER
    )""")
    for row in INTERNATIONAL_PRICES:
        c.execute("INSERT OR REPLACE INTO international_prices VALUES (?,?,?,?,?,?)", row)

    # Generic vs brand
    c.execute("""CREATE TABLE IF NOT EXISTS generic_vs_brand (
        drug_name TEXT PRIMARY KEY,
        brand_name TEXT,
        generic_name TEXT,
        brand_avg_cost INTEGER,
        generic_avg_cost INTEGER,
        medicare_brand_claims_M REAL,
        years_since_generic_entry INTEGER
    )""")
    for row in GENERIC_VS_BRAND:
        c.execute("INSERT OR REPLACE INTO generic_vs_brand VALUES (?,?,?,?,?,?,?)", row)

    # OECD per capita
    c.execute("""CREATE TABLE IF NOT EXISTS oecd_per_capita (
        country TEXT PRIMARY KEY,
        per_capita_usd INTEGER,
        pct_of_us REAL
    )""")
    for row in OECD_PER_CAPITA:
        c.execute("INSERT OR REPLACE INTO oecd_per_capita VALUES (?,?,?)", row)

    conn.commit()
    conn.close()
    print(f"Database built: {db_path}")
    return db_path


def get_dataframes():
    db = build_database()
    import pandas as pd
    conn = sqlite3.connect(db)
    return {
        "top_drugs":   pd.read_sql("SELECT * FROM medicare_part_d_top ORDER BY total_spending_2022_M DESC", conn),
        "trend":       pd.read_sql("SELECT * FROM spending_trend ORDER BY year", conn),
        "intl":        pd.read_sql("SELECT * FROM international_prices ORDER BY us_price_usd DESC", conn),
        "generic":     pd.read_sql("SELECT * FROM generic_vs_brand ORDER BY brand_avg_cost DESC", conn),
        "oecd":        pd.read_sql("SELECT * FROM oecd_per_capita ORDER BY per_capita_usd DESC", conn),
    }


if __name__ == "__main__":
    dfs = get_dataframes()
    for name, df in dfs.items():
        print(f"\n{name.upper()}:")
        print(df.to_string(index=False))
