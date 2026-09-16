#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-cadence.py -- Garde : une routine tient-elle la cadence qu'elle DECLARE ?

Pourquoi (friction 28, 2026-09-14) : `veille-flux` a tourne a 6,0 s d'ecart median
contre 300 s declarees, les 09-11 (10 494 passes) et 09-12 (8 960) -- 20 219 passes
en trop, ~5,6 h de CPU, ~39 000 lignes de journal, 19 500 appels a `corriger-ascii`,
et PERSONNE ne l'a vu pendant 3 jours. Le seul temoin fut la TAILLE du journal,
constatee trois jours plus tard (MO-078). La cause n'etait pas la routine : sa
cadence etait DECLAREE dans ses constantes et PUBLIEE dans un etat court, mais
RIEN ne MESURAIT son battement reel. Ce garde est la troisieme jambe.

LE PIEGE QUE CE GARDE A PAYE, ET QUI EXPLIQUE SA FORME (meme jour). Le premier
battement a ete lu comme `(date - derniere_ecriture) / passes_absorbes` : une
MOYENNE. Or une moyenne ne decrit AUCUN intervalle reel des qu'une passe n'est
pas a l'heure (redemarrage, passe A LA DEMANDE). Mesure sur `vigie-profil`, dont
le journal PROUVE la cadence a 900 s et dont le compteur est juste (prouve :
3 -> 4 en une passe) : la MEME cadence a ete lue 450,5 s puis 600,3 s. Une
valeur fausse mais DANS la tolerance ne crie pas -- c'est le pire des temoins,
il rassure. Ce garde lit donc une SERIE d'horodatages et un ecart MEDIAN, jamais
une moyenne : un redemarrage deplace la mediane d'un cran, il ne divise plus le
resultat par deux.

CE QU'IL EXIGE, pour chacune des SIX routines du serveur `vie` :

  1. la cadence DECLAREE se lit a UN seul endroit : le fichier de constantes
     designe par la table (le garde ne recopie aucune valeur, il dit OU lire --
     et il RESOUT les renvois, car `INTERVALLE_DECLARE_SECONDES = INTERVALLE_SECONDES`) ;

  2. le BATTEMENT REEL se mesure dans une SERIE d'horodatages, selon le temoin
     que la routine expose :
       - `serie`      : la queue BORNEE d'un journal, lue par le moteur PARTAGE
                        `rotation_journal` (jamais recopiee) ;
       - `serie-etat` : l'ANNEAU DE PASSES garde dans un etat court
                        (`dernieres_passes`), ecrit par la routine avec le moteur
                        PARTAGE `data/commun/battement.py` ;
     et l'ecart est le MEDIAN de cette serie (moteur PARTAGE, jamais recopie) ;

  3. la comparaison TOLERE les ecarts normaux et ACCUSE les derives :
       - trop vite : battement < cadence / 2 (la rafale : 6 s contre 300 s) ;
       - trop lent : battement > cadence * 3 ;
       - arretee   : age de la derniere passe > cadence * 3 + marge, ET un PID
                     existe (sans PID, la routine est hors service par choix :
                     on le DIT au lieu d'accuser -- un non-controle assume) ;
       - un etat ECRIT SANS anneau de passes -> ACCUSE : le battement n'est plus
         mesurable, et un controle muet ne doit pas passer pour un controle vert ;
       - recul insuffisant -> `[--]` : la cadence DECLAREE fait foi et le garde
         DIT explicitement < ne pas attendre > (l'anneau de passes se remplit
         SEUL) -- jamais un faux vert, et jamais une invitation a patienter :
         une preuve se LIT, elle ne s'ATTEND pas (regle immuable
         `attente-ne-prouve-rien.md`, GO createur 2026-09-14).

  4. l'AUTOTEST rejoue l'incident REEL et la MESURE QUI MENSAIT (lecon L-032) :
     la rafale a 6,0 s contre 300 s doit etre ACCUSEE, l'override a 60 s aussi, un
     battement normal non ; et sur la SERIE REELLE du 14-09 (un ecrit a 06:55:28,
     des passes a 900 s, une passe A LA DEMANDE a 07:27:43) le MEDIAN doit rendre
     900 s -- l'intervalle reel -- la ou l'ancienne regle rendait 645 s, une
     valeur qui ne decrit AUCUN intervalle de la serie.

  5. la FABRIQUE est CABLEE : chaque routine a temoin `serie-etat` doit DECLARER
     `PASSES_GARDEES_ETAT` et `CLE_ANNEAU_PASSES` dans ses constantes et APPELER
     le moteur partage (`ajouter_passe(`) dans la source qui ecrit son etat. Sans
     ce controle, on peut retirer l'anneau et laisser le garde afficher `[--]`
     pour toujours -- un controle qui ne dit plus rien.

