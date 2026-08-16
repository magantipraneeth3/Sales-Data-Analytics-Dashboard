"""Order-level sales prediction model.

Predicts Revenue from quantity, price, cost, discount and categorical business fields.
"""
from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'processed' / 'clean_sales_data.csv'
OUT = ROOT / 'outputs'

FEATURES = [
    'Quantity_Sold','Unit_Cost','Unit_Price','Discount',
    'Sales_Rep','Region','Product_Category','Customer_Type',
    'Payment_Method','Sales_Channel'
]
TARGET = 'Revenue'


def train():
    df = pd.read_csv(DATA)
    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    numeric = ['Quantity_Sold','Unit_Cost','Unit_Price','Discount']
    categorical = [c for c in FEATURES if c not in numeric]

    pre = ColumnTransformer([
        ('num', 'passthrough', numeric),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical)
    ])

    pipe = Pipeline([
        ('preprocessor', pre),
        ('model', RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42, n_jobs=-1))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)

    metrics = {
        'MAE': float(mean_absolute_error(y_test, pred)),
        'RMSE': float(mean_squared_error(y_test, pred) ** 0.5),
        'R2': float(r2_score(y_test, pred))
    }

    OUT.mkdir(exist_ok=True)
    joblib.dump({'pipeline': pipe, 'features': FEATURES, 'metrics': metrics}, OUT / 'sales_prediction_model.joblib')
    pd.DataFrame([metrics]).to_csv(OUT / 'sales_prediction_metrics.csv', index=False)

    print(metrics)
    return pipe, metrics


if __name__ == '__main__':
    train()
