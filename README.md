# 🔒 Projet de Sécurité : Analyse et Protection des Mots de Passe sous Linux

Ce projet a pour but d'évaluer la robustesse des mots de passe des utilisateurs sous Linux, en vérifiant leur conformité aux standards de sécurité et en testant leur vulnérabilité face à une attaque par dictionnaire.

## 🔧 Fonctionnalités

1. **Vérification de la sécurité d'un mot de passe**
   - Teste si un mot de passe respecte les critères de sécurité.
   - Critères : longueur minimale de 12 caractères, au moins une majuscule, une minuscule et un caractère spécial.

2. **Vérification des mots de passe dans `users.txt`**
   - Analyse un fichier contenant les utilisateurs et leurs mots de passe pour identifier les mots de passe faibles.

3. **Création d'un utilisateur avec vérification du mot de passe**
   - Crée un nouvel utilisateur uniquement si son mot de passe est robuste.

4. **Vérification des mots de passe stockés dans `/etc/shadow`**
   - Identifie les utilisateurs ayant un mot de passe présent dans le dictionnaire `rockyou.txt`.

5. **Brute-force sur `/etc/shadow`**
   - Tente de deviner les mots de passe en comparant avec les entrées du fichier `rockyou.txt`.

---

## 💻 Installation et Prérequis

### 🔗 Prérequis
- **Système d'exploitation** : Debian (WSL ou VM)
- **Paquets requis** :
  ```bash
  sudo apt update && sudo apt install -y python3 python3-pip wordlists
  ```
- **Dictionnaire de mots de passe `rockyou.txt`** :
  ```bash
  sudo gzip -d /usr/share/wordlists/rockyou.txt.gz
  ```

---

## 📂 Scripts Disponibles

### 1️⃣ **Vérification de la robustesse d'un mot de passe**
Fichier : `ispasswordsecure.py`

Exécution :
```bash
python3 /mdp/ispasswordsecure.py
```

### 2️⃣ **Vérification des mots de passe dans `users.txt`**
Fichier : `usertxt.py`

Exécution :
```bash
python3 /mdp/usertxt.py
```

### 3️⃣ **Création d'un utilisateur avec vérification**
Fichier : `userverify.py`

Exécution :
```bash
sudo python3 /mdp/userverify.py
```

### 4️⃣ **Vérification des mots de passe stockés dans `/etc/shadow`**
Fichier : `shadow.py`

Exécution :
```bash
sudo python3 /mdp/shadow.py
```

### 5️⃣ **Brute-force sur `/etc/shadow` avec `rockyou.txt`**
Fichier : `bruteforce.py`

Exécution :
```bash
sudo python3 bruteforce.py
```

---

## 🚀 Optimisations et Améliorations
- Utilisation de **`hashcat`** pour accélérer l'attaque brute-force :
  ```bash
  sudo unshadow /etc/passwd /etc/shadow > hashes.txt
  hashcat -m 1800 hashes.txt /Security_with_Python/mdp/rockyou.txt --force
  ```

---

## 💡 Bonnes Pratiques
- Toujours **utiliser des mots de passe complexes** (min. 12 caractères, majuscules, chiffres, caractères spéciaux).
- **Activer l'authentification à deux facteurs (2FA)** sur les comptes sensibles.
- **Surveiller les logs de connexions** pour détecter d'éventuelles tentatives de brute-force.
- **Changer régulièrement les mots de passe** pour minimiser les risques.

---

## 📊 Résultats Attendus
- **Utilisateurs devant changer leur mot de passe** identifiés.
- **Vérification automatisée** de la sécurité des comptes Linux.
- **Test de robustesse des mots de passe** à partir d'une attaque brute-force avec `rockyou.txt`.

---

📖 **Note :** Ces scripts doivent être utilisés uniquement dans un cadre éducatif ou administrateur pour évaluer la sécurité d'un système **dont vous avez l'autorisation**. Toute utilisation malveillante est illégale.
