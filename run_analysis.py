"""
run_analysis.py — Full pipeline for prescription-drug-pricing
"""
import sys
sys.path.insert(0, ".")

print("=" * 60)
print("Prescription Drug Pricing Analysis — Full Pipeline")
print("=" * 60)

print("\n[1/3] Building database...")
from src.drug_data import build_database
build_database()

print("\n[2/3] Generating charts...")
from src.charts import run_all
run_all()

print("\n[3/3] Building website...")
from src.build_website import build
build()

print("\n" + "=" * 60)
print("COMPLETE:")
print("  docs/index.html     → GitHub Pages dashboard")
print("  outputs/charts/     → 6 PNG charts")
print("  data/drug_pricing.db → SQLite database")
print("=" * 60)
