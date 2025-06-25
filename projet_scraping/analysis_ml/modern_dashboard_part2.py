# Fonction pour l'analyse du marché
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Définition des fonctions nécessaires
def display_modern_metric(icon, value, label, delta=None, color="#4361ee"):
    """Affiche une métrique moderne avec une icône et une valeur"""
    delta_html = f"<div style='color: {'green' if delta and delta.startswith('+') else 'red'}; font-size: 0.8rem;'>{delta}</div>" if delta else ""
    
    st.markdown(f"""
    <div style="background-color: white; border-radius: 10px; padding: 1.2rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-align: center; height: 100%;">
        <i class="fas {icon}" style="font-size: 2rem; color: {color}; margin-bottom: 0.8rem;"></i>
        <div style="font-size: 1.5rem; font-weight: 700; color: {color}; margin-bottom: 0.5rem;">{value}</div>
        <div style="font-size: 0.9rem; color: #64748b; font-weight: 500;">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_interactive_chart(df, x_col, y_col, chart_type="bar", title="", color_col=None):
    """Crée un graphique interactif avec Plotly"""
    if chart_type == "bar":
        fig = px.bar(
            df, 
            x=x_col, 
            y=y_col,
            color=color_col,
            title=title,
            template="plotly_white"
        )
    elif chart_type == "line":
        fig = px.line(
            df, 
            x=x_col, 
            y=y_col,
            color=color_col,
            title=title,
            template="plotly_white"
        )
    elif chart_type == "scatter":
        fig = px.scatter(
            df, 
            x=x_col, 
            y=y_col,
            color=color_col,
            title=title,
            template="plotly_white"
        )
    elif chart_type == "pie":
        fig = px.pie(
            df, 
            names=x_col, 
            values=y_col,
            title=title,
            template="plotly_white"
        )
    
    # Personnaliser la mise en page
    fig.update_layout(
        font=dict(family="Inter, sans-serif"),
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=20, color="#1e293b"),
            x=0.5,
            xanchor="center"
        ),
        margin=dict(l=50, r=50, t=80, b=50),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Inter, sans-serif"
        )
    )
    
    return fig

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
            chart_type='bar',
            title='Top 10 des Secteurs'
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
                chart_type='line',
                title='Évolution des Offres d\'Emploi'
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
            chart_type='bar',
            title='Top 10 des Compétences Demandées'
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
            chart_type='bar',
            title='Top 10 des Villes'
        )
