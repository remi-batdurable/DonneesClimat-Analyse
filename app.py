import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(layout="wide")

# Titre de l'application
st.title("Analyse des Données Météorologiques")

# Panneau latéral pour charger les fichiers
st.sidebar.title("Charger les fichiers CSV")
uploaded_files = {}
uploaded_files["été chaud"] = st.sidebar.file_uploader("Fichier projet été chaud", type=["csv"])
uploaded_files["prospectif"] = st.sidebar.file_uploader("Fichier projet prospectif", type=["csv"])
uploaded_files["référence"] = st.sidebar.file_uploader("Fichier de référence (observations)", type=["csv"])
uploaded_files["TRACC"] = st.sidebar.file_uploader("Fichier prospectif TRACC", type=["csv"])

# Dictionnaire pour stocker les données
data = {}

# Charger les fichiers dans des DataFrames
for name, file in uploaded_files.items():
    if file is not None:
        data[name] = pd.read_csv(file)

# Onglets
tab1, tab2 = st.tabs(["Analyse d'un fichier", "Comparaison"])

# Onglet 1 : Analyse d'un fichier
with tab1:
    st.header("Analyse d'un fichier")

    # Sélection du fichier à analyser
    file_to_analyze = st.selectbox("Choisir le fichier à analyser", list(data.keys()))

    if file_to_analyze in data:
        df = data[file_to_analyze]

        # Afficher le graphe de l'évolution de la température
        st.subheader(f"Évolution de la température pour {file_to_analyze}")
        fig, ax = plt.subplots()
        ax.plot(df)
        ax.set_xlabel("Temps (heures)")
        ax.set_ylabel("Température (°C)")
        st.pyplot(fig)

        # Paramètres pour les seuils
        st.subheader("Nombre de jours où la température dépasse un seuil")
        seuil = st.number_input("Seuil de température (°C)", value=30.0)

        # Calculer le nombre de jours où la température dépasse le seuil
        jours_depasse = (df.iloc[:, 0] > seuil).sum()
        st.write(f"Nombre d'heures où la température dépasse {seuil}°C : {jours_depasse}")

# Onglet 2 : Comparaison
with tab2:
    st.header("Comparaison des fichiers")

    if len(data) >= 2:
        # Calcul du RMSE mensuel
        st.subheader("Comparaison mensuelle du RMSE")

        # Supposons que les données sont au pas de temps horaire et sur une année
        mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

        # Exemple de calcul du RMSE entre deux fichiers (à adapter selon tes données)
        ref_name = "référence"
        if ref_name in data:
            ref_data = data[ref_name].iloc[:, 0].values
            rmse_results = {}

            for name, df in data.items():
                if name != ref_name:
                    test_data = df.iloc[:, 0].values
                    rmse = np.sqrt(np.mean((ref_data - test_data) ** 2))
                    rmse_results[name] = rmse

            # Afficher les résultats
            st.write("RMSE par rapport au fichier de référence :")
            for name, rmse in rmse_results.items():
                st.write(f"- {name} : {rmse:.2f}")
    else:
        st.warning("Veuillez charger au moins deux fichiers pour effectuer une comparaison.")
