-- =============================================================================
-- prescription-drug-pricing / sql/analysis/drug_pricing.sql
-- US Prescription Drug Pricing Analysis — CMS + OECD + FDA Data
-- =============================================================================

-- 1. Top Medicare Part D drugs by spending with YoY growth and rank
SELECT drug_name,
    manufacturer,
    drug_class,
    total_spending_2022_M,
    total_spending_2021_M,
    ROUND((total_spending_2022_M - total_spending_2021_M)
          / total_spending_2021_M * 100, 1)              AS yoy_growth_pct,
    avg_cost_per_claim_2022,
    total_claims_M,
    CASE WHEN generic_available = 1 THEN 'Generic Available' ELSE 'Brand Only' END AS status,
    RANK() OVER (ORDER BY total_spending_2022_M DESC)    AS spend_rank,
    ROUND(SUM(total_spending_2022_M) OVER (
          ORDER BY total_spending_2022_M DESC
          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
          / SUM(total_spending_2022_M) OVER () * 100, 1) AS cumulative_share_pct
FROM medicare_part_d_top
ORDER BY total_spending_2022_M DESC;

-- =============================================================================

-- 2. US vs International price ratios — same drug, different country
SELECT drug_name,
    us_price_usd,
    canada_price_usd,
    germany_price_usd,
    uk_price_usd,
    france_price_usd,
    ROUND((canada_price_usd + germany_price_usd + uk_price_usd + france_price_usd)
          / 4.0, 0)                                         AS avg_intl_price,
    ROUND(us_price_usd
          / ((canada_price_usd + germany_price_usd + uk_price_usd + france_price_usd) / 4.0), 2)
                                                            AS us_vs_avg_ratio,
    ROUND(us_price_usd / NULLIF(canada_price_usd, 0), 2)   AS us_vs_canada,
    ROUND(us_price_usd / NULLIF(germany_price_usd, 0), 2)  AS us_vs_germany,
    ROUND(us_price_usd - (canada_price_usd + germany_price_usd + uk_price_usd + france_price_usd)
          / 4.0, 0)                                         AS price_premium_usd
FROM international_prices
ORDER BY us_vs_avg_ratio DESC;

-- =============================================================================

-- 3. Generic vs brand savings calculation
SELECT drug_name,
    brand_name,
    generic_name,
    brand_avg_cost,
    generic_avg_cost,
    ROUND((brand_avg_cost - generic_avg_cost) / brand_avg_cost * 100, 1) AS savings_pct,
    years_since_generic_entry,
    medicare_brand_claims_M,
    ROUND((brand_avg_cost - generic_avg_cost) * medicare_brand_claims_M, 0) AS potential_savings_M
FROM generic_vs_brand
ORDER BY potential_savings_M DESC;

-- =============================================================================

-- 4. Drug class spending concentration
SELECT drug_class,
    COUNT(*)                           AS drugs_in_class,
    ROUND(SUM(total_spending_2022_M), 0) AS class_spend_2022_M,
    ROUND(AVG(avg_cost_per_claim_2022), 0) AS avg_cost_per_claim,
    ROUND(SUM(total_spending_2022_M)
          / SUM(SUM(total_spending_2022_M)) OVER () * 100, 1) AS pct_of_total,
    RANK() OVER (ORDER BY SUM(total_spending_2022_M) DESC) AS class_rank
FROM medicare_part_d_top
GROUP BY drug_class
ORDER BY class_spend_2022_M DESC;

-- =============================================================================

-- 5. OECD per-capita spending comparison
SELECT country,
    per_capita_usd,
    pct_of_us,
    ROUND(100 - pct_of_us, 1)           AS discount_vs_us_pct,
    CASE
        WHEN country = 'United States' THEN 'Reference'
        WHEN pct_of_us >= 50            THEN 'High Spend'
        WHEN pct_of_us >= 35            THEN 'Moderate'
        ELSE 'Low'
    END                                  AS tier,
    RANK() OVER (ORDER BY per_capita_usd DESC) AS spend_rank
FROM oecd_per_capita
ORDER BY per_capita_usd DESC;

-- =============================================================================

-- 6. High-cost brand drugs — candidates for negotiation (IRA 2022)
SELECT drug_name,
    manufacturer,
    drug_class,
    total_spending_2022_M,
    avg_cost_per_claim_2022,
    beneficiaries_M,
    ROUND(total_spending_2022_M / beneficiaries_M, 1) AS spend_per_beneficiary_M,
    CASE
        WHEN total_spending_2022_M > 5000  THEN 'Tier 1 — Negotiate First'
        WHEN total_spending_2022_M > 2000  THEN 'Tier 2 — Priority'
        WHEN total_spending_2022_M > 1000  THEN 'Tier 3 — Watch'
        ELSE 'Tier 4 — Monitor'
    END AS negotiation_priority
FROM medicare_part_d_top
WHERE generic_available = 0
ORDER BY total_spending_2022_M DESC;

-- =============================================================================

-- 7. Spending trend analysis with CAGR
SELECT year,
    total_B,
    per_capita,
    retail_B,
    LAG(total_B) OVER (ORDER BY year)                     AS prev_year_B,
    ROUND((total_B - LAG(total_B) OVER (ORDER BY year))
          / LAG(total_B) OVER (ORDER BY year) * 100, 1)   AS yoy_growth_pct,
    ROUND((total_B - FIRST_VALUE(total_B) OVER (ORDER BY year))
          / FIRST_VALUE(total_B) OVER (ORDER BY year) * 100, 1) AS growth_from_2013_pct
FROM spending_trend
ORDER BY year;

-- =============================================================================

-- 8. Price premium by manufacturer
SELECT m.manufacturer,
    COUNT(*)                            AS drugs_in_portfolio,
    ROUND(SUM(m.total_spending_2022_M), 0) AS total_medicare_spend_M,
    ROUND(AVG(m.avg_cost_per_claim_2022), 0) AS avg_cost_per_claim,
    ROUND(SUM(m.total_spending_2022_M)
          / SUM(SUM(m.total_spending_2022_M)) OVER () * 100, 2) AS pct_of_total_spend
FROM medicare_part_d_top m
WHERE m.manufacturer != 'Generic'
GROUP BY m.manufacturer
HAVING total_medicare_spend_M > 1000
ORDER BY total_medicare_spend_M DESC;
