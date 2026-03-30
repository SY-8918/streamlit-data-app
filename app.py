
# commande pour run app
# streamlit run app.py
#l'application utilise désormais st.fragment pour une mise à jour fluide toutes les 10 secondes.

# import streamlit as st
# import pandas as pd
# import snowflake.connector
# from cryptography.hazmat.primitives import serialization
#
# # --- Configuration de la page ---
# st.set_page_config(page_title="Dashboard IoT Snowflake", layout="wide")
# st.title("🌡️ Monitoring des Capteurs IoT")
#
#
# # --- Connexion Snowflake ---
# @st.cache_resource  # Pour éviter de se reconnecter à chaque clic
# def init_connection():
#     with open("rsa_key.p8", "rb") as key_file:
#         private_key = serialization.load_pem_private_key(key_file.read(), password=None)
#
#     pkb = private_key.private_bytes(
#         encoding=serialization.Encoding.DER,
#         format=serialization.PrivateFormat.PKCS8,
#         encryption_algorithm=serialization.NoEncryption()
#     )
#
#     return snowflake.connector.connect(
#         user="ZEBRA",
#         account="HAB33465",
#         private_key=pkb,
#         role="TRAINING_ROLE",
#         warehouse="E_ZEBRA_WH",
#         database="TPY_ANALYSE_RH",
#         schema="PUBLIC"
#     )
#
#
# conn = init_connection()
#
# # --- Lecture des données ---
# query = "SELECT * FROM IOT_SENSOR_TABLE ORDER BY TS DESC LIMIT 50"
# df = pd.read_sql(query, conn)
#
# # --- Affichage du Dashboard ---
# col1, col2 = st.columns(2)
#
# with col1:
#     st.subheader("Température Moyenne")
#     st.line_chart(df, x="TS", y="TEMPERATURE")
#
# with col2:
#     st.subheader("Humidité")
#     st.bar_chart(df, x="TS", y="HUMIDITY")
#
# st.subheader("Dernières données reçues")
# st.dataframe(df)


########################################################################################
import streamlit as st
import pandas as pd
import snowflake.connector
from cryptography.hazmat.primitives import serialization
import time

# --- Configuration de la page ---
st.set_page_config(page_title="Dashboard IoT temps réel", layout="wide")

# --- Style CSS pour un look "Live" ---
st.markdown("""
    <style>
    .live-indicator {
        color: #ff4b4b;
        font-weight: bold;
        animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

st.title("🌡️ Monitoring IoT Snowflake")


# --- Connexion Snowflake ---
@st.cache_resource
def init_connection():
    with open("rsa_key.p8", "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    pkb = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return snowflake.connector.connect(
        user="ZEBRA",
        account="HAB33465",
        private_key=pkb,
        role="TRAINING_ROLE",
        warehouse="E_ZEBRA_WH",
        database="TPY_ANALYSE_RH",
        schema="PUBLIC"
    )


conn = init_connection()


# --- Fragment : Cette partie se rafraîchit seule toutes les 10 secondes ---
@st.fragment(run_every="10s")
def update_dashboard():
    # Affichage du statut "Live"
    st.markdown(f'<p class="live-indicator">● LIVE - Mise à jour automatique (10s)</p>', unsafe_allow_html=True)

    # Lecture des données les plus récentes
    query = "SELECT * FROM IOT_SENSOR_TABLE ORDER BY TS DESC LIMIT 20"
    df = pd.read_sql(query, conn)

    # Métriques en haut
    m1, m2, m3 = st.columns(3)
    m1.metric("Température Actuelle", f"{df['TEMPERATURE'].iloc[0]} °C")
    m2.metric("Humidité", f"{df['HUMIDITY'].iloc[0]} %")
    m3.metric("Dernière Ville", df['LOCATION'].iloc[0])

    # Graphiques
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Courbe de Température")
        st.line_chart(df, x="TS", y="TEMPERATURE", color="#ff4b4b")

    with col2:
        st.subheader("Niveaux d'Humidité")
        st.bar_chart(df, x="TS", y="HUMIDITY")

    # Tableau de données brute
    with st.expander("Voir les données brutes"):
        st.dataframe(df, use_container_width=True)


# Lancement du dashboard
update_dashboard()
############################################################################################
## Bilan de votre réalisation
##j'ai parcouru tout le cycle de vie d'un projet de données :

##Ingestion : Création d'un script Python utilisant Faker pour simuler des données.

##Stockage : Configuration de Snowflake avec les bons rôles (TRAINING_ROLE) et entrepôts (E_ZEBRA_WH).

##Traitement : Résolution des erreurs de syntaxe SQL et optimisation de l'insertion.

##Consommation : Création d'une application Streamlit pour rendre les données compréhensibles.