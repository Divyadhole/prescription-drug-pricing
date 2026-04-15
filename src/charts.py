"""
src/charts.py
6 publication-quality charts for prescription drug pricing analysis.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import sqlite3
import pandas as pd
from pathlib import Path

Path("outputs/charts").mkdir(parents=True, exist_ok=True)

DPI     = 170
DARK    = "#070712"
CARD    = "#0f0f1e"
ACCENT  = "#e11d48"   # rose-red
ACCENT2 = "#3b82f6"   # blue
GREEN   = "#22c55e"
AMBER   = "#f59e0b"
MUTED   = "#6b7280"
TEXT    = "#f0f0f8"
VIOLET  = "#8b5cf6"

def styled_fig(w=13, h=7):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(DARK)
    ax.set_facecolor(CARD)
    ax.tick_params(colors=MUTED, labelsize=8.5)
    for spine in ax.spines.values():
        spine.set_edgecolor("#1e1e3a")
    ax.grid(axis="y", color="#1e1e3a", linewidth=0.5, alpha=0.7)
    return fig, ax

def load_db():
    return sqlite3.connect("data/drug_pricing.db")


def chart_01_top_drugs():
    """Top 15 Medicare Part D drugs by spending."""
    conn = load_db()
    df = pd.read_sql(
        "SELECT drug_name, total_spending_2022_M, generic_available FROM medicare_part_d_top ORDER BY total_spending_2022_M DESC LIMIT 15",
        conn
    )
    conn.close()

    fig, ax = styled_fig(14, 8)
    colors = [GREEN if g else ACCENT for g in df["generic_available"]]
    bars = ax.barh(df["drug_name"], df["total_spending_2022_M"] / 1000, color=colors, alpha=0.85, height=0.65)

    for bar, val in zip(bars, df["total_spending_2022_M"]):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                f"${val/1000:.1f}B", va="center", color=TEXT, fontsize=9)

    patches = [
        mpatches.Patch(color=ACCENT, label="Brand-only (no generic)"),
        mpatches.Patch(color=GREEN,  label="Generic available"),
    ]
    ax.legend(handles=patches, facecolor=CARD, edgecolor="#2a2a3e", labelcolor=TEXT, fontsize=9, loc="lower right")
    ax.set_title("Top 15 Medicare Part D Drugs by Total Spending — 2022", color=TEXT, fontsize=13, fontweight="bold", pad=16)
    ax.set_xlabel("Total Medicare Spending ($ Billion)")
    ax.set_xlim(0, 20)
    fig.text(0.12, 0.01, "Source: CMS Medicare Part D Drug Spending Dashboard | divyadhole.github.io", color=MUTED, fontsize=7)
    plt.tight_layout()
    plt.savefig("outputs/charts/01_top_drugs_spend.png", dpi=DPI, bbox_inches="tight", facecolor=DARK)
    plt.close()
    print("Chart 1 saved")


def chart_02_international_prices():
    """US vs international prices — grouped bar."""
    conn = load_db()
    df = pd.read_sql(
        "SELECT * FROM international_prices ORDER BY us_price_usd DESC LIMIT 8",
        conn
    )
    conn.close()

    fig, ax = styled_fig(14, 8)
    x = np.arange(len(df))
    width = 0.15

    bars = [
        ax.bar(x - 2*width, df["us_price_usd"],      width, color=ACCENT,   alpha=0.9, label="United States"),
        ax.bar(x - 1*width, df["canada_price_usd"],  width, color=ACCENT2,  alpha=0.85, label="Canada"),
        ax.bar(x,            df["germany_price_usd"], width, color=AMBER,    alpha=0.85, label="Germany"),
        ax.bar(x + 1*width,  df["uk_price_usd"],     width, color=GREEN,    alpha=0.85, label="United Kingdom"),
        ax.bar(x + 2*width,  df["france_price_usd"], width, color=VIOLET,   alpha=0.85, label="France"),
    ]

    ax.set_xticks(x)
    ax.set_xticklabels([n[:18] for n in df["drug_name"]], rotation=35, ha="right", fontsize=8, color=TEXT)
    ax.set_title("US vs International Drug Prices — Monthly Cost USD (Same Drug, Same Dose)", color=TEXT, fontsize=12, fontweight="bold", pad=16)
    ax.set_ylabel("Monthly Cost (USD)")
    ax.legend(facecolor=CARD, edgecolor="#2a2a3e", labelcolor=TEXT, fontsize=9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"${x:,.0f}"))
    fig.text(0.12, 0.01, "Source: ASPE 2021 Report + OECD Health Statistics | divyadhole.github.io", color=MUTED, fontsize=7)
    plt.tight_layout()
    plt.savefig("outputs/charts/02_us_vs_international.png", dpi=DPI, bbox_inches="tight", facecolor=DARK)
    plt.close()
    print("Chart 2 saved")


def chart_03_spending_growth():
    """US drug spending growth 2013-2022."""
    conn = load_db()
    df = pd.read_sql("SELECT * FROM spending_trend ORDER BY year", conn)
    conn.close()

    fig, ax = styled_fig(13, 7)
    ax.fill_between(df["year"], df["retail_B"], alpha=0.15, color=ACCENT2)
    ax.fill_between(df["year"], df["total_B"], df["retail_B"], alpha=0.1, color=AMBER)
    ax.plot(df["year"], df["total_B"],   color=ACCENT,  linewidth=2.5, marker="o", markersize=5, label="Total Spending")
    ax.plot(df["year"], df["retail_B"],  color=ACCENT2, linewidth=2,   marker="s", markersize=4, label="Retail Spending")

    ax.annotate(f"${df['total_B'].iloc[-1]:.0f}B\n(2022)", xy=(2022, df["total_B"].iloc[-1]),
                xytext=(2020, df["total_B"].iloc[-1]-50), color=ACCENT, fontsize=9, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=0.8))
    ax.annotate(f"${df['total_B'].iloc[0]:.0f}B\n(2013)", xy=(2013, df["total_B"].iloc[0]),
                xytext=(2013.5, df["total_B"].iloc[0]+30), color=MUTED, fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.7))

    ax.set_title("US Total Prescription Drug Spending 2013–2022", color=TEXT, fontsize=13, fontweight="bold", pad=16)
    ax.set_ylabel("Spending ($ Billion)")
    ax.set_xlabel("Year")
    ax.legend(facecolor=CARD, edgecolor="#2a2a3e", labelcolor=TEXT, fontsize=9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"${x:.0f}B"))
    fig.text(0.12, 0.02, "Source: CMS National Health Expenditure Accounts | divyadhole.github.io", color=MUTED, fontsize=7)
    plt.tight_layout()
    plt.savefig("outputs/charts/03_spending_growth.png", dpi=DPI, bbox_inches="tight", facecolor=DARK)
    plt.close()
    print("Chart 3 saved")


def chart_04_generic_vs_brand():
    """Generic vs brand cost savings."""
    conn = load_db()
    df = pd.read_sql("SELECT * FROM generic_vs_brand ORDER BY brand_avg_cost DESC LIMIT 8", conn)
    conn.close()

    fig, ax = styled_fig(13, 7)
    x = np.arange(len(df))
    w = 0.35

    ax.bar(x - w/2, df["brand_avg_cost"],   w, color=ACCENT,  alpha=0.85, label="Brand Average Cost ($)")
    ax.bar(x + w/2, df["generic_avg_cost"], w, color=GREEN,   alpha=0.85, label="Generic Average Cost ($)")

    for i, (bc, gc) in enumerate(zip(df["brand_avg_cost"], df["generic_avg_cost"])):
        savings = round((bc - gc) / bc * 100)
        ax.text(i, bc + 5, f"-{savings}%", ha="center", color=AMBER, fontsize=8.5, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels([n.split("/")[0] for n in df["drug_name"]], rotation=30, ha="right", fontsize=8.5, color=TEXT)
    ax.set_title("Brand vs Generic Drug Cost — Average Monthly Cost ($)", color=TEXT, fontsize=13, fontweight="bold", pad=16)
    ax.set_ylabel("Average Monthly Cost (USD)")
    ax.legend(facecolor=CARD, edgecolor="#2a2a3e", labelcolor=TEXT, fontsize=9)
    fig.text(0.12, 0.01, "Source: FDA Orange Book + AAM Generic Drug Access Report | divyadhole.github.io", color=MUTED, fontsize=7)
    plt.tight_layout()
    plt.savefig("outputs/charts/04_generic_vs_brand.png", dpi=DPI, bbox_inches="tight", facecolor=DARK)
    plt.close()
    print("Chart 4 saved")


def chart_05_oecd_comparison():
    """OECD per-capita drug spending comparison."""
    conn = load_db()
    df = pd.read_sql("SELECT * FROM oecd_per_capita ORDER BY per_capita_usd DESC", conn)
    conn.close()

    fig, ax = styled_fig(13, 8)
    colors = [ACCENT if c == "United States" else (MUTED if c == "OECD Average" else ACCENT2) for c in df["country"]]
    bars = ax.barh(df["country"], df["per_capita_usd"], color=colors, alpha=0.85, height=0.65)

    # OECD avg line
    oecd_avg = df[df["country"] == "OECD Average"]["per_capita_usd"].values[0]
    ax.axvline(x=oecd_avg, color=AMBER, linestyle="--", linewidth=1.5, alpha=0.7, label=f"OECD Avg: ${oecd_avg:,}")

    for bar, val in zip(bars, df["per_capita_usd"]):
        ax.text(bar.get_width() + 8, bar.get_y() + bar.get_height()/2,
                f"${val:,}", va="center", color=TEXT, fontsize=8.5)

    ax.set_title("Per-Capita Prescription Drug Spending by Country — 2022 (USD)", color=TEXT, fontsize=12, fontweight="bold", pad=16)
    ax.set_xlabel("Per-Capita Spending (USD)")
    ax.legend(facecolor=CARD, edgecolor="#2a2a3e", labelcolor=TEXT, fontsize=9)
    ax.set_xlim(0, 2200)
    fig.text(0.12, 0.01, "Source: OECD Health Statistics 2023 | divyadhole.github.io", color=MUTED, fontsize=7)
    plt.tight_layout()
    plt.savefig("outputs/charts/05_oecd_comparison.png", dpi=DPI, bbox_inches="tight", facecolor=DARK)
    plt.close()
    print("Chart 5 saved")


def chart_06_patent_cliff():
    """Patent cliff — price dynamics after generic entry."""
    from src.drug_data import PATENT_CLIFF

    fig, ax1 = styled_fig(12, 7)
    ax2 = ax1.twinx()

    years = PATENT_CLIFF["years_after_generic"]
    ax1.plot(years, PATENT_CLIFF["brand_price_index"],   color=ACCENT,  linewidth=2.5, marker="o", markersize=5, label="Brand Price Index")
    ax1.plot(years, PATENT_CLIFF["generic_price_index"], color=GREEN,   linewidth=2.5, marker="s", markersize=5, label="Generic Price Index")
    ax2.bar(years, PATENT_CLIFF["generic_market_share_pct"], color=ACCENT2, alpha=0.2, width=0.7, label="Generic Market Share %")

    ax1.set_xlabel("Years After Generic Entry")
    ax1.set_ylabel("Price Index (Brand Launch = 100)", color=TEXT)
    ax2.set_ylabel("Generic Market Share (%)", color=ACCENT2)
    ax2.tick_params(axis="y", colors=ACCENT2)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, facecolor=CARD, edgecolor="#2a2a3e", labelcolor=TEXT, fontsize=9)

    ax1.annotate("Brand stays\nat 100+\n(raises price)", xy=(5, 116), xytext=(6, 90),
                 color=ACCENT, fontsize=8, arrowprops=dict(arrowstyle="->", color=ACCENT, lw=0.8))
    ax1.annotate("Generic drops\nto ~14% of\nbrand price", xy=(8, 15), xytext=(5.5, 35),
                 color=GREEN, fontsize=8, arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.8))

    ax1.set_title("The Patent Cliff — Price Dynamics After Generic Market Entry", color=TEXT, fontsize=13, fontweight="bold", pad=16)
    fig.patch.set_facecolor(DARK)
    fig.text(0.12, 0.02, "Source: FDA + AAM Generic Drug Access & Biosimilars Report | divyadhole.github.io", color=MUTED, fontsize=7)
    plt.tight_layout()
    plt.savefig("outputs/charts/06_patent_cliff.png", dpi=DPI, bbox_inches="tight", facecolor=DARK)
    plt.close()
    print("Chart 6 saved")


def run_all():
    from src.drug_data import build_database
    build_database()
    chart_01_top_drugs()
    chart_02_international_prices()
    chart_03_spending_growth()
    chart_04_generic_vs_brand()
    chart_05_oecd_comparison()
    chart_06_patent_cliff()
    print("\nAll 6 charts generated.")


if __name__ == "__main__":
    run_all()
