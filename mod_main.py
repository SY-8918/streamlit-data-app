# test_connection_youness.py
import os
from snowflake.connector import connect
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# ==================== CONFIG ====================
ACCOUNT = "HAB33465"         # sans .snowflakecomputing.com
USER = "ZEBRA"
PRIVATE_KEY_PATH = "rsa_key.p8"
WAREHOUSE = "E_ZEBRA_WH"
DATABASE = "YOUNESS_STREAMING_LAB"
SCHEMA = "PUBLIC"

# ==================== LOAD PRIVATE KEY ====================
def load_private_key(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Clé introuvable : {path}")

    with open(path, "rb") as f:
        key_data = f.read()

    # Vérification format PKCS#8
    if b"ENCRYPTED" in key_data:
        raise ValueError("Clé chiffrée détectée ! Utilisez une clé NON chiffrée (PKCS#8).")
    if b"RSA PRIVATE KEY" in key_data and b"PRIVATE KEY" not in key_data:
        raise ValueError("Format PKCS#1 détecté ! Snowflake exige PKCS#8.")

    return serialization.load_pem_private_key(
        key_data,
        password=None,
        backend=default_backend()
    )

# ==================== CONNECT ====================
try:
    print("🔧 Chargement de la clé privée...")
    private_key = load_private_key(PRIVATE_KEY_PATH)

    # Conversion en BYTES PKCS#8 DER
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    print("🔌 Connexion à Snowflake...")
    conn = connect(
        user=USER,
        account=ACCOUNT,
        private_key=private_key_bytes,
        warehouse=WAREHOUSE,
        database=DATABASE,
        schema=SCHEMA
    )

    print("✅ Connexion réussie !")

    cur = conn.cursor()

    # ==================== CREATE DATABASE & TABLE ====================
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
    cur.execute(f"USE DATABASE {DATABASE}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {DATABASE}.{SCHEMA}.SIMPLE_DATA (
            id INT,
            name STRING,
            value FLOAT,
            created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)
    print(f"✅ Base {DATABASE} et table SIMPLE_DATA prêtes")

    # ==================== INSERT TEST DATA (optionnel) ====================
    test_data = [
        (1, "Capteur A", 23.5),
        (2, "Capteur B", 18.2),
        (3, "Capteur C", 29.8)
    ]
    for row in test_data:
        cur.execute(
            f"INSERT INTO {DATABASE}.{SCHEMA}.SIMPLE_DATA (id, name, value) VALUES (%s, %s, %s)",
            row
        )
    print("✅ Données test insérées")

    cur.close()
    conn.close()

    print("\n🎉 TOUT EST OK")

except Exception as e:
    print("\n❌ ERREUR")
    print(type(e).__name__)
    print(e)
    print("\n💡 Vérifie : clé privée, droits, account/user, warehouse, database")
