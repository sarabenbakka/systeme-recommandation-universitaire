import pandas as pd
import re
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SkillsGenerator:
    def __init__(self):
        # Base de connaissances des compétences par domaine IT et Finance
        self.skills_database = {
            # Domaines Data
            'data analyst': ['SQL', 'Excel', 'Tableau', 'Power BI', 'Python', 'R', 'Data Visualization', 
                            'ETL', 'Statistical Analysis', 'Data Cleaning', 'Data Modeling', 'Business Intelligence'],
            
            'data scientist': ['Python', 'R', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 
                              'Statistical Analysis', 'NLP', 'Computer Vision', 'Big Data', 'SQL', 'Data Mining',
                              'Feature Engineering', 'Jupyter', 'Scikit-learn', 'Pandas', 'NumPy'],
            
            'data engineer': ['SQL', 'Python', 'Spark', 'Hadoop', 'ETL', 'Data Pipelines', 'AWS', 'Azure', 
                             'GCP', 'Docker', 'Kubernetes', 'NoSQL', 'MongoDB', 'Cassandra', 'Kafka', 'Airflow'],
            
            # Domaines Cybersécurité
            'cybersecurity': ['Network Security', 'Penetration Testing', 'SIEM', 'Firewall', 'IDS/IPS', 
                             'Security Auditing', 'Risk Assessment', 'Cryptography', 'Ethical Hacking', 
                             'Incident Response', 'Security+', 'CISSP', 'OSCP'],
            
            'security analyst': ['SIEM', 'Threat Intelligence', 'Vulnerability Assessment', 'Security Controls', 
                                'Log Analysis', 'Incident Response', 'Compliance', 'Risk Management', 
                                'Security Frameworks', 'Network Security'],
            
            # Domaines Développement
            'software engineer': ['Java', 'Python', 'C#', 'JavaScript', 'Git', 'CI/CD', 'Agile', 'Scrum', 
                                 'OOP', 'Design Patterns', 'REST API', 'Unit Testing', 'Microservices', 
                                 'Cloud Computing', 'Linux'],
            
            'python developer': ['Python', 'Django', 'Flask', 'FastAPI', 'SQL', 'ORM', 'REST API', 
                               'Unit Testing', 'Git', 'Docker', 'AWS', 'Pandas', 'NumPy'],
            
            'full stack developer': ['JavaScript', 'TypeScript', 'React', 'Angular', 'Vue.js', 'Node.js', 
                                    'Express', 'HTML', 'CSS', 'SQL', 'NoSQL', 'Git', 'Docker', 'REST API', 
                                    'Responsive Design', 'AWS/Azure/GCP'],
            
            # Domaines Cloud
            'cloud engineer': ['AWS', 'Azure', 'GCP', 'Terraform', 'CloudFormation', 'Docker', 'Kubernetes', 
                              'IaC', 'CI/CD', 'Networking', 'Security', 'Linux', 'Python', 'Bash'],
            
            'devops': ['Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'GitHub Actions', 'Terraform', 'Ansible', 
                      'Prometheus', 'Grafana', 'ELK Stack', 'Linux', 'Bash', 'Python', 'AWS/Azure/GCP', 'CI/CD'],
            
            # Domaines Finance
            'financial analyst': ['Financial Modeling', 'Excel', 'Financial Reporting', 'Budgeting', 
                                 'Forecasting', 'Valuation', 'Bloomberg Terminal', 'Financial Statement Analysis', 
                                 'Power BI', 'SQL', 'Risk Assessment'],
            
            'finance': ['Financial Analysis', 'Accounting', 'Excel', 'Financial Reporting', 'Budgeting', 
                       'Forecasting', 'ERP Systems', 'SAP', 'Oracle Financials', 'Risk Management'],
            
            'accounting': ['General Ledger', 'Financial Reporting', 'GAAP', 'IFRS', 'Tax Accounting', 
                          'Audit', 'ERP Systems', 'Excel', 'Financial Analysis', 'Reconciliation'],
            
            'risk management': ['Risk Assessment', 'Risk Modeling', 'Compliance', 'Regulatory Frameworks', 
                               'Basel III', 'Stress Testing', 'Credit Risk', 'Market Risk', 'Operational Risk', 
                               'Risk Mitigation Strategies'],
            
            # Domaines IT Management
            'it manager': ['Project Management', 'Team Leadership', 'Budgeting', 'Strategic Planning', 
                          'Vendor Management', 'ITIL', 'Service Delivery', 'Risk Management', 
                          'Business Relationship Management', 'IT Governance'],
            
            'network engineer': ['Cisco', 'Routing', 'Switching', 'Firewalls', 'VPN', 'VLAN', 'TCP/IP', 
                               'Network Security', 'Troubleshooting', 'Network Monitoring', 'WAN', 'LAN']
        }
        
        # Vectorizer pour la similarité textuelle
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # Préparer les données pour la similarité
        self.domains = list(self.skills_database.keys())
        self.domain_matrix = self.vectorizer.fit_transform(self.domains)
        
    def find_closest_domain(self, job_title):
        """Trouve le domaine le plus proche du titre de poste"""
        job_title = job_title.lower()
        
        # Vérifier d'abord si un domaine exact est dans le titre
        for domain in self.domains:
            if domain in job_title:
                return domain
        
        # Sinon, utiliser la similarité textuelle
        job_vector = self.vectorizer.transform([job_title])
        similarities = cosine_similarity(job_vector, self.domain_matrix).flatten()
        closest_idx = np.argmax(similarities)
        
        # Retourner le domaine le plus similaire si la similarité est supérieure à un seuil
        if similarities[closest_idx] > 0.2:  # Seuil de similarité
            return self.domains[closest_idx]
        else:
            # Fallback à un domaine générique basé sur des mots-clés
            if any(kw in job_title for kw in ['data', 'analyst', 'scientist', 'analytics']):
                return 'data analyst'
            elif any(kw in job_title for kw in ['develop', 'program', 'code', 'software']):
                return 'software engineer'
            elif any(kw in job_title for kw in ['cloud', 'aws', 'azure', 'gcp']):
                return 'cloud engineer'
            elif any(kw in job_title for kw in ['security', 'cyber', 'hack', 'threat']):
                return 'cybersecurity'
            elif any(kw in job_title for kw in ['finance', 'financial', 'account', 'accounting']):
                return 'finance'
            else:
                return 'software engineer'  # Domaine par défaut
    
    def generate_skills(self, job_title, sector, num_skills=5):
        """Génère des compétences basées sur le titre du poste et le secteur"""
        # Normaliser les entrées
        job_title = job_title.lower() if job_title else ''
        sector = sector.lower() if sector else ''
        
        # Trouver le domaine le plus proche
        domain = self.find_closest_domain(job_title if job_title else sector)
        
        # Obtenir les compétences pour ce domaine
        domain_skills = self.skills_database.get(domain, self.skills_database['software engineer'])
        
        # Sélectionner un nombre aléatoire de compétences (entre num_skills et num_skills+3)
        num_to_select = random.randint(num_skills, min(num_skills+3, len(domain_skills)))
        selected_skills = random.sample(domain_skills, num_to_select)
        
        # Ajouter quelques compétences génériques si nécessaire
        generic_skills = ['Communication', 'Problem Solving', 'Teamwork', 'Analytical Thinking', 
                         'Project Management', 'Time Management', 'Attention to Detail']
        
        if random.random() < 0.7:  # 70% de chance d'ajouter des compétences génériques
            num_generic = random.randint(1, 3)
            selected_skills.extend(random.sample(generic_skills, num_generic))
        
        return selected_skills
    
    def enrich_dataframe(self, df, job_title_col='Poste', sector_col='Secteur', skills_col='Competences'):
        """Enrichit un DataFrame avec des compétences générées"""
        if skills_col not in df.columns:
            df[skills_col] = None
        
        for idx, row in df.iterrows():
            # Ne générer des compétences que si la colonne est vide
            if pd.isna(row[skills_col]) or row[skills_col] == '' or row[skills_col] is None:
                job_title = row[job_title_col] if job_title_col in df.columns and not pd.isna(row[job_title_col]) else ''
                sector = row[sector_col] if sector_col in df.columns and not pd.isna(row[sector_col]) else ''
                
                skills = self.generate_skills(job_title, sector)
                df.at[idx, skills_col] = ', '.join(skills)
        
        return df

# Exemple d'utilisation
if __name__ == "__main__":
    # Charger les données
    path = r"C:\Users\ThinkPad\OneDrive\Desktop\Master Big Data\S1 MASTER\BASE DE DONNEES ORACLE\PROJECTS\projet_scraping\projet_scraping\output\final_jobs_data_cleaned.csv"
    df = pd.read_csv(path)
    
    # Initialiser le générateur de compétences
    skills_gen = SkillsGenerator()
    
    # Enrichir le DataFrame avec des compétences
    df_enriched = skills_gen.enrich_dataframe(df)
    
    # Sauvegarder le résultat
    output_path = r"C:\Users\ThinkPad\OneDrive\Desktop\Master Big Data\S1 MASTER\BASE DE DONNEES ORACLE\PROJECTS\projet_scraping\projet_scraping\output\final_jobs_data_with_skills.csv"
    df_enriched.to_csv(output_path, index=False)
    
    print(f"[OK] Données enrichies avec des compétences générées et sauvegardées dans {output_path}")
    print(f"[INFO] Exemple de compétences générées pour 5 offres :")
    for i in range(min(5, len(df_enriched))):
        print(f"  - {df_enriched.iloc[i]['Poste']} : {df_enriched.iloc[i]['Competences']}")
