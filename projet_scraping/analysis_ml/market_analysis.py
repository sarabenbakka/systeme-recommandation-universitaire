import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from utils import load_data, extract_all_skills, predict_job_growth, display_metric_card

def run_market_analysis():
    """Exécute l'analyse du marché du travail"""
    st.markdown('<div class="section-title">📊 Analyse du Marché du Travail</div>', unsafe_allow_html=True)
    
    # Chargement des données
    df = load_data()
    
    # Métriques clés
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        display_metric_card(
            "Offres d'emploi", 
            f"{len(df):,}",
            None
        )
    
    with col2:
        top_sector = df['Secteur'].value_counts().index[0]
        display_metric_card(
            "Secteur principal", 
            f"{top_sector}",
            f"{df[df['Secteur'] == top_sector].shape[0]} offres"
        )
    
    with col3:
        avg_exp = df['Experience'].mean()
        display_metric_card(
            "Expérience moyenne", 
            f"{avg_exp:.1f} ans",
            None
        )
    
    with col4:
        skills_counter = extract_all_skills(df)
        top_skill = skills_counter.most_common(1)[0][0]
        display_metric_card(
            "Compétence la plus demandée", 
            f"{top_skill}",
            f"{skills_counter[top_skill]} mentions"
        )
    
    st.markdown('<div class="subsection-title">Répartition des offres par secteur</div>', unsafe_allow_html=True)
    
    # Visualisation des secteurs
    fig, ax = plt.subplots(figsize=(10, 6))
    sector_counts = df['Secteur'].value_counts().head(10)
    sns.barplot(x=sector_counts.values, y=sector_counts.index, palette='viridis', ax=ax)
    ax.set_title("Top 10 des secteurs qui recrutent", fontsize=14)
    ax.set_xlabel("Nombre d'offres")
    st.pyplot(fig)
    
    # Analyse temporelle
    st.markdown('<div class="subsection-title">Évolution des offres d\'emploi</div>', unsafe_allow_html=True)
    
    # Vérifier si nous avons des données temporelles
    if 'Annee' in df.columns and df['Annee'].nunique() > 1:
        # Évolution par année
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        evolution = df.groupby('Annee').size().reset_index(name='Nb_Offres')
        sns.lineplot(data=evolution, x='Annee', y='Nb_Offres', marker='o', linewidth=2, ax=ax2)
        ax2.set_title("Évolution du nombre d'offres d'emploi par année", fontsize=14)
        ax2.set_xlabel("Année")
        ax2.set_ylabel("Nombre d'offres")
        st.pyplot(fig2)
        
        # Évolution par secteur et année
        st.markdown('<div class="subsection-title">Évolution par secteur</div>', unsafe_allow_html=True)
        
        # Sélection du secteur
        sectors = df['Secteur'].unique()
        selected_sector = st.selectbox("Choisir un secteur à analyser", sorted(sectors))
        
        # Prédiction pour ce secteur
        prediction, growth_rate = predict_job_growth(df, selected_sector)
        
        if prediction is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                display_metric_card(
                    f"Prédiction pour 2025", 
                    f"{prediction} offres",
                    None
                )
            
            with col2:
                display_metric_card(
                    "Taux de croissance annuel", 
                    f"{growth_rate:.1f}%",
                    "par an",
                    "normal" if growth_rate > 0 else "inverse"
                )
            
            # Graphique d'évolution pour ce secteur
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            sector_evolution = df[df['Secteur'] == selected_sector].groupby('Annee').size().reset_index(name='Nb_Offres')
            
            # Tracer les données historiques
            sns.lineplot(data=sector_evolution, x='Annee', y='Nb_Offres', marker='o', label='Historique', ax=ax3)
            
            # Ajouter la prédiction
            years = sorted(sector_evolution['Annee'].unique())
            if years:
                last_year = max(years)
                ax3.scatter(2025, prediction, color='red', s=100, label='Prédiction 2025')
                ax3.plot([last_year, 2025], [sector_evolution[sector_evolution['Annee'] == last_year]['Nb_Offres'].values[0], prediction], 
                         'r--', label='Tendance')
            
            ax3.set_title(f"Évolution des offres pour le secteur '{selected_sector}'", fontsize=14)
            ax3.set_xlabel("Année")
            ax3.set_ylabel("Nombre d'offres")
            ax3.legend()
            st.pyplot(fig3)
        else:
            st.info(f"Pas assez de données pour prédire l'évolution du secteur '{selected_sector}'")
    else:
        st.info("Pas assez de données temporelles pour analyser l'évolution des offres d'emploi")
    
    # Analyse des compétences
    st.markdown('<div class="subsection-title">Compétences les plus demandées</div>', unsafe_allow_html=True)
    
    skills_counter = extract_all_skills(df)
    top_skills = pd.DataFrame({
        'Compétence': [skill for skill, _ in skills_counter.most_common(15)],
        'Nombre d\'offres': [count for _, count in skills_counter.most_common(15)]
    })
    
    fig4, ax4 = plt.subplots(figsize=(10, 8))
    sns.barplot(data=top_skills, x='Nombre d\'offres', y='Compétence', palette='viridis', ax=ax4)
    ax4.set_title("Top 15 des compétences les plus demandées", fontsize=14)
    st.pyplot(fig4)
    
    # Analyse des types de contrat
    st.markdown('<div class="subsection-title">Types de contrat</div>', unsafe_allow_html=True)
    
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    contract_counts = df['Contrat'].value_counts()
    sns.barplot(x=contract_counts.values, y=contract_counts.index, palette='viridis', ax=ax5)
    ax5.set_title("Répartition des types de contrat", fontsize=14)
    ax5.set_xlabel("Nombre d'offres")
    st.pyplot(fig5)
    
    # Relation entre expérience et secteur
    st.markdown('<div class="subsection-title">Expérience requise par secteur</div>', unsafe_allow_html=True)
    
    fig6, ax6 = plt.subplots(figsize=(12, 8))
    sns.boxplot(x='Secteur', y='Experience', data=df, palette='viridis', ax=ax6)
    ax6.set_title("Distribution de l'expérience requise par secteur", fontsize=14)
    ax6.set_xlabel("Secteur")
    ax6.set_ylabel("Années d'expérience")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig6)
    
    # Répartition géographique
    if 'Ville' in df.columns:
        st.markdown('<div class="subsection-title">Répartition géographique</div>', unsafe_allow_html=True)
        
        fig7, ax7 = plt.subplots(figsize=(10, 6))
        city_counts = df['Ville'].value_counts().head(10)
        sns.barplot(x=city_counts.values, y=city_counts.index, palette='viridis', ax=ax7)
        ax7.set_title("Top 10 des villes qui recrutent", fontsize=14)
        ax7.set_xlabel("Nombre d'offres")
        st.pyplot(fig7)
    
    # Analyse comparative IT vs Finance
    st.markdown('<div class="section-title">🔍 Analyse comparative IT vs Finance</div>', unsafe_allow_html=True)
    
    # Filtrer les données pour les secteurs IT et Finance
    df_it = df[df['Secteur'].str.contains('IT|Informatique|Digital|Tech', case=False, na=False)]
    df_finance = df[df['Secteur'].str.contains('Finance|Banque|Assurance|Comptabilité', case=False, na=False)]
    
    # Métriques comparatives
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card-title">Secteur IT</div>', unsafe_allow_html=True)
        display_metric_card(
            "Nombre d'offres", 
            f"{len(df_it):,}",
            f"{len(df_it)/len(df)*100:.1f}% du total"
        )
        
        if 'Experience' in df.columns:
            display_metric_card(
                "Expérience moyenne", 
                f"{df_it['Experience'].mean():.1f} ans",
                None
            )
        
        # Compétences IT les plus demandées
        skills_it = extract_all_skills(df_it)
        top_skills_it = pd.DataFrame({
            'Compétence': [skill for skill, _ in skills_it.most_common(5)],
            'Nombre': [count for _, count in skills_it.most_common(5)]
        })
        
        st.markdown('<div class="card-subtitle">Top 5 compétences IT</div>', unsafe_allow_html=True)
        st.table(top_skills_it)
    
    with col2:
        st.markdown('<div class="card-title">Secteur Finance</div>', unsafe_allow_html=True)
        display_metric_card(
            "Nombre d'offres", 
            f"{len(df_finance):,}",
            f"{len(df_finance)/len(df)*100:.1f}% du total"
        )
        
        if 'Experience' in df.columns:
            display_metric_card(
                "Expérience moyenne", 
                f"{df_finance['Experience'].mean():.1f} ans",
                None
            )
        
        # Compétences Finance les plus demandées
        skills_finance = extract_all_skills(df_finance)
        top_skills_finance = pd.DataFrame({
            'Compétence': [skill for skill, _ in skills_finance.most_common(5)],
            'Nombre': [count for _, count in skills_finance.most_common(5)]
        })
        
        st.markdown('<div class="card-subtitle">Top 5 compétences Finance</div>', unsafe_allow_html=True)
        st.table(top_skills_finance)
    
    # Comparaison des salaires si disponibles
    if 'Salaire' in df.columns:
        st.markdown('<div class="subsection-title">Comparaison des salaires</div>', unsafe_allow_html=True)
        
        fig8, ax8 = plt.subplots(figsize=(10, 6))
        data_to_plot = [df_it['Salaire'].dropna(), df_finance['Salaire'].dropna()]
        ax8.boxplot(data_to_plot, labels=['IT', 'Finance'])
        ax8.set_title("Comparaison des salaires entre IT et Finance", fontsize=14)
        ax8.set_ylabel("Salaire")
        st.pyplot(fig8)
    
    # Évolution temporelle comparative
    if 'Annee' in df.columns and df['Annee'].nunique() > 1:
        st.markdown('<div class="subsection-title">Évolution comparative</div>', unsafe_allow_html=True)
        
        fig9, ax9 = plt.subplots(figsize=(10, 6))
        
        # Évolution IT
        evolution_it = df_it.groupby('Annee').size().reset_index(name='Nb_Offres')
        sns.lineplot(data=evolution_it, x='Annee', y='Nb_Offres', marker='o', linewidth=2, label='IT', ax=ax9)
        
        # Évolution Finance
        evolution_finance = df_finance.groupby('Annee').size().reset_index(name='Nb_Offres')
        sns.lineplot(data=evolution_finance, x='Annee', y='Nb_Offres', marker='s', linewidth=2, label='Finance', ax=ax9)
        
        ax9.set_title("Évolution comparative des offres IT vs Finance", fontsize=14)
        ax9.set_xlabel("Année")
        ax9.set_ylabel("Nombre d'offres")
        ax9.legend()
        st.pyplot(fig9)
    
    # Compétences hybrides IT-Finance
    st.markdown('<div class="subsection-title">Compétences hybrides IT-Finance</div>', unsafe_allow_html=True)
    
    # Identifier les compétences communes aux deux secteurs
    common_skills = set(skills_it.keys()).intersection(set(skills_finance.keys()))
    
    if common_skills:
        hybrid_skills = pd.DataFrame({
            'Compétence': list(common_skills),
            'Mentions IT': [skills_it[skill] for skill in common_skills],
            'Mentions Finance': [skills_finance[skill] for skill in common_skills],
            'Total': [skills_it[skill] + skills_finance[skill] for skill in common_skills]
        })
        
        # Trier par total décroissant
        hybrid_skills = hybrid_skills.sort_values('Total', ascending=False).head(10)
        
        fig10, ax10 = plt.subplots(figsize=(12, 8))
        
        # Créer un graphique à barres groupées
        x = np.arange(len(hybrid_skills))
        width = 0.35
        
        ax10.bar(x - width/2, hybrid_skills['Mentions IT'], width, label='IT', color='#2C7BB6')
        ax10.bar(x + width/2, hybrid_skills['Mentions Finance'], width, label='Finance', color='#D7191C')
        
        ax10.set_title('Top 10 des compétences hybrides IT-Finance', fontsize=14)
        ax10.set_xticks(x)
        ax10.set_xticklabels(hybrid_skills['Compétence'], rotation=45, ha='right')
        ax10.legend()
        
        plt.tight_layout()
        st.pyplot(fig10)
        
        st.markdown('''
        <div class="insight-card">
            <h3>💡 Insight</h3>
            <p>Les compétences hybrides IT-Finance sont particulièrement recherchées dans les domaines de la FinTech, 
            de l'analyse de données financières et de la gestion des risques. Ces profils à double compétence 
            bénéficient généralement d'une prime salariale et d'une meilleure employabilité.</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.info("Aucune compétence commune identifiée entre les secteurs IT et Finance dans les données actuelles.")
        
    # Opportunités de carrière hybrides
    st.markdown('<div class="subsection-title">Opportunités de carrière hybrides</div>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="info-card">
        <h3>Profils à l'interface IT-Finance</h3>
        <ul>
            <li><strong>Quant Developer</strong> - Développeur spécialisé dans les algorithmes financiers</li>
            <li><strong>Data Scientist Finance</strong> - Expert en analyse de données financières</li>
            <li><strong>Risk Technology Specialist</strong> - Spécialiste des technologies de gestion des risques</li>
            <li><strong>FinTech Product Manager</strong> - Gestionnaire de produits financiers technologiques</li>
            <li><strong>Blockchain Developer for Finance</strong> - Développeur blockchain pour applications financières</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    from utils import create_custom_theme
    
    # Appliquer le thème personnalisé
    create_custom_theme()
    
    # Exécuter l'analyse du marché
    run_market_analysis()
