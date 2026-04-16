import pandas as pd
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

print("🤖 Génération des insights IA...")

# Chargement des données nettoyées
df = pd.read_csv("data/processed/cleaned_sales.csv")

# Calcul des KPI rapides
total_sales = df['sales_amount'].sum()
total_units = df['units_sold'].sum()
top_product = df.groupby('product')['sales_amount'].sum().idxmax()
top_region = df.groupby('region')['sales_amount'].sum().idxmax()

# Résumé par mois
monthly = df.groupby('year_month')['sales_amount'].sum().reset_index()

# Création du prompt
data_summary = f"""
Données de ventes (2024) :
- CA total : {total_sales:,.0f} €
- Unités vendues : {total_units}
- Produit le plus vendu : {top_product}
- Région la plus performante : {top_region}
- Évolution mensuelle : {monthly.to_string(index=False)}
"""

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Tu es un analyste business senior. Réponds toujours en français, de manière claire et actionnable."},
        {"role": "user", "content": f"""
Analyse ces données de ventes et génère 5 insights concrets + recommandations business.
Réponds UNIQUEMENT en JSON valide avec cette structure :
{{
  "insights": [
    {{"category": "global", "title": "...", "text": "..."}},
    {{"category": "produit", "title": "...", "text": "..."}},
    ...
  ]
}}
Données :
{data_summary}
"""}
    ],
    response_format={"type": "json_object"}
)

# Parsing et sauvegarde
insights = json.loads(response.choices[0].message.content)["insights"]
insights_df = pd.DataFrame(insights)

insights_df.to_csv("data/processed/ai_insights.csv", index=False)
print("✅ Insights IA générés et sauvegardés dans data/processed/ai_insights.csv")
print(insights_df[['category', 'title']])