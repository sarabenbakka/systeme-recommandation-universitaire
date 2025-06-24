import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import create_custom_theme, load_data
from market_analysis import run_market_analysis
from job_profiles_recommendations import run_job_profiles_recommendations
from university_recommendations import run_university_recommendations

# Configuration de la page
st.set_page_config(
    page_title="Système de Recommandation Universitaire",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Appliquer le thème personnalisé
create_custom_theme()

# Titre principal
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎓 Système de Recommandation Universitaire</h1>
    <p style="font-size: 1.2rem; color: #666;">Basé sur l'analyse du marché du travail IT</p>
</div>
""", unsafe_allow_html=True)

# Barre latérale pour la navigation
st.sidebar.title("Navigation")

# Options de navigation
pages = {
    "Accueil": "home",
    "Analyse du Marché": "market",
    "Recommandation de Profils": "profiles",
    "Recommandation de Filières": "university",
    "À propos": "about"
}

# Sélection de la page
page = st.sidebar.radio("Aller à", list(pages.keys()))

# Informations sur le projet dans la barre latérale
with st.sidebar.expander("Informations sur le projet"):
    st.markdown("""
    **Projet universitaire** visant à créer un système de recommandation basé sur l'analyse du marché du travail IT.
    
    **Données collectées** par web scraping sur plusieurs plateformes:
    - LinkedIn
    - Emploi.ma
    - Rekrute
    - Glassdoor
    
    **Objectifs:**
    - Recommander les filières et modules universitaires
    - Analyser les tendances du marché de l'emploi IT
    - Identifier les compétences techniques demandées
    - Proposer des recommandations basées sur le machine learning
    """)

# Contenu principal en fonction de la page sélectionnée
if pages[page] == "home":
    # Page d'accueil
    st.markdown("""
    <div class="card">
        <h2>Bienvenue dans le Système de Recommandation Universitaire</h2>
        <p>Cette application vous aide à explorer le marché du travail IT et vous propose des recommandations personnalisées pour les filières universitaires et les profils professionnels.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Charger les données
    df = load_data()
    
    # Afficher quelques statistiques clés
    st.markdown('<div class="section-title">📊 Aperçu du marché</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Offres d'emploi analysées</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Secteurs représentés</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(df['Secteur'].nunique()), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Compétences identifiées</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(sum(1 for skills in df['Competences'].dropna() for _ in skills.split(','))), unsafe_allow_html=True)
    
    # Présentation des fonctionnalités
    st.markdown('<div class="section-title">🔍 Fonctionnalités principales</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>📊 Analyse du Marché</h3>
            <p>Explorez les tendances du marché du travail IT, les secteurs qui recrutent, et les compétences les plus demandées.</p>
            <ul>
                <li>Visualisation des offres par secteur</li>
                <li>Évolution temporelle des offres</li>
                <li>Analyse des compétences demandées</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>👨‍💼 Recommandation de Profils</h3>
            <p>Découvrez les profils professionnels qui correspondent à vos compétences et préférences.</p>
            <ul>
                <li>Profils détaillés avec compétences requises</li>
                <li>Parcours éducatifs recommandés</li>
                <li>Évolution de carrière possible</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3>🎓 Recommandation de Filières</h3>
            <p>Trouvez les filières universitaires les mieux adaptées aux tendances du marché et à vos objectifs de carrière.</p>
            <ul>
                <li>Filières alignées avec le marché</li>
                <li>Modules recommandés</li>
                <li>Débouchés professionnels</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Appel à l'action
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
        <p style="font-size: 1.2rem;">Utilisez la barre latérale pour naviguer entre les différentes sections de l'application.</p>
    </div>
    """, unsafe_allow_html=True)

elif pages[page] == "market":
    # Page d'analyse du marché
    run_market_analysis()

elif pages[page] == "profiles":
    # Page de recommandation de profils professionnels
    run_job_profiles_recommendations()

elif pages[page] == "university":
    # Page de recommandation de filières universitaires
    run_university_recommendations()

elif pages[page] == "about":
    # Page À propos
    st.markdown('<div class="section-title">ℹ️ À propos du projet</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>Contexte du projet</h3>
        <p>Ce projet universitaire vise à créer un système de recommandation universitaire basé sur l'analyse du marché du travail, en se concentrant sur le domaine IT et ses sous-domaines.</p>
        <p>Les données ont été collectées par web scraping sur plusieurs plateformes nationales et internationales (LinkedIn, emploi.ma, Rekrute, Glassdoor).</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>Méthodologie</h3>
        <p>Le projet suit une approche en plusieurs étapes :</p>
        <ol>
            <li><strong>Collecte des données</strong> : Web scraping des offres d'emploi</li>
            <li><strong>Nettoyage et fusion</strong> : Harmonisation des données provenant de différentes sources</li>
            <li><strong>Génération des compétences</strong> : Extraction automatique des compétences techniques à partir des titres de poste et secteurs</li>
            <li><strong>Analyse du marché</strong> : Visualisation des tendances et patterns</li>
            <li><strong>Recommandations</strong> : Suggestion de filières universitaires et profils professionnels basée sur l'analyse des données</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>Technologies utilisées</h3>
        <ul>
            <li><strong>Python</strong> : Langage principal pour le traitement des données et l'analyse</li>
            <li><strong>Pandas & NumPy</strong> : Manipulation et analyse des données</li>
            <li><strong>Scikit-learn</strong> : Algorithmes de machine learning (TF-IDF, similarité cosinus, régression)</li>
            <li><strong>Matplotlib & Seaborn</strong> : Visualisation des données</li>
            <li><strong>Streamlit</strong> : Interface web interactive</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>Équipe</h3>
        <p>Ce projet a été réalisé dans le cadre du Master Big Data à l'Université.</p>
    </div>
    """, unsafe_allow_html=True)

# Pied de page
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #eee; color: #666;">
    <p>© 2025 - Système de Recommandation Universitaire - Projet Master Big Data</p>
</div>
""", unsafe_allow_html=True)
