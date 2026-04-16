# Dashboard Ventes Qlik Sense + IA Générative

Projet : Dashboard interactif Qlik Sense qui analyse les ventes e-commerce et utilise ChatGPT pour générer automatiquement des insights et recommandations business.

## Fonctionnalités
- Nettoyage et préparation des données (Python)
- Visualisations interactives dans Qlik Sense
- KPI + tendances
- Section "Insights IA" avec recommandations automatiques (GPT)

## Comment lancer le pipeline
```bash
pip install -r requirements.txt
cp .env.example .env          # ← remplis ta clé OpenAI
python scripts/prepare_data.py
python scripts/generate_ai_insights.py