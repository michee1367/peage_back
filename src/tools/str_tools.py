import random
import string

def generer_chaine_alea(taille=10):
    caracteres = string.ascii_letters + string.digits  # lettres + chiffres
    return ''.join(random.choice(caracteres) for _ in range(taille))

