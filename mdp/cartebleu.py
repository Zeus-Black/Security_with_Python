import hashlib
import itertools

# Hash fourni dans l'exercice
hash_provided = "fa4193dce1e5dc5a77bf77729caaab5f336dd1942e9cd8c6e6a81f766563e44c"

# BIN de la carte (Visa Boursorama, supposé)
bin_prefix = "497010"

def luhn_checksum(card_number):
    """ Vérifie si un numéro de carte est valide avec l'algorithme de Luhn """
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10

def generate_valid_cards(bin_prefix):
    """ Génère toutes les combinaisons possibles des 9 chiffres identifiants """
    for num in itertools.product("0123456789", repeat=9):
        card_body = bin_prefix + "".join(num)
        checksum_digit = (10 - luhn_checksum(card_body + "0")) % 10
        full_card = card_body + str(checksum_digit)
        yield full_card

def test_hash_methods(card_number):
    """ Teste les méthodes de hachage courantes et compare au hash fourni """
    for hash_func in [hashlib.md5, hashlib.sha1, hashlib.sha256]:
        hashed = hash_func(card_number.encode()).hexdigest()
        if hashed == hash_provided:
            print(f"✅ Carte trouvée : {card_number} (Hash: {hash_func.__name__})")
            return card_number
    return None

# Recherche brute-force
for card in generate_valid_cards(bin_prefix):
    if test_hash_methods(card):
        break  # Stoppe dès qu'on trouve la carte valide
