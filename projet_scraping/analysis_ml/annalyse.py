import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.linear_model import LinearRegression

# Configuration
st.set_page_config(layout="wide", page_title="Dashboard du Marché de l'Emploi")
st.title("💼 Tableau de Bord du Marché de l'Emploi")

# 📥 Chargement des données brutes
path = r"C:\Users\HP\OneDrive\Nouveau dossier\OneDrive\Desktop\projet_scraping\output\final_jobs_data_cleaned.csv"
df = pd.read_csv(path)

# 🧹 Nettoyage des données
df.columns = df.columns.str.strip().str.title()

df['Experience'] = df['Experience'].astype(str).str.extract(r'(\d+)')
df['Experience'] = pd.to_numeric(df['Experience'], errors='coerce')

required_cols = ['Experience', 'Poste', 'Secteur', 'Ville', 'Niveau_Etude', 'Contrat', 'Date_De_Publication']
df.dropna(subset=required_cols, inplace=True)

df['Date_De_Publication'] = pd.to_datetime(df['Date_De_Publication'], errors='coerce')
df['Annee'] = df['Date_De_Publication'].dt.year

# 💾 Enregistrer le fichier nettoyé
cleaned_path = path.replace("final_jobs_data.csv", "final_jobs_data_cleaned.csv")
df.to_csv(cleaned_path, index=False)

# 🔢 Nb d'offres par secteur et année
annonces_par_annee = df.groupby(['Annee', 'Secteur']).size().reset_index(name='Nb_Annonces')

# 📊 Mise en page
col1, col2 = st.columns([1.3, 1.2])

# ----------------------------------------------------
# 🧠 COLONNE 1 : ANALYSE DES OFFRES D'EMPLOI
# ----------------------------------------------------
with col1:
    st.subheader("📊 Analyse Interne des Offres")

    visualisation = st.selectbox("Choisir une visualisation", [
        "Répartition des emplois par secteur", 
        "Répartition des types de contrat", 
        "Relation entre expérience et secteurs", 
        "Relation entre niveau d'études et types de contrat", 
        "Répartition des emplois par ville", 
        "Top 10 des entreprises qui recrutent", 
        "Répartition de l'expérience par type de contrat", 
        "Expérience moyenne par secteur"
    ])

    fig, ax = plt.subplots(figsize=(10, 5))

    if visualisation == "Répartition des emplois par secteur":
        sns.countplot(x='Secteur', data=df, ax=ax)
        ax.set_title("Répartition des emplois par secteur")
        plt.xticks(rotation=45)

    elif visualisation == "Répartition des types de contrat":
        sns.countplot(x='Contrat', data=df, ax=ax)
        ax.set_title("Répartition des types de contrat")
        plt.xticks(rotation=45)

    elif visualisation == "Relation entre expérience et secteurs":
        sns.boxplot(x='Secteur', y='Experience', data=df, ax=ax)
        ax.set_title("Relation entre l'expérience et les secteurs")
        plt.xticks(rotation=45)

    elif visualisation == "Relation entre niveau d'études et types de contrat":
        sns.countplot(x='Niveau_Etude', hue='Contrat', data=df, ax=ax)
        ax.set_title("Niveau d'études vs Types de contrat")
        plt.xticks(rotation=45)

    elif visualisation == "Répartition des emplois par ville":
        top_villes = df['Ville'].value_counts().head(10).index
        sns.countplot(x='Ville', data=df[df['Ville'].isin(top_villes)], hue='Secteur', ax=ax)
        ax.set_title("Répartition des emplois par ville (Top 10)")
        plt.xticks(rotation=45)

    elif visualisation == "Top 10 des entreprises qui recrutent":
        if 'Entreprise' in df.columns:
            top_entreprises = df['Entreprise'].value_counts().head(10).index
            sns.countplot(x='Entreprise', data=df[df['Entreprise'].isin(top_entreprises)], ax=ax)
            ax.set_title("Top 10 des entreprises qui recrutent")
            plt.xticks(rotation=45)
        else:
            st.warning("La colonne 'Entreprise' est absente du fichier.")

    elif visualisation == "Répartition de l'expérience par type de contrat":
        sns.boxplot(x='Contrat', y='Experience', data=df, ax=ax)
        ax.set_title("Répartition de l'expérience par type de contrat")

    elif visualisation == "Expérience moyenne par secteur":
        secteur_experience = df.groupby('Secteur')['Experience'].mean().sort_values(ascending=False)
        secteur_experience.plot(kind='bar', ax=ax)
        ax.set_title("Expérience moyenne par secteur")
        plt.xticks(rotation=45)

    plt.tight_layout()
    st.pyplot(fig)

