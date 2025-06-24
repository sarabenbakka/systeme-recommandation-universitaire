import pandas as pd
import numpy as np
from collections import Counter

class UniversityRecommender:
    def __init__(self):
        # Définition des filières universitaires avec leurs modules et compétences associées
        self.university_programs = {
            'Master en Data Science': {
                'description': 'Formation avancée en science des données, combinant statistiques, informatique et expertise métier.',
                'modules': [
                    'Fondamentaux de la Data Science',
                    'Programmation Python pour l\'analyse de données',
                    'Machine Learning et Deep Learning',
                    'Statistiques avancées',
                    'Big Data et technologies associées',
                    'Visualisation de données',
                    'Projet Data Science appliqué'
                ],
                'skills_developed': [
                    'Python', 'R', 'Machine Learning', 'Deep Learning', 'SQL', 'Big Data', 
                    'Data Visualization', 'Statistical Analysis', 'NLP', 'Data Mining'
                ],
                'career_prospects': [
                    'Data Scientist', 'Data Analyst', 'Machine Learning Engineer', 
                    'AI Researcher', 'Business Intelligence Analyst'
                ],
                'duration': '2 ans'
            },
            'Master en Développement Web': {
                'description': 'Formation spécialisée dans la conception et le développement d\'applications web modernes.',
                'modules': [
                    'Développement Front-end (HTML/CSS/JavaScript)',
                    'Frameworks modernes (React, Angular, Vue)',
                    'Développement Back-end (Node.js, Django, Laravel)',
                    'Architecture web et API',
                    'UX/UI Design',
                    'Sécurité web',
                    'Projet de développement web full stack'
                ],
                'skills_developed': [
                    'JavaScript', 'HTML', 'CSS', 'React', 'Angular', 'Node.js', 'REST API',
                    'SQL', 'NoSQL', 'Git', 'Responsive Design', 'Web Security'
                ],
                'career_prospects': [
                    'Développeur Full Stack', 'Développeur Frontend', 'Développeur Backend',
                    'Architecte Web', 'Lead Developer'
                ],
                'duration': '2 ans'
            },
            'Master en Cybersécurité': {
                'description': 'Formation spécialisée dans la protection des systèmes d\'information et la gestion des risques informatiques.',
                'modules': [
                    'Fondamentaux de la cybersécurité',
                    'Sécurité des réseaux',
                    'Cryptographie appliquée',
                    'Analyse des vulnérabilités',
                    'Réponse aux incidents',
                    'Sécurité offensive (ethical hacking)',
                    'Gouvernance et conformité'
                ],
                'skills_developed': [
                    'Network Security', 'Penetration Testing', 'SIEM', 'Cryptography',
                    'Risk Assessment', 'Incident Response', 'Security Auditing', 'Ethical Hacking'
                ],
                'career_prospects': [
                    'Analyste en Cybersécurité', 'Pentester', 'Consultant en Sécurité',
                    'Architecte Sécurité', 'RSSI'
                ],
                'duration': '2 ans'
            },
            'Master en Cloud Computing': {
                'description': 'Formation spécialisée dans les technologies cloud, la virtualisation et les infrastructures distribuées.',
                'modules': [
                    'Fondamentaux du Cloud Computing',
                    'Services AWS/Azure/GCP',
                    'Conteneurisation et orchestration (Docker, Kubernetes)',
                    'Infrastructure as Code',
                    'DevOps et CI/CD',
                    'Sécurité dans le cloud',
                    'Projet d\'architecture cloud'
                ],
                'skills_developed': [
                    'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform',
                    'CI/CD', 'IaC', 'Microservices', 'Serverless'
                ],
                'career_prospects': [
                    'Ingénieur DevOps', 'Architecte Cloud', 'SRE',
                    'Cloud Solutions Architect', 'DevSecOps Engineer'
                ],
                'duration': '2 ans'
            },
            'Master en Intelligence Artificielle': {
                'description': 'Formation de pointe en intelligence artificielle, couvrant les aspects théoriques et pratiques.',
                'modules': [
                    'Fondements de l\'intelligence artificielle',
                    'Apprentissage profond avancé',
                    'Vision par ordinateur',
                    'Traitement du langage naturel',
                    'Systèmes multi-agents',
                    'Robotique et systèmes autonomes',
                    'Éthique et IA responsable',
                    'Projet de recherche en IA'
                ],
                'skills_developed': [
                    'Python', 'TensorFlow', 'PyTorch', 'Deep Learning', 'NLP',
                    'Computer Vision', 'Reinforcement Learning', 'AI Ethics'
                ],
                'career_prospects': [
                    'Ingénieur IA', 'Chercheur en ML/DL', 'Data Scientist',
                    'Computer Vision Engineer', 'NLP Specialist'
                ],
                'duration': '2 ans'
            },
            'Master en Business Intelligence': {
                'description': 'Formation spécialisée dans l\'analyse des données d\'entreprise pour la prise de décision stratégique.',
                'modules': [
                    'Conception de Data Warehouse',
                    'Outils de BI (Tableau, Power BI)',
                    'SQL avancé',
                    'ETL et intégration de données',
                    'Analyse décisionnelle',
                    'Reporting et dashboarding',
                    'Projet BI en entreprise'
                ],
                'skills_developed': [
                    'SQL', 'Tableau', 'Power BI', 'ETL', 'Data Modeling',
                    'Data Warehouse', 'OLAP', 'Business Analytics'
                ],
                'career_prospects': [
                    'Analyste BI', 'Consultant BI', 'Data Analyst',
                    'ETL Developer', 'Data Warehouse Architect'
                ],
                'duration': '2 ans'
            },
            'Master en Génie Logiciel': {
                'description': 'Formation avancée en conception, développement et maintenance de logiciels complexes.',
                'modules': [
                    'Programmation orientée objet avancée',
                    'Architecture logicielle',
                    'Design patterns',
                    'Tests et qualité logicielle',
                    'Développement Agile',
                    'DevOps et CI/CD',
                    'Projet de développement logiciel'
                ],
                'skills_developed': [
                    'Java', 'C#', 'Python', 'OOP', 'Design Patterns', 'Unit Testing',
                    'CI/CD', 'Agile', 'Scrum', 'Software Architecture'
                ],
                'career_prospects': [
                    'Ingénieur Logiciel', 'Architecte Logiciel', 'Tech Lead',
                    'DevOps Engineer', 'Quality Assurance Engineer'
                ],
                'duration': '2 ans'
            },
            'Master en Finance Quantitative': {
                'description': 'Formation spécialisée à l\'intersection de la finance, des mathématiques et de l\'informatique.',
                'modules': [
                    'Finance quantitative',
                    'Analyse financière',
                    'Gestion des risques',
                    'Technologies financières (FinTech)',
                    'Modélisation financière',
                    'Programmation pour la finance (Python, R)',
                    'Projet de recherche en finance'
                ],
                'skills_developed': [
                    'Financial Modeling', 'Risk Assessment', 'Python', 'R',
                    'Statistical Analysis', 'Financial Analysis', 'Algorithmic Trading'
                ],
                'career_prospects': [
                    'Analyste Quantitatif', 'Risk Manager', 'Trader Algorithmique',
                    'Consultant FinTech', 'Analyste Financier'
                ],
                'duration': '2 ans'
            },
            'Master en FinTech': {
                'description': 'Formation spécialisée dans les technologies financières innovantes et la transformation digitale du secteur financier.',
                'modules': [
                    'Introduction aux FinTech',
                    'Blockchain et cryptomonnaies',
                    'Paiements digitaux et banque mobile',
                    'API bancaires et Open Banking',
                    'Réglementation financière et conformité',
                    'Développement d\'applications financières',
                    'Intelligence artificielle pour la finance',
                    'Projet FinTech innovant'
                ],
                'skills_developed': [
                    'Blockchain', 'API Development', 'Mobile Banking', 'Payment Systems',
                    'Regulatory Compliance', 'JavaScript', 'Python', 'Smart Contracts'
                ],
                'career_prospects': [
                    'FinTech Product Manager', 'Blockchain Developer', 'Consultant FinTech',
                    'Digital Banking Specialist', 'Regulatory Technology Expert'
                ],
                'duration': '2 ans'
            },
            'Master en Gestion des Risques Financiers': {
                'description': 'Formation spécialisée dans l\'identification, l\'analyse et la gestion des risques financiers et opérationnels.',
                'modules': [
                    'Fondamentaux de la gestion des risques',
                    'Risques de marché et de crédit',
                    'Risques opérationnels et de conformité',
                    'Modélisation des risques',
                    'Stress testing et scénarios',
                    'Réglementation prudentielle (Bâle, Solvabilité)',
                    'Technologies pour la gestion des risques',
                    'Projet de gestion des risques'
                ],
                'skills_developed': [
                    'Risk Modeling', 'VaR', 'Stress Testing', 'Regulatory Compliance',
                    'Credit Scoring', 'Excel Avancé', 'Python/R', 'Financial Analysis'
                ],
                'career_prospects': [
                    'Risk Manager', 'Analyste des Risques', 'Consultant en Risques',
                    'Responsable Conformité', 'Auditeur Interne'
                ],
                'duration': '2 ans'
            },
            'Master en Data Science pour la Finance': {
                'description': 'Formation hybride combinant science des données et expertise financière pour l\'analyse et la prise de décision dans le secteur financier.',
                'modules': [
                    'Fondamentaux de la data science',
                    'Finance quantitative',
                    'Machine learning pour la finance',
                    'Analyse prédictive des marchés financiers',
                    'Détection de fraude et anomalies',
                    'Analyse de sentiment et alternative data',
                    'Big data en finance',
                    'Projet d\'application data science en finance'
                ],
                'skills_developed': [
                    'Python', 'R', 'Machine Learning', 'Financial Analysis',
                    'Time Series Analysis', 'NLP', 'Big Data', 'Fraud Detection'
                ],
                'career_prospects': [
                    'Data Scientist Finance', 'Analyste Quantitatif', 'Spécialiste en IA Financière',
                    'Analyste de Risque', 'Consultant en Data Finance'
                ],
                'duration': '2 ans'
            }
        }
    
    def get_all_programs(self):
        """Retourne toutes les filières universitaires disponibles"""
        return self.university_programs
    
    def get_program_details(self, program_name):
        """Retourne les détails d'une filière universitaire spécifique"""
        return self.university_programs.get(program_name, None)
    
    def recommend_programs(self, skills=None, career_goal=None, top_n=3):
        """Recommande des filières universitaires basées sur les compétences et les objectifs de carrière"""
        scores = {}
        
        for program_name, program_data in self.university_programs.items():
            score = 0
            
            # Score basé sur les compétences
            if skills:
                skills_list = [skill.lower() for skill in skills]
                program_skills = [skill.lower() for skill in program_data['skills_developed']]
                
                # Calculer l'intersection des compétences
                common_skills = set(skills_list).intersection(set(program_skills))
                score += len(common_skills) * 2  # Pondération plus élevée pour les compétences
            
            # Score basé sur l'objectif de carrière
            if career_goal:
                career_goal_lower = career_goal.lower()
                # Vérifier si l'objectif de carrière est mentionné dans les perspectives de carrière
                career_prospects = [prospect.lower() for prospect in program_data['career_prospects']]
                if any(career_goal_lower in prospect for prospect in career_prospects):
                    score += 3  # Forte pondération pour l'alignement avec l'objectif de carrière
            
            scores[program_name] = score
        
        # Trier les filières par score et prendre les top_n
        sorted_programs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_programs = [program for program, score in sorted_programs[:top_n] if score > 0]
        
        # Si aucune filière n'a un score positif, retourner les 3 filières les plus populaires
        if not top_programs:
            top_programs = list(self.university_programs.keys())[:top_n]
        
        return top_programs
    
    def recommend_modules(self, skills=None, program=None):
        """Recommande des modules spécifiques basés sur les compétences et la filière"""
        if program and program in self.university_programs:
            # Si une filière est spécifiée, retourner ses modules
            return self.university_programs[program]['modules']
        
        # Sinon, recommander des modules basés sur les compétences
        recommended_modules = set()
        
        if skills:
            skills_lower = [skill.lower() for skill in skills]
            
            for program_name, program_data in self.university_programs.items():
                program_skills = [skill.lower() for skill in program_data['skills_developed']]
                
                # Si au moins une compétence correspond, ajouter les modules de cette filière
                if any(skill in program_skills for skill in skills_lower):
                    recommended_modules.update(program_data['modules'])
        
        return list(recommended_modules)
    
    def get_market_aligned_programs(self, market_trends):
        """Identifie les filières les mieux alignées avec les tendances du marché"""
        if not market_trends:
            return list(self.university_programs.keys())[:3]
        
        scores = {}
        
        for program_name, program_data in self.university_programs.items():
            score = 0
            program_skills = [skill.lower() for skill in program_data['skills_developed']]
            
            for trend, weight in market_trends.items():
                if trend.lower() in ' '.join(program_skills).lower():
                    score += weight
            
            scores[program_name] = score
        
        # Trier les filières par score
        sorted_programs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        return [program for program, _ in sorted_programs[:3]]

# Test du module
if __name__ == "__main__":
    recommender = UniversityRecommender()
    
    # Test de recommandation basée sur les compétences
    test_skills = ['Python', 'Machine Learning', 'Data Visualization']
    recommended_programs = recommender.recommend_programs(skills=test_skills)
    
    print(f"Filières recommandées pour les compétences {test_skills}:")
    for program in recommended_programs:
        print(f"- {program}")
        details = recommender.get_program_details(program)
        print(f"  Modules: {', '.join(details['modules'][:3])}...")
