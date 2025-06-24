import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from collections import Counter
import re
import numpy as np

def load_data():
    """Charge les données avec les compétences générées"""
    try:
        # Essayer d'abord de charger les données enrichies avec compétences
        path = r"C:\Users\ThinkPad\OneDrive\Desktop\Master Big Data\S1 MASTER\BASE DE DONNEES ORACLE\PROJECTS\projet_scraping\projet_scraping\output\final_jobs_data_with_skills.csv"
        df = pd.read_csv(path)
        if 'Competences' not in df.columns:
            raise FileNotFoundError("Le fichier existe mais ne contient pas de compétences")
    except FileNotFoundError:
        # Si le fichier n'existe pas, générer les compétences
        print("Génération des compétences en cours...")
        from skills_generator import SkillsGenerator
        
        # Charger les données originales
        path_orig = r"C:\Users\ThinkPad\OneDrive\Desktop\Master Big Data\S1 MASTER\BASE DE DONNEES ORACLE\PROJECTS\projet_scraping\projet_scraping\output\final_jobs_data_cleaned.csv"
        df = pd.read_csv(path_orig)
        
        # Générer les compétences
        skills_gen = SkillsGenerator()
        df = skills_gen.enrich_dataframe(df)
        
        # Sauvegarder pour utilisation future
        df.to_csv(path, index=False)
        print("Compétences générées et sauvegardées.")
    
    # Prétraitement des données
    df['Experience'] = pd.to_numeric(df['Experience'], errors='coerce')
    df['Date_De_Publication'] = pd.to_datetime(df['Date_De_Publication'], errors='coerce')
    df['Annee'] = df['Date_De_Publication'].dt.year
    
    return df

def extract_all_skills(df):
    """Extrait toutes les compétences du DataFrame et compte leur fréquence"""
    all_skills = []
    
    for skills_str in df['Competences'].dropna():
        # Diviser la chaîne de compétences et nettoyer
        skills = [skill.strip() for skill in skills_str.split(',')]
        all_skills.extend(skills)
    
    # Compter les occurrences
    skills_counter = Counter(all_skills)
    
    return skills_counter

def get_market_trends(df):
    """Analyse les tendances du marché basées sur les données d'offres d'emploi"""
    # Tendances par secteur
    sector_counts = df['Secteur'].value_counts().head(5).to_dict()
    
    # Tendances par compétence
    skills_counter = extract_all_skills(df)
    top_skills = {skill: count for skill, count in skills_counter.most_common(10)}
    
    # Tendances par type de contrat
    contract_counts = df['Contrat'].value_counts().to_dict()
    
    # Tendances par niveau d'études
    education_counts = df['Niveau_Etude'].value_counts().to_dict()
    
    return {
        'sectors': sector_counts,
        'skills': top_skills,
        'contracts': contract_counts,
        'education': education_counts
    }

def predict_job_growth(df, sector, target_year=2025):
    """Prédit la croissance des offres d'emploi pour un secteur donné"""
    from sklearn.linear_model import LinearRegression
    
    # Regrouper les données par année et secteur
    annonces_par_annee = df.groupby(['Annee', 'Secteur']).size().reset_index(name='Nb_Annonces')
    
    # Filtrer pour le secteur spécifié
    data_sec = annonces_par_annee[annonces_par_annee['Secteur'] == sector]
    
    # Vérifier s'il y a assez de données
    if len(data_sec) < 2:
        return None, None
    
    # Préparer les données pour la régression
    X = data_sec[['Annee']]
    y = data_sec['Nb_Annonces']
    
    # Créer et entraîner le modèle
    model = LinearRegression()
    model.fit(X, y)
    
    # Prédire pour l'année cible
    prediction = int(model.predict([[target_year]])[0])
    
    # Calculer le taux de croissance
    years = sorted(data_sec['Annee'].unique())
    if len(years) >= 2:
        first_year = years[0]
        last_year = years[-1]
        first_count = data_sec[data_sec['Annee'] == first_year]['Nb_Annonces'].values[0]
        last_count = data_sec[data_sec['Annee'] == last_year]['Nb_Annonces'].values[0]
        
        # Calculer le taux de croissance annuel moyen
        if first_count > 0 and last_year > first_year:
            growth_rate = ((last_count / first_count) ** (1 / (last_year - first_year)) - 1) * 100
        else:
            growth_rate = 0
    else:
        growth_rate = 0
    
    return prediction, growth_rate

