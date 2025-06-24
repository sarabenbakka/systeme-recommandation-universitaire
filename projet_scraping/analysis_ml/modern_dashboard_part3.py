import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from job_profiles_recommender import recommend_profiles, get_profile_details
from university_recommender import UniversityRecommender

# Fonction pour les recommandations de profils professionnels
def show_job_profiles_recommendations():
    st.markdown("<h2 class='section-title'>Recommandations de Profils Professionnels</h2>", unsafe_allow_html=True)
    
    # Interface utilisateur pour les entrées
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        user_skills = st.text_area("Vos compétences (séparées par des virgules)", 
                                  placeholder="Ex: Python, Data Analysis, Finance")
    
    with col2:
        sectors = ["IT", "Finance", "Les deux"]
        selected_sector = st.selectbox("Secteur d'intérêt", sectors)
        experience = st.slider("Années d'expérience", 0, 15, 3)
    
    submit_button = st.button("Obtenir des recommandations", key="job_profiles_button")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Traitement et affichage des recommandations
    if submit_button and user_skills:
        skills_list = [skill.strip() for skill in user_skills.split(',')]
        
        # Mapping du secteur sélectionné
        sector_mapping = {
            "IT": "IT",
            "Finance": "Finance",
            "Les deux": None  # None pour ne pas filtrer par secteur
        }
        
        # Animation de chargement
        with st.spinner("Analyse de votre profil en cours..."):
            time.sleep(1)  # Simuler un traitement
            
            # Obtenir les recommandations
            recommended_profiles = recommend_profiles(
                skills=skills_list, 
                sector=sector_mapping[selected_sector], 
                experience=experience
            )
        
        # Afficher les résultats
        st.markdown("<h3 class='subsection-title'>Profils recommandés pour vous</h3>", unsafe_allow_html=True)
        
        if recommended_profiles:
            for i, (profile_name, score) in enumerate(recommended_profiles):
                # Créer des badges pour le secteur
                from job_profiles_recommender import job_profiles
                profile_data = job_profiles.get(profile_name, {})
                sector = profile_data.get('sector', ['Non spécifié'])
                
                badges = []
                for s in sector:
                    is_primary = (s == "IT" and selected_sector in ["IT", "Les deux"]) or \
                                (s == "Finance" and selected_sector in ["Finance", "Les deux"])
                    badges.append((s, is_primary))
                
                # Afficher la carte de profil
                display_profile_card(
                    title=profile_name,
                    description=profile_data.get('description', 'Aucune description disponible'),
                    skills=profile_data.get('skills', []),
                    badges=badges
                )
        else:
            st.warning("Aucun profil correspondant trouvé. Essayez d'autres compétences ou critères.")

# Fonction pour les recommandations de filières universitaires
def show_university_recommendations():
    st.markdown("<h2 class='section-title'>Recommandations de Filières Universitaires</h2>", unsafe_allow_html=True)
    
    # Initialiser le recommandeur
    recommender = UniversityRecommender()
    
    # Interface utilisateur pour les entrées
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        user_skills = st.text_area("Vos compétences (séparées par des virgules)", 
                                  placeholder="Ex: Python, Machine Learning, Finance", key="uni_skills")
    
    with col2:
        career_goals = ["Data Scientist", "Développeur Full Stack", "Analyste Financier", 
                       "Risk Manager", "Ingénieur Cloud", "Analyste Cybersécurité", "Autre"]
        career_goal = st.selectbox("Objectif de carrière", career_goals)
        if career_goal == "Autre":
            career_goal = st.text_input("Précisez votre objectif de carrière")
    
    submit_button = st.button("Obtenir des recommandations", key="university_button")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Traitement et affichage des recommandations
    if submit_button:
        skills_list = [skill.strip() for skill in user_skills.split(',')] if user_skills else None
        
        # Animation de chargement
        with st.spinner("Analyse de votre profil académique en cours..."):
            time.sleep(1)  # Simuler un traitement
            
            # Obtenir les recommandations
            recommended_programs = recommender.recommend_programs(
                skills=skills_list, 
                career_goal=career_goal, 
                top_n=5
            )
        
        # Afficher les résultats
        st.markdown("<h3 class='subsection-title'>Filières recommandées pour vous</h3>", unsafe_allow_html=True)
        
        if recommended_programs:
            for program in recommended_programs:
                program_details = recommender.get_program_details(program)
                
                # Créer des badges pour les perspectives de carrière
                badges = []
                for prospect in program_details.get('career_prospects', [])[:2]:
                    is_primary = career_goal.lower() in prospect.lower()
                    badges.append((prospect, is_primary))
                
                # Afficher la carte de recommandation
                st.markdown(f"""
                <div class="recommendation-card">
                    <div class="recommendation-title">{program}</div>
                    <div class="recommendation-subtitle">{program_details.get('duration', '2 ans')} | {len(program_details.get('modules', []))} modules</div>
                    <div class="recommendation-content">{program_details.get('description', 'Aucune description disponible')}</div>
                    <div class="recommendation-subtitle" style="margin-top: 10px;">Modules clés:</div>
                    <div>{"<br>".join([f"• {module}" for module in program_details.get('modules', [])[:3]])}</div>
                    <div class="recommendation-subtitle" style="margin-top: 10px;">Compétences développées:</div>
                    <div>
                        {"".join([f'<span class="badge">{skill}</span>' for skill in program_details.get('skills_developed', [])[:5]])}
                    </div>
                    <div style="margin-top: 10px;">
                        {"".join([f'<span class="badge-primary" style="margin-right: 5px;">{badge}</span>' if is_primary else f'<span class="badge" style="margin-right: 5px;">{badge}</span>' for badge, is_primary in badges])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Aucune filière correspondante trouvée. Essayez d'autres compétences ou objectifs de carrière.")