CE QU'IL NE FAIT PAS : il ne touche RIEN, ne lance AUCUN processus de routine, et
ne lit que des fichiers d'etat et de journal -- en QUEUE BORNEE. Les fichiers de
service ne sont jamais modifies (un garde qui ecrit dans le service n'est plus un
garde, lecon L-040).

Usage: python verifier-cadence.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = racine introuvable.
"""

import argparse
import importlib.util
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# --- REFERENCES (aucune valeur en dur dans la logique) ----------------------
# Les DEUX moteurs PARTAGES : la queue bornee d'un journal, et le battement
# (anneau + ecart median). Charges par leur CHEMIN, jamais recopies (L-029).
MODULE_ROTATION = Path("matrice") / "data" / "commun" / "rotation_journal.py"
MODULE_BATTEMENT = Path("matrice") / "data" / "commun" / "battement.py"
# Fenetre de lecture : PLUS DE NOMBRE ICI (MO-099). Elle vient du moteur PARTAGE,
# qui la deduit de la borne que le journal lu declare lui-meme
# (`SEUIL_OCTETS_JOURNAL` : 2 Mo veille, 8 Mo espion, 512 Ko vigies) : une queue
# plus petite que la borne declaree laisserait une rotation cacher des passes.

# Tolerances de la comparaison (nommees, jamais dispersees dans la logique).
FACTEUR_TROP_VITE = 0.5
FACTEUR_TROP_LENT = 3.0
FACTEUR_ARRET = 3.0
MARGE_ARRET_SECONDES = 60

FORMAT_HORODATAGE = "%Y-%m-%d %H:%M:%S"

# Doctrine (regle immuable `attente-ne-prouve-rien.md`, GO createur 2026-09-14) :
# un manque de recul ne se repare JAMAIS en attendant -- il se DIT. Le premier jet
# de ce garde laissait croire qu'il fallait trois passes (30 min) pour lire un
# battement : le repli est la cadence DECLAREE, et ce marqueur l'interdit.
MARQUEUR_NE_PAS_ATTENDRE = "NE PAS ATTENDRE"
MOTIF_ASSIGNATION = re.compile(
    r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*(\d+|[A-Z][A-Z0-9_]*)\s*(?:#.*)?$"
)

# Fabrique de l'anneau : les DEUX noms que la source d'une routine a temoin
# `serie-etat` doit declarer et appeler. Ils sont NOMMES ici parce que le garde
# les cherche dans la source ; ils vivent, eux, dans les constantes de chaque
# routine (un seul nom par chose).
CONSTANTE_LONGUEUR_ANNEAU = "PASSES_GARDEES_ETAT"
CONSTANTE_CLEF_ANNEAU = "CLE_ANNEAU_PASSES"
APPEL_FABRIQUE_ANNEAU = "ajouter_passe("

# --- TABLE DES ROUTINES -----------------------------------------------------
# (routine, fichier des constantes, constante de cadence, fichier PID, temoin,
#  source qui ecrit l'anneau).
# Le fichier PID est DECLARE : deux routines ne le nomment pas comme leur dossier
# (`espion.pid`, `routeur.pid`) -- l'inventer ferait croire une routine "hors
# service" qui tourne tres bien (premier passage de ce garde).
# Le temoin est : ("serie", journal, marqueur) -- la queue bornee du journal ;
#                 ("serie-etat", etat, clef) -- l'anneau de passes de l'etat.
# La source (6e champ) n'est renseignee que pour les temoins `serie-etat` :
# c'est la ou l'anneau est ECRIT, donc la ou le garde verifie que la fabrique
# partagee est bien appelee.
# Aucune valeur de cadence n'est recopiee : chaque routine reste la seule voix.
ROUTINES = (
    (
        "veille-flux",
        Path("matrice/routines/veille-flux/constants.py"),
        "INTERVALLE_DECLARE_SECONDES",
        Path("matrice/routines/veille-flux/veille-flux.pid"),
        ("serie", Path("matrice/routines/veille-flux/journal-veille.txt"), "passe-debut"),
        None,
    ),
    (
        "espion-integrite",
        Path("matrice/routines/espion-integrite/constants.py"),
        "INTERVALLE_DECLARE_SECONDES",
        Path("matrice/routines/espion-integrite/espion.pid"),
        ("serie", Path("matrice/routines/espion-integrite/espion-log.jsonl"), "passe"),
        None,
    ),
    (
        "vigie-profil",
        Path("matrice/routines/vigie-profil/constants.py"),
        "INTERVALLE_DECLARE_SECONDES",
        Path("matrice/routines/vigie-profil/vigie-profil.pid"),
        ("serie-etat", Path("matrice/routines/vigie-profil/vigie-profil-etat-passes.json"),
         "dernieres_passes"),
        Path("matrice/routines/vigie-profil/tour/entry.py"),
    ),
    (
        "vigie-portes",
        Path("matrice/routines/vigie-portes/constants.py"),
        "INTERVALLE_DECLARE_SECONDES",
        Path("matrice/routines/vigie-portes/vigie-portes.pid"),
        ("serie-etat", Path("matrice/routines/vigie-portes/vigie-portes-etat-passes.json"),
         "dernieres_passes"),
        Path("matrice/routines/vigie-portes/tour/fonctions.py"),
    ),
    (
        "suivi-sync",
        Path("matrice/routines/suivi-sync/constants.py"),
        "INTERVALLE_DECLARE_SECONDES",
        Path("matrice/routines/suivi-sync/suivi-sync.pid"),
        ("serie-etat", Path("matrice/routines/suivi-sync/suivi-sync-etat.json"),
         "dernieres_passes"),
        Path("matrice/routines/suivi-sync/commun.py"),
    ),
    (
        "routeur-maintenance",
        Path("matrice/routines/routeur-maintenance/routeur.py"),
        "INTERVALLE_DECLARE_SECONDES",
        Path("matrice/routines/routeur-maintenance/routeur.pid"),
        ("serie-etat", Path("matrice/routines/routeur-maintenance/routeur-etat.json"),
         "dernieres_passes"),
        Path("matrice/routines/routeur-maintenance/routeur.py"),
    ),
)

RESULTATS = []


def trouver_matrix(racine):
    """Retourne le dossier matrix/, ou None."""
    candidats = [racine / "cerveau-projet" / "matrix", racine / "matrix"]
    if racine.name == "matrix":
        candidats.insert(0, racine)
    for candidat in candidats:
        if (candidat / "matrice").is_dir():
            return candidat
    return None


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def charger_module(matrix, chemin_relatif, nom_module):
    """Un moteur PARTAGE, charge par son CHEMIN (jamais recopie)."""
    chemin = matrix / chemin_relatif
    if not chemin.is_file():
        return None
    specification = importlib.util.spec_from_file_location(nom_module, str(chemin))
    module = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(module)
    except Exception:  # noqa: BLE001 -- un moteur illisible est un ECHEC dit, pas un plantage
        return None
    return module


def horodate(texte):
    """datetime d'un horodatage du format unique, ou None (jamais d'exception)."""
    try:
        return datetime.strptime(str(texte), FORMAT_HORODATAGE)
    except (TypeError, ValueError):
        return None


def lire_texte(chemin):
    """Contenu d'un fichier, ou "" (un fichier illisible ne fait pas tomber un garde)."""
    try:
        return Path(chemin).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def lire_json(chemin):
    """JSON d'un fichier, ou {} (jamais d'exception dans un garde)."""
    try:
        return json.loads(Path(chemin).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def cadence_declaree(chemin, nom):
    """Valeur de la constante de cadence, lue dans SON fichier (renvois resolus).

    `INTERVALLE_DECLARE_SECONDES = INTERVALLE_SECONDES` est la forme reelle : on
    resout donc les renvois (bornes) au lieu d'exiger un nombre la ou il n'y en a
    pas. Rien n'est importe : les modules `constants` des routines portent tous le
    meme nom (lecon L-029), un import les ferait se marcher dessus.
    """
    valeurs = {}
    for ligne in lire_texte(chemin).splitlines():
        resultat = MOTIF_ASSIGNATION.match(ligne)
        if resultat:
            valeurs[resultat.group(1)] = resultat.group(2)
    courant = nom
    vus = set()
    while courant is not None and courant not in vus:
        vus.add(courant)
        valeur = valeurs.get(courant)
        if valeur is None:
            return None
        if valeur.isdigit():
            return int(valeur)
        courant = valeur
    return None


# --- SERIES D'HORODATAGES ---------------------------------------------------

def serie_journal(chemin, marqueur, moteur_rotation):
    """Horodatages d'un marqueur, depuis la QUEUE BORNEE d'un journal."""
    horodatages = []
    if not chemin.is_file() or moteur_rotation is None:
        return horodatages
    for ligne in moteur_rotation.lire_queue_journal(
        chemin, moteur_rotation.octets_queue_du_journal(chemin)
    ):
        if not ligne.strip():
            continue
        try:
            donnees = json.loads(ligne)
        except ValueError:
            continue
        if marqueur and str(donnees.get("type")) != marqueur:
            continue
        if donnees.get("date"):
            horodatages.append(str(donnees.get("date")))
    return horodatages


def serie_etat(chemin, clef):
    """(horodatages, clef_presente) : l'anneau de passes garde dans un etat court."""
    donnees = lire_json(chemin)
    return list(donnees.get(clef) or []), (clef in donnees)


# --- DECISION (PURE) --------------------------------------------------------

def juger(cadence, battement, age, pid_vivant):
    """(etat, motif) : DECISION PURE -- aucune horloge, aucun disque, aucun import.

    `etat` vaut "OK", "KO" ou "--" (non-controle ASSUME, jamais un faux vert).
    """
    if cadence is None:
        return "--", "cadence declaree illisible"
    if age is not None and not pid_vivant:
        return "--", "sans PID : routine hors service (non controle)"
    if age is not None and age > cadence * FACTEUR_ARRET + MARGE_ARRET_SECONDES:
        return "KO", ("arretee : derniere passe il y a " + str(int(age)) + " s"
                      + " (cadence declaree " + str(cadence) + " s)")
    if battement is None:
        return "--", ("recul insuffisant pour mesurer un battement : la cadence"
                      " DECLAREE (" + str(cadence) + " s) fait foi -- "
                      + MARQUEUR_NE_PAS_ATTENDRE + ", cet anneau se remplit SEUL")
    if battement < cadence * FACTEUR_TROP_VITE:
        return "KO", ("trop vite : " + str(round(battement, 1)) + " s de battement"
                      + " pour " + str(cadence) + " s declarees")
    if battement > cadence * FACTEUR_TROP_LENT:
        return "KO", ("trop lent : " + str(round(battement, 1)) + " s de battement"
                      + " pour " + str(cadence) + " s declarees")
    return "OK", (str(round(battement, 1)) + " s de battement pour "
                  + str(cadence) + " s declarees")


def controler_decision_pure():
    """La decision est PURE : elle se rejoue sans disque ni horloge."""
    cas = (
        ("battement conforme", juger(300, 302.0, 1.0, True), "OK"),
        ("rafale a 6 s accusees", juger(300, 6.0, 1.0, True), "KO"),
        ("override a 60 s accuse", juger(300, 60.0, 1.0, True), "KO"),
        ("trop lent accuse", juger(300, 4000.0, 1.0, True), "KO"),
        ("routine arretee accuse", juger(300, None, 100000.0, True), "KO"),
        ("sans PID : non controle", juger(300, None, 100000.0, False), "--"),
        ("recul insuffisant : non controle", juger(300, None, 1.0, True), "--"),
    )
    echecs = [nom for nom, (etat, _), attendu in cas if etat != attendu]
    controler("decision-pure", not echecs,
              str(len(cas)) + " cas" + ("" if not echecs else " : ECHECS " + str(echecs)))
    return echecs


def controler_autotest():
    """L'incident REEL doit etre ACCUSE (lecon L-032) : la rafale de la friction 28."""
    rafale_veille_flux = 6.0        # ecart median mesure les 09-11 et 09-12
    override_vie = 60.0             # l'override du serveur, avant correction
    cadence_veille_flux = 300
    accusees = [valeur for valeur in (rafale_veille_flux, override_vie)
                if juger(cadence_veille_flux, valeur, 1.0, True)[0] == "KO"]
    conforme = juger(cadence_veille_flux, 301.0, 1.0, True)[0] == "OK"
    controler("autotest-rafale-reelle-accusee", len(accusees) == 2 and conforme,
              "la rafale (6,0 s) et l'override (60 s) contre 300 declarees : "
              + str(len(accusees)) + "/2 ACCUSE(s) ; un battement conforme reste OK")

    # Le manque de recul ne doit jamais se lire comme < attends trois passes >.
    etat_recul, motif_recul = juger(900, None, 1.0, True)
    recul_parle = etat_recul == "--" and MARQUEUR_NE_PAS_ATTENDRE in motif_recul
    controler("autotest-recul-ne-pas-attendre", recul_parle,
              "un recul insuffisant rend la cadence DECLAREE et DIT '"
              + MARQUEUR_NE_PAS_ATTENDRE + "' (regle immuable : une preuve se LIT)")

    echecs = [] if (len(accusees) == 2 and conforme) else ["l'autotest n'accuse pas l'incident reel"]
    if not recul_parle:
        echecs.append("un recul insuffisant n'interdit pas explicitement d'attendre")
    return echecs


def controler_battement(moteur_battement):
    """Le MEDIAN doit resister a ce qui a fait mentir la MOYENNE (L-032).

    On rejoue la SERIE REELLE du 2026-09-14 sur `vigie-profil` : un ecrit a
    06:55:28 (passe notable), des passes a 900 s (07:10:29, 07:25:29), puis une
    passe A LA DEMANDE a 07:27:43 -- l'intervalle irregulier qui a fait dire 450,5
    s puis 600,3 s a l'ancienne regle `(dernier - premier) / passes_absorbes`.
    """
    if moteur_battement is None:
        controler("autotest-mediane-robuste", False,
                  "moteur PARTAGE introuvable : " + str(MODULE_BATTEMENT))
        return ["moteur de battement introuvable"]
    serie = ("2026-09-14 06:55:28", "2026-09-14 07:10:29",
             "2026-09-14 07:25:29", "2026-09-14 07:27:43")
    median, _ = moteur_battement.battement_median(serie, FORMAT_HORODATAGE)
    debut = horodate(serie[0])
    fin = horodate(serie[-1])
    ancienne = (fin - debut).total_seconds() / (len(serie) - 1)
    controler("autotest-mediane-robuste",
              median == 900 and abs(ancienne - 645) < 1,
              "MEME serie : mediane " + str(median) + " s (un intervalle REEL de la serie)"
              " contre ancienne regle " + str(round(ancienne, 1)) + " s (qui ne decrit"
              " AUCUN intervalle de la serie)")

    suite = moteur_battement.ajouter_passe([], "2026-09-14 00:00:00", 3)
    for rang in range(1, 5):
        suite = moteur_battement.ajouter_passe(suite, "2026-09-14 00:0" + str(rang) + ":00", 3)
    borne = len(suite) == 3 and suite[-1] == "2026-09-14 00:04:00"
    controler("autotest-anneau-borne", borne,
              "5 ajouts avec une longueur de 3 : la suite en garde " + str(len(suite))
              + " (un etat ne grandit pas)")

    peu = moteur_battement.battement_median(("2026-09-14 00:00:00",), FORMAT_HORODATAGE)
    controler("autotest-recul-dit", peu[0] is None,
              "un seul horodatage : aucun ecart median rendu (le manque de recul se DIT)")

    if median == 900 and abs(ancienne - 645) < 1 and borne and peu[0] is None:
        return []
    return ["le battement en mediane ne se comporte pas comme exige"]


def controler_fabrique(matrix):
    """Chaque routine a temoin `serie-etat` doit DECLARER et APPELER la fabrique.

    Sans ce controle, on peut retirer l'anneau de passes : le garde afficherait
    alors `[--]` pour toujours, et un controle qui ne dit plus rien passe pour un
    controle vert.
    """
    echecs = []
    for nom, chemin_constantes, _, _, temoin, source in ROUTINES:
        if temoin[0] != "serie-etat":
            continue
        declarations = lire_texte(matrix / chemin_constantes)
        manquants = [constante for constante in (CONSTANTE_LONGUEUR_ANNEAU, CONSTANTE_CLEF_ANNEAU)
                     if constante not in declarations]
        appel = APPEL_FABRIQUE_ANNEAU in lire_texte(matrix / source) if source else False
        detail = (nom + " : declare " + CONSTANTE_LONGUEUR_ANNEAU + " + " + CONSTANTE_CLEF_ANNEAU
                  + " et appelle " + APPEL_FABRIQUE_ANNEAU.rstrip("("))
        if manquants or not appel:
            echecs.append(nom)
            detail = (nom + " : ECART -- manquant " + str(manquants)
                      + (" ; " + APPEL_FABRIQUE_ANNEAU + " ABSENT de " + str(source) if not appel else ""))
        controler("fabrique-cablee-" + nom, not manquants and appel, detail)
    return echecs


def controler_routine(matrix, nom, chemin_constantes, constante, chemin_pid, temoin,
                      moteur_rotation, moteur_battement, maintenant):
    """Controle UNE routine : cadence declaree vs battement reel."""
    cadence = cadence_declaree(matrix / chemin_constantes, constante)
    if cadence is None:
        controler(nom, False, "cadence declaree ILLISIBLE (" + str(chemin_constantes)
                  + ", constante " + constante + ")")
        return nom + " : cadence declaree illisible"

    genre = temoin[0]
    chemin_temoin = matrix / temoin[1]
    anneau_absent = False
    if genre == "serie":
        horodatages = serie_journal(chemin_temoin, temoin[2], moteur_rotation)
        source = "journal " + temoin[1].name + " (" + temoin[2] + ")"
    else:
        horodatages, clef_presente = serie_etat(chemin_temoin, temoin[2])
        source = "etat " + temoin[1].name + " (" + temoin[2] + ")"
        # Un etat ECRIT mais SANS anneau : la routine tourne et la mesure a
        # disparu. C'est un ECART, pas un manque de recul -- le dire, sinon le
        # garde afficherait `[--]` pour toujours.
        anneau_absent = bool(chemin_temoin.is_file()) and not clef_presente

    if anneau_absent:
        controler(nom, False, "[KO] etat ecrit SANS anneau de passes : le battement"
                  " n'est plus mesurable (la serie est le seul temoin)")
        return nom + " : anneau de passes absent de " + temoin[1].name

    battement, dernier = (moteur_battement.battement_median(horodatages, FORMAT_HORODATAGE)
                          if moteur_battement is not None else (None, None))
    pid_vivant = (matrix / chemin_pid).is_file()
    age = (maintenant - dernier).total_seconds() if dernier is not None else None
    etat, motif = juger(cadence, battement, age, pid_vivant)

    controler(nom, etat != "KO",
              "[" + etat + "] " + motif + " [declaree " + str(cadence) + " s, lue dans "
              + chemin_constantes.name + " ; battement lu dans " + source + "]")
    return None if etat != "KO" else nom + " : " + motif


def main():
    parser = argparse.ArgumentParser(description="Garde : une routine tient sa cadence declaree")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = parser.parse_args()

    matrix = trouver_matrix(Path(arguments.racine).resolve())
    if matrix is None:
        print("Dossier matrix/ introuvable sous " + str(arguments.racine))
        return 2

    ecarts = []
    print("VERIFIER CADENCE -- le battement REEL contre la cadence DECLAREE")
    print("-- la decision (pure) --")
    ecarts += controler_decision_pure()
    ecarts += controler_autotest()

    moteur_rotation = charger_module(matrix, MODULE_ROTATION, "moteur_lecture_cadence")
    controler("moteur-lecture-bornee", moteur_rotation is not None,
              "moteur partage charge par son chemin (lecture bornee de la queue)"
              if moteur_rotation is not None else "moteur PARTAGE introuvable : " + str(MODULE_ROTATION))
    if moteur_rotation is None:
        ecarts.append("moteur de lecture bornee introuvable")

    moteur_battement = charger_module(matrix, MODULE_BATTEMENT, "moteur_battement_cadence")
    controler("moteur-battement", moteur_battement is not None,
              "moteur partage charge par son chemin (anneau borne + ecart MEDIAN)"
              if moteur_battement is not None else "moteur PARTAGE introuvable : " + str(MODULE_BATTEMENT))
    if moteur_battement is None:
        ecarts.append("moteur de battement introuvable")

    print("-- le battement (le median resiste a ce qui a fait mentir la moyenne) --")
    ecarts += controler_battement(moteur_battement)

    controler("table-complete", len(ROUTINES) == 6,
              str(len(ROUTINES)) + " routine(s) declaree(s) avec leur temoin")

    print("-- la fabrique de l'anneau est-elle cablee --")
    ecarts += controler_fabrique(matrix)

    print("-- le battement des routines --")
    maintenant = datetime.now()
    for nom, chemin_constantes, constante, chemin_pid, temoin, _ in ROUTINES:
        ecart = controler_routine(matrix, nom, chemin_constantes, constante, chemin_pid,
                                  temoin, moteur_rotation, moteur_battement, maintenant)
        if ecart:
            ecarts.append(ecart)

    if ecarts:
        print("\nVERDICT KO : une routine ne tient pas la cadence qu'elle declare"
              " (voir les ecarts nommes).")
        return 1
    print("\nVERDICT OK : chaque routine tient la cadence qu'elle declare"
          " (ou son manque de recul est DIT).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
