import pandas as pd
import os

# Spécifiez les chemins des fichiers CSV à fusionner dans le dossier 'output'
csv_linkedin_path = "C:/Users/HP/OneDrive/Nouveau dossier/OneDrive/Desktop/projet_scraping/output/linkedin_jobs_500.csv"
csv_ma_path = "C:/Users/HP/OneDrive/Nouveau dossier/OneDrive/Desktop/projet_scraping/output/offres_emploi_ma_IT_Finance.csv"
csv_ork_path = "C:/Users/HP/OneDrive/Nouveau dossier/OneDrive/Desktop/projet_scraping/output/ORK.csv"
csv_demo_path = "C:/Users/HP/OneDrive/Nouveau dossier/OneDrive/Desktop/projet_scraping/output/glassdoor_jobs_demo.csv"  # Ajout du fichier demo

# Vérification si les fichiers existent dans le dossier 'output'
if not os.path.exists(csv_linkedin_path):
    print(f"Erreur : Le fichier {csv_linkedin_path} n'existe pas.")
elif not os.path.exists(csv_ma_path):
    print(f"Erreur : Le fichier {csv_ma_path} n'existe pas.")
elif not os.path.exists(csv_ork_path):
    print(f"Erreur : Le fichier {csv_ork_path} n'existe pas.")
elif not os.path.exists(csv_demo_path):
    print(f"Erreur : Le fichier {csv_demo_path} n'existe pas.")
else:
    try:
        # Lecture des fichiers CSV
        df_linkedin = pd.read_csv(csv_linkedin_path)
        df_ma = pd.read_csv(csv_ma_path)
        df_ork = pd.read_csv(csv_ork_path)
        df_demo = pd.read_csv(csv_demo_path)  # Lecture du fichier demo

        # Transformation des noms de colonnes pour qu'ils commencent par une majuscule
        df_linkedin.columns = [col.capitalize() for col in df_linkedin.columns]
        df_ma.columns = [col.capitalize() for col in df_ma.columns]
        df_ork.columns = [col.capitalize() for col in df_ork.columns]
        df_demo.columns = [col.capitalize() for col in df_demo.columns]

        # Fusion des DataFrames
        df_fusion = pd.concat([df_linkedin, df_ma, df_ork, df_demo], ignore_index=True)  # Ajout du fichier demo à la fusion

        # Sauvegarde du fichier fusionné dans le dossier 'output'
        output_dir = "C:/Users/HP/OneDrive/Nouveau dossier/OneDrive/Desktop/projet_scraping/output"  # Spécifiez le chemin complet
        output_file = os.path.join(output_dir, "final_jobs_data.csv")

        # Enregistrer le fichier fusionné
        df_fusion.to_csv(output_file, index=False, encoding='utf-8-sig')

        print(f"Fichiers fusionnés et sauvegardés dans {output_file}")

    except Exception as e:
        print(f"Une erreur est survenue lors de la fusion des fichiers : {e}")
