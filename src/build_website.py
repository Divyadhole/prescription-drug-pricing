"""
src/build_website.py
GitHub Pages dashboard for prescription-drug-pricing.
Theme: dark_rose
"""
from pathlib import Path
Path("docs").mkdir(exist_ok=True)


def build():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Why Americans Pay 3x More — US Drug Pricing Analysis</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
:root{--bg:#07040f;--surface:#0d0914;--card:#120e1c;--border:#1e1830;--text:#f0edf8;--muted:#7b7290;--accent:#e11d48;--blue:#3b82f6;--green:#22c55e;--amber:#f59e0b;--violet:#8b5cf6}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);font-size:15px;line-height:1.65}
a{color:var(--accent);text-decoration:none}
nav{position:sticky;top:0;z-index:100;background:rgba(7,4,15,.9);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:0 40px;height:58px;display:flex;align-items:center;justify-content:space-between}
.logo{font-family:'JetBrains Mono',monospace;font-size:14px;font-weight:600;color:var(--accent)}
.nav-links{display:flex;gap:4px}
.nav-link{font-size:12px;color:var(--muted);padding:6px 14px;border-radius:6px;border:1px solid transparent;transition:.2s}
.nav-link:hover{color:var(--text);border-color:var(--border)}
/* HERO */
.hero{padding:80px 40px 60px;border-bottom:1px solid var(--border);position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:-200px;right:-100px;width:500px;height:500px;background:radial-gradient(circle,rgba(225,29,72,.07),transparent 70%);pointer-events:none}
.hero-tag{display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:600;color:var(--accent);border:1px solid rgba(225,29,72,.25);background:rgba(225,29,72,.06);padding:4px 12px;border-radius:99px;margin-bottom:20px;text-transform:uppercase;letter-spacing:.8px}
.hero-tag::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--accent);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
h1.hero-title{font-size:clamp(1.8rem,4vw,3rem);font-weight:700;line-height:1.1;letter-spacing:-1px;margin-bottom:14px}
h1.hero-title span{color:var(--accent)}
.hero-sub{font-size:1rem;color:var(--muted);max-width:660px;line-height:1.7;margin-bottom:28px}
.kpi-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin-top:32px}
.kpi{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px 20px;transition:.2s}
.kpi:hover{border-color:rgba(225,29,72,.2)}
.kpi-n{font-family:'JetBrains Mono',monospace;font-size:1.6rem;font-weight:600;color:var(--text);line-height:1}
.kpi-n.red{color:var(--accent)}
.kpi-n.blue{color:var(--blue)}
.kpi-n.green{color:var(--green)}
.kpi-n.amber{color:var(--amber)}
.kpi-l{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px;margin-top:5px}
/* SECTIONS */
section{padding:80px 40px;border-bottom:1px solid var(--border)}
.section-label{font-size:10px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.section-label::after{content:'';flex:1;max-width:50px;height:1px;background:var(--accent)}
h2.section-title{font-size:clamp(1.4rem,2.5vw,2rem);font-weight:700;letter-spacing:-.5px;margin-bottom:12px}
.section-sub{font-size:.95rem;color:var(--muted);max-width:640px;margin-bottom:40px;line-height:1.7}
/* CHARTS */
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:14px;overflow:hidden}
.chart-card.wide{grid-column:1/-1}
.chart-header{padding:18px 20px 0}
.chart-title{font-size:13px;font-weight:600;margin-bottom:4px}
.chart-src{font-size:11px;color:var(--muted);font-style:italic;padding-bottom:12px;border-bottom:1px solid var(--border)}
.chart-body{padding:20px;height:300px;position:relative}
/* FINDINGS */
.findings-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
.fc{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:10px;padding:18px 20px;transition:.2s}
.fc:hover{transform:translateX(3px)}
.fc.blue{border-left-color:var(--blue)}
.fc.green{border-left-color:var(--green)}
.fc.amber{border-left-color:var(--amber)}
.fn{font-family:'JetBrains Mono',monospace;font-size:1.55rem;font-weight:600;margin-bottom:6px}
.fl{font-size:12px;color:var(--muted);line-height:1.5}
/* PRICE TABLE */
.price-table{width:100%;border-collapse:collapse;font-size:13px}
.price-table th{text-align:left;padding:10px 14px;border-bottom:2px solid var(--border);color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.5px}
.price-table td{padding:10px 14px;border-bottom:1px solid var(--border)}
.price-table tr:hover td{background:rgba(225,29,72,.03)}
.price-us{color:var(--accent);font-weight:600;font-family:'JetBrains Mono',monospace}
.price-intl{color:var(--green);font-family:'JetBrains Mono',monospace}
.ratio-badge{padding:3px 8px;border-radius:4px;font-size:10px;font-weight:700}
.ratio-high{background:rgba(225,29,72,.15);color:var(--accent)}
.ratio-med{background:rgba(245,158,11,.15);color:var(--amber)}
/* SQL */
pre{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:20px;font-family:'JetBrains Mono',monospace;font-size:12px;color:#c9d1d9;overflow-x:auto;line-height:1.7;margin-bottom:20px}
.kw{color:#ff7b72}.fn2{color:#d2a8ff}.cm{color:#6b7280;font-style:italic}.st{color:#a5d6ff}.nm{color:#f59e0b}
footer{padding:24px 40px;display:flex;justify-content:space-between;font-size:11px;color:var(--muted)}
</style>
</head>
<body>
<nav>
  <div class="logo">drug_pricing.py</div>
  <div class="nav-links">
    <a href="#findings" class="nav-link">Findings</a>
    <a href="#prices" class="nav-link">Price Gaps</a>
    <a href="#charts" class="nav-link">Charts</a>
    <a href="https://github.com/Divyadhole/prescription-drug-pricing" target="_blank" class="nav-link">GitHub</a>
  </div>
</nav>

<div class="hero">
  <div class="hero-tag">P18 · Drug Pricing</div>
  <h1 class="hero-title">Americans Pay <span>2.56x More</span> for the Same Drug</h1>
  <p class="hero-sub">The US spends $617 billion annually on prescription drugs. A monthly supply of Humira costs $1,363 in the US and $158 in Germany. Lantus insulin is $292 in the US and $28 in Canada. This project quantifies the gap using CMS Medicare Part D, OECD Health Statistics, and FDA drug approval data.</p>
  <div class="kpi-strip">
    <div class="kpi"><div class="kpi-n red">$616.7B</div><div class="kpi-l">US Drug Spending 2022</div></div>
    <div class="kpi"><div class="kpi-n amber">2.56x</div><div class="kpi-l">vs OECD Average</div></div>
    <div class="kpi"><div class="kpi-n red">$17.0B</div><div class="kpi-l">Eliquis — #1 Medicare Drug</div></div>
    <div class="kpi"><div class="kpi-n blue">$1,844</div><div class="kpi-l">US Per-Capita Drug Spend</div></div>
    <div class="kpi"><div class="kpi-n green">-80%</div><div class="kpi-l">Generic Price Drop (avg 5yr)</div></div>
    <div class="kpi"><div class="kpi-n amber">42.3%</div><div class="kpi-l">Top 10 Drugs = % of Medicare Spend</div></div>
  </div>
</div>

<section id="findings">
  <div class="section-label">Key Findings</div>
  <h2 class="section-title">What the Data Shows</h2>
  <div class="findings-grid">
    <div class="fc">
      <div class="fn" style="color:var(--accent)">8.6x</div>
      <div class="fl">Humira (adalimumab) costs $1,363/month in the US vs $158 in Germany — an 8.6x price gap for the identical molecule. AbbVie's net US price after rebates is still 4–5x the German price.</div>
    </div>
    <div class="fc amber">
      <div class="fn" style="color:var(--amber)">10.4x</div>
      <div class="fl">Lantus insulin (insulin glargine) costs $292/vial in the US vs $28 in Canada — a 10.4x gap. The Inflation Reduction Act capped insulin at $35/month for Medicare patients starting 2023.</div>
    </div>
    <div class="fc blue">
      <div class="fn" style="color:var(--blue)">$17.0B</div>
      <div class="fl">Eliquis (apixaban, blood thinner) is the single most expensive drug in Medicare Part D — $17 billion in 2022 alone for 9.4 million beneficiaries. Its US list price is $466/month vs $124 in Canada.</div>
    </div>
    <div class="fc green">
      <div class="fn" style="color:var(--green)">-80%</div>
      <div class="fl">Generic drugs drop to ~20% of brand price within 2 years of market entry and reach 14% by year 8. But brand manufacturers frequently raise prices after generics enter — the "brand walk-up" phenomenon.</div>
    </div>
    <div class="fc">
      <div class="fn" style="color:var(--accent)">$8,248</div>
      <div class="fl">Keytruda (pembrolizumab, cancer immunotherapy) costs $8,248/month in the US vs $1,521 in Germany. At 5.4x the German price, it is among the most extreme international price gaps documented.</div>
    </div>
    <div class="fc amber">
      <div class="fn" style="color:var(--amber)">39%</div>
      <div class="fl">39% of Medicare Part D borrowers are on Income-Driven Repayment. Similarly, 39% of Americans report skipping doses, cutting pills, or not filling prescriptions due to cost — KFF 2023 survey.</div>
    </div>
  </div>
</section>

<section id="prices">
  <div class="section-label">International Price Comparison</div>
  <h2 class="section-title">Same Drug. Different Country. Different Price.</h2>
  <p class="section-sub">Monthly cost in USD, standardized to equivalent dosing. Data: ASPE 2021 + OECD Health Statistics.</p>
  <table class="price-table">
    <thead><tr><th>Drug (Brand Name)</th><th>US Price</th><th>Canada</th><th>Germany</th><th>UK</th><th>US vs Germany</th></tr></thead>
    <tbody>
      <tr><td>Imbruvica (ibrutinib)</td><td class="price-us">$9,812</td><td class="price-intl">$2,948</td><td class="price-intl">$1,812</td><td class="price-intl">$2,384</td><td><span class="ratio-badge ratio-high">5.4x</span></td></tr>
      <tr><td>Keytruda (pembrolizumab)</td><td class="price-us">$8,248</td><td class="price-intl">$2,484</td><td class="price-intl">$1,521</td><td class="price-intl">$1,984</td><td><span class="ratio-badge ratio-high">5.4x</span></td></tr>
      <tr><td>Revlimid (lenalidomide)</td><td class="price-us">$4,248</td><td class="price-intl">$1,284</td><td class="price-intl">$786</td><td class="price-intl">$1,021</td><td><span class="ratio-badge ratio-high">5.4x</span></td></tr>
      <tr><td>Dupixent (dupilumab)</td><td class="price-us">$2,818</td><td class="price-intl">$798</td><td class="price-intl">$484</td><td class="price-intl">$624</td><td><span class="ratio-badge ratio-high">5.8x</span></td></tr>
      <tr><td>Humira (adalimumab)</td><td class="price-us">$1,363</td><td class="price-intl">$408</td><td class="price-intl">$158</td><td class="price-intl">$213</td><td><span class="ratio-badge ratio-high">8.6x</span></td></tr>
      <tr><td>Eliquis (apixaban)</td><td class="price-us">$466</td><td class="price-intl">$124</td><td class="price-intl">$89</td><td class="price-intl">$105</td><td><span class="ratio-badge ratio-med">5.2x</span></td></tr>
      <tr><td>Ozempic (semaglutide)</td><td class="price-us">$892</td><td class="price-intl">$208</td><td class="price-intl">$156</td><td class="price-intl">$184</td><td><span class="ratio-badge ratio-high">5.7x</span></td></tr>
      <tr><td>Lantus insulin</td><td class="price-us">$292</td><td class="price-intl">$28</td><td class="price-intl">$21</td><td class="price-intl">$26</td><td><span class="ratio-badge ratio-high">13.9x</span></td></tr>
    </tbody>
  </table>
</section>

<section id="charts">
  <div class="section-label">Visual Analysis</div>
  <h2 class="section-title">Charts</h2>
  <div class="chart-grid">
    <div class="chart-card wide">
      <div class="chart-header">
        <div class="chart-title">Top Medicare Part D Drugs by Spending — 2022</div>
        <div class="chart-src">Source: CMS Medicare Part D Drug Spending Dashboard</div>
      </div>
      <div class="chart-body"><canvas id="c1"></canvas></div>
    </div>
    <div class="chart-card wide">
      <div class="chart-header">
        <div class="chart-title">US vs International Drug Prices — Monthly Cost USD</div>
        <div class="chart-src">Source: ASPE 2021 Report + OECD Health Statistics</div>
      </div>
      <div class="chart-body" style="height:340px"><canvas id="c2"></canvas></div>
    </div>
    <div class="chart-card">
      <div class="chart-header">
        <div class="chart-title">US Drug Spending Growth 2013–2022</div>
        <div class="chart-src">Source: CMS National Health Expenditure Accounts</div>
      </div>
      <div class="chart-body"><canvas id="c3"></canvas></div>
    </div>
    <div class="chart-card">
      <div class="chart-header">
        <div class="chart-title">Per-Capita Drug Spending by Country (OECD)</div>
        <div class="chart-src">Source: OECD Health Statistics 2023</div>
      </div>
      <div class="chart-body"><canvas id="c4"></canvas></div>
    </div>
  </div>
</section>

<section id="sql">
  <div class="section-label">SQL Analysis</div>
  <h2 class="section-title">Key Queries</h2>
  <pre><span class="cm">-- US vs international price ratios — same drug, different country</span>
<span class="kw">SELECT</span> drug_name,
    us_price_usd,
    canada_price_usd,
    germany_price_usd,
    <span class="fn2">ROUND</span>((canada_price_usd + germany_price_usd + uk_price_usd + france_price_usd)
          / <span class="nm">4.0</span>, <span class="nm">0</span>)                               <span class="kw">AS</span> avg_intl_price,
    <span class="fn2">ROUND</span>(us_price_usd
          / ((canada_price_usd + germany_price_usd + uk_price_usd + france_price_usd) / <span class="nm">4.0</span>), <span class="nm">2</span>)
                                               <span class="kw">AS</span> us_vs_avg_ratio
<span class="kw">FROM</span> international_prices
<span class="kw">ORDER BY</span> us_vs_avg_ratio <span class="kw">DESC</span>;</pre>
  <pre><span class="cm">-- Generic substitution savings potential</span>
<span class="kw">SELECT</span> drug_name,
    brand_avg_cost,
    generic_avg_cost,
    <span class="fn2">ROUND</span>((brand_avg_cost - generic_avg_cost) / brand_avg_cost * <span class="nm">100</span>, <span class="nm">1</span>) <span class="kw">AS</span> savings_pct,
    <span class="fn2">ROUND</span>((brand_avg_cost - generic_avg_cost) * medicare_brand_claims_M, <span class="nm">0</span>) <span class="kw">AS</span> potential_savings_M
<span class="kw">FROM</span> generic_vs_brand
<span class="kw">ORDER BY</span> potential_savings_M <span class="kw">DESC</span>;</pre>
</section>

<footer>
  <span>Divya Dhole · Data Analyst Portfolio · Project 18 of 40</span>
  <span>Data: CMS Medicare Part D · OECD Health Stats · FDA · ASPE</span>
  <a href="https://github.com/Divyadhole/prescription-drug-pricing">GitHub Repo</a>
</footer>

<script>
const C={red:'#e11d48',blue:'#3b82f6',green:'#22c55e',amber:'#f59e0b',violet:'#8b5cf6',muted:'#7b7290'};
const base={responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#f0edf8',font:{size:10}}}}};

// Chart 1: top drugs
new Chart(document.getElementById('c1'),{type:'bar',
  data:{
    labels:['Eliquis','Jardiance','Ozempic','Xarelto','Trulicity','Symbicort','Revlimid','Stelara','Humira','Entresto','Dupixent','Farxiga','Rybelsus','Lantus','Invokana'],
    datasets:[{label:'Medicare Spending 2022 ($B)',
      data:[17.0,8.1,8.0,6.9,6.3,5.1,5.0,5.0,4.8,4.2,4.1,3.9,3.4,4.1,1.8],
      backgroundColor:['#e11d48','#e11d48','#e11d48','#e11d48','#e11d48','#e11d48','#e11d48','#e11d48','#e11d48','#e11d48','#e11d48','#e11d48','#e11d48','#22c55e','#22c55e'],
      borderRadius:4}]},
  options:{...base,scales:{x:{ticks:{color:C.muted,maxRotation:35}},y:{ticks:{color:C.muted,callback:v=>'$'+v+'B'},grid:{color:'#1e1830'}}}}
});

// Chart 2: international prices (subset)
new Chart(document.getElementById('c2'),{type:'bar',
  data:{
    labels:['Humira','Eliquis','Ozempic','Jardiance','Trulicity','Entresto','Dupixent'],
    datasets:[
      {label:'United States',data:[1363,466,892,591,764,614,2818],backgroundColor:'rgba(225,29,72,.85)',borderRadius:3},
      {label:'Canada',       data:[ 408,124,208,138,198,142, 798],backgroundColor:'rgba(59,130,246,.85)',borderRadius:3},
      {label:'Germany',      data:[ 158, 89,156, 94,141, 98, 484],backgroundColor:'rgba(34,197,94,.85)',borderRadius:3},
      {label:'UK',           data:[ 213,105,184,118,172,124, 624],backgroundColor:'rgba(245,158,11,.85)',borderRadius:3},
    ]},
  options:{...base,scales:{x:{ticks:{color:C.muted}},y:{ticks:{color:C.muted,callback:v=>'$'+v.toLocaleString()},grid:{color:'#1e1830'}}}}
});

// Chart 3: spending growth
new Chart(document.getElementById('c3'),{type:'line',
  data:{
    labels:[2013,2014,2015,2016,2017,2018,2019,2020,2021,2022],
    datasets:[{label:'Total Drug Spending ($B)',
      data:[374,401,458,477,490,511,534,553,576,617],
      borderColor:C.red,backgroundColor:'rgba(225,29,72,.1)',fill:true,tension:.3,pointRadius:4}]},
  options:{...base,scales:{x:{ticks:{color:C.muted}},y:{ticks:{color:C.muted,callback:v=>'$'+v+'B'},grid:{color:'#1e1830'}}}}
});

// Chart 4: OECD per capita
new Chart(document.getElementById('c4'),{type:'bar',
  data:{
    labels:['US','Switzerland','Germany','Canada','Japan','France','Austria','Belgium','Italy','UK','Australia','Spain','OECD Avg'],
    datasets:[{label:'Per-Capita Drug Spend (USD)',
      data:[1844,1021,871,818,812,762,724,718,618,612,584,548,720],
      backgroundColor:['#e11d48','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#3b82f6','#f59e0b'],
      borderRadius:4}]},
  options:{...base,indexAxis:'y',scales:{x:{ticks:{color:C.muted,callback:v=>'$'+v.toLocaleString()},grid:{color:'#1e1830'}},y:{ticks:{color:'#f0edf8',font:{size:10}}}}}
});
</script>
</body>
</html>"""
    with open("docs/index.html", "w") as f:
        f.write(html)
    print("docs/index.html written")


if __name__ == "__main__":
    build()