def create_custom_theme():
    """Crée un thème personnalisé moderne pour l'application"""
    # Charger le CSS externe pour un design plus moderne
    import os
    import pathlib
    
    # Chemin vers le fichier CSS
    css_path = pathlib.Path(__file__).parent / "style.css"
    
    # Vérifier si le fichier existe
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        # Fallback si le fichier CSS n'existe pas
        primary_color = "#4361ee"
        secondary_color = "#4cc9f0"
        background_color = "#f8fafc"
        text_color = "#1e293b"
        
        st.markdown(f"""
        <style>
        /* Variables de couleurs */
        :root {{
          --primary: {primary_color};
          --secondary: {secondary_color};
          --light: {background_color};
          --dark: {text_color};
          --gradient-primary: linear-gradient(135deg, {primary_color}, #3a0ca3);
          --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
          --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
          --radius: 12px;
        }}
        
        /* Styles globaux */
        .stApp {{
          font-family: 'Inter', sans-serif;
          background-color: var(--light);
          color: var(--dark);
        }}
        
        /* Boutons */
        .stButton > button {{
          background: var(--gradient-primary);
          color: white;
          border-radius: var(--radius);
          padding: 0.75rem 1.5rem;
          border: none;
          font-weight: 600;
          transition: all 0.3s ease;
          box-shadow: var(--shadow-sm);
        }}
        
        .stButton > button:hover {{
          transform: translateY(-2px);
          box-shadow: var(--shadow-md);
        }}
        
        /* Cartes métriques */
        .metric-card {{
          background-color: white;
          border-radius: var(--radius);
          padding: 1.5rem;
          box-shadow: var(--shadow-sm);
          text-align: center;
          transition: all 0.3s ease;
          border: 1px solid rgba(0, 0, 0, 0.05);
        }}
        
        .metric-card:hover {{
          transform: translateY(-5px);
          box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .metric-value {{
          font-size: 2.5rem;
          font-weight: 700;
          color: var(--primary);
          background: var(--gradient-primary);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }}
        
        .metric-label {{
          font-size: 1rem;
          color: #64748b;
          font-weight: 500;
        }}
        
        /* Cartes de recommandation */
        .recommendation-card {{
          background-color: white;
          border-radius: var(--radius);
          padding: 1.5rem;
          box-shadow: var(--shadow-sm);
          margin-bottom: 1.5rem;
          transition: all 0.3s ease;
          border: 1px solid rgba(0, 0, 0, 0.05);
          position: relative;
        }}
        
        .recommendation-card::before {{
          content: '';
          position: absolute;
          left: 0;
          top: 0;
          height: 100%;
          width: 5px;
          background: var(--gradient-primary);
        }}
        
        .recommendation-card:hover {{
          transform: translateY(-5px);
          box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        }}
        
        /* Titres */
        .section-title {{
          font-size: 1.8rem;
          font-weight: 800;
          margin-bottom: 1.5rem;
          color: var(--dark);
          position: relative;
          padding-bottom: 0.75rem;
        }}
        
        .section-title::after {{
          content: '';
          position: absolute;
          left: 0;
          bottom: 0;
          height: 4px;
          width: 60px;
          background: var(--gradient-primary);
          border-radius: 2px;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    # Ajouter les polices Google
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    # Ajouter Font Awesome pour les icônes
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)

def display_metric_card(title, value, delta=None, delta_color="normal"):
    """Affiche une carte métrique avec un titre, une valeur et une variation"""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        {f'<div style="color: {"green" if delta_color == "normal" else "red"}; font-size: 0.9rem;">{delta}</div>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

def display_recommendation_card(title, subtitle, content, badges=None):
    """Affiche une carte de recommandation avec titre, sous-titre, contenu et badges"""
    badges_html = ""
    if badges:
        for badge, is_primary in badges:
            badge_class = "badge-primary" if is_primary else "badge"
            badges_html += f'<span class="{badge_class}">{badge}</span>'
    
    st.markdown(f"""
    <div class="recommendation-card">
        <div class="recommendation-title">{title}</div>
        <div class="recommendation-subtitle">{subtitle}</div>
        <div>{badges_html}</div>
        <div class="recommendation-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)
