# Projet de Scraping d'Offres d'Emploi

Ce projet consiste à récupérer des données d'offres d'emploi depuis différentes plateformes (LinkedIn, emploi.ma, rekrute.com), fusionner les résultats, et les nettoyer pour une utilisation dans une base de données Oracle.

## Structure du Projet

- `/scrapers` : Contient les scripts de scraping pour chaque plateforme.
- `/output` : Contient les fichiers CSV générés après chaque scraping.
- `/merge` : Contient le script pour fusionner les fichiers CSV et le fichier final nettoyé.
- `/config` : Contient le fichier `requirements.txt` pour installer les dépendances Python.

## Comment Exécuter le Projet

1. Clonez ce repository.
2. Installez les dépendances : 
    ```bash
    pip install -r config/requirements.txt
    ```
3. Exécutez chaque script de scraping dans `/scrapers` pour générer les fichiers CSV.
4. Exécutez le script `merge_scrapers.py` dans le dossier `/merge` pour fusionner les CSVs en un fichier final :
    ```bash
    python merge/merge_scrapers.py
    ```
5. Le fichier final `final_jobs_data.csv` sera généré dans le dossier `/merge`.

## Dépendances

- `requests` : pour faire les requêtes HTTP.
- `beautifulsoup4` : pour parser le contenu HTML.
- `pandas` : pour manipuler et fusionner les données.

