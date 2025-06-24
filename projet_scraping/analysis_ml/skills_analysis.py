import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from collections import Counter
import re

def load_data_with_skills():
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
    
    return df

def extract_skills_from_df(df):
    """Extrait toutes les compétences du DataFrame et compte leur fréquence"""
    all_skills = []
    
    for skills_str in df['Competences'].dropna():
        # Diviser la chaîne de compétences et nettoyer
        skills = [skill.strip() for skill in skills_str.split(',')]
        all_skills.extend(skills)
    
    # Compter les occurrences
    skills_counter = Counter(all_skills)
    
    return skills_counter

def skills_by_sector(df):
    """Analyse les compétences les plus demandées par secteur"""
    sectors = df['Secteur'].unique()
    sector_skills = {}
    
    for sector in sectors:
        sector_df = df[df['Secteur'] == sector]
        sector_skills[sector] = extract_skills_from_df(sector_df)
    
    return sector_skills

def skills_by_experience(df):
    """Analyse les compétences en fonction du niveau d'expérience"""
    # Convertir l'expérience en catégories
    df['Experience_Cat'] = pd.cut(
        pd.to_numeric(df['Experience'], errors='coerce'),
        bins=[0, 2, 5, 10, 100],
        labels=['Junior (0-2 ans)', 'Intermédiaire (3-5 ans)', 'Senior (6-10 ans)', 'Expert (10+ ans)']
    )
    
    exp_categories = df['Experience_Cat'].dropna().unique()
    exp_skills = {}
    
    for exp_cat in exp_categories:
        exp_df = df[df['Experience_Cat'] == exp_cat]
        exp_skills[exp_cat] = extract_skills_from_df(exp_df)
    
    return exp_skills

def skills_evolution(df):
    """Analyse l'évolution des compétences au fil du temps"""
    df['Annee'] = pd.to_datetime(df['Date_De_Publication'], errors='coerce').dt.year
    years = sorted(df['Annee'].dropna().unique())
    
    year_skills = {}
    for year in years:
        year_df = df[df['Annee'] == year]
        year_skills[year] = extract_skills_from_df(year_df)
    
    return year_skills

