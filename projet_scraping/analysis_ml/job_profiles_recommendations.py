import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data, extract_all_skills, display_recommendation_card
from job_profiles_recommender import JobProfilesRecommender

def run_job_profiles_recommendations():
    """Exécute les recommandations de profils professionnels"""
    st.markdown('<div class="section-title">👨‍💼 Recommandation de Profils Professionnels</div>', unsafe_allow_html=True)
    
    # Chargement des données
    df = load_data()
    
    # Initialisation du recommandeur de profils
    job_recommender = JobProfilesRecommender()
    
    # Interface utilisateur pour la recommandation
    st.markdown('<div class="subsection-title">Trouvez votre profil professionnel idéal</div>', unsafe_allow_html=True)
    
    # Formulaire pour la recommandation personnalisée
    with st.container():
        st.markdown("""
        <div class="card">
            <h3>Personnalisez votre recommandation</h3>
            <p>Sélectionnez vos préférences pour obtenir des recommandations de profils professionnels adaptées à votre profil.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sélection des compétences
            all_skills = job_recommender.get_all_skills()
            selected_skills = st.multiselect(
                "Sélectionnez vos compétences",
                options=sorted(all_skills),
                default=all_skills[:3] if len(all_skills) > 3 else all_skills
            )
        
        with col2:
            # Sélection du secteur
            sectors = sorted(df['Secteur'].unique())
            selected_sector = st.selectbox(
                "Secteur d'activité préféré",
                options=sectors,
                index=0 if len(sectors) > 0 else 0
            )
            
            # Sélection du niveau d'expérience
            experience_level = st.select_slider(
                "Niveau d'expérience",
                options=["Débutant", "Intermédiaire", "Avancé", "Expert"],
                value="Intermédiaire"
            )
    
    # Bouton pour lancer la recommandation
    if st.button("Obtenir des recommandations de profils", type="primary"):
        # Obtenir les recommandations
        recommended_profiles = job_recommender.recommend_profiles(
            skills=selected_skills,
            sector=selected_sector,
            experience_level=experience_level
        )
        
        if recommended_profiles:
            st.markdown('<div class="subsection-title">Profils recommandés</div>', unsafe_allow_html=True)
            
            for profile_name in recommended_profiles:
                profile = job_recommender.get_profile_details(profile_name)
                
                # Créer des badges pour les compétences
                badges = [(skill, True) for skill in profile.get('skills_required', [])[:5]]
                
                # Afficher la carte de recommandation
                display_recommendation_card(
                    title=profile_name,
                    subtitle=f"Salaire moyen: {profile.get('avg_salary', 'Non spécifié')}",
                    content=f"""
                    <p><strong>Description:</strong> {profile.get('description', 'Non spécifié')}</p>
                    <p><strong>Parcours éducatif recommandé:</strong> {', '.join(profile.get('education', []))}</p>
                    <p><strong>Évolution de carrière:</strong> {', '.join(profile.get('career_path', []))}</p>
                    """,
                    badges=badges
                )
        else:
            st.info("Aucun profil ne correspond à vos critères. Essayez de modifier vos sélections.")
    
    # Afficher tous les profils disponibles
    st.markdown('<div class="subsection-title">Tous les profils professionnels</div>', unsafe_allow_html=True)
    
    # Créer des onglets pour chaque domaine principal et leurs sous-domaines
    all_profiles = job_recommender.get_all_profiles()
    
    # Fonction pour obtenir le secteur principal d'un profil
    def get_main_sector(profile_name):
        profile = job_recommender.get_profile_details(profile_name)
        sectors = profile.get('sector', [])
        if 'Finance' in sectors:
            return 'Finance'
        elif any(s in sectors for s in ['IT', 'Data', 'Développement', 'Cybersécurité', 'Cloud']):
            return 'IT'
        else:
            return 'Autres'
    
    # Fonction pour obtenir le sous-domaine d'un profil
    def get_subdomain(profile_name):
        profile = job_recommender.get_profile_details(profile_name)
        sectors = profile.get('sector', [])
        
        # Sous-domaines Finance
        if 'Finance' in sectors:
            if 'Data' in sectors:
                return 'Finance Quantitative'
            elif 'IT' in sectors:
                return 'Fintech'
            else:
                return 'Finance Traditionnelle'
        
        # Sous-domaines IT
        elif any(s in sectors for s in ['IT', 'Data', 'Développement', 'Cybersécurité', 'Cloud']):
            if 'Data' in sectors:
                return 'Data & Analytics'
            elif 'Développement' in sectors:
                return 'Développement Logiciel'
            elif 'Cybersécurité' in sectors:
                return 'Cybersécurité'
            elif 'Cloud' in sectors:
                return 'Cloud & DevOps'
            else:
                return 'IT Général'
        else:
            return 'Autres'
    
    # Organiser les profils par domaine principal et sous-domaine
    profile_categories = {
        "Finance": {
            "Finance Traditionnelle": [p for p in all_profiles if get_main_sector(p) == 'Finance' and get_subdomain(p) == 'Finance Traditionnelle'],
            "Finance Quantitative": [p for p in all_profiles if get_main_sector(p) == 'Finance' and get_subdomain(p) == 'Finance Quantitative'],
            "Fintech": [p for p in all_profiles if get_main_sector(p) == 'Finance' and get_subdomain(p) == 'Fintech']
        },
        "IT": {
            "Data & Analytics": [p for p in all_profiles if get_main_sector(p) == 'IT' and get_subdomain(p) == 'Data & Analytics'],
            "Développement Logiciel": [p for p in all_profiles if get_main_sector(p) == 'IT' and get_subdomain(p) == 'Développement Logiciel'],
            "Cybersécurité": [p for p in all_profiles if get_main_sector(p) == 'IT' and get_subdomain(p) == 'Cybersécurité'],
            "Cloud & DevOps": [p for p in all_profiles if get_main_sector(p) == 'IT' and get_subdomain(p) == 'Cloud & DevOps'],
            "IT Général": [p for p in all_profiles if get_main_sector(p) == 'IT' and get_subdomain(p) == 'IT Général']
        }
    }
    
    # Créer des onglets pour les domaines principaux
    main_domain_tabs = st.tabs(list(profile_categories.keys()))
    
    # Pour chaque domaine principal
    for i, (main_domain, subdomains) in enumerate(profile_categories.items()):
        with main_domain_tabs[i]:
            # Afficher un en-tête pour le domaine principal
            st.markdown(f"<div class='domain-header'><h3>💼 Domaine: {main_domain}</h3></div>", unsafe_allow_html=True)
            
            # Créer des onglets pour les sous-domaines
            if subdomains:
                subdomain_tabs = st.tabs(list(subdomains.keys()))
                
                # Pour chaque sous-domaine
                for j, (subdomain, profiles) in enumerate(subdomains.items()):
                    with subdomain_tabs[j]:
                        if profiles:
                            # Afficher un en-tête pour le sous-domaine
                            st.markdown(f"<div class='subdomain-header'><h4>📊 Sous-domaine: {subdomain}</h4></div>", unsafe_allow_html=True)
                            
                            # Afficher les profils du sous-domaine
                            for profile_name in profiles:
                                profile = job_recommender.get_profile_details(profile_name)
                                
                                # Créer un expander pour chaque profil
                                with st.expander(f"{profile_name}"):
                                    # Afficher le secteur du profil
                                    sectors = profile.get('sector', [])
                                    st.markdown(f"**Secteur:** {', '.join(sectors)}")
                                    
                                    # Description
                                    st.markdown(f"**Description:** {profile.get('description', 'Non spécifié')}")
                                    
                                    # Compétences requises
                                    st.markdown("**Compétences requises:**")
                                    skills_cols = st.columns(3)
                                    for k, skill in enumerate(profile.get('skills_required', [])):
                                        skills_cols[k % 3].markdown(f"- {skill}")
                                    
                                    # Parcours éducatif
                                    st.markdown(f"**Parcours éducatif recommandé:** {', '.join(profile.get('education', []))}")
                                    
                                    # Évolution de carrière
                                    st.markdown(f"**Évolution de carrière:** {', '.join(profile.get('career_path', []))}")
                                    
                                    # Salaire moyen
                                    st.markdown(f"**Salaire moyen:** {profile.get('avg_salary', 'Non spécifié')}")
                        else:
                            st.info(f"Aucun profil dans le sous-domaine {subdomain}")
            else:
                st.info(f"Aucun sous-domaine défini pour {main_domain}")
    
    # Analyse des compétences par profil
    st.markdown('<div class="subsection-title">Analyse des compétences par profil</div>', unsafe_allow_html=True)
    
    # Créer un DataFrame des compétences par profil
    profile_skills = {}
    for profile_name in all_profiles:
        profile = job_recommender.get_profile_details(profile_name)
        profile_skills[profile_name] = len(profile.get('skills_required', []))
    
    profile_skills_df = pd.DataFrame({
        'Profil': list(profile_skills.keys()),
        'Nombre de compétences': list(profile_skills.values())
    }).sort_values('Nombre de compétences', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=profile_skills_df, x='Nombre de compétences', y='Profil', palette='viridis', ax=ax)
    ax.set_title("Nombre de compétences requises par profil professionnel")
    st.pyplot(fig)
    
    # Compétences communes entre profils
    st.markdown('<div class="subsection-title">Compétences transversales</div>', unsafe_allow_html=True)
    
    # Créer un dictionnaire des compétences par profil
    profile_skills_dict = {}
    for profile_name in all_profiles:
        profile = job_recommender.get_profile_details(profile_name)
        profile_skills_dict[profile_name] = set(profile.get('skills_required', []))
    
    # Trouver les compétences communes
    all_skills_set = set()
    for skills in profile_skills_dict.values():
        all_skills_set.update(skills)
    
    common_skills = {}
    for skill in all_skills_set:
        count = sum(1 for skills in profile_skills_dict.values() if skill in skills)
        if count > 1:  # La compétence est présente dans au moins 2 profils
            common_skills[skill] = count
    
    # Afficher les compétences les plus transversales
    common_skills_df = pd.DataFrame({
        'Compétence': list(common_skills.keys()),
        'Nombre de profils': list(common_skills.values())
    }).sort_values('Nombre de profils', ascending=False).head(15)
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=common_skills_df, x='Nombre de profils', y='Compétence', palette='viridis', ax=ax2)
    ax2.set_title("Top 15 des compétences transversales (présentes dans plusieurs profils)")
    st.pyplot(fig2)

if __name__ == "__main__":
    from utils import create_custom_theme
    
    # Appliquer le thème personnalisé
    create_custom_theme()
    
    # Exécuter les recommandations de profils
    run_job_profiles_recommendations()
