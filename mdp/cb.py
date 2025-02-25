import torch
import hashlib
import itertools
import time

# Activation du GPU Metal sur macOS
device = torch.device("mps")

# Hash fourni dans l'exercice
hash_provided = "fa4193dce1e5dc5a77bf77729caaab5f336dd1942e9cd8c6e6a81f766563e44c"

# BIN Visa (exemple)
bin_prefix = "497010"

# Nombre total de combinaisons possibles (10^9, ajusté avec Luhn)
TOTAL_COMBINATIONS = 10**9 // 10  # On divise par 10 car Luhn élimine certaines cartes

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

def generate_valid_cards(bin_prefix, batch_size=4096):
    """ Génère des batchs de combinaisons de cartes valides """
    batch = []
    total_generated = 0  # Compteur pour la progression
    start_time = time.time()  # Temps de départ

    for num in itertools.product("0123456789", repeat=9):
        card_body = bin_prefix + "".join(num)
        checksum_digit = (10 - luhn_checksum(card_body + "0")) % 10
        full_card = card_body + str(checksum_digit)
        batch.append(full_card)
        total_generated += 1

        # Affichage de la progression toutes les 1%
        if total_generated % (TOTAL_COMBINATIONS // 100) == 0:
            elapsed_time = time.time() - start_time
            progress = (total_generated / TOTAL_COMBINATIONS) * 100
            speed = total_generated / elapsed_time  # Cartes testées par seconde
            estimated_time = (TOTAL_COMBINATIONS - total_generated) / speed if speed > 0 else float("inf")

            print(f"🔄 Progression : {progress:.2f}% | Temps écoulé : {elapsed_time:.2f}s | Estimé restant : {estimated_time:.2f}s | Vitesse : {speed:.2f} cartes/s")

        if len(batch) >= batch_size:
            yield batch
            batch = []

    if batch:
        yield batch

def test_hash_methods(cards):
    """ Teste les méthodes de hachage sur GPU """
    # Conversion en tensor PyTorch (accéléré sur MPS)
    cards_tensor = torch.tensor([list(map(ord, card)) for card in cards], dtype=torch.int8, device=device)

    # Vérification par batch avec SHA-256
    for hash_func in [hashlib.md5, hashlib.sha1, hashlib.sha256]:
        hashed_cards = [hash_func("".join(map(chr, card.tolist())).encode()).hexdigest() for card in cards_tensor.cpu()]
        if hash_provided in hashed_cards:
            index = hashed_cards.index(hash_provided)
            print(f"✅ Carte trouvée : {cards[index]} (Hash: {hash_func.__name__})")
            return cards[index]
    return None

# Recherche GPU optimisée
start_time_global = time.time()  # Début du script global
for batch in generate_valid_cards(bin_prefix, batch_size=4096):  # Test par batch
    if test_hash_methods(batch):
        break  # Stop dès qu'on trouve la carte

# Temps total
end_time_global = time.time()
print(f"✅ Recherche terminée en {end_time_global - start_time_global:.2f}s")
