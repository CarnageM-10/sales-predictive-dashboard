import pandas as pd
from datetime import datetime

print("🔄 Préparation des données...")

# Chargement
df = pd.read_csv("data/raw/sales_data.csv")

# Nettoyage
df['date'] = pd.to_datetime(df['date'])
df['sales_amount'] = df['sales_amount'].astype(float)
df['units_sold'] = df['units_sold'].astype(int)

# Ajout de colonnes utiles pour Qlik
df['year_month'] = df['date'].dt.strftime('%Y-%m')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# Sauvegarde
df.to_csv("data/processed/cleaned_sales.csv", index=False)
print("✅ Données nettoyées sauvegardées dans data/processed/cleaned_sales.csv")
print(f"   {len(df)} lignes | {df['date'].min().date()} → {df['date'].max().date()}")