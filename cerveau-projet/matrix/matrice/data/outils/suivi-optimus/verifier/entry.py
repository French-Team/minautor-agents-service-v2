"""Categorie verifier : orchestre le controle d'integrite de la BDD suivi-optimus.jsonl.

Interface entre main.py et les fonctions simples (verifier/fonctions.py).
Verifie SHA-256 + coherence debut/fin (marbre, Flux 2) -- ainsi la correction
de l'usage d'Optimus est ENFERMEE dans l'outil lui-meme.
"""
from commun import calculer_empreinte_si_existe, lire_empreinte, lire_evenements
from constants import CHEMIN_BDD
from verifier.fonctions import verifier_coherence, verifier_integrite


def executer(arguments):
    empreinte_enregistree = lire_empreinte()
    empreinte_reelle = calculer_empreinte_si_existe(CHEMIN_BDD)
    succes_sha, message_sha = verifier_integrite(empreinte_reelle, empreinte_enregistree)
    print(message_sha)
    if not succes_sha:
        return 1
    # Coherence debut/fin (marbre) : Optimus declare debut puis fin.
    evenements = lire_evenements()
    ok_coherence, messages_coherence, _stats = verifier_coherence(evenements)
    for msg in messages_coherence:
        print(msg)
    return 0 if ok_coherence else 1
