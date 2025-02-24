import spwd # type: ignore
import crypt # type: ignore
import sys
import os

def check_weak_passwords():
    if os.geteuid() != 0:
        print("Lancez le script en root (sudo).")
        sys.exit(1)
    try:
        with open("rockyou.txt", "r", encoding="latin-1") as file:
            common_passwords = {line.strip() for line in file}
    except FileNotFoundError:
        print("Fichier rockyou.txt introuvable.")
        sys.exit(1)

    users_to_warn = []

    for entry in spwd.getspall():
        if entry.sp_pwdp in ("*", "!", ""):
            continue  # Ignore comptes désactivés

        salt = "$".join(entry.sp_pwdp.split("$")[:3])  # Récupérer le sel
        if any(crypt.crypt(pwd, salt) == entry.sp_pwdp for pwd in common_passwords):
            users_to_warn.append(entry.sp_nam)

    print("Utilisateurs à alerter :", ", ".join(users_to_warn) if users_to_warn else "Aucun.")

if __name__ == "__main__":
    check_weak_passwords()
