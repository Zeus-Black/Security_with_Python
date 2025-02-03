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

def check_users_passwords(file_path="users.txt"):
    """ Vérifie les mots de passe des utilisateurs dans un fichier """
    with open(file_path, "r") as file:
        for line in file:
            user, password = line.strip().split(":")
            valid, details = is_password_secure(password)
            if not valid:
                print(f"❌ {user} doit changer son mot de passe : {details}")
            else:
                print(f"✅ {user} a un mot de passe valide")

# Test du script
check_users_passwords()
