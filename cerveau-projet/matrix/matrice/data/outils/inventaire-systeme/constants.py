"""Constantes de l outil inventaire-systeme : domicile de la fiche et perimetre.

Zero valeur en dur : la logique CONSOMME ces valeurs, elle ne les contient pas.

LA FICHE et LA PORTE (MO-251) :
  - la FICHE vit dans matrice/data/systeme-machine.md, a cote des autres fiches de
    la Matrice (manuel-outils.md, data-readme.md) : c est le domicile UNIQUE des
    informations systeme (EO-154, une seule maison par valeur) ;
  - la PORTE qui la tient a jour est CET outil, et lui seul ecrit la fiche.

Le MODELE est la v1 (cerveau-projet/agents/tools/verifier/verifier-systeme,
v0.2.3-py) : meme mesure (OS, architecture, ressources, shells, langages, outils),
meme forme de sortie. Ce qui est ajoute ici : la carte d identite (regle de la
Matrice), la section RESUME MACHINE que l injection du pilote sert aux missions,
et la porte de VERIFICATION (la fiche contre la machine, mesuree, pas supposee).
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_OUTIL) + " n est pas dans data/outils/"
    )

NOM_FICHE = "systeme-machine.md"
CHEMIN_FICHE = REPERTOIRE_DATA / NOM_FICHE
CHEMIN_TMP = CHEMIN_FICHE.with_name(CHEMIN_FICHE.name + ".tmp")
ENCODAGE = "utf-8"
NF = "\n"

# La CARTE D IDENTITE de la fiche : les trois cles exigees par le garde
# verifier-cartes-identite, et un type de son vocabulaire ferme.
CARTE_IDENTITE = (
    "---",
    "identite:",
    "  type: fiche",
    "  appartient_a: matrice",
    "  commun: true",
    "---",
)

TITRE_FICHE = "# SYSTEME DE LA MACHINE -- fiche de la Matrice"
# La section COURTE que l injection du pilote sert (entree `contexte-machine` du
# catalogue). Elle est demandee PAR SON NOM : renommer la section sans corriger le
# catalogue ferait un refus nomme a la source suivante, jamais un silence.
TITRE_RESUME = "## RESUME MACHINE"
# L entree du catalogue d injection qui consomme cette fiche (la relation
# fiche <-> pilote est DITE ici, et verifiee par le verbe `verifier`).
ID_INJECTION = "contexte-machine"
CHEMIN_CATALOGUE = (Path("_operateur") / "optimus-prime" / "pilote" / "injection"
                    / "config.json")

# Les BRIQUES sondees sur la machine : le nom cherche dans le PATH et la commande
# de version. UNE seule table, consommee par la mesure ET par la verification.
# La commande de version est un TUPLE : subprocess recoit une LISTE d arguments
# (aucun shell, donc rien a interpreter et rien a injecter).
OUTILS_SONDES = (
    {"nom": "python3", "version": ("--version",)},
    {"nom": "pip3", "version": ("--version",)},
    {"nom": "node", "version": ("--version",)},
    {"nom": "npm", "version": ("--version",)},
    {"nom": "git", "version": ("--version",)},
    {"nom": "bash", "version": ("--version",)},
    {"nom": "rg", "version": ("--version",)},
)
DELAI_VERSION = 10

# LE REGISTRE Windows (MO-319) : la cle de CLASSE des cartes graphiques et les deux
# valeurs lues -- le nom du pilote affiche (DriverDesc) et la memoire video en
# OCTETS (HardwareInformation.qwMemorySize, une valeur 64 BITS). C est cette cle,
# et pas AdapterRAM (DWORD signe plafonne a 4 Go), qui dit la VRAIE VRAM.
# Le SEPARATEUR de chemin Windows, ecrit par son CODE (chr 92) et non par un
# antislash litteral : mesure du 2026-09-20 (MO-319) -- un antislash traverse le
# shell et se fait DOUBLER ou PERDRE selon le transport, exactement le defaut
# declare par MO-286. Un code ne se deforme pas.
SEPARATEUR = chr(92)
CLASSE_CARTES_GRAPHIQUES = "4d36e968-e325-11ce-bfc1-08002be10318"
VALEUR_DESC = "DriverDesc"
VALEUR_VRAM = "HardwareInformation.qwMemorySize"

# Les champs de la mesure qui SONT repris dans la fiche et re-mesures par
# `verifier` : un ecart sur l un d eux est un ecart de la fiche (elle a perime).
CHAMPS_COMPARES = (
    ("systeme", "OS", "os"),
    ("systeme", "Architecture", "arch"),
    ("systeme", "Hote", "hote"),
    ("outils", "python3", "python3"),
    ("outils", "node", "node"),
    ("outils", "git", "git"),
)
CASES_RESUME = ("Machine", "CPU", "RAM", "Disque libre", "GPU", "Reseau", "Outils",
                "Racine de la Matrice")

# data/commun (motif unique M-076) : installe le dossier partage dans sys.path en
# REMONTANT jusqu a lui -- jamais un parents[N] nu (le nombre d etages n est pas
# une adresse stable).
_courant = REPERTOIRE_OUTIL
for _ in range(30):
    if (_courant / "commun" / "racine.py").is_file():
        sys.path.insert(0, str(_courant / "commun"))
        break
    _courant = _courant.parent
else:
    raise RuntimeError("data/commun introuvable en remontant.")

from cible import racine_matrice  # noqa: E402

RACINE_MATRIX = racine_matrice(REPERTOIRE_OUTIL)
CHEMIN_CATALOGUE_ABSOLU = RACINE_MATRIX / CHEMIN_CATALOGUE
