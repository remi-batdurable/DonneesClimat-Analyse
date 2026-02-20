import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Application d'analyse de données climatiques")

# Panneau latéral pour charger les fichiers
st.sidebar.title("Charger les données")
uploaded_files = st.sidebar.file_uploader(
    "Déposez vos fichiers CSV ici :",
    type=["csv"],
    accept_multiple_files=True
)

# Vérifier si des fichiers ont été chargés
if uploaded_files:
    # Lire les fichiers CSV
    data = {}
    for i, file in enumerate(uploaded_files):
        data[f"fichier_{i+1}"] = pd.read_csv(file, sep=",")

    # Créer les onglets
    tab1, tab2, tab3 = st.tabs(["Aperçu des données", "Statistiques", "Visualisations"])

    # Contenu de l'onglet 1 : Aperçu des données
    with tab1:
        st.header("Aperçu des données")
        for name, df in data.items():
            st.subheader(f"Fichier : {name}")
            st.write(df.head())

    # Contenu de l'onglet 2 : Statistiques
    with tab2:
        st.header("Statistiques")
        for name, df in data.items():
            st.subheader(f"Statistiques pour {name}")
            st.write(df.describe())

    # Contenu de l'onglet 3 : Visualisations
    with tab3:
        st.header("Visualisations")
        for name, df in data.items():
            st.subheader(f"Graphique pour {name}")
            # Exemple : Sélectionner une colonne numérique pour afficher un graphique
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            if len(numeric_cols) > 0:
                col = st.selectbox(f"Sélectionnez une colonne pour {name}", numeric_cols, key=f"col_{name}")
                st.line_chart(df[col])
            else:
                st.write("Aucune colonne numérique trouvée.")
else:
    st.warning("Veuillez charger au moins un fichier CSV pour commencer l'analyse.")
