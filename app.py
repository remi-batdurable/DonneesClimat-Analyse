import streamlit as st
import pandas as pd
from streamlit import cache_data

@cache_data
def load_data(file):
    return pd.read_csv(file)

# Charger le fichier
uploaded_file = st.file_uploader("Chargez votre fichier CSV (8760 lignes × 10 colonnes)", type=["csv"])
if uploaded_file:
    df = load_data(uploaded_file)

    # Aperçu des données
    st.subheader("Aperçu des données")
    st.dataframe(df.head(100))  # Affiche les 100 premières lignes

    # Statistiques
    st.subheader("Statistiques")
    st.write(df.describe())

    # Visualisation d'une colonne
    st.subheader("Visualisation")
    colonne = st.selectbox("Choisissez une colonne à visualiser", df.columns)
    st.line_chart(df[colonne])
