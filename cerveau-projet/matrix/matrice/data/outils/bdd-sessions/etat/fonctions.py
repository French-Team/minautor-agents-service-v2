"""Categorie etat : l'ETAT de session, et RIEN d'autre (MO-121).

Le pilote a besoin de SAVOIR s'il doit ouvrir une session : une question,
une reponse, une ligne (lecture bornee, L-068). La regle de lecture vit
dans le moteur partage data/commun/derniere_session.py et le VOCABULAIRE
dans data/commun/trace_session.py (M-076) -- jamais recopies ici.
"""
import json

from constants import CHEMIN_BDD, ENCODAGE

# Moteurs partages (M-076) : data/commun est deja sur sys.path par constants.
from derniere_session import derniere_session  # noqa: E402
from trace_session import MARQUEUR_ETAT  # noqa: E402


def lire_etat():
    """Retourne l'etat de session : 'fermee', 'ouverte' ou 'aucune'."""
    if not CHEMIN_BDD.exists():
        return "aucune"
    with open(CHEMIN_BDD, "r", encoding=ENCODAGE) as flux:
        donnees = json.load(flux)
    entree, etat = derniere_session(donnees.get("sessions", []))
    if entree is None:
        return "aucune"
    return etat


def afficher_etat():
    """Imprime l'etat seul, sous le format stable attendu par les appelants."""
    print(MARQUEUR_ETAT + lire_etat())
    return 0
