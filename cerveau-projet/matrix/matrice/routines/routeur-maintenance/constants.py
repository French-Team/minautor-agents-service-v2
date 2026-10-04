#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Constantes de la routine routeur-maintenance.

POURQUOI CE FICHIER EXISTE (friction du 2026-09-23) : le CONTROLE D'ATTRIBUTION
lit les declarations d'une routine dans SES constantes (`PRODUCTIONS`) -- un
monolithe qui les porte dans son script est une declaration INLISIBLE, donc un
SILENCE (le controle ne devine pas, et il le DIT desormais a chaque passe :
`declarations de routine NON LUES`). Le moule `templates/routine/constants.py.moule`
fait de `constants.py` le domicile des valeurs : ce fichier applique le moule au
DERNIER des neuf qui ne l'avait pas. Le SCRIPT reste `routeur.py` (le moule accepte
qu'un script porte un autre nom : `vie/constants.py` le declare dans sa table), et
il CONSOMME ces valeurs -- aucune n'est recopiee ici (M-076).

Convention zero-valeur-en-dur : la logique consomme ces valeurs, elle ne les
contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_ROUTINE = Path(__file__).resolve().parent
# Alias HISTORIQUE : la boucle en service nommait son dossier BASE depuis sa
# naissance. Meme objet, jamais une seconde valeur -- et le nom du moule reste
# LISIBLE a cote.
BASE = REPERTOIRE_ROUTINE
# Remonter jusqu'a cerveau-projet/matrix
RACINE_MATRIX = None
for p in [REPERTOIRE_ROUTINE, *REPERTOIRE_ROUTINE.parents]:
    if p.name == "matrix" and (p / "matrice").is_dir():
        RACINE_MATRIX = p
        break
if RACINE_MATRIX is None:
    # Jamais un compte de parents (L-013) : la remontee ci-dessus EST l'ancre et son
    # echec doit se DIRE -- un repli compte serait un chemin FAUX et SILENCIEUX.
    raise RuntimeError(
        "Racine matrix/ introuvable en remontant depuis " + str(REPERTOIRE_ROUTINE)
    )
REPERTOIRE_MATRICE = RACINE_MATRIX / "matrice"
REPERTOIRE_OPERATEUR = RACINE_MATRIX / "_operateur"

# Boites
BOITE_MATRICE_IN = REPERTOIRE_MATRICE / "intercom" / "matrice" / "inbox.jsonl"
BOITE_MAINTENANCE_IN = REPERTOIRE_OPERATEUR / "maintenance" / "matrice" / "inbox.jsonl"
HISTORIQUE = REPERTOIRE_ROUTINE / "routeur-historique.jsonl"

# Le PID et le DRAPEAU : noms du MOULE (une routine se nomme partout pareil), avec
# l'alias historique que la logique de la boucle utilise -- meme objet, une seule
# valeur. Le drapeau garde son extension `.flag`, CHOIX de cette boucle (mesure du
# 2026-09-23 : trois extensions differentes pour huit drapeaux ; la table unique du
# serveur de vie dit le nom REEL de chacun, aucune FORME ne pouvait le deviner).
NOM_PID = "routeur.pid"
CHEMIN_PID = REPERTOIRE_ROUTINE / NOM_PID
PID_FILE = CHEMIN_PID
NOM_DRAPEAU_ARRET = "routeur-arret.flag"
CHEMIN_DRAPEAU_ARRET = REPERTOIRE_ROUTINE / NOM_DRAPEAU_ARRET
DRAPEAU_ARRET = CHEMIN_DRAPEAU_ARRET

# LA CADENCE VIT AU PLANNING (decision createur D1, 2026-09-26, MO-429) : elle
# est LUE plus bas, juste APRES l insertion de data/commun (motif unique M-076)
# -- voir le bloc CADENCE PLANNING de ce fichier. Ce bloc ne la CONTIENT plus.

# --- Rotation du journal (MO-079) -------------------------------------------
# Le routeur est le DERNIER journal de routine sans borne. Mesure du 2026-09-14 :
# 1919 lignes / 296 Ko en 2 jours (~30 s par passe). Rien ne s'y supprime jamais :
# le borner, c'est DEPLACER ses evenements anciens dans une archive DATEE.
# Le moteur est PARTAGE (`matrice/data/commun/rotation_journal.py`, motif unique
# M-076) : cette routine ne declare que SES valeurs.
NOM_ARCHIVE_PREFIXE = "routeur-archive"
SEUIL_OCTETS_JOURNAL = 512 * 1024
EVENEMENTS_GARDES_JOURNAL = 500
ESSAIS_ROTATION = 3
NOM_HISTORIQUE = "routeur-historique.jsonl"
NOM_REPERTOIRE = REPERTOIRE_ROUTINE.name
CHEMIN_RELATIF_JOURNAL = Path("matrice") / "routines" / NOM_REPERTOIRE / NOM_HISTORIQUE
# FIN DE PASSE (maillon 3 de la non-regression du flux, MO-478) : l'historique du
# routeur porte une ligne par passe, SANS champ `type`. Aucun marqueur de fin n'est
# donc lisible : le fait est DECLARE `None` (le maillon le DIT), et la vie du
# routeur reste surveillee par le maillon 7.
EVENEMENT_FIN_PASSE = None

