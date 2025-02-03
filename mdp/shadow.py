import spwd

def load_common_passwords(rockyou_path):
    """Charge les mots de passe communs depuis le fichier rockyou.txt"""
    with open(rockyou_path, "r", encoding="latin-1") as file:
        return {line.strip() for line in file}

def check_shadow_passwords(rockyou_path):
    """Vérifie si des utilisateurs utilisent un mot de passe commun"""
    common_passwords = load_common_passwords(rockyou_path)
    users_to_warn = []

    for entry in spwd.getspall():
        if entry.sp_pwdp in common_passwords:
            users_to_warn.append(entry.sp_nam)

    if users_to_warn:
        print("❌ Ces utilisateurs doivent changer de mot de passe :", ", ".join(users_to_warn))
    else:
        print("✅ Aucun mot de passe faible détecté")

rockyou_file = "rockyou.txt"
check_shadow_passwords(rockyou_file)
