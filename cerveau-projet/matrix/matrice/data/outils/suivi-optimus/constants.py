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
    "intervention",  # INTERVENTION du createur sur la mission EN COURS (crochet
                     # `[si]`, 2026-09-21) : une mini-reflexion de remise en question,
                     # tenue PENDANT le round et morte avec lui. Meme lecon que `purge` :
                     # un acte qui n'est pas une action DECLAREE part sans trace -- ici
                     # la porte REFUSAIT l'evenement (mesure : "Action inconnue :
                     # 'intervention'"), donc l'intervention du createur n'aurait
                     # laisse AUCUNE trace lisible apres coup.
    "report",       # mission PARQUEE par le verbe `reporter` (EO-182 / MO-199) :
                    # le pilote la remet en attente, donc le DEBUT est NEUTRALISE
                    # (elle n'est plus en cours) SANS etre termine. Mesure EO-190 :
                    # sans cette action, le garde de coherence voyait un debut sans
                    # fin sur une mission en attente, et son message ACCUSAIT le
                    # pilote de ne pas l'avoir chargee -- un faux diagnostic.
                    # NON SINGULIERE (hors ACTIONS_SINGULIERES) : une mission peut
                    # etre parquee plusieurs fois.
    "charge",       # mission FORGEE par le verbe `charger` du pilote (demande du
                    # createur, 2026-09-22) : l'acte de charger une mission n'etait
                    # trace NULLE PART -- la file portait bien `chargee_le`, mais un
                    # LOT entier partage cet horodatage (mesure du jour : les 30
                    # missions en attente du lot REPRISE DU RETARD portent TOUTES le
                    # meme `chargee_le`), donc < chargee > et < chargee avec d autres >
                    # etaient indiscernables. Consequence mesuree : la CLOTURE FAUSSE
                    # payee en MO-387 (deux missions closes qui n'avaient pas eu lieu,
                    # avec une coherence file <-> journal PARFAITE) n'etait detectable
                    # par AUCUN garde. Meme lecon que `purge` et `intervention` : un
                    # acte qui n'est pas une action DECLAREE part sans trace -- la porte
                    # `noter` REFUSERAIT l'evenement. Le detail porte le NOM DU LOT
                    # quand c'en est un, et rien du tout quand la charge est
                    # individuelle : c'est ce qui separe les deux classes.
                    # NON SINGULIERE : une mission peut etre chargee plusieurs fois.
    "prise",        # PRISE DE ROUND par l agent (EO-360, demande du createur
                    # 2026-09-22) : la doctrine du demarrage PROMETTAIT que la chaine
                    # repart toute seule, mais elle n ecrivait JAMAIS le geste de
                    # boucle -- donc RIEN ne distinguait un round ARME (la machine a
                    # injecte et pose le debut) d un round PRIS (l agent l a recu et
                    # le conduit). Mesure du 2026-09-22 : MO-348 etait en-cours, son
                    # debut etait trace, l injection etait deposee, et PERSONNE ne
                    # l avait pris -- les trois traces disaient d ACCORD et elles
                    # etaient fausses (famille de la cloture fausse de MO-387).
                    # Meme lecon que `purge`, `intervention` et `charge` : un acte qui
                    # n est pas une action DECLAREE part sans trace. Elle est notee par
                    # le GESTE DE RECEPTION (le verbe `injecter` : ORDRE 2 du demarrage
                    # et boucle de l ORDRE 4.7) -- l agent n a rien de plus a jouer.
                    # NON SINGULIERE : un round peut etre repris plusieurs fois.
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
# trace, jamais edite a la main.
# DOMICILE DEPLACE (MO-235, demande createur) : la vue vivait dans `matrice/`
# (comme journal-multi-encarts.md) et n'etait cachee au cameleon que par une
# EXCLUSION DE NOM (`suivi-optimus` est un plancher de data/commun/invisibilite.py).
# Elle vit desormais dans la zone privee `_operateur/optimus-prime/` : elle est
# invisible PAR CONSTRUCTION (la zone `_operateur` est exclue), et non plus par le
# nom d'un fichier -- une protection de FORME tient tant que le nom ne change pas.
REPERTOIRE_MATRICE = RACINE / "cerveau-projet" / "matrix" / "matrice"
REPERTOIRE_OPTIMUS = REPERTOIRE_MATRICE.parent / "_operateur" / "optimus-prime"
NOM_VUE = "suivi-optimus.md"
CHEMIN_VUE = REPERTOIRE_OPTIMUS / NOM_VUE

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
# Action qui NEUTRALISE le debut SANS terminer la mission (EO-190) : elle dit
# "la mission n'est plus en cours" sans dire "elle est finie". C'est l'etat que
# cree le verbe `reporter` -- et le garde de coherence la lit dans l'ORDRE.
ACTION_REPORT = "report"

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
# Le REPORT est volontairement ABSENT de cette liste (EO-190) : un debut et une
# fin sont des BORNES (une seule fois), un report est un EVENEMENT -- une mission
# peut etre parquee plusieurs fois, et c'est la DERNIERE borne qui fait foi.
ACTIONS_SINGULIERES = (ACTION_DEBUT, ACTION_FIN)
NOM_ARCHIVE_DOUBLONS = "suivi-optimus-doublons.jsonl"
CHEMIN_RELATIF_ARCHIVE_DOUBLONS = Path("matrice") / "data" / NOM_ARCHIVE_DOUBLONS