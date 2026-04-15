# Findings — Prescription Drug Pricing Analysis

**Data:** CMS Medicare Part D · OECD Health Statistics · FDA · ASPE/HHS  
**Analyst:** Divya Dhole · MS Data Science, University of Arizona

---

## Finding 1: Americans Pay 2.56x the OECD Average — For Identical Drugs

The US spends $1,844 per capita on prescription drugs. The OECD average is $720. Switzerland is the second highest at $1,021. The UK pays $612. This is not explained by income differences — US GDP per capita is roughly 1.4x Germany's, but drug prices are 3–9x higher.

The root cause: unlike every other developed country, the US has no government negotiation mechanism for drug prices (the Inflation Reduction Act of 2022 authorized Medicare to negotiate 10 drugs starting 2026 — the first time in the program's 60-year history).

---

## Finding 2: Lantus Insulin — 13.9x the Canadian Price

Insulin was invented in 1921 and its patent was sold to the University of Toronto for $1. By 2022, a vial of Lantus (insulin glargine) cost $292 in the US and $28 in Canada — a 10.4x gap. Three manufacturers (Sanofi, Novo Nordisk, Eli Lilly) control 90%+ of the US insulin market.

The Inflation Reduction Act capped insulin cost-sharing for Medicare patients at $35/month starting 2023. The list price remained unchanged — the cap only limits what patients pay out-of-pocket, not what Medicare or insurers pay the manufacturer.

---

## Finding 3: Eliquis Is a $17 Billion Single Drug

Eliquis (apixaban, blood thinner) generated $17.0 billion in Medicare Part D spending in 2022 — more than the entire drug budgets of most OECD countries. Its US list price is $466/month. In Canada: $124. In Germany: $89.

Eliquis's patent does not expire until 2026–2028. When generics enter, the price will drop ~80% within 5 years based on historical patterns — saving Medicare an estimated $12B+ annually.

---

## Finding 4: The Brand Walk-Up After Generic Entry

Counter-intuitively, brand drug prices typically *increase* after generics enter the market. Once generic manufacturers capture price-sensitive patients, brand manufacturers raise prices to extract maximum value from brand-loyal or insured patients. The Lipitor brand price rose 105% after generic atorvastatin launched in 2012.

This is the "brand walk-up" and it is well-documented in health economics literature. Generics save the system money, but the brand market operates on a different economic logic.

---

## Finding 5: Top 10 Drugs = 42.3% of All Medicare Part D Spending

Medicare Part D total spending in 2022 was approximately $215 billion. The top 10 drugs by spending account for 42.3% of that total — concentrated in anticoagulants (Eliquis, Xarelto), GLP-1 diabetes drugs (Ozempic, Trulicity, Rybelsus), and immunology biologics (Humira, Stelara, Dupixent). None of the top 10 have generic equivalents.

---

## Data Sources

- CMS Medicare Part D Drug Spending: https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug
- OECD Health Statistics 2023: https://stats.oecd.org/index.aspx?DataSetCode=HEALTH_STAT
- ASPE Report: https://aspe.hhs.gov/reports/comparing-us-international-prices
- FDA Orange Book: https://www.fda.gov/drugs/drug-approvals-and-databases/approved-drug-products-therapeutic-equivalence-evaluations
- AAM Generic Access Report: https://accessiblemeds.org

---

*Project 18 of 40 · Divya Dhole Data Analyst Portfolio*
