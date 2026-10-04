"""Fonctions simples de la categorie noter : une seule tache chacune."""
from datetime import datetime

# CONTRAT DE TRANSPORT (friction 72, MO-149) : le caractere qui separe une liste
# transportee vit dans son DOMICILE data/commun/transport_listes.py, installe
# dans sys.path par constants.py (motif M-076) -- comme les autres moteurs
# partages importes par le pilote (trace_session, zone_tmp). Cette porte est le
# COUPANT : elle importe le MEME module que le joignant, et ne recopie donc
# jamais la forme (une forme recopiee derive en silence, L-100/L-102).
from transport_listes import decouper_liste


def separer_liste(chaine):
    """Transforme "a, b" en ["a", "b"] (chaine vide -> liste vide).

    Le separateur n'est pas decide ici : il vient de son domicile, d'ou le
    pendant exact du joignant (pilote/commun.py `joindre_liste`).
    """
    return decouper_liste(chaine)


def construire_evenement(mission, theme, action, detail, fichiers, portes, duree_s):
    """Construit UN evenement de la trace (format valide par le createur, M-084)."""
    evenement = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mission": mission,
        "theme": theme,
        "action": action,
        "detail": detail,
        "fichiers": fichiers,
        "portes": portes,
        "duree_s": duree_s,
    }
    return evenement