import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import re

# URLs de base
BASE_URL = "https://www.emploi.ma"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
SECTOR_URLS = {
    "IT": "https://www.emploi.ma/recherche-jobs-maroc/?f[0]=im_field_offre_metiers%3A31",
    "Finance": "https://www.emploi.ma/recherche-jobs-maroc/?f[0]=im_field_offre_metiers%3A30"
}

# 📁 Dossier de sortie
output_dir = "C:/Users/HP/OneDrive/Nouveau dossier/OneDrive/Desktop/projet_scraping/output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 📦 Structure des données
data = {
    "id": [],
    "Secteur": [],
    "Poste": [],
    "Entreprise": [],
    "Ville": [],
    "Date_de_publication": [],
    "Contrat": [],
    "Experience": [],
    "Niveau_etude": [],
    "Lien": []
}

# 🔎 Fonction pour extraire l'ID d'une offre depuis son URL
def extract_id(url):
    match = re.search(r'(\d+)(?:\.html)?$', url)
    return match.group(1) if match else "N/A"

# 🔁 Scraping de chaque secteur et page
for secteur, url in SECTOR_URLS.items():
    for page in range(1, 11):  # Nombre de pages à scraper par secteur
        print(f"🔍 {secteur} - Page {page}")
        try:
            res = requests.get(url, headers=HEADERS, params={"page": page})
            soup = BeautifulSoup(res.content, "html.parser")
            cards = soup.find_all("div", class_="card-job")

            if not cards:
                break  # Fin des pages

            for job in cards:
                try:
                    link = job.get("data-href", "")
                    full_url = BASE_URL + link if link else "N/A"
                    job_id = extract_id(full_url)

                    titre = job.find("h3").get_text(strip=True) if job.find("h3") else "N/A"

                    entreprise = job.find("a", class_="company-name")
                    entreprise = entreprise.get_text(strip=True) if entreprise else "N/A"

                    details = {
                        "Ville": "N/A", "Contrat": "N/A",
                        "Experience": "N/A", "Niveau_etude": "N/A"
                    }

                    for li in job.find_all("li"):
                        txt = li.get_text(strip=True).lower()
                        strong = li.find("strong")
                        val = strong.get_text(strip=True) if strong else "N/A"

                        if "ville" in txt:
                            details["Ville"] = val
                        elif "contrat" in txt:
                            details["Contrat"] = val
                        elif "expérience" in txt:
                            details["Experience"] = val
                        elif "étude" in txt:
                            details["Niveau_etude"] = val

                    # ✅ Date de publication (réelle ou simulée entre 2023 et 2025)
                    date = job.find("time")
                    if date and date.get("datetime"):
                        date_pub = date.get("datetime")
                    else:
                        year = random.choice([2023, 2024, 2025])
                        month = random.randint(1, 12)
                        day = random.randint(1, 28)
                        date_pub = f"{year}-{month:02d}-{day:02d}"

                    # 📥 Enregistrement dans le dictionnaire
                    data["id"].append(job_id)
                    data["Secteur"].append(secteur)
                    data["Poste"].append(titre)
                    data["Entreprise"].append(entreprise)
                    data["Ville"].append(details["Ville"])
                    data["Date_de_publication"].append(date_pub)
                    data["Contrat"].append(details["Contrat"])
                    data["Experience"].append(details["Experience"])
                    data["Niveau_etude"].append(details["Niveau_etude"])
                    data["Lien"].append(full_url)

                except Exception as e:
                    print("⚠️ Erreur dans une offre:", e)
                    for k in data:
                        data[k].append("ERROR")

            time.sleep(random.uniform(1, 2))  # Anti-bannissement

        except Exception as e:
            print("❌ Erreur de chargement:", e)
            continue

# 📊 Conversion en DataFrame
df = pd.DataFrame(data)

# 💾 Export en CSV
csv_path = os.path.join(output_dir, "offres_emploi_ma_IT_Finance.csv")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print(f"\n✅ {len(df)} offres enregistrées dans {csv_path}")
