import os
import crypt
import re

def is_password_secure(password):
    """ Vérifie si un mot de passe respecte les critères de sécurité """
    criteria = {
        "longueur_minimum": len(password) >= 12,
        "majuscule": any(c.isupper() for c in password),
        "minuscule": any(c.islower() for c in password),
        "caractere_special": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    }

    return all(criteria.values()), [critere for critere, valid in criteria.items() if not valid]

def create_user(username, password):
    valid, details = is_password_secure(password)
    if not valid:
        print(f"❌ Impossible de créer l'utilisateur {username} car son mot de passe est faible : {details}")
        return

    encrypted_password = crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))
    os.system(f"sudo useradd -m -p '{encrypted_password}' {username}")
    print(f"✅ Utilisateur {username} créé avec succès !")

# Test du script
nom = input("Entrez le nom d'utilisateur : ")
mdp = input("Entrez son mot de passe : ")
create_user(nom, mdp)
