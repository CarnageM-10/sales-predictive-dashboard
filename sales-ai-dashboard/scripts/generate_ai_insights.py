from groq import Groq
from dotenv import load_dotenv
import os, json, pandas as pd

load_dotenv()

print("🤖 Génération des insights IA avec Groq (Llama 3)...")

# Chargement des données
df = pd.read_csv("data/processed/cleaned_sales.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

total_revenue      = df['Total Amount'].sum()
total_transactions = len(df)
avg_order_value    = total_revenue / total_transactions
top_category       = df.groupby('Product Category')['Total Amount'].sum().idxmax()
top_gender         = df.groupby('Gender')['Total Amount'].sum().idxmax()
monthly_sales      = df.groupby('Year_Month')['Total Amount'].sum().reset_index()

data_summary = f"""
Données de ventes retail ({total_transactions} transactions) :
- Chiffre d'affaires total   : {total_revenue:,.2f} €
- Panier moyen               : {avg_order_value:.2f} €
- Catégorie la plus rentable : {top_category}
- Genre dominant             : {top_gender}
- Période : {df['Date'].min().strftime('%d/%m/%Y')} → {df['Date'].max().strftime('%d/%m/%Y')}

Ventes mensuelles :
{monthly_sales.to_string(index=False)}
"""

prompt = f"""
Analyse ces données de ventes retail et génère exactement 5 insights avec recommandations concrètes.

Réponds UNIQUEMENT avec du JSON valide, sans markdown, sans backticks, sans texte avant ou après :
{{
  "insights": [
    {{"category": "global", "title": "Titre court", "text": "Explication + recommandation actionnable"}},
    {{"category": "catégorie", "title": "Titre court", "text": "Explication + recommandation actionnable"}}
  ]
}}

Données :
{data_summary}
"""

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": "Tu es un analyste business senior spécialisé en retail. Réponds toujours en français. Réponds UNIQUEMENT avec du JSON valide, sans markdown ni backticks."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.7,
    max_tokens=1024
)

raw = response.choices[0].message.content.strip()

# Nettoyer si backticks présents malgré tout
if "```" in raw:
    raw = raw.split("```")[1]
    if raw.startswith("json"):
        raw = raw[4:]
raw = raw.strip()

insights = json.loads(raw)["insights"]
insights_df = pd.DataFrame(insights)
insights_df.to_csv("data/processed/ai_insights.csv", index=False)

print("✅ Insights générés avec succès !")
print("   Fichier : data/processed/ai_insights.csv\n")
print(insights_df[['category', 'title']].to_string(index=False))