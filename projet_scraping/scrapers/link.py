import csv
import random
import os  # Pour vérifier si le dossier output existe

# Fonction pour générer des données fictives pour les offres d'emploi LinkedIn
def generate_fake_data(num_entries):
    sectors = [
        'Data Analyst', 'Data Scientist', 'Data Engineer', 'Cybersecurity', 'Security Analyst',
        'Software Engineer', 'Python Developer', 'Cloud Engineer', 'Machine Learning Engineer',
        'Financial Analyst', 'Finance', 'Accounting', 'Risk Management', 'Audit', 'Investment',
        'Business Intelligence', 'DevOps', 'IT Manager', 'Network Engineer', 'Full Stack Developer'
    ]
    
    companies = [
        'TechCorp', 'DataCorp', 'CloudWorks', 'PythonTech', 'FinCorp', 'InnovateTech', 'SoftWare Solutions',
        'AI Technologies', 'DeepMind', 'CyberGuard', 'FinanceX', 'CloudVision', 'RiskNet', 'InvestPlus', 'DataBrains'
    ]
    
    cities = ['Paris', 'Casablanca', 'Marrakesh', 'Lyon', 'Berlin', 'London', 'New York', 'San Francisco', 'Toronto', 'Amsterdam']
    contracts = ['CDI', 'CDD', 'Freelance', 'Stage', 'Alternance']
    levels = ['Bac +2', 'Bac +3', 'Bac +5', 'Master', 'Doctorat']
    
    job_data = []
    
    for i in range(num_entries):
        job_id = random.randint(10000, 99999)
        
        # Augmenter la probabilité d'avoir des offres en Finance et Informatique
        if random.random() < 0.4:  # 40% des offres seront dans Finance ou Informatique
            sector = random.choice(['Finance', 'Financial Analyst', 'Accounting', 'Risk Management', 'Investment'])
        else:
            sector = random.choice([
                'Data Analyst', 'Data Scientist', 'Data Engineer', 'Cybersecurity', 'Security Analyst',
                'Software Engineer', 'Python Developer', 'Cloud Engineer', 'Machine Learning Engineer',
                'Business Intelligence', 'DevOps', 'IT Manager', 'Network Engineer', 'Full Stack Developer'
            ])

        job_title = f"{sector} {random.choice(['Junior', 'Senior', 'Lead', 'Intern'])}"
        company = random.choice(companies)
        city = random.choice(cities)

        # ✅ Génération aléatoire de l'année entre 2023 et 2025
        year = random.choice([2023, 2024, 2025])
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # éviter les erreurs de date
        date_posted = f"{year}-{month:02d}-{day:02d}"

        job_link = f"https://linkedin.com/jobs/view/{job_id}"
        experience = f"{random.randint(1, 7)} ans"
        contract = random.choice(contracts)
        level = random.choice(levels)
        
        job_data.append({
            "id": job_id,
            "Secteur": sector,
            "Poste": job_title,
            "Entreprise": company,
            "Ville": city,
            "Date_de_publication": date_posted,
            "Lien": job_link,
            "Experience": experience,
            "Contrat": contract,
            "Niveau_etude": level
        })
        
    return job_data

# 📁 Vérifier/créer le dossier output
output_dir = "C:/Users/HP/OneDrive/Nouveau dossier/OneDrive/Desktop/projet_scraping/output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 📝 Chemin du fichier de sortie
csv_path = os.path.join(output_dir, "linkedin_jobs_500.csv")

# 🛠️ Génération des données
job_data = generate_fake_data(500)

# 💾 Sauvegarde des données dans un fichier CSV
with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=[
        "id", "Secteur", "Poste", "Entreprise", "Ville",
        "Date_de_publication", "Lien", "Experience", "Contrat", "Niveau_etude"
    ])
    
    writer.writeheader()
    for job in job_data:
        writer.writerow(job)

print(f"✅ Fichier CSV généré avec succès → {csv_path}")
print(f"📌 Total : {len(job_data)} offres exportées.")
