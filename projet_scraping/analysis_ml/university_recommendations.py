import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data, extract_all_skills, display_recommendation_card
from university_recommender import UniversityRecommender

def run_university_recommendations():
    """Exécute les recommandations de filières et modules universitaires"""
    st.markdown('<div class="section-title">🎓 Recommandation de Filières Universitaires</div>', unsafe_allow_html=True)
    
    # Chargement des données
    df = load_data()
    
    # Initialisation du recommandeur universitaire
    uni_recommender = UniversityRecommender()
    
    # Extraire les compétences du marché
    skills_counter = extract_all_skills(df)
    top_market_skills = [skill for skill, _ in skills_counter.most_common(20)]
    
    # Interface utilisateur pour la recommandation
    st.markdown('<div class="subsection-title">Trouvez la filière universitaire idéale</div>', unsafe_allow_html=True)
    
    # Formulaire pour la recommandation personnalisée
    with st.container():
        st.markdown("""
        <div class="card">
            <h3>Personnalisez votre recommandation</h3>
            <p>Sélectionnez vos préférences pour obtenir des recommandations de filières universitaires adaptées à votre profil.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sélection des compétences à développer
            selected_skills = st.multiselect(
                "Compétences que vous souhaitez développer",
                options=sorted(top_market_skills),
                default=top_market_skills[:3] if len(top_market_skills) > 3 else top_market_skills
            )
        
        with col2:
            # Sélection de l'objectif de carrière
            all_profiles = []
            for program in uni_recommender.get_all_programs().values():
                all_profiles.extend(program['career_prospects'])
            
            career_goal = st.selectbox(
                "Objectif de carrière",
                options=sorted(set(all_profiles)),
                index=0
            )
    
    # Bouton pour lancer la recommandation
    if st.button("Obtenir des recommandations de filières", type="primary"):
        # Obtenir les recommandations
        recommended_programs = uni_recommender.recommend_programs(
            skills=selected_skills,
            career_goal=career_goal,
            top_n=3
        )
        
        if recommended_programs:
            st.markdown('<div class="subsection-title">Filières recommandées</div>', unsafe_allow_html=True)
            
            for program_name in recommended_programs:
                program = uni_recommender.get_program_details(program_name)
                
                # Créer des badges pour les compétences développées
                badges = [(skill, True) for skill in program['skills_developed'][:5]]
                
                # Afficher la carte de recommandation
                display_recommendation_card(
                    title=program_name,
                    subtitle=f"Durée: {program['duration']} | Débouchés: {', '.join(program['career_prospects'][:2])}...",
                    content=f"""
                    <p><strong>Description:</strong> {program['description']}</p>
                    <p><strong>Modules principaux:</strong></p>
                    <ul>
                        {''.join([f'<li>{module}</li>' for module in program['modules'][:5]])}
                    </ul>
                    """,
                    badges=badges
                )
        else:
            st.info("Aucune filière ne correspond à vos critères. Essayez de modifier vos sélections.")
    
    # Recommandation basée sur les tendances du marché
    st.markdown('<div class="subsection-title">Filières alignées avec les tendances du marché</div>', unsafe_allow_html=True)
    
    # Créer un dictionnaire des tendances du marché (basé sur la fréquence des compétences)
    market_trends = {skill: count for skill, count in skills_counter.most_common(30)}
    
    # Obtenir les filières les mieux alignées
    market_aligned_programs = uni_recommender.get_market_aligned_programs(market_trends)
    
    for program_name in market_aligned_programs:
        program = uni_recommender.get_program_details(program_name)
        
        # Créer des badges pour les compétences développées qui sont demandées sur le marché
        market_skills = [skill for skill in program['skills_developed'] 
                        if skill in market_trends and market_trends[skill] > skills_counter.most_common(50)[-1][1]]
        badges = [(skill, True) for skill in market_skills[:5]]
        
        # Afficher la carte de recommandation
        display_recommendation_card(
            title=program_name,
            subtitle="Recommandé selon les tendances actuelles du marché",
            content=f"""
            <p><strong>Description:</strong> {program['description']}</p>
            <p><strong>Débouchés:</strong> {', '.join(program['career_prospects'])}</p>
            """,
            badges=badges
        )
    
    # Afficher tous les programmes disponibles
    st.markdown('<div class="subsection-title">Toutes les filières universitaires</div>', unsafe_allow_html=True)
    
    all_programs = uni_recommender.get_all_programs()
    
    # Regrouper les programmes par domaine
    program_domains = {
        "Data & IA": ["Master en Data Science", "Master en Intelligence Artificielle", "Master en Business Intelligence"],
        "Développement": ["Master en Développement Web", "Master en Génie Logiciel"],
        "Infrastructure & Sécurité": ["Master en Cloud Computing", "Master en Cybersécurité"],
        "Finance": ["Master en Finance Quantitative"]
    }
    
    tabs = st.tabs(list(program_domains.keys()))
    
    for i, (domain, programs) in enumerate(program_domains.items()):
        with tabs[i]:
            for program_name in programs:
                if program_name in all_programs:
                    program = uni_recommender.get_program_details(program_name)
                    
                    # Créer un expander pour chaque programme
                    with st.expander(f"{program_name}"):
                        st.markdown(f"**Description:** {program['description']}")
                        
                        # Modules
                        st.markdown("**Modules:**")
                        for module in program['modules']:
                            st.markdown(f"- {module}")
                        
                        # Compétences développées
                        st.markdown("**Compétences développées:**")
                        skills_cols = st.columns(3)
                        for j, skill in enumerate(program['skills_developed']):
                            skills_cols[j % 3].markdown(f"- {skill}")
                        
                        # Débouchés
                        st.markdown("**Débouchés:**")
                        for prospect in program['career_prospects']:
                            st.markdown(f"- {prospect}")
                        
                        # Durée
                        st.markdown(f"**Durée:** {program['duration']}")
    
    # Analyse des compétences développées par filière
    st.markdown('<div class="subsection-title">Analyse des compétences par filière</div>', unsafe_allow_html=True)
    
    # Créer un DataFrame des compétences par filière
    program_skills = {}
    for program_name, program_data in all_programs.items():
        program_skills[program_name] = len(program_data['skills_developed'])
    
    program_skills_df = pd.DataFrame({
        'Filière': list(program_skills.keys()),
        'Nombre de compétences': list(program_skills.values())
    }).sort_values('Nombre de compétences', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=program_skills_df, x='Nombre de compétences', y='Filière', palette='viridis', ax=ax)
    ax.set_title("Nombre de compétences développées par filière universitaire")
    st.pyplot(fig)
    
    # Compétences communes entre filières
    st.markdown('<div class="subsection-title">Compétences transversales</div>', unsafe_allow_html=True)
    
    # Créer un dictionnaire des compétences par filière
    program_skills_dict = {}
    for program_name, program_data in all_programs.items():
        program_skills_dict[program_name] = set(program_data['skills_developed'])
    
    # Trouver les compétences communes
    all_skills_set = set()
    for skills in program_skills_dict.values():
        all_skills_set.update(skills)
    
    common_skills = {}
    for skill in all_skills_set:
        count = sum(1 for skills in program_skills_dict.values() if skill in skills)
        if count > 1:  # La compétence est présente dans au moins 2 filières
            common_skills[skill] = count
    
    # Afficher les compétences les plus transversales
    common_skills_df = pd.DataFrame({
        'Compétence': list(common_skills.keys()),
        'Nombre de filières': list(common_skills.values())
    }).sort_values('Nombre de filières', ascending=False)
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=common_skills_df, x='Nombre de filières', y='Compétence', palette='viridis', ax=ax2)
    ax2.set_title("Compétences transversales (présentes dans plusieurs filières)")
    st.pyplot(fig2)

if __name__ == "__main__":
    from utils import create_custom_theme
    
    # Appliquer le thème personnalisé
    create_custom_theme()
    
    # Exécuter les recommandations universitaires
    run_university_recommendations()
