"""Constantes de l'outil suivi-optimus.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
# L'outil vit dans outils/suivi-optimus/ ; la BDD vit deux niveaux au-dessus (dans data/).
REPERTOIRE_DATA = REPERTOIRE_OUTIL.parent.parent
if REPERTOIRE_DATA.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_DATA) + " n'est pas le dossier data/"
    )

NOM_BDD = "suivi-optimus.jsonl"
NOM_BDD_TMP = NOM_BDD + ".tmp"
CHEMIN_BDD = REPERTOIRE_DATA / NOM_BDD
CHEMIN_EMPREINTE = REPERTOIRE_DATA / (NOM_BDD + ".sha256")

# Actions fermees de la trace (anti-bruit : par EVENEMENT, jamais par fichier).
ACTIONS = (
    "debut",        # debut de mission
    "fin",          # fin de mission avec bilan
    "porte",        # porte officielle utilisee (pilote, lot, tresse, defcon, pause/reprise)
    "depot",        # mission deposee au vrac de l'entonnoir (E-XXX)
    "decision",     # GO / arbitrage du createur
    "decouverte",   # constat d'audit interne (ex : angle mort detecte)
    "purge",        # zone jetable VIDEe par le pilote a la cloture (MO-136/EO-123) :
                    # l'acte est celui du PILOTE, pas de l'agent -- il doit donc etre
                    # une action DECLAREE, comme les autres. Sans cette declaration la
                    # porte noter REFUSAIT l'evenement et la suppression d'une preuve
                    # partait sans trace (mesure MO-136 : "Action inconnue : 'purge'").
    "bilan",        # bilan-periode demande et rendu
)

ENCODAGE = "utf-8"
TAILLE_BLOC_LECTURE = 65536

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

# Vue markdown dediee (decision createur 2026-09-09) : visuel lisible de la
# trace, dans matrice/ (comme journal-multi-encarts.md), jamais edite a la main.
REPERTOIRE_MATRICE = RACINE / "cerveau-projet" / "matrix" / "matrice"
NOM_VUE = "suivi-optimus.md"
CHEMIN_VUE = REPERTOIRE_MATRICE / NOM_VUE

# Inbox OPTIMUS (zone privee _operateur/maintenance, invisible cameleon L-016).
# Correction MO-032 : pointait sur l'inbox du CAMELEON (intercom/matrice/inbox.jsonl),
# ce qui comptait ses missions dans la trace d'optimus.
CHEMIN_INBOX = REPERTOIRE_MATRICE.parent / "_operateur" / "maintenance" / "matrice" / "inbox.jsonl"

# File du pilote OPTIMUS (jamais matrice/pilote/file-missions.json, cf. pilote/constants.py).
# Correction MO-032 : lisait la file du CAMELEON (6 missions M-115..M-120 comptees a tort).
CHEMIN_FILE_PILOTE = (
    REPERTOIRE_MATRICE.parent / "_operateur" / "optimus-prime" / "pilote"
    / "file-missions-optimus.json"
)

# Journal OPTIMUS (mission-creee sans mission-terminee = en attente).
# Correction MO-032 : lisait historiques-missions.jsonl du CAMELEON (jamais celui-ci).
CHEMIN_JOURNAL_MISSIONS = REPERTOIRE_DATA / "historiques-missions-optimus.jsonl"

# --- Controle de COHERENCE file du pilote <-> journal (verbe `coherence`) ----
# Le journal et la file sont DEUX traces qui vivent separement : le pilote ecrit
# la file (charger / injecter / fin), l'agent declare le journal (marbre L-020,
# le pilote ne note RIEN). Rien ne les compare -- c'est par ce trou qu'une
# mission close dans la file sans fin declaree passe inapercue.
#
# Racine du croisement : matrix/. Les chemins sont donnes RELATIFS pour que le
# controle accepte une AUTRE racine (--racine) et reste ainsi PROUVABLE sur un
# cobaye (lecon L-032 : un controle qu'on ne peut pas pieger n'est pas un controle).
REPERTOIRE_MATRIX = REPERTOIRE_MATRICE.parent
CHEMIN_RELATIF_FILE_PILOTE = (
    Path("_operateur") / "optimus-prime" / "pilote" / "file-missions-optimus.json"
)
# Missions sorties de la file active par le plafond d'archivage automatique (50).
# Sans elle, toute mission ancienne serait vue comme "inconnue de la file".
CHEMIN_RELATIF_ARCHIVE_PILOTE = (
    Path("_operateur") / "optimus-prime" / "pilote" / "file-missions-optimus-archive.json"
)
CHEMIN_RELATIF_BDD = Path("matrice") / "data" / NOM_BDD

# Seul le prefixe des missions d'optimus est croise : le journal peut porter
# d'autres identifiants (cameleon), ils sont HORS PERIMETRE de ce controle.
PREFIXE_MISSION = "MO-"
# Prefixe des missions du CAMELEON (Flux 1, matrice/pilote/constants.py
# PREFIXE_ID) : l'outil ne le croise pas, il le RECONNAIT pour avertir qu'une
# mission etrangere est notee dans la trace d'Optimus (garde M-030).
PREFIXE_CAMELEON = "M-"
LONGUEUR_NUMERO = 3

STATUT_EN_ATTENTE = "en-attente"
STATUT_EN_COURS = "en-cours"
STATUT_TERMINEE = "terminee"

# Libelles des actions du journal que le croisement consomme.
ACTION_DEBUT = "debut"
ACTION_FIN = "fin"

# --- Archivage des evenements HORS PERIMETRE (verbe `archiver`) --------------
# Le journal est la trace d'OPTMUS. Il a recemporte le 2026-09-12 les missions du
# cameleon (M-XXX) et des libelles d'entonnoir (E-089, AUDIT-NEMESIS) : 184
# evenements qui ne concernent pas Optimus et faussent ses compteurs.
# On les ARCHIVE (rien ne se perd -- jamais de suppression seche) : le journal
# actif est reecrit sans eux, l'empreinte SHA-256 est recalculee.
# Meme discipline que MO-023 (fins orphelines archivees) et MO-029 (rotation).
NOM_ARCHIVE_HORS_PERIMETRE = "suivi-optimus-hors-perimetre.jsonl"
CHEMIN_RELATIF_ARCHIVE_HORS_PERIMETRE = Path("matrice") / "data" / NOM_ARCHIVE_HORS_PERIMETRE
CHEMIN_RELATIF_EMPREINTE = Path("matrice") / "data" / (NOM_BDD + ".sha256")

# --- Doublons debut/fin (option `--doublons` du verbe `archiver`) ------------
# Une mission a UN debut et UNE fin (marbre suivi-optimus) : le controle
# `verifier` remonte tout autre compte en ECART. Le 2026-09-13, le verbe
# `enregistrer` du pilote a DOUBLE MO-061 (2 debuts, 2 fins) en notant un debut
# qui existait deja. Meme discipline que l'archivage hors perimetre : on ne
# SUPPRIME pas, on ARCHIVE, et le PREMIER evenement fait foi (c'est le fait
# d'origine ; le second est la copie accidentelle).
ACTIONS_SINGULIERES = (ACTION_DEBUT, ACTION_FIN)
NOM_ARCHIVE_DOUBLONS = "suivi-optimus-doublons.jsonl"
CHEMIN_RELATIF_ARCHIVE_DOUBLONS = Path("matrice") / "data" / NOM_ARCHIVE_DOUBLONS