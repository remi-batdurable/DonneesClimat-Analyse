import streamlit as st
import pandas as pd
from streamlit import cache_data

@cache_data
def load_data(file):
    return pd.read_csv(file)

st.title("Analyse de Données Climatiques")

# Créer 4 uploaders distincts
st.subheader("Chargez vos fichiers CSV")
uploaded_file_1 = st.file_uploader("Fichier 1 - Chargez votre fichier CSV (8760 lignes × 10 colonnes)", type=["csv"], key="file1")
uploaded_file_2 = st.file_uploader("Fichier 2 - Chargez votre fichier CSV (8760 lignes × 10 colonnes)", type=["csv"], key="file2")
uploaded_file_3 = st.file_uploader("Fichier 3 - Chargez votre fichier CSV (8760 lignes × 10 colonnes)", type=["csv"], key="file3")
uploaded_file_4 = st.file_uploader("Fichier 4 - Chargez votre fichier CSV (8760 lignes × 10 colonnes)", type=["csv"], key="file4")

# Traiter les fichiers uploadés
files = {
    "Fichier 1": uploaded_file_1,
    "Fichier 2": uploaded_file_2,
    "Fichier 3": uploaded_file_3,
    "Fichier 4": uploaded_file_4
}

for file_name, uploaded_file in files.items():
    if uploaded_file:
        st.subheader(file_name)
        df = load_data(uploaded_file)

        # Aperçu des données
        st.write("**Aperçu des données**")
        st.dataframe(df.head(100))  # Affiche les 100 premières lignes

        # Statistiques
        st.write("**Statistiques**")
        st.write(df.describe())

        # Visualisation d'une colonne
        st.write("**Visualisation**")
        colonne = st.selectbox("Choisissez une colonne à visualiser", df.columns, key=f"selectbox_{file_name}")
        st.line_chart(df[colonne])
        
        st.divider()