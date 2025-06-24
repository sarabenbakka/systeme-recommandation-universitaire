import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import pandas as pd
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealGlassdoorScraper:
    def __init__(self, headless: bool = True):
        self.base_url = "https://www.glassdoor.fr"
        self.headless = headless
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Driver Selenium initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du driver: {e}")
            raise

    def search_jobs(self, keyword: str, location: str = "France", max_pages: int = 3):
        jobs = []
        try:
            search_url = f"{self.base_url}/Emplois/index.htm"
            self.driver.get(search_url)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            keyword_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-test='job-search-bar-keywords']"))
            )
            keyword_input.clear()
            keyword_input.send_keys(keyword)
            
            location_input = self.driver.find_element(By.CSS_SELECTOR, "input[data-test='job-search-bar-location']")
            location_input.clear()
            location_input.send_keys(location)
            
            search_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-test='job-search-button']")
            search_button.click()
            
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='jobListing']"))
            )
            
            for page in range(1, max_pages + 1):
                logger.info(f"Scraping page {page} pour '{keyword}'")
                page_jobs = self.extract_jobs_from_page(keyword)
                jobs.extend(page_jobs)
                
                if page < max_pages:
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next']")
                        if next_button.is_enabled():
                            next_button.click()
                            time.sleep(random.uniform(3, 6))
                        else:
                            logger.info("Pas de page suivante disponible")
                            break
                    except NoSuchElementException:
                        logger.info("Bouton 'Suivant' non trouvé")
                        break
                
                time.sleep(random.uniform(2, 4))
                
        except Exception as e:
            logger.error(f"Erreur lors de la recherche: {e}")
        
        return jobs

    def extract_jobs_from_page(self, keyword: str):
        jobs = []
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='jobListing']"))
            )
            
            job_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-test='jobListing']")
            
            for job_element in job_elements:
                try:
                    job_data = self.extract_job_details(job_element, keyword)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    logger.warning(f"Erreur lors de l'extraction d'une offre: {e}")
                    continue
            
            logger.info(f"Extraites {len(jobs)} offres de cette page")
            
        except TimeoutException:
            logger.warning("Timeout lors de l'attente des offres d'emploi")
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction: {e}")
        
        return jobs

    def extract_job_details(self, job_element, keyword: str):
        try:
            title_element = job_element.find_element(By.CSS_SELECTOR, "[data-test='job-title'] a")
            title = title_element.text.strip()
            job_link = title_element.get_attribute('href')
            
            company_element = job_element.find_element(By.CSS_SELECTOR, "[data-test='employer-name']")
            company = company_element.text.strip()
            
            location_element = job_element.find_element(By.CSS_SELECTOR, "[data-test='job-location']")
            location = location_element.text.strip()
            
            salary_element = job_element.find_element(By.CSS_SELECTOR, "[data-test='detailSalary']")
            salary = salary_element.text.strip()
            
            description_element = job_element.find_element(By.CSS_SELECTOR, "[data-test='job-description']")
            description = description_element.text.strip()[:300] + "..."
            
            date_element = job_element.find_element(By.CSS_SELECTOR, ".job-search-key-9ujsbx")
            date_posted = date_element.text.strip()
            
            return {
                'id': job_link.split('/')[-1], 
                'Secteur': keyword.capitalize(),
                'Poste': title,
                'Entreprise': company,
                'Ville': location,
                'Date_de_publication': date_posted,
                'Lien': job_link,
                'Experience': salary,
                'Contrat': salary,
                'Niveau_etude': salary,
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction des détails: {e}")
            return None

    def save_jobs_to_csv(self, jobs, filename="glassdoor_jobs.csv"):
        output_path = r"C:\Users\HP\OneDrive\Nouveau dossier\OneDrive\Desktop\projet_scraping\output"
        df = pd.DataFrame(jobs)
        df.to_csv(f'{output_path}\\{filename}', index=False, encoding='utf-8-sig')
        print(f"Fichier sauvegardé sous: {output_path}\\{filename}")

    def scrape_multiple_keywords(self, keywords: List[str], location: str = "France", max_pages: int = 2):
        all_jobs = []
        for keyword in keywords:
            logger.info(f"Début du scraping pour: {keyword}")
            jobs = self.search_jobs(keyword, location, max_pages)
            all_jobs.extend(jobs)
            time.sleep(random.uniform(10, 20))
        
        return all_jobs

    def close(self):
        if self.driver:
            self.driver.quit()
            logger.info("Driver Selenium fermé")

def main():
    keywords = ['développeur python', 'data scientist', 'analyste financier', 'risk manager', 'software engineer']
    scraper = None
    
    try:
        logger.info("Initialisation du scraper Glassdoor réel...")
        scraper = RealGlassdoorScraper(headless=True)
        
        jobs = scraper.scrape_multiple_keywords(keywords, location="France", max_pages=3)
        
        if jobs:
            logger.info(f"Total d'offres récupérées: {len(jobs)}")
            
            df = pd.DataFrame(jobs)
            df = df.drop_duplicates(subset=['poste', 'entreprise'], keep='first')
            
            filename = f"glassdoor_jobs_real_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
            scraper.save_jobs_to_csv(jobs, filename)
            
            logger.info(f"Données sauvegardées dans: {filename}")
            print(f"✅ Scraping terminé: {len(df)} offres uniques sauvegardées")
        else:
            logger.warning("Aucune offre d'emploi récupérée")
            
    except Exception as e:
        logger.error(f"Erreur lors du scraping: {e}")
        print(f"❌ Erreur: {e}")
        
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    print("⚠️  ATTENTION: Ce script utilise Selenium pour scraper Glassdoor")
    print("📋 Assurez-vous d'avoir ChromeDriver installé")
    print("⚖️  Respectez les conditions d'utilisation de Glassdoor")
    print("🕐 Le scraping peut prendre plusieurs minutes...")
    
    response = input("\nContinuer? (y/N): ")
    if response.lower() == 'y':
        main()
    else:
        print("Scraping annulé")
