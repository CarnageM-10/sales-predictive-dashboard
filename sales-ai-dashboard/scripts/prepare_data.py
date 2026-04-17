import pandas as pd

print("🔄 Préparation des données...")

# Chargement du fichier avec tes vraies colonnes
df = pd.read_csv("data/raw/sales_data.csv")

# Nettoyage et conversion
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')   # Conversion date

# Création de colonnes utiles pour Qlik
df['Year_Month'] = df['Date'].dt.strftime('%Y-%m')
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day_of_Week'] = df['Date'].dt.day_name()

# Calcul du Total Amount si jamais il manque (sécurité)
if 'Total Amount' not in df.columns:
    df['Total Amount'] = df['Quantity'] * df['Price per Unit']

# Suppression des lignes avec dates invalides
df = df.dropna(subset=['Date'])

# Sauvegarde du fichier nettoyé
df.to_csv("data/processed/cleaned_sales.csv", index=False)

print("✅ Données nettoyées et sauvegardées dans data/processed/cleaned_sales.csv")
print(f"   {len(df)} lignes | Période : {df['Date'].min().date()} → {df['Date'].max().date()}")
print(f"   Colonnes disponibles : {list(df.columns)}")