def run_skills_analysis():
    """Exécute l'analyse des compétences et affiche les résultats dans Streamlit"""
    st.title("🔍 Analyse des Compétences Techniques")
    
    # Charger les données
    df = load_data_with_skills()
    
    # Extraire toutes les compétences
    all_skills_counter = extract_skills_from_df(df)
    
    # Afficher les compétences les plus demandées
    st.header("📊 Compétences les plus demandées")
    
    # Nombre de compétences à afficher
    top_n = st.slider("Nombre de compétences à afficher:", 5, 30, 15)
    
    # Créer un DataFrame pour les compétences les plus demandées
    top_skills = pd.DataFrame({
        'Compétence': [skill for skill, _ in all_skills_counter.most_common(top_n)],
        'Nombre d\'offres': [count for _, count in all_skills_counter.most_common(top_n)]
    })
    
    # Afficher le graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_skills, x='Nombre d\'offres', y='Compétence', palette='viridis', ax=ax)
    ax.set_title(f"Top {top_n} des compétences les plus demandées")
    st.pyplot(fig)
    
    # Analyse par secteur
    st.header("🏢 Compétences par secteur")
    
    sector_skills = skills_by_sector(df)
    selected_sector = st.selectbox("Choisir un secteur:", sorted(sector_skills.keys()))
    
    if selected_sector:
        top_sector_skills = pd.DataFrame({
            'Compétence': [skill for skill, _ in sector_skills[selected_sector].most_common(10)],
            'Nombre d\'offres': [count for _, count in sector_skills[selected_sector].most_common(10)]
        })
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=top_sector_skills, x='Nombre d\'offres', y='Compétence', palette='magma', ax=ax2)
        ax2.set_title(f"Top 10 des compétences pour le secteur: {selected_sector}")
        st.pyplot(fig2)
    
    # Analyse par niveau d'expérience
    st.header("👨‍💼 Compétences par niveau d'expérience")
    
    exp_skills = skills_by_experience(df)
    selected_exp = st.selectbox("Choisir un niveau d'expérience:", sorted(exp_skills.keys()))
    
    if selected_exp:
        top_exp_skills = pd.DataFrame({
            'Compétence': [skill for skill, _ in exp_skills[selected_exp].most_common(10)],
            'Nombre d\'offres': [count for _, count in exp_skills[selected_exp].most_common(10)]
        })
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=top_exp_skills, x='Nombre d\'offres', y='Compétence', palette='rocket', ax=ax3)
        ax3.set_title(f"Top 10 des compétences pour le niveau: {selected_exp}")
        st.pyplot(fig3)
    
    # Évolution des compétences au fil du temps
    st.header("📈 Évolution des compétences")
    
    year_skills = skills_evolution(df)
    years = sorted(year_skills.keys())
    
    if len(years) > 1:
        # Sélectionner les compétences à suivre (top 5 de l'année la plus récente)
        latest_year = max(years)
        skills_to_track = [skill for skill, _ in year_skills[latest_year].most_common(5)]
        
        # Créer un DataFrame pour l'évolution
        evolution_data = []
        for year in years:
            for skill in skills_to_track:
                evolution_data.append({
                    'Année': year,
                    'Compétence': skill,
                    'Nombre d\'offres': year_skills[year].get(skill, 0)
                })
        
        evolution_df = pd.DataFrame(evolution_data)
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=evolution_df, x='Année', y='Nombre d\'offres', hue='Compétence', marker='o', ax=ax4)
        ax4.set_title("Évolution des compétences les plus demandées")
        st.pyplot(fig4)
    else:
        st.info("Pas assez de données temporelles pour analyser l'évolution des compétences.")
    
    # Recommandations pour les filières universitaires
    st.header("🎓 Recommandations pour les filières universitaires")
    
    # Regrouper les compétences par domaine
    domains = {
        'Data Science': ['Python', 'R', 'Machine Learning', 'Deep Learning', 'Statistical Analysis', 'Data Mining'],
        'Développement Web': ['JavaScript', 'HTML', 'CSS', 'React', 'Angular', 'Node.js', 'PHP'],
        'Développement Logiciel': ['Java', 'C#', 'C++', 'OOP', 'Design Patterns', 'Microservices'],
        'Cloud Computing': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform'],
        'Cybersécurité': ['Network Security', 'Penetration Testing', 'SIEM', 'Cryptography', 'Security+'],
        'Business Intelligence': ['SQL', 'Tableau', 'Power BI', 'ETL', 'Data Visualization', 'Excel'],
        'Finance': ['Financial Modeling', 'Financial Analysis', 'Accounting', 'Risk Management']
    }
    
    # Calculer le score pour chaque domaine
    domain_scores = {}
    for domain, skills in domains.items():
        score = sum(all_skills_counter.get(skill, 0) for skill in skills)
        domain_scores[domain] = score
    
    # Créer un DataFrame pour les scores des domaines
    domain_df = pd.DataFrame({
        'Domaine': list(domain_scores.keys()),
        'Score': list(domain_scores.values())
    }).sort_values('Score', ascending=False)
    
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=domain_df, x='Score', y='Domaine', palette='viridis', ax=ax5)
    ax5.set_title("Recommandations de filières universitaires basées sur la demande du marché")
    st.pyplot(fig5)
    
    # Afficher les recommandations textuelles
    st.subheader("Recommandations spécifiques:")
    
    top_domains = domain_df.head(3)['Domaine'].tolist()
    for i, domain in enumerate(top_domains):
        st.markdown(f"**{i+1}. {domain}**")
        
        # Modules recommandés pour chaque domaine
        if domain == 'Data Science':
            st.markdown("""
            - **Modules recommandés**: 
                - Fondamentaux de la Data Science
                - Programmation Python pour l'analyse de données
                - Machine Learning et Deep Learning
                - Statistiques avancées
                - Visualisation de données
            """)
        elif domain == 'Développement Web':
            st.markdown("""
            - **Modules recommandés**: 
                - Développement Front-end (HTML/CSS/JavaScript)
                - Frameworks modernes (React, Angular)
                - Développement Back-end (Node.js, Django)
                - Architecture web et API
                - UX/UI Design
            """)
        elif domain == 'Cloud Computing':
            st.markdown("""
            - **Modules recommandés**: 
                - Fondamentaux du Cloud Computing
                - Services AWS/Azure/GCP
                - Conteneurisation et orchestration (Docker, Kubernetes)
                - Infrastructure as Code
                - DevOps et CI/CD
            """)
        elif domain == 'Cybersécurité':
            st.markdown("""
            - **Modules recommandés**: 
                - Fondamentaux de la cybersécurité
                - Sécurité des réseaux
                - Cryptographie appliquée
                - Analyse des vulnérabilités
                - Réponse aux incidents
            """)
        elif domain == 'Business Intelligence':
            st.markdown("""
            - **Modules recommandés**: 
                - Conception de Data Warehouse
                - Outils de BI (Tableau, Power BI)
                - SQL avancé
                - ETL et intégration de données
                - Analyse décisionnelle
            """)
        elif domain == 'Développement Logiciel':
            st.markdown("""
            - **Modules recommandés**: 
                - Programmation orientée objet
                - Architecture logicielle
                - Design patterns
                - Tests et qualité logicielle
                - Développement Agile
            """)
        elif domain == 'Finance':
            st.markdown("""
            - **Modules recommandés**: 
                - Finance quantitative
                - Analyse financière
                - Gestion des risques
                - Technologies financières (FinTech)
                - Modélisation financière
            """)

if __name__ == "__main__":
    run_skills_analysis()
