from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw' / 'sales_data.csv'
OUT = ROOT / 'data' / 'processed' / 'clean_sales_data.csv'


def clean_sales_data(path=RAW):
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    df['Sale_Date'] = pd.to_datetime(df['Sale_Date'], errors='coerce')

    numeric = ['Product_ID','Sales_Amount','Quantity_Sold','Unit_Cost','Unit_Price','Discount']
    for c in numeric:
        df[c] = pd.to_numeric(df[c], errors='coerce')

    categorical = ['Sales_Rep','Region','Product_Category','Customer_Type','Payment_Method','Sales_Channel','Region_and_Sales_Rep']
    for c in categorical:
        df[c] = df[c].astype('string').str.strip()

    # Remove impossible/missing rows required for analysis.
    df = df.dropna(subset=['Sale_Date','Product_ID','Quantity_Sold','Unit_Cost','Unit_Price'])
    df = df[df['Quantity_Sold'] > 0].copy()
    df['Discount'] = df['Discount'].fillna(0).clip(0, 1)

    # Business metrics used consistently by the dashboard and models.
    df['Revenue'] = df['Quantity_Sold'] * df['Unit_Price']
    df['Cost'] = df['Quantity_Sold'] * df['Unit_Cost']
    df['Profit'] = df['Revenue'] - df['Cost']
    df['Profit_Margin'] = np.where(df['Revenue'] != 0, df['Profit'] / df['Revenue'] * 100, 0)
    df['Year'] = df['Sale_Date'].dt.year
    df['Month'] = df['Sale_Date'].dt.month
    df['Month_Name'] = df['Sale_Date'].dt.strftime('%b')
    df['Year_Month'] = df['Sale_Date'].dt.to_period('M').astype(str)

    df = df.sort_values('Sale_Date').reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    return df


if __name__ == '__main__':
    cleaned = clean_sales_data()
    print(f'Cleaned rows: {len(cleaned):,}')
    print(f'Saved: {OUT}')
    print(f'Revenue: ₹{cleaned.Revenue.sum():,.2f}')
    print(f'Profit: ₹{cleaned.Profit.sum():,.2f}')
