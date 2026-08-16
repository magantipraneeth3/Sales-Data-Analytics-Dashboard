"""Monthly sales forecasting for the Sales Pulse dashboard project.

Usage:
    python src/forecasting.py

Outputs:
    outputs/monthly_forecast.csv
    outputs/forecast_model.joblib
"""
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'processed' / 'clean_sales_data.csv'
OUT = ROOT / 'outputs'


def load_monthly():
    df = pd.read_csv(DATA, parse_dates=['Sale_Date'])
    monthly = (df.groupby(df['Sale_Date'].dt.to_period('M'))
                 .agg(Revenue=('Revenue','sum'), Orders=('Product_ID','count'), Units=('Quantity_Sold','sum'))
                 .reset_index())
    monthly['Date'] = monthly['Sale_Date'].dt.to_timestamp()
    monthly = monthly[['Date','Revenue','Orders','Units']].sort_values('Date').reset_index(drop=True)
    return monthly


def make_features(monthly, lags=(1,2,3)):
    x = monthly.copy()
    for lag in lags:
        x[f'lag_{lag}'] = x['Revenue'].shift(lag)
    x['month_num'] = x['Date'].dt.month
    x['time_idx'] = np.arange(len(x))
    return x.dropna().reset_index(drop=True)


def train_forecast(horizon=6):
    monthly = load_monthly()
    feat = make_features(monthly)
    features = ['lag_1','lag_2','lag_3','month_num','time_idx']

    if len(feat) < 8:
        raise ValueError('Not enough monthly history to train the forecasting model.')

    split = max(5, len(feat) - 3)
    X_train, y_train = feat[features].iloc[:split], feat['Revenue'].iloc[:split]
    X_test, y_test = feat[features].iloc[split:], feat['Revenue'].iloc[split:]

    model = RandomForestRegressor(n_estimators=400, max_depth=6, random_state=42, min_samples_leaf=1)
    model.fit(X_train, y_train)

    pred_test = model.predict(X_test)
    mae = mean_absolute_error(y_test, pred_test)
    rmse = mean_squared_error(y_test, pred_test) ** 0.5

    # Refit on all known observations before recursive future forecasting.
    model.fit(feat[features], feat['Revenue'])
    history = monthly[['Date','Revenue']].copy()
    forecasts = []

    for _ in range(horizon):
        next_date = history['Date'].iloc[-1] + pd.offsets.MonthBegin(1)
        values = history['Revenue'].tolist()
        row = pd.DataFrame([{
            'lag_1': values[-1],
            'lag_2': values[-2],
            'lag_3': values[-3],
            'month_num': next_date.month,
            'time_idx': len(history)
        }])
        yhat = max(0.0, float(model.predict(row[features])[0]))
        forecasts.append({'Date': next_date, 'Revenue': yhat, 'Type': 'Forecast'})
        history = pd.concat([history, pd.DataFrame({'Date':[next_date], 'Revenue':[yhat]})], ignore_index=True)

    actual = monthly[['Date','Revenue']].assign(Type='Actual')
    forecast_df = pd.concat([actual, pd.DataFrame(forecasts)], ignore_index=True)
    OUT.mkdir(exist_ok=True)
    forecast_df.to_csv(OUT / 'monthly_forecast.csv', index=False)
    joblib.dump({'model': model, 'features': features, 'mae': mae, 'rmse': rmse}, OUT / 'forecast_model.joblib')

    print(f'MAE: ₹{mae:,.2f}')
    print(f'RMSE: ₹{rmse:,.2f}')
    print(forecast_df.tail(horizon).to_string(index=False))
    return forecast_df, mae, rmse


if __name__ == '__main__':
    train_forecast(6)