# Etat COURT de la cadence EFFECTIVE (une ligne, ecrasee a chaque demarrage).
# Sans lui, la rotation rendrait AVEUGLE le controle de cadence :
# `verifier-sans-attendre` cherchait le `demarrage` DANS LE JOURNAL, et la
# premiere rotation l'aurait emporte dans l'archive -- le controle aurait ete
# neutralise par le nettoyage qu'il surveille (lecon L-040). Un etat se lit dans
# un fichier d'etat, une histoire dans un journal.
NOM_CADENCE = "routeur-cadence.json"
CHEMIN_CADENCE = REPERTOIRE_ROUTINE / NOM_CADENCE

# --- Etat de passe (MO-080) -------------------------------------------------
# L'HISTORIQUE ne portait que des REPETITIONS : mesure du 2026-09-14, 510 lignes
# identiques a la date pres sur 512 (99,4 %), parce que la passe recopiait le
# meme tableau a chaque tour (~150 Ko par jour pour rien).
#
# Un journal est une suite de FAITS ; le tableau courant des boites est un ETAT.
# Le FAIT, ici, c'est : du courrier a ete ROUTE, ou le tableau des ANOMALIES a
# change. Le reste (l'inbox qui se remplit de trafic normal fin-mission /
# retour-lot) s'ecrit comme ETAT -- ecrase a chaque passe.
#
# L'etat porte AUSSI le nombre de passes absorbees depuis la derniere ligne : la
# redondance supprimee est TRACEE, jamais silencieuse -- et il distingue "rien a
# ecrire" de "le routeur est mort".
NOM_ETAT = "routeur-etat.json"
CHEMIN_ETAT = REPERTOIRE_ROUTINE / NOM_ETAT
# L'ANNEAU DES PASSES (friction 28) : les derniers horodatages de passe, pour que
# le battement REEL soit mesurable en MEDIANE. `passes_absorbes` /
# `derniere_ecriture` disent COMBIEN de passes ont ete absorbees, ils ne disent
# pas QUAND -- en tirer une moyenne est faux des qu'une passe n'est pas a
# l'heure (mesure du 2026-09-14 : la meme cadence de 900 s lue 450,5 s puis
# 600,3 s sur les vigies). La fabrique de l'anneau et sa lecture sont le moteur
# PARTAGE `data/commun/battement.py` (L-029), le routeur ne declare QUE la
# longueur.
PASSES_GARDEES_ETAT = 5
CLE_ANNEAU_PASSES = "dernieres_passes"
# TEMOIN DE CADENCE (MO-479) : le fait que `verifier-cadence` lit pour mesurer le
# BATTEMENT REEL, declare ICI (M-076) au lieu d etre recopie dans la table du garde.
# (genre, fichier, clef) : fichier et clef DESIGNENT des constantes du dossier (jamais
# une valeur en double). Aucun temoin = la routine n est PAS mesuree, et le garde le DIT.
TEMOIN_CADENCE = ("anneau", NOM_ETAT, CLE_ANNEAU_PASSES)

# data/commun (motif unique M-076) : l'attente cooperative est PARTAGEE, jamais
# recopiee. Sans elle, un arret demande attendait la cadence entiere en un seul
# `time.sleep`. L'INSERTION dans sys.path vit ICI (invariant 1 du moule) : le
# script importe ces constantes AVANT ses modules partages, donc l'ordre est
# garanti par la lecture du fichier, pas par un voeu.
REPERTOIRE_COMMUN = REPERTOIRE_MATRICE / "data" / "commun"
if not (REPERTOIRE_COMMUN / "attente.py").is_file():
    raise RuntimeError(
        "Motif attente introuvable : " + str(REPERTOIRE_COMMUN / "attente.py")
    )
sys.path.insert(0, str(REPERTOIRE_COMMUN))

# --- CADENCE PLANNING (D1, MO-429) -----------------------------------------
# LA cadence est au PLANNING (vie/planning.json) : ce fichier la LIT a sa
# source partagee, il ne la CONTIENT plus (M-076). Nom CANONIQUE conserve :
# vie etat, le serveur et les gardes lisent INTERVALLE_DECLARE_SECONDES.
from planning_routines import cadence_planning  # noqa: E402

INTERVALLE_DECLARE_SECONDES = cadence_planning('routeur-maintenance')
# L ALIAS historique (la boucle, la doc, les modes d emploi) : meme objet.
INTERVALLE_SECONDS = INTERVALLE_DECLARE_SECONDES

# Types de messages qui ne regardent PAS le routeur (trafic normal des autres
# maillons : le pilote, les fins de mission). Tout AUTRE type non route est
# anormal et doit laisser une trace (voir tour()).
TYPES_NORMAUX = ("fin-mission", "retour-lot")

# LES PRODUCTIONS DE LA ROUTINE : les fichiers qu'elle ECRIT et qui ne sont PAS
# des sources -- ni ses etats courts de forme CONVENTIONNELLE (etat, journal,
# cadence, PID : le controle les reconnait par leur FORME), ni un fichier ecrit a
# la main. Un rapport, un inventaire, la MEMOIRE d'une passe se declarent ICI.
# VIDE, ET VERIFIE VIDE (friction du 2026-09-23) : le routeur ecrit sa cadence
# (`routeur-cadence.json`), son etat (`routeur-etat.json`), son histoire
# (`routeur-historique.jsonl`), son PID, son drapeau et les BOITES (`.jsonl`) --
# toutes des formes ou des declarations lues ailleurs, AUCUNE production propre.
# La liste est donc vide PARCE QUE C'EST VRAI, pas parce qu'on ne l'a pas remplie :
# le jour ou le routeur ecrira un rapport, c'est ici qu'il se declare.
PRODUCTIONS = ()
