# generate_keys.py
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Générer la clé privée
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Sauvegarder la clé privée (NE JAMAIS COMMIT DANS GIT !)
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
with open('rsa_key.p8', 'wb') as f:
    f.write(pem)

# Extraire et sauvegarder la clé publique
pub_pem = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
with open('rsa_key.pub', 'wb') as f:
    f.write(pub_pem)

print("Clés générées ! Copiez le contenu de rsa_key.pub dans Snowflake :")
print(pub_pem.decode())

