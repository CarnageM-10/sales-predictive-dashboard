import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///sales.db")

df = pd.read_csv("../data/processed/cleaned_sales.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Year_Month'] = df['Date'].dt.strftime('%Y-%m')
df.to_sql("sales", engine, if_exists="replace", index=False)

print("✅ sales.db créé avec succès !")