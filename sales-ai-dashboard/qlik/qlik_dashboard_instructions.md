# Comment créer le dashboard Qlik Sense

1. Ouvre Qlik Sense (Desktop ou Cloud)
2. Crée une nouvelle app → "Sales AI Dashboard"
3. Charge les deux fichiers :
   - data/processed/cleaned_sales.csv
   - data/processed/ai_insights.csv
4. Crée les visuels :
   - KPI : CA total, Unités, Top produit
   - Graphiques : Barres (ventes par produit), Carte (par région), Ligne (évolution temporelle)
   - Filtres : Date, Produit, Région
5. Section "Insights IA" :
   - Ajoute une table ou un objet texte avec les colonnes "title" + "text" de ai_insights.csv
6. Ajoute un titre "Recommandations IA générées par ChatGPT"

Tu as maintenant un dashboard complet avec partie IA automatique !