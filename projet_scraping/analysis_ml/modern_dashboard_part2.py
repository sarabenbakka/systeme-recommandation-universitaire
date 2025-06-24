# Fonction pour l'analyse du marché
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def show_market_analysis(df):
    st.markdown("<h2 class='section-title'>Analyse du Marché du Travail</h2>", unsafe_allow_html=True)
    
    # Filtres interactifs avec design moderne
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        secteurs = ['Tous'] + sorted(df['Secteur'].unique().tolist())
        secteur = st.selectbox('Secteur', secteurs)
    
    with col2:
        annees = ['Toutes'] + sorted(df['Annee'].dropna().unique().astype(int).astype(str).tolist())
        annee = st.selectbox('Année', annees)
    
    with col3:
        contrats = ['Tous'] + sorted(df['Contrat'].unique().tolist())
        contrat = st.selectbox('Type de Contrat', contrats)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Filtrer les données selon les sélections
    filtered_df = df.copy()
    if secteur != 'Tous':
        filtered_df = filtered_df[filtered_df['Secteur'] == secteur]
    if annee != 'Toutes':
        filtered_df = filtered_df[filtered_df['Annee'] == int(annee)]
    if contrat != 'Tous':
        filtered_df = filtered_df[filtered_df['Contrat'] == contrat]
    
    # Métriques clés avec animation
    st.markdown("<h3 class='subsection-title'>Métriques Clés</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        display_modern_metric(
            "fa-briefcase",
            "Offres d'Emploi",
            f"{len(filtered_df):,}",
            f"+{len(filtered_df) - len(df[df['Annee'] < filtered_df['Annee'].max()])}" if annee == 'Toutes' else None
        )
    
    with col2:
        avg_exp = filtered_df['Experience'].mean()
        display_modern_metric(
            "fa-chart-line",
            "Expérience Moyenne",
            f"{avg_exp:.1f} ans"
        )
    
    with col3:
        top_secteur = filtered_df['Secteur'].value_counts().index[0] if not filtered_df.empty else "N/A"
        display_modern_metric(
            "fa-industry",
            "Secteur Principal",
            top_secteur
        )
    
    with col4:
        top_ville = filtered_df['Ville'].value_counts().index[0] if not filtered_df.empty else "N/A"
        display_modern_metric(
            "fa-map-marker-alt",
            "Ville Principale",
            top_ville
        )
    
    # Visualisations interactives
    st.markdown("<h3 class='subsection-title'>Visualisations</h3>", unsafe_allow_html=True)
    
    # Onglets pour les différentes visualisations
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Secteurs", "📈 Évolution", "🔍 Compétences", "🌍 Géographie"])
    
    with tab1:
        # Distribution des offres par secteur
        secteur_counts = filtered_df['Secteur'].value_counts().reset_index()
        secteur_counts.columns = ['Secteur', 'Nombre']
        secteur_counts = secteur_counts.sort_values('Nombre', ascending=False).head(10)
        
        fig = create_interactive_chart(
            secteur_counts,
            'Secteur',
            'Nombre',
            'Top 10 des Secteurs',
            type='bar'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Évolution temporelle des offres
        if annee == 'Toutes':
            evolution_df = df.groupby('Annee').size().reset_index(name='Nombre')
            fig = create_interactive_chart(
                evolution_df,
                'Annee',
                'Nombre',
                'Évolution des Offres d\'Emploi',
                type='line'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sélectionnez 'Toutes' dans le filtre Année pour voir l'évolution temporelle.")
    
    with tab3:
        # Extraction et visualisation des compétences
        all_skills = []
        for skills_str in filtered_df['Competences'].dropna():
            skills = [skill.strip() for skill in skills_str.split(',')]
            all_skills.extend(skills)
        
        from collections import Counter
        skills_counter = Counter(all_skills)
        top_skills = pd.DataFrame(skills_counter.most_common(10), columns=['Compétence', 'Nombre'])
        
        fig = create_interactive_chart(
            top_skills,
            'Compétence',
            'Nombre',
            'Top 10 des Compétences Demandées',
            type='bar'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # Répartition géographique
        geo_df = filtered_df['Ville'].value_counts().reset_index()
        geo_df.columns = ['Ville', 'Nombre']
        
        fig = create_interactive_chart(
            geo_df.head(10),
            'Ville',
            'Nombre',
            'Top 10 des Villes',
            type='bar'
        )
