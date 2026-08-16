from pathlib import Path
import pandas as pd
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'processed' / 'clean_sales_data.csv'
REPORT = ROOT / 'reports' / 'generated_summary.html'

def generate():
    df = pd.read_csv(DATA)
    region = df.groupby('Region')['Revenue'].sum().sort_values(ascending=False)
    category = df.groupby('Product_Category')['Revenue'].sum().sort_values(ascending=False)
    channel = df.groupby('Sales_Channel')['Revenue'].sum().sort_values(ascending=False)
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Sales Intelligence Report</title>
<style>body{{font-family:Inter,Arial,sans-serif;background:#f5f7fb;color:#0f172a;max-width:1000px;margin:40px auto;padding:0 20px}}.hero{{background:#0b1220;color:white;padding:28px;border-radius:18px}}.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:20px 0}}.card{{background:white;padding:18px;border:1px solid #e2e8f0;border-radius:14px}}table{{width:100%;border-collapse:collapse;background:white}}td,th{{padding:10px;border-bottom:1px solid #e2e8f0;text-align:left}}</style></head><body>
<div class="hero"><h1>Sales Intelligence Report</h1><p>Generated {datetime.now():%d %b %Y %H:%M}</p></div>
<div class="grid"><div class="card"><b>Revenue</b><h2>₹{df.Revenue.sum():,.0f}</h2></div><div class="card"><b>Profit</b><h2>₹{df.Profit.sum():,.0f}</h2></div><div class="card"><b>Orders</b><h2>{len(df):,}</h2></div><div class="card"><b>Units</b><h2>{df.Quantity_Sold.sum():,.0f}</h2></div></div>
<h2>Top Regions</h2><table><tr><th>Region</th><th>Revenue</th></tr>{''.join(f'<tr><td>{k}</td><td>₹{v:,.0f}</td></tr>' for k,v in region.items())}</table>
<h2>Categories</h2><table><tr><th>Category</th><th>Revenue</th></tr>{''.join(f'<tr><td>{k}</td><td>₹{v:,.0f}</td></tr>' for k,v in category.items())}</table>
<h2>Channels</h2><table><tr><th>Channel</th><th>Revenue</th></tr>{''.join(f'<tr><td>{k}</td><td>₹{v:,.0f}</td></tr>' for k,v in channel.items())}</table>
</body></html>'''
    REPORT.write_text(html, encoding='utf-8')
    print(REPORT)

if __name__ == '__main__':
    generate()
