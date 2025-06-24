import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
from datetime import datetime
import time

# Import des modules personnalisés
from utils import load_data, create_custom_theme, display_metric_card, display_recommendation_card
from job_profiles_recommender import recommend_profiles
from university_recommender import UniversityRecommender

# Importer les fonctions des autres fichiers
from modern_dashboard import create_animated_header, display_modern_metric, display_profile_card, create_interactive_chart
from modern_dashboard_part2 import show_market_analysis
from modern_dashboard_part3 import show_job_profiles_recommendations, show_university_recommendations

# Configuration de la page
st.set_page_config(
    page_title="Système de Recommandation Universitaire",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Appliquer le thème personnalisé
create_custom_theme()

# Fonction pour l'analyse comparative IT vs Finance
def show_comparative_analysis(df):
    st.markdown("<h2 class='section-title'>Analyse Comparative IT vs Finance</h2>", unsafe_allow_html=True)
    
    # Filtrer les données pour IT et Finance
    it_keywords = ['IT', 'Informatique', 'Développement', 'Software', 'Web', 'Data', 'Cloud', 'Cybersécurité']
    finance_keywords = ['Finance', 'Banque', 'Comptabilité', 'Audit', 'Assurance', 'Trading', 'Investment']
    
    # Fonction pour vérifier si une offre appartient à un secteur
    def is_in_sector(row, keywords):
        secteur = str(row['Secteur']).lower()
        poste = str(row['Poste']).lower() if 'Poste' in row else ''
        description = str(row['Description_Poste']).lower() if 'Description_Poste' in row else ''
        
        for keyword in keywords:
            if keyword.lower() in secteur or keyword.lower() in poste or keyword.lower() in description:
                return True
        return False
    
    # Créer des masques pour les secteurs
    df['is_it'] = df.apply(lambda row: is_in_sector(row, it_keywords), axis=1)
    df['is_finance'] = df.apply(lambda row: is_in_sector(row, finance_keywords), axis=1)
    
    # Filtrer les dataframes
    it_df = df[df['is_it']]
    finance_df = df[df['is_finance']]
    
    # Métriques comparatives
    st.markdown("<h3 class='subsection-title'>Métriques Comparatives</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card' style='height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #4361ee;'>Secteur IT</h4>", unsafe_allow_html=True)
        
        it_metrics_col1, it_metrics_col2 = st.columns(2)
        
        with it_metrics_col1:
            display_modern_metric(
                "fa-laptop-code",
                "Offres d'Emploi",
                f"{len(it_df):,}"
            )
        
        with it_metrics_col2:
            it_avg_exp = it_df['Experience'].mean()
            display_modern_metric(
                "fa-chart-line",
                "Expérience Moyenne",
                f"{it_avg_exp:.1f} ans"
            )
        
        # Top compétences IT
        all_it_skills = []
        for skills_str in it_df['Competences'].dropna():
            skills = [skill.strip() for skill in skills_str.split(',')]
            all_it_skills.extend(skills)
        
        from collections import Counter
        it_skills_counter = Counter(all_it_skills)
        top_it_skills = pd.DataFrame(it_skills_counter.most_common(5), columns=['Compétence', 'Nombre'])
        
        st.markdown("<h5 style='margin-top: 20px;'>Top 5 Compétences IT</h5>", unsafe_allow_html=True)
        fig = create_interactive_chart(
            top_it_skills,
            'Compétence',
            'Nombre',
            '',
            type='bar'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card' style='height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #4cc9f0;'>Secteur Finance</h4>", unsafe_allow_html=True)
        
        finance_metrics_col1, finance_metrics_col2 = st.columns(2)
        
        with finance_metrics_col1:
            display_modern_metric(
                "fa-chart-pie",
                "Offres d'Emploi",
                f"{len(finance_df):,}"
            )
        
        with finance_metrics_col2:
            finance_avg_exp = finance_df['Experience'].mean()
            display_modern_metric(
                "fa-chart-line",
                "Expérience Moyenne",
                f"{finance_avg_exp:.1f} ans"
            )
        
        # Top compétences Finance
        all_finance_skills = []
        for skills_str in finance_df['Competences'].dropna():
            skills = [skill.strip() for skill in skills_str.split(',')]
            all_finance_skills.extend(skills)
        
        finance_skills_counter = Counter(all_finance_skills)
        top_finance_skills = pd.DataFrame(finance_skills_counter.most_common(5), columns=['Compétence', 'Nombre'])
        
        st.markdown("<h5 style='margin-top: 20px;'>Top 5 Compétences Finance</h5>", unsafe_allow_html=True)
        fig = create_interactive_chart(
            top_finance_skills,
            'Compétence',
            'Nombre',
            '',
            type='bar'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Évolution temporelle comparative
    st.markdown("<h3 class='subsection-title'>Évolution Temporelle Comparative</h3>", unsafe_allow_html=True)
    
    # Grouper par année et secteur
    it_evolution = it_df.groupby('Annee').size().reset_index(name='Nombre')
    it_evolution['Secteur'] = 'IT'
    
    finance_evolution = finance_df.groupby('Annee').size().reset_index(name='Nombre')
    finance_evolution['Secteur'] = 'Finance'
    
    # Combiner les données
    combined_evolution = pd.concat([it_evolution, finance_evolution])
    
    # Créer le graphique
    fig = create_interactive_chart(
        combined_evolution,
        'Annee',
        'Nombre',
        'Évolution des Offres d\'Emploi par Secteur',
        color='Secteur',
        type='line'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Compétences hybrides
    st.markdown("<h3 class='subsection-title'>Compétences Hybrides IT-Finance</h3>", unsafe_allow_html=True)
    
    # Identifier les compétences communes
    it_skills_set = set([skill for skill, _ in it_skills_counter.most_common(20)])
    finance_skills_set = set([skill for skill, _ in finance_skills_counter.most_common(20)])
    
    common_skills = it_skills_set.intersection(finance_skills_set)
    
    if common_skills:
        # Créer un dataframe pour les compétences communes
        common_skills_data = []
        for skill in common_skills:
            common_skills_data.append({
                'Compétence': skill,
                'IT': it_skills_counter[skill],
                'Finance': finance_skills_counter[skill]
            })
        
        common_skills_df = pd.DataFrame(common_skills_data)
        common_skills_df = common_skills_df.sort_values(by=['IT', 'Finance'], ascending=False)
        
        # Créer un graphique pour comparer les compétences communes
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=common_skills_df['Compétence'],
            y=common_skills_df['IT'],
            name='IT',
            marker_color='#4361ee'
        ))
        
        fig.add_trace(go.Bar(
            x=common_skills_df['Compétence'],
            y=common_skills_df['Finance'],
            name='Finance',
            marker_color='#4cc9f0'
        ))
        
        fig.update_layout(
            title='Compétences Communes aux Secteurs IT et Finance',
            xaxis_title='Compétence',
            yaxis_title='Nombre d\'offres',
            barmode='group',
            template='plotly_white',
            font=dict(family="Inter, sans-serif"),
            title_font=dict(size=20, family="Inter, sans-serif", color="#1e293b"),
            legend_title_font=dict(size=14),
            legend_font=dict(size=12),
            hoverlabel=dict(font_size=14, font_family="Inter, sans-serif")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insight sur les compétences hybrides
        st.markdown("""
        <div class="card">
            <h4>🔍 Insight: L'importance des compétences hybrides IT-Finance</h4>
            <p>Les professionnels possédant des compétences à l'intersection de l'IT et de la Finance sont de plus en plus recherchés. 
            Ces profils hybrides combinent expertise technique et connaissance du secteur financier, les rendant particulièrement 
            précieux dans des domaines comme la FinTech, l'analyse quantitative et la gestion des risques.</p>
            
            <p>Les filières universitaires qui développent cette double compétence, comme le Master en Finance Quantitative ou 
            le Master en Data Science pour la Finance, offrent d'excellentes perspectives d'emploi.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Pas assez de données pour identifier des compétences hybrides entre IT et Finance.")

# Fonction principale
def main():
    # Sidebar pour la navigation
    st.sidebar.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=80)
    st.sidebar.title("Navigation")
    
    # Menu de navigation
    pages = {
        "🏠 Accueil": "home",
        "📊 Analyse du Marché": "market",
        "🔄 Analyse Comparative IT-Finance": "comparative",
        "👨‍💼 Recommandations de Profils": "profiles",
        "🎓 Recommandations Universitaires": "university"
    }
    
    selection = st.sidebar.radio("Aller à", list(pages.keys()))
    
    # Charger les données
    df = load_data()
    
    # Afficher la page sélectionnée
    if pages[selection] == "home":
        # Page d'accueil
        create_animated_header(
            "Système de Recommandation Universitaire",
            "Analyse du marché du travail et recommandations personnalisées pour votre parcours académique"
        )
        
        st.markdown("""
        <div class="card">
            <h3>👋 Bienvenue dans votre assistant d'orientation professionnelle et académique</h3>
            <p>Ce système vous aide à prendre des décisions éclairées sur votre parcours universitaire en fonction des tendances du marché du travail et de vos objectifs de carrière.</p>
            
            <h4>Fonctionnalités principales:</h4>
            <ul>
                <li>Analyse détaillée du marché du travail dans les secteurs IT et Finance</li>
                <li>Comparaison des tendances entre les secteurs</li>
                <li>Recommandations de profils professionnels adaptés à vos compétences</li>
                <li>Suggestions de filières universitaires alignées avec vos objectifs</li>
            </ul>
            
            <p>Utilisez le menu de navigation à gauche pour explorer les différentes sections.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Métriques clés sur la page d'accueil
        st.markdown("<h3 class='subsection-title'>Aperçu du Marché</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            display_modern_metric(
                "fa-briefcase",
                "Offres d'Emploi",
                f"{len(df):,}"
            )
        
        with col2:
            sectors_count = len(df['Secteur'].unique())
            display_modern_metric(
                "fa-industry",
                "Secteurs",
                f"{sectors_count}"
            )
        
        with col3:
            avg_exp = df['Experience'].mean()
            display_modern_metric(
                "fa-chart-line",
                "Expérience Moyenne",
                f"{avg_exp:.1f} ans"
            )
        
        with col4:
            cities_count = len(df['Ville'].unique())
            display_modern_metric(
                "fa-map-marker-alt",
                "Villes",
                f"{cities_count}"
            )
        
        # Aperçu des secteurs
        st.markdown("<h3 class='subsection-title'>Répartition par Secteur</h3>", unsafe_allow_html=True)
        
        secteur_counts = df['Secteur'].value_counts().reset_index()
        secteur_counts.columns = ['Secteur', 'Nombre']
        secteur_counts = secteur_counts.sort_values('Nombre', ascending=False).head(5)
        
        fig = create_interactive_chart(
            secteur_counts,
            'Secteur',
            'Nombre',
            'Top 5 des Secteurs',
            type='bar'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    elif pages[selection] == "market":
        # Page d'analyse du marché
        show_market_analysis(df)
        
    elif pages[selection] == "comparative":
        # Page d'analyse comparative
        show_comparative_analysis(df)
        
    elif pages[selection] == "profiles":
        # Page de recommandations de profils
        show_job_profiles_recommendations()
        
    elif pages[selection] == "university":
        # Page de recommandations universitaires
        show_university_recommendations()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #eee;">
        <p style="color: #64748b; font-size: 0.8rem;">
            © 2025 Système de Recommandation Universitaire | Développé avec ❤️ et Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
