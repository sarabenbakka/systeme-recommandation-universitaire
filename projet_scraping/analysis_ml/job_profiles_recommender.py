import pandas as pd
import numpy as np
from collections import Counter
import re

# Variable globale pour stocker l'instance du recommandeur
_recommender_instance = None

# Variable globale pour les profils
job_profiles = {}

class JobProfilesRecommender:
    def __init__(self):
        # Définition des profils professionnels avec leurs compétences requises
        self.job_profiles = {
            # Profils Data
            'Data Analyst': {
                'description': 'Spécialiste de l\'analyse de données qui transforme les données brutes en insights exploitables pour les décisions d\'affaires.',
                'skills_required': ['SQL', 'Excel', 'Tableau/Power BI', 'Python/R', 'Statistiques', 'Data Visualization', 'Business Intelligence'],
                'education': ['Licence en informatique/statistiques', 'Master en Data Science/Analytics'],
                'career_path': ['Junior Data Analyst', 'Data Analyst', 'Senior Data Analyst', 'Data Analytics Manager', 'Head of Analytics'],
                'avg_salary': '45,000€ - 65,000€',
                'sector': ['IT', 'Data']
            },
            'Data Scientist': {
                'description': 'Expert en analyse avancée qui utilise des algorithmes de machine learning pour extraire des connaissances et faire des prédictions.',
                'skills_required': ['Python', 'R', 'Machine Learning', 'Deep Learning', 'SQL', 'Statistiques avancées', 'NLP', 'Big Data'],
                'education': ['Master en Data Science/IA', 'Doctorat en informatique/mathématiques'],
                'career_path': ['Junior Data Scientist', 'Data Scientist', 'Senior Data Scientist', 'Lead Data Scientist', 'Chief Data Scientist'],
                'avg_salary': '55,000€ - 85,000€',
                'sector': ['IT', 'Data']
            },
            'Data Engineer': {
                'description': 'Spécialiste qui conçoit et maintient l\'architecture de données et les pipelines pour assurer la disponibilité des données.',
                'skills_required': ['SQL', 'Python', 'Spark', 'Hadoop', 'ETL', 'Cloud (AWS/Azure/GCP)', 'Docker/Kubernetes', 'NoSQL'],
                'education': ['Master en informatique/génie logiciel', 'Formation spécialisée en Big Data'],
                'career_path': ['Junior Data Engineer', 'Data Engineer', 'Senior Data Engineer', 'Data Architect', 'Chief Data Officer'],
                'avg_salary': '50,000€ - 75,000€',
                'sector': ['IT', 'Data']
            },
            
            # Profils Développement
            'Développeur Full Stack': {
                'description': 'Développeur polyvalent capable de travailler sur le front-end et le back-end des applications web.',
                'skills_required': ['JavaScript', 'HTML/CSS', 'React/Angular/Vue', 'Node.js/Django/Laravel', 'SQL', 'Git', 'REST API', 'Docker'],
                'education': ['Licence/Master en informatique', 'Formation développeur web'],
                'career_path': ['Junior Developer', 'Full Stack Developer', 'Senior Developer', 'Tech Lead', 'CTO'],
                'avg_salary': '45,000€ - 70,000€',
                'sector': ['IT', 'Développement']
            },
            'Développeur Backend': {
                'description': 'Spécialiste du développement côté serveur, des API et des bases de données.',
                'skills_required': ['Java/Python/C#/.NET', 'SQL/NoSQL', 'API Design', 'Cloud Services', 'Microservices', 'Docker/Kubernetes'],
                'education': ['Licence/Master en informatique', 'Formation spécialisée backend'],
                'career_path': ['Junior Backend Developer', 'Backend Developer', 'Senior Backend Developer', 'Backend Architect', 'Tech Lead'],
                'avg_salary': '45,000€ - 70,000€',
                'sector': ['IT', 'Développement']
            },
            'Développeur Frontend': {
                'description': 'Expert en interfaces utilisateur et expérience utilisateur pour les applications web et mobiles.',
                'skills_required': ['HTML/CSS', 'JavaScript', 'React/Angular/Vue', 'UI/UX Design', 'Responsive Design', 'SASS/LESS', 'Testing'],
                'education': ['Licence en informatique', 'Formation développeur frontend'],
                'career_path': ['Junior Frontend Developer', 'Frontend Developer', 'Senior Frontend Developer', 'UI/UX Lead', 'Frontend Architect'],
                'sector': ['IT', 'Développement']
            },
            
            # Profils Finance
            'Analyste Financier': {
                'description': 'Spécialiste qui analyse les données financières pour évaluer la performance et les perspectives d\'une entreprise ou d\'un secteur.',
                'skills_required': ['Analyse financière', 'Excel avancé', 'Modélisation financière', 'Comptabilité', 'SQL', 'Bloomberg/Reuters', 'Power BI'],
                'education': ['Master en finance/comptabilité', 'CFA (Chartered Financial Analyst)'],
                'career_path': ['Analyste Junior', 'Analyste Financier', 'Analyste Senior', 'Responsable Analyse Financière', 'Directeur Financier'],
                'avg_salary': '45,000€ - 70,000€',
                'sector': ['Finance']
            },
            'Risk Manager': {
                'description': 'Expert qui identifie, évalue et atténue les risques financiers et opérationnels d\'une organisation.',
                'skills_required': ['Gestion des risques', 'Modélisation statistique', 'VaR', 'Réglementation financière', 'Python/R', 'Excel avancé', 'Stress Testing'],
                'education': ['Master en finance/gestion des risques', 'FRM (Financial Risk Manager)', 'PRM (Professional Risk Manager)'],
                'career_path': ['Analyste des risques', 'Risk Manager', 'Senior Risk Manager', 'Head of Risk', 'Chief Risk Officer'],
                'avg_salary': '55,000€ - 90,000€',
                'sector': ['Finance']
            },
            'Quant Analyst': {
                'description': 'Spécialiste qui développe des modèles mathématiques et statistiques pour l\'analyse financière et la prise de décision.',
                'skills_required': ['Mathématiques avancées', 'Statistiques', 'Python/R/C++', 'Machine Learning', 'Algorithmes financiers', 'Pricing d\'options', 'Séries temporelles'],
                'education': ['Master/PhD en mathématiques/physique/finance quantitative'],
                'career_path': ['Junior Quant', 'Quant Analyst', 'Senior Quant', 'Quant Researcher', 'Head of Quantitative Research'],
                'avg_salary': '65,000€ - 120,000€',
                'sector': ['Finance', 'Data']
            },
            'Conseiller en Investissement': {
                'description': 'Professionnel qui conseille les clients sur les stratégies d\'investissement et la gestion de patrimoine.',
                'skills_required': ['Connaissance des marchés financiers', 'Planification financière', 'Gestion de portefeuille', 'Réglementation financière', 'Communication client', 'CRM'],
                'education': ['Master en finance/gestion de patrimoine', 'Certification AMF/CIF'],
                'career_path': ['Conseiller Junior', 'Conseiller en Investissement', 'Conseiller Senior', 'Responsable d\'équipe', 'Directeur de la Gestion Privée'],
                'avg_salary': '40,000€ - 80,000€',
                'sector': ['Finance']
            },
            'Analyste Crédit': {
                'description': 'Spécialiste qui évalue la solvabilité des emprunteurs et le risque de crédit pour les institutions financières.',
                'skills_required': ['Analyse financière', 'Évaluation du risque de crédit', 'Modélisation de scoring', 'Réglementation bancaire', 'Excel avancé', 'SQL'],
                'education': ['Master en finance/banque', 'Formation en analyse de crédit'],
                'career_path': ['Analyste Crédit Junior', 'Analyste Crédit', 'Analyste Crédit Senior', 'Responsable Crédit', 'Directeur des Risques de Crédit'],
                'avg_salary': '42,000€ - 65,000€',
                'sector': ['Finance']
            },
            'Fintech Product Manager': {
                'description': 'Responsable du développement et de la gestion de produits financiers innovants basés sur la technologie.',
                'skills_required': ['Gestion de produit', 'Finance', 'UX/UI', 'Agile/Scrum', 'API bancaires', 'Réglementation fintech', 'Analyse de données'],
                'education': ['Master en finance/technologie/gestion de produit', 'Formation en fintech'],
                'career_path': ['Product Owner', 'Product Manager', 'Senior Product Manager', 'Head of Product', 'Chief Product Officer'],
                'avg_salary': '55,000€ - 95,000€',
                'sector': ['Finance', 'IT']
            },
            
            # Profils Cybersécurité
            'Analyste en Cybersécurité': {
                'description': 'Spécialiste qui surveille, détecte et répond aux menaces de sécurité informatique.',
                'skills_required': ['Network Security', 'SIEM', 'Threat Intelligence', 'Incident Response', 'Security Controls', 'Risk Assessment'],
                'education': ['Master en cybersécurité/sécurité informatique', 'Certifications (CISSP, Security+, CEH)'],
                'career_path': ['Security Analyst', 'Senior Security Analyst', 'Security Engineer', 'Security Architect', 'CISO'],
                'avg_salary': '50,000€ - 75,000€',
                'sector': ['IT', 'Cybersécurité']
            },
            'Pentester': {
                'description': 'Expert qui teste la sécurité des systèmes en simulant des attaques pour identifier les vulnérabilités.',
                'skills_required': ['Penetration Testing', 'Ethical Hacking', 'Network Security', 'Web Application Security', 'Scripting', 'Social Engineering'],
                'education': ['Formation en cybersécurité', 'Certifications (OSCP, CEH, GPEN)'],
                'career_path': ['Junior Pentester', 'Penetration Tester', 'Senior Pentester', 'Red Team Lead', 'Security Consultant'],
                'avg_salary': '45,000€ - 80,000€',
                'sector': ['IT', 'Cybersécurité']
            },
            
            # Profils Cloud & DevOps
            'Ingénieur DevOps': {
                'description': 'Spécialiste qui combine le développement et les opérations IT pour optimiser le cycle de vie des applications.',
                'skills_required': ['Docker', 'Kubernetes', 'CI/CD', 'Infrastructure as Code', 'Cloud (AWS/Azure/GCP)', 'Monitoring', 'Linux'],
                'education': ['Master en informatique', 'Certifications cloud (AWS, Azure, GCP)'],
                'career_path': ['DevOps Engineer', 'Senior DevOps Engineer', 'DevOps Architect', 'Head of DevOps', 'CTO'],
                'avg_salary': '55,000€ - 80,000€',
                'sector': ['IT', 'Cloud']
            },
            'Architecte Cloud': {
                'description': 'Expert qui conçoit et implémente des solutions d\'infrastructure cloud robustes et évolutives.',
                'skills_required': ['AWS/Azure/GCP', 'Infrastructure as Code', 'Networking', 'Security', 'Microservices', 'Serverless', 'Cost Optimization'],
                'education': ['Master en informatique', 'Certifications avancées cloud'],
                'career_path': ['Cloud Engineer', 'Senior Cloud Engineer', 'Cloud Architect', 'Enterprise Architect', 'CTO'],
                'avg_salary': '65,000€ - 90,000€',
                'sector': ['IT', 'Cloud']
            },
            
            # Profils Finance & IT
            'Analyste Financier IT': {
                'description': 'Spécialiste qui combine expertise financière et compétences IT pour analyser les données financières.',
                'skills_required': ['Financial Analysis', 'Excel avancé', 'SQL', 'BI Tools', 'ERP Systems', 'Modélisation financière', 'Python/R'],
                'education': ['Master en finance/économie avec spécialisation IT', 'Formation en analyse de données'],
                'career_path': ['Financial Analyst', 'Senior Financial Analyst', 'Finance Manager', 'Finance Director', 'CFO'],
                'avg_salary': '50,000€ - 75,000€',
                'sector': ['Finance', 'IT', 'Data']
            },
            'Consultant FinTech': {
                'description': 'Expert qui conseille sur l\'implémentation de solutions technologiques dans le secteur financier.',
                'skills_required': ['Finance Knowledge', 'Banking Systems', 'Payment Solutions', 'Blockchain', 'Regulatory Compliance', 'Project Management'],
                'education': ['Master en finance/informatique', 'MBA avec spécialisation FinTech'],
                'career_path': ['FinTech Consultant', 'Senior Consultant', 'Manager', 'Partner', 'FinTech Entrepreneur'],
                'avg_salary': '60,000€ - 90,000€',
                'sector': ['Finance', 'IT']
            }
        }
    
    def get_all_profiles(self):
        """Retourne tous les profils professionnels disponibles"""
        return self.job_profiles
    
    def get_profile_details(self, profile_name):
        """Retourne les détails d'un profil professionnel spécifique"""
        return self.job_profiles.get(profile_name, None)
    
    def recommend_profiles(self, skills=None, sector=None, experience_level=None, top_n=3):
        """Recommande des profils professionnels basés sur les compétences, le secteur et l'expérience"""
        scores = {}
        
        for profile_name, profile_data in self.job_profiles.items():
            score = 0
            
            # Score basé sur les compétences
            if skills:
                skills_list = [skill.lower() for skill in skills]
                profile_skills = [skill.lower() for skill in profile_data['skills_required']]
                
                # Calculer l'intersection des compétences
                common_skills = set(skills_list).intersection(set(profile_skills))
                score += len(common_skills) * 2  # Pondération plus élevée pour les compétences
            
            # Score basé sur le secteur
            if sector:
                sector_lower = sector.lower()
                # Vérifier si le secteur est dans la liste des secteurs du profil
                if 'sector' in profile_data and any(s.lower() == sector_lower for s in profile_data['sector']):
                    score += 3  # Pondération élevée pour correspondance exacte du secteur
                # Vérifier si le secteur est mentionné dans la description ou le nom du profil
                elif sector_lower in profile_name.lower() or sector_lower in profile_data['description'].lower():
                    score += 1
            
            # Score basé sur le niveau d'expérience
            if experience_level:
                exp_level = experience_level.lower()
                if exp_level == 'junior' and 'junior' in ' '.join(profile_data['career_path']).lower():
                    score += 1
                elif exp_level == 'senior' and 'senior' in ' '.join(profile_data['career_path']).lower():
                    score += 1
                elif exp_level == 'manager' and any(role in ' '.join(profile_data['career_path']).lower() for role in ['manager', 'lead', 'head', 'chief']):
                    score += 1
            
            scores[profile_name] = score
        
        # Trier les profils par score et prendre les top_n
        sorted_profiles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_profiles = [profile for profile, score in sorted_profiles[:top_n] if score > 0]
        
        # Si aucun profil n'a un score positif, retourner les 3 profils les plus populaires
        if not top_profiles:
            top_profiles = list(self.job_profiles.keys())[:top_n]
        
        return top_profiles
    
    def get_required_skills_for_sector(self, sector):
        """Retourne les compétences les plus demandées pour un secteur spécifique"""
        all_skills = []
        
        for profile_name, profile_data in self.job_profiles.items():
            if sector.lower() in profile_name.lower() or sector.lower() in profile_data['description'].lower():
                all_skills.extend(profile_data['skills_required'])
        
        # Compter les occurrences de chaque compétence
        skill_counter = Counter(all_skills)
        
        # Retourner les compétences les plus fréquentes
        return skill_counter.most_common(10)
    
    def get_career_path_for_profile(self, profile_name):
        """Retourne le parcours de carrière pour un profil spécifique"""
        profile = self.job_profiles.get(profile_name)
        if profile:
            return profile.get('career_path', [])
        return []
        
    def get_all_skills(self):
        """Retourne toutes les compétences uniques de tous les profils"""
        all_skills = set()
        for profile_data in self.job_profiles.values():
            all_skills.update(profile_data.get('skills_required', []))
        return list(all_skills)

