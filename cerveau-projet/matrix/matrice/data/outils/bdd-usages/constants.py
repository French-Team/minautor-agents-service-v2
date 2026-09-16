"""Constantes de l'outil bdd-usages.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
# L'outil vit dans outils/bdd-usages/ ; la BDD vit deux niveaux au-dessus (dans data/).
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )

NOM_BDD = "usages-outils-combos.jsonl"
CHEMIN_BDD = REPERTOIRE_DATA / NOM_BDD

# Cles requises dans CHAQUE ligne de la BDD (controle structurel du verifier).
CLES_REQUISES = ("date", "outil", "commande", "code", "tags")

ENCODAGE = "utf-8"

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

# --- CAPACITE DU JOURNAL, DECLAREE PAR SON PROPRIETAIRE (MO-101 / P3) --------
# Ce journal n'etait borne PAR PERSONNE. Sa capacite vivait chez l'OBSERVATEUR
# (cockpit, `SEUILS_PERFS["usages_lignes"] = 50000`, sans proprietaire sur
# disque) alors qu'une rotation PONCTUELLE l'avait ramene a 500 lignes le
# 15/09 (MO-093 : 69519 evenements archives, 0 perdu). Deux politiques sans
# lien : un seuil qui ignore la rotation qui le precede ne mesure rien.
#
# Desormais la valeur appartient ici -- au proprietaire du journal, qui l'ecrit
# ET le borne -- et la rotation y est LIEE (commun.borner_si_necessaire).
#
# MESURES du 2026-09-15 (sequentielle, machine de l'operateur) :
#   245 559 octets / 1259 lignes = 195 octets par ligne ;
#   1259 lignes en 24 h -> ~240 Ko par jour.
#
# LA BORNE SE DEDUIT DU PLUS LONG LECTEUR, pas d'un gout : `bilan-periode`
# accepte `--periode mois` = 30 jours, soit ~38 000 lignes (~7,2 Mo). Une borne
# qui garderait moins que ce que le plus long lecteur demande casserait ce
# lecteur en silence -- c'est le piege que la revue redoutait.
#   -> declencheur 16 Mo (~68 jours) et 40 000 evenements gardes (~30 jours) :
#      chaque rotation libere ~8 Mo (~34 jours) et laisse TOUJOURS au moins les
#      30 jours que `--periode mois` reclame.
SEUIL_OCTETS_JOURNAL = 16 * 1024 * 1024
EVENEMENTS_GARDES_JOURNAL = 40000
ESSAIS_ROTATION = 3
NOM_ARCHIVE_PREFIXE = "usages-outils-combos-archive"
CHEMIN_RELATIF_JOURNAL = Path("matrice") / "data" / NOM_BDD