# ----------------------------------------------------
# 🔮 COLONNE 2 : PRÉDICTION DES OFFRES D'EMPLOI
# ----------------------------------------------------
with col2:
    st.subheader("🔮 Prédiction des Offres d'Emploi")

    secteurs_valables = annonces_par_annee.groupby('Secteur')['Annee'].nunique()
    secteurs_filtres = secteurs_valables[secteurs_valables >= 2].index.tolist()

    if not secteurs_filtres:
        st.error("Aucun secteur n'a suffisamment d'années pour entraîner un modèle.")
    else:
        secteur_choisi = st.selectbox("Sélectionnez un secteur :", sorted(secteurs_filtres))
        annee_cible = st.slider("Année à prédire :", 2023, 2030, 2025)

        if st.button("Lancer la prédiction"):
            data_sec = annonces_par_annee[annonces_par_annee['Secteur'] == secteur_choisi]
            X = data_sec[['Annee']]
            y = data_sec['Nb_Annonces']

            model = LinearRegression()
            model.fit(X, y)
            pred = model.predict([[annee_cible]])
            st.success(f"📈 Nombre d'offres prévues en {annee_cible} pour '{secteur_choisi}' : {int(pred[0])}")

            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.lineplot(data=data_sec, x='Annee', y='Nb_Annonces', marker='o', ax=ax2, label='Historique')
            ax2.axvline(annee_cible, color='gray', linestyle='--')
            ax2.scatter(annee_cible, pred, color='red', label='Prédiction')

            ax2.set_xticks(range(min(data_sec['Annee']), max(data_sec['Annee']) + 1))
            ax2.set_title(f"Tendance & Prédiction pour '{secteur_choisi}'")
            ax2.set_xlabel('Année')
            ax2.set_ylabel('Nb_Annonces')
            ax2.legend()

            st.pyplot(fig2)

# ----------------------------------------------------
# 🔎 FONCTION DE RECHERCHE DES OFFRES D’EMPLOI
# ----------------------------------------------------
st.write("---")
st.subheader("🔎 Rechercher une offre d'emploi")

search_term = st.text_input("Entrez un mot-clé du poste")
if st.button("Rechercher des offres d'emploi"):
    filtered_offres = df[df['Poste'].str.contains(search_term, case=False, na=False)] if search_term else df

    if filtered_offres.empty:
        st.info("Aucune offre trouvée pour cette recherche.")
    else:
        st.write("### Résultats :")
        st.markdown("""<style>
            .offer-list {
                list-style-type: none;
                padding: 0;
            }
            .offer-item {
                background-color: #f1f1f1;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 5px;
                font-size: 16px;
                color: #333;
            }
            .offer-item:hover {
                background-color: #e1e1e1;
            }
        </style>""", unsafe_allow_html=True)
        st.markdown('<ul class="offer-list">', unsafe_allow_html=True)
        for _, row in filtered_offres.iterrows():
            st.markdown(f'<li class="offer-item">{row["Poste"]}</li>', unsafe_allow_html=True)
        st.markdown('</ul>', unsafe_allow_html=True)

        csv = filtered_offres.to_csv(index=False)
        st.download_button("📥 Télécharger les offres filtrées", csv, "filtered_jobs.csv")
