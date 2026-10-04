"""Constantes de l'outil dupliquer-template.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import re
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )
REPERTOIRE_OUTILS = REPERTOIRE_DATA / "outils"
REPERTOIRE_MATRICE = REPERTOIRE_DATA.parent
# Chemin du moule historique (outil BDD) : la generation lit desormais
# `templates/<moule>/` (un dossier par moule), ce chemin reste la reference du
# moule principal, pas une liste de moules possibles.
CHEMIN_MOULE = REPERTOIRE_MATRICE / "templates" / "outil-bdd"
SUFFIXE_MOULE = ".moule"

MOTIF_NOM = re.compile(r"^bdd-[a-z][a-z0-9-]*$")
MOTIF_NOM_THEME = re.compile(r"^theme-[a-z][a-z0-9-]*$")
# Une routine porte un nom de dossier simple (veille-flux, suivi-sync) : forme
# stricte (minuscules, chiffres, tirets), sans prefixe impose.
MOTIF_NOM_ROUTINE = re.compile(r"^[a-z][a-z0-9-]*$")
MOTIF_JETON = re.compile(r"__[A-Z_]+__")

REPERTOIRE_TEMPLATES = REPERTOIRE_MATRICE / "templates"
# Le vivier des routines supervisees : le clone d'une ROUTINE y atterrit (un
# OUTIL atterrit sous data/outils/) -- c'est la seule difference de destination.
REPERTOIRE_ROUTINES = REPERTOIRE_MATRICE / "routines"
# ZONES NOMMEES DE GENERATION (une surcharge + une cible par zone) -----------
# Une zone choisit A LA FOIS le MOULE DE SURCHARGE (des fichiers qui REMPLACENT
# ceux du moule outil-bdd) et le REPERTOIRE ou le clone atterrit -- hors de
# `matrice/` (donc hors du dossier data/outils/ ou la BDD vivrait sinon deux
# niveaux au-dessus). Cette table est la SEULE source : zero valeur en dur.
#
#   - `privee`   : la BDD de raisonnement d OPTIMUS. `_operateur/` est FRERE de
#                  `matrice/` (zone invisible L-016 : le cameleon ne la lit JAMAIS) ;
#   - `cameleon` : la BDD de raisonnement du CAMELEON, dans SON domicile
#                  `agents/cameleon/raisonnement/` -- VISIBLE et PARTAGEE entre
#                  les deux agents (decision createur 2026-09-27 : la BDD du
#                  cameleon est partagee dans la Matrice).
NOM_OPTION_ZONE = "zone"
ZONE_PRIVEE = "privee"
ZONE_CAMELEON = "cameleon"
MOULE_PRIVE = "outil-bdd-prive"
MOULE_CAMELEON = "outil-bdd-cameleon"
REPERTOIRE_OPTIMUS = REPERTOIRE_MATRICE.parent / "_operateur" / "optimus-prime"
REPERTOIRE_CAMELEON = REPERTOIRE_MATRICE.parent / "agents" / "cameleon"
ZONES = {
    ZONE_PRIVEE: {
        "moule": MOULE_PRIVE,
        "repertoire": REPERTOIRE_OPTIMUS / "raisonnement",
    },
    ZONE_CAMELEON: {
        "moule": MOULE_CAMELEON,
        "repertoire": REPERTOIRE_CAMELEON / "raisonnement",
    },
}
MOULE_DEFAUT = "outil-bdd"
MOULE_ROUTINE = "routine"
NOM_MOULE_PRINCIPAL = "main.py.moule"
# Forme de l horodatage que le generateur POSE dans le marqueur de provenance
# d une routine (EO-389) : une seule ecriture, un seul format, lu par le garde.
FORMAT_HORODATAGE_GENERATION = "%Y-%m-%d %H:%M:%S"
# Cadence d'une routine generee, en secondes : celle du modele-mere
# (suivi-sync). Le PLANCHER n'est pas un gout : une routine qui repasse toutes
# les 2 s sollicite le disque sans relache, et rien ne le dirait.
CADENCE_DEFAUT_ROUTINE = 300
PLANCHER_CADENCE_ROUTINE = 5

NOMS_OPTIONS = ("moule", "nom", "bdd", "prefixe", "liste", "champ", "humain",
                "nom-affiche", "role", "cadence", NOM_OPTION_ZONE)

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
