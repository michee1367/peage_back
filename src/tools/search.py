
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def trouver_correspondance(nom, liste_noms):
    meilleure_correspondance = process.extractOne(nom, liste_noms, scorer=fuzz.token_sort_ratio)
    return meilleure_correspondance