# Fonction pour obtenir l'instance du recommandeur (singleton pattern)
def get_recommender_instance():
    global _recommender_instance
    if _recommender_instance is None:
        _recommender_instance = JobProfilesRecommender()
    return _recommender_instance

# Fonction de niveau supérieur pour recommander des profils
def recommend_profiles(skills=None, sector=None, experience=None, top_n=3):
    """Recommande des profils professionnels basés sur les compétences, le secteur et l'expérience"""
    recommender = get_recommender_instance()
    return recommender.recommend_profiles(skills, sector, experience, top_n)

# Fonction pour accéder aux profils
def get_profile_details(profile_name):
    """Retourne les détails d'un profil professionnel spécifique"""
    recommender = get_recommender_instance()
    return recommender.get_profile_details(profile_name)

# Fonction pour obtenir les compétences requises pour un secteur
def get_required_skills_for_sector(sector):
    """Retourne les compétences les plus demandées pour un secteur spécifique"""
    recommender = get_recommender_instance()
    return recommender.get_required_skills_for_sector(sector)

# Fonction pour obtenir le parcours de carrière pour un profil
def get_career_path_for_profile(profile_name):
    """Retourne le parcours de carrière pour un profil spécifique"""
    recommender = get_recommender_instance()
    return recommender.get_career_path_for_profile(profile_name)

# Initialiser les profils au chargement du module
def initialize_job_profiles():
    global job_profiles
    recommender = get_recommender_instance()
    job_profiles = recommender.job_profiles

# Initialiser les profils
initialize_job_profiles()

# Test du module
if __name__ == "__main__":
    recommender = JobProfilesRecommender()
    
    # Test de recommandation basée sur les compétences
    test_skills = ['Python', 'SQL', 'Machine Learning']
    recommended_profiles = recommender.recommend_profiles(skills=test_skills)
    
    print(f"Profils recommandés pour les compétences {test_skills}:")
    for profile in recommended_profiles:
        print(f"- {profile}")
        details = recommender.get_profile_details(profile)
        print(f"  Compétences requises: {', '.join(details['skills_required'])}")
        print(f"  Parcours éducatif: {', '.join(details['education'])}")
