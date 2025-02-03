import re

def is_password_secure(password):
    criteria = {
        "longueur_minimum": len(password) >= 12,
        "majuscule": any(c.isupper() for c in password),
        "minuscule": any(c.islower() for c in password),
        "caractere_special": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    }

    if all(criteria.values()):
        return True, "Mot de passe valide"
    else:
        return False, [critere for critere, valid in criteria.items() if not valid]

# Test du script
password = input("Entrez un mot de passe à vérifier : ")
valid, details = is_password_secure(password)

if valid:
    print("✅ Mot de passe valide")
else:
    print("❌ Mot de passe invalide, critères non respectés :", details)

