# analysis.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import os
import sys

# --- Data (quarterly MRR growth for 2024) ---
data = {
    'quarter': ['Q1', 'Q2', 'Q3', 'Q4'],
    'mrr_growth_percent': [1.88, 8.47, 12.31, 10.84]
}
df = pd.DataFrame(data)

# --- Metrics ---
average = round(df['mrr_growth_percent'].mean(), 2)  # should be 8.38
industry_target = 15.0

# Console output
print("Quarterly MRR growth (2024):")
print(df.to_string(index=False))
print(f"\nComputed average MRR growth: {average}%")
print(f"Industry target: {industry_target}%")
if abs(average - 8.38) > 1e-6:
    print("\nWARNING: Average computed is not exactly 8.38; check source data.")
else:
    print("\nAverage matches required value (8.38).")

# --- Visualization: trend + benchmark ---
sns.set(style="whitegrid", context="talk")
plt.figure(figsize=(9,5))
ax = sns.lineplot(x='quarter', y='mrr_growth_percent', marker='o', linewidth=2.5, data=df)
ax.axhline(industry_target, color='red', linestyle='--', linewidth=2, label=f'Industry target: {industry_target}%')
ax.axhline(average, color='green', linestyle=':', linewidth=1.5, label=f'Average: {average}%')
ax.set_title('MRR Growth Trend — 2024 Quarters')
ax.set_ylabel('MRR Growth (%)')
ax.set_xlabel('Quarter')
ax.set_ylim(min(0, df['mrr_growth_percent'].min() - 5), max(industry_target + 5, df['mrr_growth_percent'].max() + 5))
ax.legend()
plt.tight_layout()

# Save PNG
png_path = "mrr_trend.png"
plt.savefig(png_path, dpi=200)
print(f"\nSaved chart to {png_path}")

# Also create a simple HTML report embedding the PNG and the code snippet
with open(png_path, "rb") as f:
    encoded = base64.b64encode(f.read()).decode('utf-8')

html_template = f"""
<!doctype html>
<html>
<head><meta charset="utf-8"><title>MRR Growth — 2024 Trend</title></head>
<body style="font-family:Arial,Helvetica,sans-serif; margin:30px;">
  <h1>MRR Growth Trend (2024)</h1>
  <p><strong>Average MRR growth:</strong> {average}%</p>
  <p><strong>Industry target:</strong> {industry_target}%</p>
  <div><img src="data:image/png;base64,{encoded}" alt="MRR trend" style="max-width:900px;"></div>
  <hr>
  <h2>Data</h2>
  {df.to_html(index=False)}
  <hr>
  <h2>Contact / Verification</h2>
  <p>Verification email: 23f1000470@ds.study.iitm.ac.in</p>
</body>
</html>
"""

html_path = "mrr_report.html"
with open(html_path, "w", encoding="utf-8") as fh:
    fh.write(html_template)
print(f"Saved HTML report to {html_path}")

# Optionally show plot inline if running interactively
try:
    plt.show()
except:
    pass

# Print short analysis summary
summary = f"""
Short summary:
- Average MRR growth (2024): {average}%
- Industry benchmark target: {industry_target}%
- Gap to target: {round(industry_target - average, 2)} percentage points

Interpretation:
The company is underperforming relative to the 15% industry benchmark.
Main suggested strategic thrust: expand into new market segments (see README.md for full recommended actions).
"""
print(summary)
