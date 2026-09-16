"""Listes FERMEES de l'entonnoir : types, categories, urgences, regles de classement.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
Une valeur hors liste est REFUSEE : la structure ne derive jamais (decision createur).

NOMMAGE : ce module s'appelle listes.py (PAS constants.py) pour ne pas entrer en
collision avec les modules du pilote (le script importe depuis son propre dossier).
"""
# Echelon 1 : les types de missions (file d'arrivee de l'echelon 0).
# revision : nouveau type (decision createur 2026-09-07, mot-crochet [revision]).
TYPES = ("dev", "reparation", "doc", "audit", "revision")

# Echelon 2 : les categories DANS chaque type (la file-type se deroule ici).
CATEGORIES = {
    "dev": ("outil", "routine", "bdd", "pilote", "matrice", "autre"),
    "reparation": ("outil", "routine", "bdd", "pilote", "marbre", "autre"),
    "doc": ("manuel", "contrat", "lecon", "autre"),
    "audit": ("marbre", "flux", "file", "autre"),
    "revision": ("marbre", "contrat", "regle", "protocole", "autre"),
}

# Categorie par defaut d'un type (quand aucun mot-cle ne parle).
CATEGORIES_DEFAUT = {
    "dev": "autre",
    "reparation": "autre",
    "doc": "autre",
    "audit": "autre",
    "revision": "autre",
}

# Echelon 3 : les niveaux d'urgence (du plus urgent au moins urgent).
URGENCES = ("bloquante", "haute", "normale", "basse")

# Urgence par defaut quand le createur ne precise pas.
URGENCE_DEFAUT = "normale"

# Urgence obligatoire pour une mission deposee par la veille (M-020).
URGENCE_VEILLE = "bloquante"

# Regles de classement propose (echelon 1) : mot-cle dans theme+objectif -> type.
MOTS_CLES_TYPES = (
    ("reparer", "reparation"),
    ("reparation", "reparation"),
    ("raccorder", "dev"),
    ("construire", "dev"),
    ("creer", "dev"),
    ("verifier", "audit"),
    ("audit", "audit"),
    ("documenter", "doc"),
    ("manuel", "doc"),
    ("contrat", "doc"),
    ("revision", "revision"),
    ("reviser", "revision"),
)

# Regles de classement propose (echelon 2) : mot-cle -> categorie.
MOTS_CLES_CATEGORIES = (
    ("outil", "outil"),
    ("bdd", "bdd"),
    ("routine", "routine"),
    ("pilote", "pilote"),
    ("marbre", "marbre"),
    ("manuel", "manuel"),
    ("contrat", "contrat"),
    ("lecon", "lecon"),
    ("protocole", "protocole"),
    ("regle", "regle"),
)

# Prefixe des ITEMS de CET entonnoir (regle CV-009 : une famille = un prefixe,
# jamais partage). E- etait emis par les DEUX entonnoirs avec DEUX compteurs
# separes (cameleon/fichier 89, Optimus/fichier 101) : les deux plages se
# recouvraient (E-084..E-089 emis des deux cotes), donc le meme id designait
# deux items differents -- exactement la maladie de M- (mission d'Optimus
# portant le prefixe du cameleon). Meme remede : Optimus prend SON prefixe.
# Le cameleon garde E- : ses ids sont dans des journaux en AJOUT SEUL
# (historiques-missions.jsonl), un renommage les ferait mentir.
PREFIXE_ITEM = "EO-"

# Chemin du fichier des files de l'entonnoir (a cote de file-missions.json).
# Nom CANONIQUE de l'entonnoir OPTIMUS (alignement MO-033) : le pilote
# (constants.py NOM_ENTONNOIR + commun.py CHEMIN_ENTONNOIR) lit/ecrit deja
# entonnoir-files-optimus.json -- l'outil ecrivait l'ANCIEN nom
# "entonnoir-files.json", donc les missions deposees n'etaient pas vues
# par le pilote. Jamais le nom du cameleon (matrice/pilote/entonnoir-files.json).
NOM_ENTONNOIR = "entonnoir-files-optimus.json"
