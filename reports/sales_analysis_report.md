# Sales Intelligence — Analysis Report

## 1. Executive Summary

This project analyzes transactional sales data containing product, date, sales representative, region, category, pricing, customer type, payment method and sales channel information.

The dashboard provides an executive view of revenue, profit, orders, units sold, profit margin, regional performance, category performance and customer/channel mix.

## 2. Dataset

- Records: 1,000
- Date range: 01 Jan 2023 to 01 Jan 2024
- Regions: North, South, East, West
- Product categories: Furniture, Food, Clothing, Electronics
- Sales representatives: 5
- Customer types: New, Returning
- Sales channels: Online, Retail
- Payment methods: Cash, Bank Transfer, Credit Card

## 3. Business Metrics

Revenue is calculated as:

`Quantity Sold × Unit Price`

Cost is calculated as:

`Quantity Sold × Unit Cost`

Gross profit is calculated as:

`Revenue − Cost`

Profit margin is:

`Gross Profit / Revenue × 100`

## 4. Machine Learning

### Order-level prediction

A Random Forest regression pipeline predicts order revenue using quantity, unit cost, unit price, discount and categorical business attributes.

### Forecasting

Monthly revenue is aggregated and forecast using a lag-feature Random Forest model. The model uses the previous three months of revenue plus month number and time index. Six future months are generated recursively.

## 5. Deliverables

- Streamlit executive dashboard
- EDA notebook
- Modeling and forecasting notebook
- Order-level prediction model
- Monthly revenue forecasting model
- Forecast CSV output
- Model evaluation metrics

## 6. Important Data Note

The dataset contains both `Sales_Amount` and unit economics. The project uses unit price and quantity for the dashboard's analytical revenue metric so revenue and unit-level profitability are calculated consistently. The original `Sales_Amount` column remains available for comparison and audit.

## 7. Recommended Business Actions

1. Prioritize high-revenue regions and categories.
2. Compare Online and Retail performance before allocating channel budgets.
3. Monitor representatives with high revenue but weaker margins.
4. Use the forecast as a planning signal rather than a guaranteed future value.
5. Review discounting and unit-cost assumptions before using profit figures for financial decisions.
