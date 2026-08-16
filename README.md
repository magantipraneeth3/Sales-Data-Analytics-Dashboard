# Sales Intelligence Dashboard

A professional end-to-end sales analytics project built with Python, Pandas, Scikit-learn, Plotly and Streamlit.

## Project structure

```text
Sales_Analysis_Dashboard/
├── data/
│   ├── raw/sales_data.csv
│   └── processed/clean_sales_data.csv
├── models/
│   ├── sales_prediction.py
│   └── forecast_model.py
├── notebooks/
│   ├── 01_eda.ipynb
│   └── 02_modeling_and_forecasting.ipynb
├── reports/
│   ├── sales_analysis_report.md
│   └── generate_report.py
├── src/
│   ├── app.py
│   ├── data_cleaning.py
│   └── forecasting.py
├── outputs/
└── requirements.txt
```

## Setup

```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
```

## Run in order

```bash
python src/data_cleaning.py
python models/sales_prediction.py
python src/forecasting.py
python reports/generate_report.py
streamlit run src/app.py
```

Open the Streamlit URL shown in the terminal.

## Forecasting

The forecasting script creates a six-month revenue forecast and stores it in `outputs/monthly_forecast.csv`.

## Models

The order-level Random Forest predicts revenue. The forecasting Random Forest predicts monthly revenue from lagged revenue and calendar features.
