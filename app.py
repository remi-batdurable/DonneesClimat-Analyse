import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Fonction pour calculer le RMSE
def calculer_rmse(serie_reference, serie_test):
    if len(serie_reference) != len(serie_test):
        raise ValueError("Les séries doivent avoir la même longueur.")
    differences = (serie_reference - serie_test) ** 2
    moyenne_differences = np.mean(differences)
    rmse = np.sqrt(moyenne_differences)
    return rmse

# Configuration de la page
st.set_page_config(layout="wide")
st.title("Analyse des Données Météorologiques")

# Panneau latéral pour charger les fichiers
st.sidebar.title("Charger les fichiers CSV")

# Dictionnaire pour stocker les fichiers et leurs noms personnalisés
uploaded_files = {}

# Liste des types de fichiers attendus
file_types = ["été chaud", "prospectif", "référence", "TRACC"]

# Charger chaque fichier avec un champ pour le renommer
for file_type in file_types:
    uploaded_file = st.sidebar.file_uploader(f"Fichier {file_type}", type=["csv"])
    if uploaded_file is not None:
        custom_name = st.sidebar.text_input(f"Nom personnalisé pour {file_type}", value=file_type)
        uploaded_files[custom_name] = uploaded_file

# Dictionnaire pour stocker les données
data = {}

# Charger les fichiers dans des DataFrames
for name, file in uploaded_files.items():
    if file is not None:
        df = pd.read_csv(file, header=None, names=["temperature"])
        data[name] = df

# Onglets
tab1, tab2 = st.tabs(["Analyse d'un fichier", "Comparaison"])

# Onglet 1 : Analyse d'un fichier
with tab1:
    st.header("Analyse d'un fichier")
    if data:
        file_to_analyze = st.selectbox("Choisir le fichier à analyser", list(data.keys()))
        df = data[file_to_analyze]

        # Générer les dates et heures pour l'axe x
        start_date = datetime(2023, 1, 1, 0, 0)
        dates = [start_date + timedelta(hours=i) for i in range(len(df))]
        df["date"] = dates

        # Afficher le graphe de l'évolution de la température
        st.subheader(f"Évolution de la température pour {file_to_analyze}")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df["date"], df["temperature"], label="Température (°C)")
        ax.set_xlabel("Date et heure")
        ax.set_ylabel("Température (°C)")
        ax.set_ylim(0, 50)
        ax.grid(True)
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Paramètres pour les seuils
        st.subheader("Nombre d'heures où la température dépasse un seuil")
        seuil = st.number_input("Seuil de température (°C)", value=30.0)

        # Calculer le nombre d'heures où la température dépasse le seuil
        heures_depasse = (df["temperature"] > seuil).sum()
        st.write(f"Nombre d'heures où la température dépasse {seuil}°C : {heures_depasse}")
    else:
        st.warning("Veuillez charger au moins un fichier CSV.")

# Onglet 2 : Comparaison
with tab2:
    st.header("Comparaison des fichiers")

    if len(data) >= 2:
        st.subheader("Comparaison mensuelle du RMSE")

        # Sélection du fichier de référence
        ref_name = st.selectbox("Choisir le fichier de référence", list(data.keys()))

        if ref_name in data:
            ref_data = data[ref_name]["temperature"].values
            rmse_results = {}

            for name, df in data.items():
                if name != ref_name:
                    test_data = df["temperature"].values
                    rmse = calculer_rmse(ref_data, test_data)
                    rmse_results[name] = rmse

            # Afficher les résultats
            st.write("RMSE par rapport au fichier de référence :")
            for name, rmse in rmse_results.items():
                st.write(f"- {name} : {rmse:.2f}")
    else:
        st.warning("Veuillez charger au moins deux fichiers pour effectuer une comparaison.")
