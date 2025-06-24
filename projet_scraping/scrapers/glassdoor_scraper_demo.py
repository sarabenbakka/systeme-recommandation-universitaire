import random
import time
from datetime import datetime
import pandas as pd

class GlassdoorScraperDemo:
    def __init__(self):
        self.companies = ['BNP Paribas', 'Société Générale', 'Crédit Agricole']
        self.job_titles_finance = ['Risk Manager', 'Analyste Financier', 'Développeur Python', 'Data Scientist']
        self.job_titles_tech = ['Développeur Python', 'Data Scientist', 'Machine Learning Engineer', 'Software Engineer']
        self.locations = ['Marseille', 'Lyon', 'Paris', 'Bordeaux', 'Nice']
    
    def generate_job(self):
        job = {
            'id': f'job_{random.randint(1000, 9999)}',
            'Secteur': random.choice(['Finance', 'Tech']),
            'Poste': random.choice(self.job_titles_finance + self.job_titles_tech),
            'Entreprise': random.choice(self.companies),
            'Ville': random.choice(self.locations),
            'Date_de_publication': datetime.now().strftime('%Y-%m-%d'),
            'Lien': f"https://www.glassdoor.fr/job/{random.randint(1000, 9999)}",
            'Experience': '50k - 70k € par an',
            'Contrat': 'CDI',
            'Niveau_etude': 'Bac+5'
        }
        return job
    
    def simulate_scraping(self, num_jobs=10):
        jobs = [self.generate_job() for _ in range(num_jobs)]
        return jobs

def main():
    scraper = GlassdoorScraperDemo()
    jobs = scraper.simulate_scraping(200)
    # Spécifiez le chemin de sauvegarde pour les données simulées
    output_path = r"C:\Users\HP\OneDrive\Nouveau dossier\OneDrive\Desktop\projet_scraping\output"
    df = pd.DataFrame(jobs)
    df.to_csv(f'{output_path}\\glassdoor_jobs_demo.csv', index=False, encoding='utf-8-sig')
    print("Données sauvegardées dans: glassdoor_jobs_demo.csv")

if __name__ == "__main__":
    main()
