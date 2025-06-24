import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

class GlassdoorScraper:
    def __init__(self):
        self.base_url = "https://www.glassdoor.com"
        self.session = requests.Session()

    def search_jobs(self, keyword: str, location: str = "France", max_pages: int = 3):
        jobs = []
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/Emplois/{keyword}-emplois-SRCH_KO0,{len(keyword)}.htm?locId=96&locT=N&page={page}"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_elements = soup.find_all('li', class_='jl')
            for job_element in job_elements:
                try:
                    job_data = self.extract_job_details(job_element)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    print(f"Erreur lors de l'extraction d'une offre: {e}")
                    continue
            
            time.sleep(random.uniform(2, 4))  # Délai entre les pages pour éviter le blocage
        return jobs

    def extract_job_details(self, job_element):
        try:
            title = job_element.find('a', class_='jobLink').text.strip()
            company = job_element.find('div', class_='jobInfoItem').text.strip()
            location = job_element.find('span', class_='subtle loc').text.strip()
            job_link = self.base_url + job_element.find('a', class_='jobLink')['href']
            
            return {
                'id': job_link.split('/')[-1],
                'Secteur': 'Finance',  # Exemple, ajustez selon les données réelles
                'Poste': title,
                'Entreprise': company,
                'Ville': location,
                'Date_de_publication': '2025-06-16',  # Vous pouvez ajuster cette date
                'Lien': job_link,
                'Experience': '50k - 70k € par an',
                'Contrat': 'CDI',
                'Niveau_etude': 'Bac+5'
            }
        except Exception as e:
            print(f"Erreur lors de l'extraction des détails: {e}")
            return None

    def save_jobs_to_csv(self, jobs, filename="glassdoor_jobs.csv"):
        output_path = r"C:\Users\HP\OneDrive\Nouveau dossier\OneDrive\Desktop\projet_scraping\output"
        df = pd.DataFrame(jobs)
        df.to_csv(f'{output_path}\\{filename}', index=False, encoding='utf-8-sig')
        print(f"Fichier sauvegardé sous: {output_path}\\{filename}")
