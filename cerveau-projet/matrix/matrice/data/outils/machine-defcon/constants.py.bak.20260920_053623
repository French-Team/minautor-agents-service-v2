"""Constantes de l'outil machine-defcon : chemins et echelle defcon fermee.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_OUTIL) + " n'est pas dans data/outils/"
    )

# Le niveau courant vit dans le classeur-variables (cle defcon) : UNE source de verite.
CLE_DEFCON = "defcon"
CHEMIN_CLASSEUR = REPERTOIRE_DATA / "classeur-variables.json"
CHEMIN_EMPREINTE_CLASSEUR = REPERTOIRE_DATA / "classeur-variables.json.sha256"
NOM_CLASSEUR_TMP = "classeur-variables.tmp"

# Journal append-only des transitions (une ligne JSON par transition).
NOM_JOURNAL = "defcon-historique.jsonl"
CHEMIN_JOURNAL = REPERTOIRE_DATA / NOM_JOURNAL

ENCODAGE = "utf-8"
INDENTATION_JSON = 2
TAILLE_BLOC_LECTURE = 65536

# L'echelle defcon est FERMEE (decision createur, convention des crochets).
# 1 = reserve (jamais atteint : la descente s'arrete a 2), 2 = normal,
# 3 = surveiller puis valider, 4 = suivi de bout en bout, 5 = max.
NIVEAU_NORMAL = 2
NIVEAUX = (1, 2, 3, 4, 5)
NIVEAUX_MONTABLES = (3, 4, 5)
DESCENTES_PERMISES = ((5, 4), (4, 3))

NOMS_NIVEAUX = {
    1: "reserve (non defini par l'operateur)",
    2: "normal",
    3: "surveiller puis valider (la validation clot def3)",
    4: "suivi des problemes a resoudre, de bout en bout",
    5: "stop de l'agent par defaut (cameleon a venir), maintenance reveillee",
}

# A defcon 5, seul ce theme reste injectable (garde posee dans le pilote).
THEME_DEFCON = "DEFCON"

# data/commun (motif unique M-076) : installe le dossier partage dans sys.path.
_courant = REPERTOIRE_OUTIL
for _ in range(30):
    if (_courant / "commun" / "racine.py").is_file():
        sys.path.insert(0, str(_courant / "commun"))
        break
    _courant = _courant.parent
else:
    raise RuntimeError("data/commun introuvable en remontant.")

from racine import detecter_racine  # noqa: E402

RACINE = detecter_racine(REPERTOIRE_OUTIL)

# --- LES DECLENCHEURS (voie A, 2026-09-19, EO-181) -------------------------
# Un declencheur est une CONDITION MESUREE par une PORTE REELLE : jamais un
# sentiment, jamais une valeur qu'on s'invente. Chaque entree NOMME les quatre
# choses que la demande du createur exige -- le FAIT mesure, le MESUREUR (la
# porte qui rend le verdict), le SEUIL (le verdict qui declenche) et la TRACE
# du declenchement (celle de `monter` : defcon-historique.jsonl, append-only).
# Un declencheur ecrit mais JAMAIS BRANCHE serait un declencheur MORT : c'est
# exactement le defaut que l'audit EO-181 a trouve, et pourquoi la table est
# consommee par le verbe `surveiller`, lui-meme appele par la veille.
#
# NIVEAU : chaque declencheur DIT le niveau qu'il pose. 5 = stop de l'agent par
# defaut (mise en securite) ; 4 = suivi de bout en bout. JAMAIS de BAISSE : un
# declencheur MONTE, il ne redescend pas -- la descente reste une DECISION, par
# la porte de la machine (5 -> 4 -> 3 -> 2, et `valider` pour clore def3).
# Un mesureur INTROUVABLE ou en echec n'est PAS un declenchement : il est
# RAPPORTE (une mesure qu'on ne peut pas faire ne doit jamais passer pour une
# mesure qui dit non).
DECLENCHEURS = (
    {
        "id": "perimetre-write",
        "fait": "une ecriture constatee HORS de matrix/ dans la fenetre du garde",
        "mesureur": "_operateur/optimus-prime/super-combos/combos/outils/garde-perimetre-write.py",
        "arguments": ("--racine", ".", "--jours", "7"),
        "seuil": "code 1 (PERIMETRE VIOLE)",
        "niveau": 5,
    },
    {
        "id": "marbre-hors-porte",
        "fait": "une BDD du MARBRE ne s'accorde plus avec sa porte (regles, protocoles, conventions)",
        "mesureur": "matrice/data/outils/verifier-regles/main.py",
        "arguments": ("verifier",),
        "seuil": "code 1 (BDD en ecart)",
        "niveau": 5,
    },
    {
        "id": "perimetre-tmp",
        "fait": "une zone jetable hors de son domicile, ou privee de son README",
        "mesureur": "_operateur/optimus-prime/super-combos/combos/outils/garde-tmp.py",
        "arguments": ("--racine", "."),
        "seuil": "code 1 (ecarts de perimetre temporaire)",
        "niveau": 4,
    },
)
