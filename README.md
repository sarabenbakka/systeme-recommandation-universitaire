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
![image](https://github.com/user-attachments/assets/efab3c03-f561-4228-8cde-e246cc91f283)

![image](https://github.com/user-attachments/assets/3a9e44b9-91e8-4bcd-ad3a-6f8ce3f134e4)

![image](https://github.com/user-attachments/assets/c41e68bd-5466-492f-b1bb-b272a6e979d5)

![image](https://github.com/user-attachments/assets/58e33cb8-fa96-45c4-8b4e-385763dd4368)

![image](https://github.com/user-attachments/assets/128e5238-343b-4972-b427-02f476d50443)

![image](https://github.com/user-attachments/assets/fc2453a7-d09f-40df-bde3-d5a40949266f)

![image](https://github.com/user-attachments/assets/dccb66b2-4989-4d4e-8758-b9712707489e)

![image](https://github.com/user-attachments/assets/bc89b5bd-a432-47de-b1b5-3da56d04266f)

![image](https://github.com/user-attachments/assets/b41c30bf-7dd7-4f2c-a131-2a697c608d66)










## Auteurs
Ce projet a été réalisé dans le cadre du projet du module base de données Oracle au Master Big Data.

Les membres de l'équipe sont :

Aya BELHOU
Sara BENBAKKA
Ouissal ELHOR
Oumayma ESSABRI
