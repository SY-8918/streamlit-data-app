import time
from datetime import datetime, timezone
from faker import Faker
import snowflake.connector
from cryptography.hazmat.primitives import serialization

with open("rsa_key.p8", "rb") as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), password=None)
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

conn = snowflake.connector.connect(
    user="ZEBRA",
    account="HAB33465",
    private_key=private_key_bytes,
    role="TRAINING_ROLE",
    warehouse="E_ZEBRA_WH",
    database="TPY_ANALYSE_RH",
    schema="PUBLIC"
)
cursor = conn.cursor()

fake = Faker()
Faker.seed(42)

try:
    i = 1
    while True:
        sensor_id = fake.uuid4()
        ts = datetime.now(timezone.utc)
        temperature = round(fake.pyfloat(min_value=15, max_value=35), 2)
        humidity = round(fake.pyfloat(min_value=30, max_value=90), 2)
        location = fake.city()

        cursor.execute(
            """
            INSERT INTO IOT_SENSOR_TABLE
            (SENSOR_ID, TS, TEMPERATURE, HUMIDITY, LOCATION)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (sensor_id, ts, temperature, humidity, location)
        )

        conn.commit()
        print(f"Ligne {i} insérée : {sensor_id}")

        i += 1
        time.sleep(10)  # pause de 10 secondes entre chaque insertion

finally:
    cursor.close()
    conn.close()
