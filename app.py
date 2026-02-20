import streamlit as st
import pandas as pd
from streamlit import cache_data

@cache_data
def load_data(file):
    return pd.read_csv(file)

# Charger les fichiers
uploaded_files = st.file_uploader(
    "Chargez jusqu'à 4 fichiers CSV (8760 lignes × 10 colonnes)",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    data = {}
    for i, file in enumerate(uploaded_files):
        data[f"fichier_{i+1}"] = load_data(file)

    # Aperçu des données
    st.header("Aperçu des données")
    for name, df in data.items():
        st.subheader(f"Aperçu de {name}")
        st.dataframe(df.head(100))

    # Statistiques
    st.header("Statistiques")
    for name, df in data.items():
        st.subheader(f"Statistiques pour {name}")
        st.write(df.describe())

    # Visualisation
    st.header("Visualisation")
    colonne = st.selectbox("Choisissez une colonne à visualiser", data["fichier_1"].columns)
    for name, df in data.items():
        st.subheader(f"Visualisation pour {name}")
        st.line_chart(df[colonne].sample(1000))

