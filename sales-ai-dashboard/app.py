from flask import Flask, render_template, jsonify
from flask.json.provider import DefaultJSONProvider
import pandas as pd
import json
import numpy as np
import os
import subprocess
from pathlib import Path
from datetime import datetime


# ── Fix Flask 2.2+ : numpy int64/float64 non sérialisables ──────────────────
class NumpyJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)
# ────────────────────────────────────────────────────────────────────────────


app = Flask(__name__)
app.json_provider_class = NumpyJSONProvider
app.json = NumpyJSONProvider(app)

BASE_DIR = Path(__file__).resolve().parent


def load_sales_data():
    path = BASE_DIR / "data" / "processed" / "cleaned_sales.csv"
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Year_Month'] = df['Date'].dt.strftime('%Y-%m')
    return df


def load_insights():
    path = BASE_DIR / "data" / "processed" / "ai_insights.csv"
    if not path.exists():
        return []
    df = pd.read_csv(path)
    return df.to_dict(orient='records')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/kpis')
def api_kpis():
    df = load_sales_data()

    total_revenue      = round(df['Total Amount'].sum(), 2)
    total_transactions = len(df)
    avg_basket         = round(df['Total Amount'].mean(), 2)
    top_category       = df.groupby('Product Category')['Total Amount'].sum().idxmax()

    # Croissance MoM
    monthly = df.groupby('Year_Month')['Total Amount'].sum().sort_index()
    mom_pct = 0
    if len(monthly) >= 2:
        last  = monthly.iloc[-1]
        prev  = monthly.iloc[-2]
        mom_pct = round((last - prev) / prev * 100, 1) if prev else 0

    return jsonify({
        'total_revenue'     : total_revenue,
        'total_transactions': total_transactions,
        'avg_basket'        : avg_basket,
        'top_category'      : top_category,
        'mom_growth'        : mom_pct,
        'date_min'          : str(df['Date'].min().date()),
        'date_max'          : str(df['Date'].max().date()),
    })


@app.route('/api/charts')
def api_charts():
    df = load_sales_data()

    # Ventes par catégorie
    by_cat = (
        df.groupby('Product Category')['Total Amount']
          .sum()
          .sort_values(ascending=False)
          .reset_index()
    )

    # Évolution mensuelle
    by_month = (
        df.groupby('Year_Month')['Total Amount']
          .sum()
          .reset_index()
          .sort_values('Year_Month')
    )

    # Ventes par genre
    by_gender = (
        df.groupby('Gender')['Total Amount']
          .sum()
          .reset_index()
    )

    # Top 5 produits
    top5 = (
        df.groupby('Product Category')['Total Amount']
          .sum()
          .sort_values(ascending=False)
          .head(5)
          .reset_index()
    )

    return jsonify({
        'by_category': {
            'labels': by_cat['Product Category'].tolist(),
            'values': by_cat['Total Amount'].round(2).tolist(),
        },
        'by_month': {
            'labels': by_month['Year_Month'].tolist(),
            'values': by_month['Total Amount'].round(2).tolist(),
        },
        'by_gender': {
            'labels': by_gender['Gender'].tolist(),
            'values': by_gender['Total Amount'].round(2).tolist(),
        },
        'top5': {
            'labels': top5['Product Category'].tolist(),
            'values': top5['Total Amount'].round(2).tolist(),
        },
    })


@app.route('/api/insights')
def api_insights():
    return jsonify(load_insights())


@app.route('/api/refresh', methods=['POST'])
def api_refresh():
    try:
        script = BASE_DIR / "scripts" / "generate_ai_insights.py"
        result = subprocess.run(
            ['python', str(script)],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return jsonify({'status': 'ok', 'message': 'Insights régénérés avec succès'})
        else:
            return jsonify({'status': 'error', 'message': result.stderr}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
