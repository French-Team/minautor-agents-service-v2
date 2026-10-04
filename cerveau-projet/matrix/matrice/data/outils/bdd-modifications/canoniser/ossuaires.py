"""Categorie `solder-orphelines` : solder les fiches dont le FICHIER n'existe plus.

LE TROU, MESURE (MO-577, 2026-10-04). Sur 1174 cles de la BDD, 213 ne
designaient aucun fichier : absentes du disque ET absentes de l'historique git
(0 commit). Elles portaient 275 entrees d'historique. Elles n'etaient pas
fautives de FORME -- `verifier_cles_canoniques` les laissait passer, et
`canoniser` ne pouvait rien en faire (la forme etait deja correcte). Elles
etaient donc muettes : un registre qui porte des fiches mortes sans le dire
laisse croire a une histoire complete.

CE QUE CETTE CATEGORIE FAIT. Elle ne DISPARAIT rien et n'efface rien (L-055) :
elle porte chaque fiche orpheline dans un champ temoin, avec son nom, ses
entrees entieres, ses tags et le MOTIF. Un solder sans temoin serait un
effacement, et un effacement ne se repare pas.

CE QU'ELLE NE FAIT PAS, ET LE DIT. Elle ne decide pas si un fichier doit
revenir : elle constate que la CLE ne designe plus rien et la met au registre
des ossuaires, ou elle reste lisible et reversible. Si le fichier revient, la
fiche se relit telle quelle -- c est le point.

LE LOT EST UN LIEU UNIQUE, comme `fusionner_cles`. Une regle reecrite ici
divergerait en silence de celle de la porte (M-076 / L-029) : la fonction
prend donc `designer` en ARGUMENT et ne connait pas l'escalier.
"""
from canoniser.fonctions import recenser_modifications

# LE CHAMP DES OSSUAIRES. Son nom vit ICI et l'auto-test le relit : une seule
# forme, ecrite et lue au meme endroit (M-076).
CHAMP_OSSUAIRES = "ossuaires"


def solder_les_orphelines(donnees, designer, motif):
    """(rapport, recensement_avant, recensement_apres).

    `designer(cle)` rend la cle ANCREE ou une valeur fausse : c'est la regle du
    domicile (`cible.niveau_de_chemin`), passee en argument.

    Le MULTISET des entrees est rendu AVANT et APRES, comme pour `fusionner_cles` :
    l'appelant REFUSE une migration qui perdrait une entree. Un compte ne
    prouve rien -- une entree peut disparaitre pendant qu'une autre se duplique
    (L-032).
    """
    fichiers = donnees.get("fichiers", {}) or {}
    recensement_avant = recenser_modifications(donnees)
    rapport = []
    ossuaires = donnees.setdefault(CHAMP_OSSUAIRES, [])
    for cle in sorted(list(fichiers)):
        if designer(cle):
            continue
        fiche = fichiers.pop(cle)
        ossuaires.append({
            "cle": cle,
            "modifications": list(fiche.get("modifications", []) or []),
            "retraits": list(fiche.get("retraits", []) or []),
            "tags": list(fiche.get("tags", []) or []),
            "motif": motif,
        })
        rapport.append((cle, len(fiche.get("modifications", []) or [])))
    return rapport, recensement_avant, recenser_modifications(donnees)