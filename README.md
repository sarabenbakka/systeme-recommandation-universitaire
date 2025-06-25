# Système de Recommandation Universitaire

## Description
Ce projet est un système de recommandation universitaire basé sur l'analyse du marché du travail dans les secteurs IT et Finance. Il utilise des données collectées par web scraping pour analyser les tendances du marché et proposer des recommandations personnalisées de filières universitaires et de profils professionnels.

## Fonctionnalités
- **Analyse du marché du travail** : Visualisations interactives des tendances du marché dans les secteurs IT et Finance
- **Analyse comparative** : Comparaison des compétences et opportunités entre les secteurs IT et Finance
- **Recommandations de profils professionnels** : Suggestions de carrières basées sur les compétences et préférences de l'utilisateur
- **Recommandations de filières universitaires** : Propositions de parcours académiques alignés avec les objectifs de carrière

## Technologies utilisées
- **Python** : Langage principal pour le traitement des données et l'analyse
- **Streamlit** : Interface web interactive
- **Pandas & NumPy** : Manipulation et analyse des données
- **Plotly** : Visualisations interactives
- **Matplotlib & Seaborn** : Visualisations statiques

## Structure du projet
- `analysis_ml/` : Dossier principal contenant les modules d'analyse et de recommandation
  - `modern_dashboard_main.py` : Application principale avec navigation
  - `modern_dashboard_part2.py` : Module d'analyse du marché
  - `modern_dashboard_part3.py` : Module de recommandations
  - `job_profiles_recommender.py` : Recommandation de profils professionnels
  - `university_recommender.py` : Recommandation de filières universitaires
  - `utils.py` : Fonctions utilitaires
  - `style.css` : Styles personnalisés pour l'interface

## Installation et exécution
1. Cloner ce dépôt
2. Installer les dépendances : `pip install -r requirements.txt`
3. Lancer l'application :

   ```bash
   # Si vous êtes dans le répertoire racine du projet
   streamlit run projet_scraping/analysis_ml/main_dashboard.py
   
   # OU si vous préférez utiliser le dashboard moderne
   streamlit run projet_scraping/analysis_ml/modern_dashboard.py
   ```

   **Note importante :** Assurez-vous d'exécuter la commande depuis le bon répertoire. Si vous êtes déjà dans le dossier `projet_scraping`, utilisez :
   ```bash
   streamlit run projet_scraping/analysis_ml/main_dashboard.py
   ```
   
   Si vous êtes dans le sous-dossier `analysis_ml`, utilisez simplement :
   ```bash
   streamlit run main_dashboard.py
   ```

## Captures d'écran
![Dashboard](screenshots/dashboard.png)
*À venir*

## Auteurs
Projet réalisé dans le cadre du Master Big Data à l'Université.
