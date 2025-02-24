import spwd
import crypt

def load_common_passwords(rockyou_path):
    """Charge les mots de passe communs depuis le fichier rockyou.txt"""
    with open(rockyou_path, "r", encoding="latin-1") as file:
        return [line.strip() for line in file]

def brute_force_passwords(rockyou_path):
    """Tente de deviner les mots de passe des utilisateurs en comparant avec rockyou.txt"""
    common_passwords = load_common_passwords(rockyou_path)

    for entry in spwd.getspall():
        username, hashed_password = entry.sp_nam, entry.sp_pwdp

        if hashed_password in ["!", "*", ""] or "$" not in hashed_password:
            continue

        for password in common_passwords:
            if crypt.crypt(password, hashed_password) == hashed_password:
                print(f"⚠️ Mot de passe trouvé pour {username}: {password}")
                break 

rockyou_file = "rockyou.txt"
brute_force_passwords(rockyou_file)
