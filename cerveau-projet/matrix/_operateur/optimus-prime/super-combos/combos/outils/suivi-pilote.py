#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""suivi-pilote.py -- LA PORTE DU SUIVI DU PILOTE (T2 de la chaine PB-003/SP-003/TD-003).

POURQUOI (demande createur, EO-273) : < creer le SUIVI DU PILOTE d Optimus : le fichier
qui permet de reperer les problemes DU PILOTE, comme suivi-optimus le fait pour les
missions >. Suivi-optimus regarde les missions ; ce suivi regarde le PILOTE : une file
qui ne repart pas, un lot perdu, une injection refusee, un enchainement casse, une pause
armee et oubliee.

CE QU'IL EST : une VUE DERIVEE. Les faits du pilote vivent deja ailleurs (suivi-optimus,
file-missions, entonnoir, cycle-historique, outbox, journal des pauses). Cette porte ne
les recopie PAS : elle les LIT, les RASSEMBLE sous l angle PILOTE, et n ECRIT que ce
qu'elle a JUGE -- un verdict de panne. Aucun fait n'est ecrit deux fois (L-055).

CE QU'IL ECRIT (deux fichiers, deux natures) :
  - suivi-pilote.md    : la VUE, regenerable, recalculee a chaque passage. C'est le
    fichier a lire pour voir l etat du pilote. Elle porte une carte d'identite.
  - suivi-pilote.jsonl : les VERDICTS DE PANNE seulement, append-only. Une panne deja
    tracee (meme id, meme signature) n'est pas reecrite : un journal n'est pas un
    compte a rebours qui se repete.
  Les DEUX sont poses par la PORTE ECRIRE (`--mode creer|remplacer|ajouter`), jamais par
  une ecriture directe : la Matrice possede et verifie ce qui est publie (L-007).

LA LOI DES COLONNES (exigence createur) : une colonne se garde si elle VARIE ou si elle
PORTE UN VERDICT. Une colonne qui vaut < - > pour tout le monde est un placeholder qui
ment (lecon du 2026-09-19) : elle est OMISE, et la vue DIT lesquelles elle a omises --
une omission muette serait l angle mort meme que ce suivi surveille (MO-075). Sur un
EVENEMENT, jamais de duree ; un VIDE se dit (inconnu), il ne s'affiche JAMAIS 0.

LES SEUILS NE SONT PAS ICI : ils vivent dans `suivi-pilote/pannes-declarees.json` (la
liste FERMEE des pannes). La porte la LIT ; un seuil absent se DIT et la panne n'est
jamais accusee a l aveugle. Une panne DECLAREE sans detecteur est NOMMEE < sans
detecteur > -- une couverture muette serait muette (mesure du 2026-09-26 : 2 sur 17).

Usage:
  python suivi-pilote.py [--racine <chemin>]   recalcule la vue, trace les verdicts, rend le verdict
  python suivi-pilote.py --json                la vue en JSON (pour un appelant)
  python suivi-pilote.py --auto-test           eprouve les detecteurs (cobaye + temoin)
  code 0 = AUCUNE PANNE, 1 = au moins une panne (Table 0 non vide), 2 = racine ou
  declaration illisible.
"""

import argparse
import copy
import json
import re
import subprocess
import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-414, vague 3 du lot) -----------------
RACINE_MATRICE_LANCEMENT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
if RACINE_MATRICE_LANCEMENT.name != "matrix":
    raise RuntimeError("Structure inattendue : " + str(RACINE_MATRICE_LANCEMENT)
                       + " n est pas la racine `matrix` (garde-foi L-006)")
REPERTOIRE_COMMUN_LANCEMENT = RACINE_MATRICE_LANCEMENT / "matrice" / "data" / "commun"
if not (REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402
# LE ROUND SERVI ET JAMAIS CONDUIT (MO-451) : le FAIT vit au DOMICILE PARTAGE
# (matrice/data/commun/round_servi.py). Le pilote le consomme AUSSI (rappel
# immediat a la remise) ; ici on y ajoute le SEUIL declare pour en faire une panne.
import round_servi  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())
import sys
from datetime import datetime
from pathlib import Path

# --- DOMICILES (declares une fois, jamais recopies dans la logique) ----------
DOSSIER_PILOTE = Path("_operateur") / "optimus-prime" / "pilote"
DOSSIER_SUIVI = Path("_operateur") / "optimus-prime" / "suivi-pilote"
NOM_VUE = "suivi-pilote.md"
NOM_JOURNAL = "suivi-pilote.jsonl"
NOM_DECLARATION = "pannes-declarees.json"
FICHIER_FILE_MISSIONS = Path("file-missions-optimus.json")
FICHIER_ENTONNOIR = Path("entonnoir-files-optimus.json")
FICHIER_HISTORIQUE = Path("data") / "cycle-historique-archive.json"
CHEMIN_SUIVI_OPTIMUS = Path("matrice") / "data" / "suivi-optimus.jsonl"
CHEMIN_PAUSES = Path("matrice") / "data" / "pauses-session-matrix.jsonl"
CHEMIN_ETAT_PAUSE = Path("matrice") / "data" / "session-matrix-etat.json"
CHEMIN_DEFCON = Path("matrice") / "data" / "defcon-historique.jsonl"
# Le SAC-A-DOS : l ACTIVITE REELLE de l agent, chaque invocation d outil horodatee.
# C est la trace FINE de la panne bilan-rapport-entre-deux-rounds : le marbre
# (suivi-optimus) n a que des actes de mission (p95 = 25.8 min), le sac-a-dos a un
# p95 de 1.5 min sur 62773 actes -- d ou un seuil bien plus PETIT (30 min).
CHEMIN_SAC_A_DOS = Path("matrice") / "data" / "usages-outils-combos.jsonl"
# L outbox d'Optimus vit dans `_operateur/maintenance/` : c'est la constante DOMICILE
# du pilote (`pilote/constants.py` : REPERTOIRE_INTERCOM = matrix/_operateur/maintenance).
# Mesure du 2026-09-22 : la boite `_operateur/optimus-prime/intercom/pilote/` est une
# ANCIENNE boite (derniere injection le 2026-09-12, aucun `poids_tokens`) ; la boite
# vivante est celle-ci (288 lignes, 111 injections, les missions du jour).
MOTIF_OUTBOX = ("_operateur", "maintenance", "pilote", "outbox.jsonl")
DOSSIER_COMMUN = Path("matrice") / "data" / "commun"
NOM_SERVICE_RESOLUTION = "resolution_outils.py"
NOM_PORTE_ECRIRE = "ecrire"
# Le PREDICAT PARTAGE du jugement de cloture fausse (data/commun/, MO-426).
NOM_PREDICAT_CLOTURE_FAUSSE = "cloture_fausse.py"

# --- LE VERDICT D ENCHAINEMENT (consomme du DOMICILE, jamais recopie) ----------
# L index des auto-validees porte des ids d ITEM (EO-N), jamais des ids de MISSION
# (MO-N) : comparer les deux ne peut pas marcher (mesure MO-175/EO-264). Le verdict se
# resout donc par la PROVENANCE, avec la FONCTION DU PILOTE -- la recopier serait une
# copie de plus (L-029).
FICHIER_COMMUN_PILOTE = Path("commun.py")
FICHIER_FONCTIONS_INJECTION = Path("injection") / "fonctions.py"


def charger_est_auto(pilote):
    """La fonction de verdict du pilote, ou (None, motif) si son import est muet."""
    if not (pilote / FICHIER_COMMUN_PILOTE).is_file():
        return None, "module du pilote absent"
    if str(pilote) not in sys.path:
        sys.path.insert(0, str(pilote))
    try:
        from injection.fonctions import est_auto_validee  # noqa: E402
        return est_auto_validee, ""
    except Exception as erreur:  # noqa: BLE001 -- un import muet se DIT, il ne leve pas
        return None, type(erreur).__name__


def charger_fichiers_de_la_mission(pilote):
    """La REGLE de DERIVATION du pilote (EO-362), ou (None, motif) si l import est muet.

    La regle vit dans le PILOTE (`commun.py`) ; cette porte l EPROUVE, elle ne la
    recopie pas (L-029). Meme idiome que `charger_est_auto` : le chemin du pilote est
    pose en tete de `sys.path`, et un import muet se DIT sans lever. Sans cet import,
    aucun cobaye n est possible : l epreuve ne peut pas tester la VRAIE regle.
    """
    if not (pilote / FICHIER_COMMUN_PILOTE).is_file():
        return None, "module du pilote absent"
    if str(pilote) not in sys.path:
        sys.path.insert(0, str(pilote))
    try:
        from commun import fichiers_de_la_mission  # noqa: E402
        return fichiers_de_la_mission, ""
    except Exception as erreur:  # noqa: BLE001 -- un import muet se DIT, il ne leve pas
        return None, type(erreur).__name__


# --- LA LOI DES COLONNES -----------------------------------------------------
# Les colonnes qui PORTENT UN VERDICT ne sont jamais omises, meme constantes : elles
# disent un jugement, pas une mesure. Les autres ne se gardent que si elles VARIENT.
COLONNES_VERDICT = ("Gravite", "Silence", "Constat", "Motif", "Refus", "Bilan",
                    "Enchainement", "Action posee")
MENTION_INCONNU = "inconnu"
ENCART_VIDE = "AUCUNE PANNE CONSTATEE"
CARTE_VUE = ("---", "identite:", "  type: analyse", "  appartient_a: optimus-prime",
             "  commun: false", "---")
CLES_JOURNAL = ("date", "id", "gravite", "constat", "silence", "signature")


def ascii_propre(texte):
    """Le texte d'une vue est TOUJOURS ASCII (une valeur lue peut porter un accent)."""
    return "".join(c if ord(c) < 128 else "?" for c in str(texte))


def trouver_racine(depart):
    """Le dossier qui porte `_operateur/optimus-prime/pilote/commun.py`, ou None."""
    for candidat in [depart, depart / "cerveau-projet" / "matrix", depart / "matrix"]:
        if (candidat / DOSSIER_PILOTE / "commun.py").is_file():
            return candidat
    return None


# --- LECTURES (lecture seule, jamais d'exception non dite) -------------------

def lire_json(chemin):
    """(donnees, None) ou (None, motif). Un fichier absent n'est pas une erreur."""
    if not chemin.is_file():
        return None, "absent"
    try:
        return json.loads(chemin.read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as erreur:
        return None, type(erreur).__name__


def lire_jsonl(chemin):
    """Les evenements lisibles d'un journal, dans l ordre du fichier."""
    if not chemin.is_file():
        return []
    evenements = []
    for ligne in chemin.read_text(encoding="utf-8", errors="replace").splitlines():
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            evenements.append(json.loads(ligne))
        except json.JSONDecodeError:
            continue
    return evenements


def horodate(texte):
    for forme in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(str(texte)[:19], forme)
        except (ValueError, TypeError):
            continue
    return None


def minutes_ecoulees(depuis, maintenant):
    moment = horodate(depuis)
    if moment is None:
        return None
    return (maintenant - moment).total_seconds() / 60.0


def duree_dite(minutes):
    if minutes is None:
        return MENTION_INCONNU
    if minutes >= 1440:
        return "%.1f j" % (minutes / 1440.0)
    if minutes >= 60:
        return "%.1f h" % (minutes / 60.0)
    return "%.0f min" % minutes


# --- LA PORTE D ECRITURE (resolution partagee, M-076) -----------------------

def resoudre_porte(racine):
    """Le chemin de la porte d ecriture, par la RESOLUTION PARTAGEE, ou None."""
    commun = racine / DOSSIER_COMMUN
    if not (commun / NOM_SERVICE_RESOLUTION).is_file():
        return None
    if str(commun) not in sys.path:
        sys.path.insert(0, str(commun))
    try:
        import resolution_outils
        return Path(resolution_outils.chemin_outil(NOM_PORTE_ECRIRE))
    except Exception:  # noqa: BLE001 -- une resolution muette ne doit pas lever ici
        return None


def publier(racine, chemin, contenu, mode):
    """Pose un artefact par la PORTE (jamais a la main). Rend (code, sortie)."""
    porte = resoudre_porte(racine)
    if porte is None:
        return 2, "porte '" + NOM_PORTE_ECRIRE + "' introuvable (resolution partagee muette)"
    commande = [sys.executable, str(porte), "ecrire", "--fichier", str(chemin),
                "--contenu", contenu, "--mode", mode]
    resultat = lancer_enfant(commande, capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
    return resultat.returncode, ((resultat.stdout or "") + (resultat.stderr or "")).strip()


# --- LA VUE : ce que la porte a lu, une fois --------------------------------

class Vue:
    def __init__(self, racine, declaration):
        self.racine = racine
        self.declaration = declaration
        self.maintenant = datetime.now()
        self.pilote = racine / DOSSIER_PILOTE
        self.file_missions, self.erreur_file = lire_json(self.pilote / FICHIER_FILE_MISSIONS)
        self.entonnoir, self.erreur_entonnoir = lire_json(self.pilote / FICHIER_ENTONNOIR)
        self.historique, _ = lire_json(self.pilote / FICHIER_HISTORIQUE)
        self.evenements = lire_jsonl(racine / CHEMIN_SUIVI_OPTIMUS)
        self.dates_par_mission = {}
        self.dernier_fait = {}
        for evenement in self.evenements:
            mission, action, date = (evenement.get("mission"), evenement.get("action"),
                                     evenement.get("date"))
            if mission and action and date:
                self.dates_par_mission.setdefault(mission, {}).setdefault(action, []).append(date)
            moment = horodate(date)
            if mission and moment and (mission not in self.dernier_fait
                                       or moment > self.dernier_fait[mission][0]):
                self.dernier_fait[mission] = (moment, date, action)
        # L ACTIVITE REELLE de l agent (le sac-a-dos, hors routines `auto`) : c est
        # le signal FIN de la panne bilan-rapport. Charge une fois, comme les autres
        # sources de la vue.
        self.acte_agent = dernier_acte_agent(racine)

    def missions(self):
        return list((self.file_missions or {}).get("missions") or [])

    def en_cours(self):
        return [m for m in self.missions() if m.get("statut") == "en-cours"]

    def lot(self):
        return list(((self.file_missions or {}).get("lot") or {}).get("ids") or [])

    def brin(self):
        return list((self.entonnoir or {}).get("brin") or [])

    def dernier_evenement(self):
        datables = [(horodate(e.get("date")), e) for e in self.evenements if horodate(e.get("date"))]
        return max(datables, key=lambda paire: paire[0]) if datables else (None, None)


# --- LA LOI DES COLONNES, appliquee et DITE --------------------------------

def garder_colonnes(entetes, lignes):
    """(entetes gardees, omises) -- une colonne constante ET sans verdict est omise."""
    gardees, omises = [], []
    for rang, entete in enumerate(entetes):
        valeurs = {str(ligne[rang]) for ligne in lignes}
        if entete in COLONNES_VERDICT or len(valeurs) > 1 or len(lignes) <= 1:
            gardees.append(entete)
        else:
            omises.append((entete, len(lignes)))
    return gardees, omises


def rendre_table(numero, titre, entetes, lignes, resume=None):
    sortie = ["", "## Table " + str(numero) + " -- " + ascii_propre(titre)]
    if resume:
        sortie += ["", "> " + ascii_propre(resume)]
    if not lignes:
        sortie += ["", "(rien a lire sur cette partie)"]
        return sortie
    gardees, omises = garder_colonnes(entetes, lignes)
    rangs = [i for i, entete in enumerate(entetes) if entete in gardees]
    sortie += ["", "| " + " | ".join(entetes[i] for i in rangs) + " |",
               "|" + "---|" * len(rangs)]
    for ligne in lignes:
        sortie.append("| " + " | ".join(ascii_propre(ligne[i]) for i in rangs) + " |")
    if omises:
        sortie += ["", "Colonnes OMISES (constantes, sans verdict) : "
                   + " ; ".join(nom + " (" + str(n) + " lignes)" for nom, n in omises) + "."]
    return sortie


# --- LES DETECTEURS (un par panne DECLAREE ; aucun seuil en dur) -------------

def seuil_de(declaration, identifiant, cle="seuil_minutes"):
    for panne in declaration.get("pannes") or []:
        if panne.get("id") == identifiant:
            regle = panne.get("regle") or {}
            return regle.get(cle, regle.get("seuil"))
    return None


def detecter_serie_stricte(vue, declaration, sortie_pilote):
    """MAILLON 4 du flux : le pilote repond, et jamais plus d'une mission en cours."""
    code, texte = sortie_pilote
    if code != 0:
        dernier = (texte.strip().splitlines() or ["aucune sortie"])
        return ("haute", "pilote muet (code " + str(code) + ")",
                str(dernier[-1])[:90], "code non nul : la porte ne repond pas",
                "relancer le pilote, lire le dernier refus")
    en_cours = vue.en_cours()
    if len(en_cours) > 1:
        return ("haute", str(len(en_cours)) + " missions EN COURS ("
                + ", ".join(str(m.get("id", "?")) for m in en_cours) + ")",
                "la serie stricte est violee", "deux missions ouvertes",
                "reporter ou finir l une des deux")
    return None


def detecter_age_mission(vue, declaration, _sortie):
    """Une mission EN COURS se termine dans la fenetre (p95 mesure = 92 min)."""
    seuil = seuil_de(declaration, "mission-qui-n-avance-pas")
    if not seuil:
        return None
    # L AGE SE MESURE SUR LA TRACE DE SERVICE, JAMAIS SUR LE CHAMP (MO-501).
    # `chargee_le` est l instant de CHARGEMENT DU LOT : un lot entier le partage, donc
    # une mission servie depuis deux minutes se lisait < en cours depuis 2.4 j > -- le
    # rouge est alors NORMAL pendant toute la conduite d un lot arme, et tout le monde
    # apprend a l ignorer (exactement le motif que le createur a fait inverser en
    # MO-487). Le remede existait DEJA dans ce fichier -- `charges_tracees`, ecrit par
    # la porte depuis le 2026-09-22 -- et n etait consomme par personne : un remede
    # ecrit et non consomme est une decision qui dort (regle evolution-decidee).
    charges = dernieres_chargees(vue)
    for mission in vue.en_cours():
        identifiant = mission.get("id")
        trace = charges.get(identifiant)
        # LA SOURCE EST NOMMEE dans le fait accuse : un age sans horloge dit d ou il
        # sort est un age qu on ne peut pas discuter.
        horloge = ("trace de service du " + trace[1]) if trace else \
            ("champ chargee_le du " + str(mission.get("chargee_le")) + " (aucune trace)")
        age = minutes_ecoulees(trace[1] if trace else mission.get("chargee_le"),
                               vue.maintenant)
        if age is None or age <= seuil:
            continue
        fait = vue.dernier_fait.get(identifiant)
        return ("haute", str(identifiant) + " en cours depuis " + duree_dite(age),
                "seuil declare : " + duree_dite(seuil) + " ; age mesure sur : " + horloge,
                fait[1] if fait else MENTION_INCONNU,
                "conduire, finir ou reporter la mission")
    return None


def charges_tracees(vue):
    """Les CHARGES tracees par le pilote : (moment, date, mission), dans l ordre du journal.

    Depuis le 2026-09-22 (demande du createur) `charger` NOTE l acte par la porte :
    c est la trace qui MANQUAIT -- `chargee_le` seul etait ambigu, un LOT entier
    partageant le meme horodatage (mesure : les 30 missions en attente du lot
    REPRISE DU RETARD, toutes au meme instant, aucune avec un debut).
    """
    traces = []
    for evenement in vue.evenements:
        if evenement.get("action") != "charge":
            continue
        moment = horodate(evenement.get("date"))
        if moment and evenement.get("mission"):
            traces.append((moment, evenement.get("date"), evenement.get("mission")))
    return traces


def dernieres_chargees(vue):
    """{mission: (moment, date)} -- la DERNIERE charge tracee, par mission.

    Elle CONSOMME `charges_tracees`, qui est le seul endroit du depot qui lit les
    actes `charge` du journal : relire le journal ici creerait une SECONDE lecture
    de la meme question, qui divergerait des que l une des deux change (M-076).

    C'est cette table, et non `chargee_le`, qui dit l age REEL d'une mission en
    cours : un LOT entier partage le meme `chargee_le` (mesure de la famille :
    les 30 missions du lot REPRISE DU RETARD, toutes au meme instant), donc le champ
    donne l age du LOT et le garde concluait que la mission, servie depuis deux
    minutes, tournait depuis deux jours (MO-501).
    """
    dernieres = {}
    for moment, date, mission in charges_tracees(vue):
        if moment is not None and mission:
            dernieres[mission] = (moment, date)
    return dernieres


def missions_en_lot(vue):
    """Les missions chargees AVEC un lot : elles ATTENDENT leur tour (etat legitime)."""
    return {m.get("id") for m in vue.missions() if m.get("lot")}


def detecter_chargee_sans_debut(vue, declaration, _sortie):
    """La panne PAYEE en MO-387 : chargee, et JAMAIS conduite.

    DEUX faits, mesures separement :
    1. la CONTRADICTION INTERNE du pilote -- une mission donnee EN COURS dont
       l ouverture n est tracee nulle part (`debut` absent) ;
    2. la CHARGE INDIVIDUELLE jamais conduite -- une charge TRACEE (donc l acte est
       date), la mission n appartient a AUCUN lot (elle n attend pas son tour : son
       tour ETAIT venu), et aucun `debut` ne suit dans la fenetre.

    LE LOT EST L EXEMPTION NOMMEE, ET ELLE VIENT DE LA FILE : une mission portant un
    `lot` est chargee AVEC d autres et attend son tour -- l accuser serait le faux
    positif qui a REFUTE la premiere regle (mesure du 2026-09-22 : 31 missions, meme
    `chargee_le`, aucune avec un debut).
    """
    seuil = seuil_de(declaration, "mission-chargee-sans-conduite")
    if not seuil:
        return None
    for mission in vue.en_cours():
        age = minutes_ecoulees(mission.get("chargee_le"), vue.maintenant)
        if age is None or age <= seuil:
            continue
        debuts = (vue.dates_par_mission.get(mission.get("id")) or {}).get("debut") or []
        if not debuts:
            return ("haute", str(mission.get("id")) + " EN COURS sans aucun debut declare",
                    "le pilote la donne en cours depuis " + duree_dite(age)
                    + " mais son ouverture n est tracee nulle part",
                    str(mission.get("chargee_le")), "pilote conduire (jouer la mission chargee)")
    par_id = {m.get("id"): m for m in vue.missions()}
    en_lot = missions_en_lot(vue)
    for moment, date, mission_id in charges_tracees(vue):
        if mission_id in en_lot:
            continue
        if (vue.dates_par_mission.get(mission_id) or {}).get("debut"):
            continue
        statut = (par_id.get(mission_id) or {}).get("statut")
        if statut in ("terminee", None):
            continue  # close : c est la CLOTURE FAUSSE, une autre panne la juge
        age = (vue.maintenant - moment).total_seconds() / 60.0
        if age > seuil:
            return ("haute", str(mission_id) + " chargee INDIVIDUELLEMENT et jamais conduite",
                    "charge tracee le " + str(date) + " (il y a " + duree_dite(age)
                    + ", seuil " + duree_dite(seuil) + ") et aucun debut ne l a suivie",
                    str(date), "pilote conduire --id " + str(mission_id))
    return None


def _predicat_cloture_fausse(vue):
    """Le PREDICAT PARTAGE (data/commun/cloture_fausse.py), importe, ou None.

    Il vit a SON domicile (M-076) : le MEME jugement sert au DIAGNOSTIC (ce
    fichier) et au REFUS de la cloture (pilote, MO-426). On l importe depuis la
    RACINE de la vue ; INTROUVABLE, on rend None -- le detecteur se TAIT plutot
    que de recopier la regle (une copie divergerait, L-029).
    """
    for base in (vue.racine, Path(__file__).resolve()):
        courant = base
        for _ in range(12):
            candidat = courant / DOSSIER_COMMUN
            if (candidat / NOM_PREDICAT_CLOTURE_FAUSSE).is_file():
                if str(candidat) not in sys.path:
                    sys.path.insert(0, str(candidat))
                try:
                    import cloture_fausse
                except Exception:  # noqa: BLE001 -- un import muet ne doit pas lever ici
                    return None
                return cloture_fausse.clotures_fausses
            courant = courant.parent
    return None


def detecter_cloture_fausse(vue, _declaration, _sortie):
    """EO-356 : la CLOTURE FAUSSE -- une charge individuelle close sous un AUTRE nom.

    C est la panne payee en MO-387 : le pilote charge une mission, et la premiere
    cloture qui suit nomme une AUTRE mission (la tete du lot). Les deux traces
    etaient alors d ACCORD -- la file disait MO-345 terminee, le journal aussi --
    donc AUCUN garde ne pouvait le voir. La CHARGE TRACEE rend le fait mesurable :
    elle dit QUELLE mission le round avait ouverte, et la cloture doit NOMMER
    celle-la.

    CONTRE-TEMOIN : une mission chargee AVEC un lot est epargnee (son tour vient
    plus tard, la premiere cloture ne parle pas d elle) ; une cloture qui nomme la
    mission chargee est epargnee ; un PARQUAGE de la meme mission l epargne aussi
    (mesure du 2026-09-25 : MO-412 parquee a 08:32 puis MO-413 close a 08:37 -- le
    pilote avait remis MO-412 EN ATTENTE, elle etait sortie du round SANS cloture,
    et le detecteur criait une cloture fausse qui n avait PAS eu lieu). Sans trace
    de charge, RIEN n est accuse : la porte ne devine pas (les charges anterieures
    au 2026-09-22 sont muettes).
    """
    clotures_fausses = _predicat_cloture_fausse(vue)
    if clotures_fausses is None:
        return None
    fausses = clotures_fausses(vue.evenements, missions_en_lot(vue))
    if not fausses:
        return None
    mission_id, cloturee = fausses[0]
    return ("haute", "CLOTURE FAUSSE : la charge de " + str(mission_id)
            + " est suivie de la cloture de " + str(cloturee),
            "le round a ouvert " + str(mission_id) + " et a clos " + str(cloturee)
            + " a sa place", "a l instant de la charge",
            "pilote fin (clore la mission REELLEMENT menee) + pilote reporter")


def detecter_lot_sans_tete(vue, _declaration, _sortie):
    """Un lot arme et NON ecoule a toujours une tete servie."""
    ids = vue.lot()
    if not ids:
        return None
    par_id = {m.get("id"): m for m in vue.missions()}
    restantes = [i for i in ids if par_id.get(i, {}).get("statut") not in ("terminee", "retiree")]
    if not restantes or vue.en_cours() or vue.brin():
        return None
    return ("haute", "lot arme sans AUCUNE tete servie",
            str(len(restantes)) + " mission(s) du lot non ecoulee(s), aucune en cours, brin vide",
            str(restantes[0]), "pilote charger (servir la tete) ou lot retirer")


def detecter_stop_sans_suite(vue, declaration, _sortie):
    """Une cloture sans suite servie : le STOP laisse la chaine arretee."""
    seuil = seuil_de(declaration, "enchainement-stop")
    moment, evenement = vue.dernier_evenement()
    if moment is None or evenement.get("action") != "fin" or vue.en_cours():
        return None
    age = (vue.maintenant - moment).total_seconds() / 60.0
    if seuil and age <= seuil:
        return None
    return ("haute", "dernier fait = une CLOTURE, aucune suite servie",
            "derniere fin : " + str(evenement.get("mission")) + " (" + str(evenement.get("date")) + ")",
            str(evenement.get("date")), "pilote conduire (servir la suite)")


def detecter_brin_perime(vue, _declaration, _sortie):
    """MAILLON 5 : brin == somme des files."""
    files = (vue.entonnoir or {}).get("files") or {}
    nombre = sum(len(v or []) for v in files.values())
    brin = len(vue.brin())
    if brin != nombre:
        return ("haute", "brin (" + str(brin) + ") et files (" + str(nombre) + ") divergent",
                "tissage non refait depuis le dernier classement", "mesure immediate",
                "tresse tisser")
    return None


def detecter_item_dort(vue, declaration, _sortie):
    """LA FILE ENTIERE qui dort -- combien de dormeurs, ou est le plus vieux.

    EO-420 (2026-09-25) : la mesure portait sur la SEULE tete (brin[0]). Ce defaut se
    paie : consommer la tete REVELAIT la suivante, le reste restait invisible, et le
    remede < charger la tete > ne vidait JAMAIS le brin. Mesure du 2026-09-25 : 44
    items au brin, 27 dormeurs au-dela du seuil declare (1440 min), le plus vieux
    (EO-353) depose depuis 3.0 j -- que la seule tete disait deja, en CACHANT les 26
    autres dormeurs. L accusation NOMME donc COMBIEN d items dorment et LEQUEL dort
    depuis le plus longtemps. Un item sans `deposee_le` n est pas accuse : la porte ne
    devine pas.

    EO-489 (2026-09-29, decision createur sur la question ouverte depuis MO-460) : le
    SCAN etait bon depuis EO-420, mais le LANGAGE ne l avait pas suivi. Ce texte
    parlait encore de "l ARRIERE" et la sortie preservait "l arriere" -- alors que le
    detecteur mesure une file dont il ne distingue pas la tete du fond. Les MESURES
    disent pourquoi cela coute : les 2 dormeurs accuses ce jour-la (EO-475, EO-476)
    portaient `position_brin` 1 et 2. Ils etaient les TETES. Il n y avait donc RIEN a
    vider derriere eux, et la question posee au createur ("vider l arriere, ou
    regrouper en lot ?") PORTAIT sur un endroit inexistant. Le second remede offert,
    `file verser --lot`, ne pouvait pas non plus etre execute : `verser_tresse` verse
    `brin` ENTIER, sans le moindre filtre (mesure directe du 2026-09-29) -- il
    entrainait 9 items NON dormeurs, dont 4 auto-valides, et un lot n aurait debloque
    rien : les 2 items sont `auto_validation: non`, bloques par l axe `perimetre`
    (zone critique nommee). Un remede qui nomme un lieu inexistant, ou un geste que
    la porte ne sait pas faire, transmet une confiance qu il ne peut pas honourer --
    et il dispense son lecteur de chercher (lecon L-224).

    DONC : l accusation nomme des ETATS (combien, lequel, depuis quand) et propose un
    geste dont l EXECUTABILITE a ete mesuree. Ni "l arriere", ni le lot : la file
    se sert par la tete, et le remede le dit ainsi. Le mot `lot` peut disparaitre du
    texte sans que la DETECTION change -- c est le contre-temoin exige par EO-489.
    """
    seuil = seuil_de(declaration, "item-qui-dort")
    brin = vue.brin()
    if not brin or not seuil:
        return None
    dormeurs = []
    for item in brin:
        age = minutes_ecoulees(item.get("deposee_le"), vue.maintenant)
        if age is not None and age > seuil:
            dormeurs.append((age, item))
    if not dormeurs:
        return None
    age, plus_vieux = max(dormeurs, key=lambda paire: paire[0])
    # LE RANG EST DIT (EO-489). C est l absence qui a coute : les dormeurs accuses
    # ce jour-la etaient les TETES (rang 1 et 2), et rien dans la sortie ne le
    # montrait -- le lecteur en a deduit un "arriere" qui n existait pas. Le rang se
    # lit dans la file ENTIERE, donc il est toujours connu : une position absente
    # n est pas devinee, elle se lit par l indice qu elle occupe.
    rang = brin.index(plus_vieux) + 1
    return ("normale",
            str(len(dormeurs)) + " item(s) du brin dorment (le plus vieux : "
            + str(plus_vieux.get("id")) + ", rang " + str(rang) + "/" + str(len(brin)) + ")",
            str(len(dormeurs)) + " dormeur(s) sur " + str(len(brin)) + " items, au-dela de "
            + duree_dite(seuil) + " ; le plus vieux (" + str(plus_vieux.get("id"))
            + ") est depose depuis " + duree_dite(age) + " et occupe le rang "
            + str(rang) + " de la file",
            str(plus_vieux.get("deposee_le")),
            "servir le brin par la tete, une par une (file consommer) : le plus vieux "
            "dort au rang " + str(rang) + "/" + str(len(brin)) + " -- "
            + ("c est la tete, il part des la liberation de la serie stricte"
               if rang == 1 else
               "il part apres les " + str(rang - 1) + " item(s) qui le precedent"))


def detecter_pause_contradictoire(vue, _declaration, _sortie):
    """La panne VIVANTE du 2026-09-22 : le journal et l etat ne disent pas la meme chose."""
    journal = lire_jsonl(vue.racine / CHEMIN_PAUSES)
    if not journal:
        return None
    dernier = journal[-1]
    etat_present = (vue.racine / CHEMIN_ETAT_PAUSE).is_file()
    if dernier.get("type") == "pause" and not etat_present:
        age = minutes_ecoulees(dernier.get("date"), vue.maintenant)
        return ("haute", "journal en PAUSE sans reprise, etat de pause ABSENT",
                "derniere ligne : pause du " + str(dernier.get("date")) + " (il y a "
                + duree_dite(age) + "), etat absent", str(dernier.get("date")),
                "pause-session clore --motif \"...\" (regularise la pause orpheline : journalise la reprise SANS toucher la file)")
    if dernier.get("type") == "reprise" and etat_present:
        return ("haute", "journal en REPRISE, etat de pause PRESENT",
                "etat pose alors que la reprise est journalisee", str(dernier.get("date")),
                "pause-session reprendre")
    return None


def detecter_bilan_absent(vue, _declaration, _sortie):
    """Une mission close sans fin declaree (trace muette)."""
    manquantes = [m.get("id") for m in vue.missions()
                  if m.get("statut") == "terminee"
                  and not (vue.dates_par_mission.get(m.get("id")) or {}).get("fin")]
    if manquantes:
        return ("haute", str(len(manquantes)) + " mission(s) close(s) sans fin declaree",
                ", ".join(str(x) for x in manquantes[:6]), "mesure immediate",
                "pilote fin (rejouer) ou suivi-optimus (rattrapage)")
    return None


def detecter_cablage_non_enregistre(vue, _declaration, _sortie):
    """MO-528 : un OUTIL ou une ROUTINE qui existe mais n est pas au REGISTRE.

    LE FAIT, et sa cause : l instrument qui mesure le cablage existe deja
    (`registre-outils verifier`) et il MORD -- il nomme aujourd h ui 3 elements
    presents sur le disque et absents de la BDD. Ce que personne ne fait, c est
    le JOUER : aucune routine, aucun maillon de la non-regression ne l appelle
    (mesure du 2026-10-02, recherche sur toute la zone : la seule reference est
    la liste des outils que le pilote propose a l agent). Une mesure qui ne se
    joue pas est une mesure qui n existe pas -- l agent n y pense que par hasard.

    CE QUE CE DETECTEUR FAIT, et la limite qu il DIT : il APPELLE l instrument
    existant au lieu d en ecrire un autre (M-076), et il rend son verdict NOMME.
    Il ne juge que le SENS "present sur disque, absent du registre" : l autre
    sens (declare et disparu) est deja couvert par le meme outil, et un registre
    volontairement alllege n est pas accuse ici.

    LE BRUIT : la sortie reprend celle de l instrument, sans la reecrire.
    """
    racine = vue.racine if hasattr(vue, "racine") else None
    if racine is None:
        return None
    outil = racine / "matrice" / "data" / "outils" / "registre-outils" / "main.py"
    if not racine.joinpath("matrice", "data", "outils", "registre-outils").is_dir():
        racine = racine / "cerveau-projet" / "matrix"
        outil = racine / "matrice" / "data" / "outils" / "registre-outils" / "main.py"
    if not outil.is_file():
        return None
    try:
        processus = subprocess.run(
            [sys.executable, str(outil), "verifier"],
            cwd=str(racine), capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as erreur:
        return ("normale", "l instrument de cablage n a PAS pu etre joue : "
                + type(erreur).__name__, "", "mesure immediate",
                "jouer registre-outils verifier a la main")
    sortie = ((processus.stdout or "") + (processus.stderr or "")).splitlines()
    non_enregistres = [l.strip() for l in sortie if "NON ENREGISTRES" in l]
    if not non_enregistres:
        return None
    noms = []
    for ligne in non_enregistres:
        reste = ligne.split(":", 1)[-1].strip()
        if reste:
            noms.append(reste.split(" ")[0])
    return ("haute",
            str(len(non_enregistres)) + " element(s) du parc ABSENTS du registre "
            "des outils -- ils existent, ils travaillent, personne ne les voit",
            ", ".join(noms[:6]), "mesure immediate",
            "registre-outils rafraichir (le registre se REGENERE, il ne s edite pas)")


def detecter_bilan_adresse_a_autre(vue, _declaration, _sortie):
    """MO-540 : un bilan qui S ANNONCE comme une AUTRE mission (le role, premier test).

    LE FAIT : le bilan d une mission close commence par se nommer -- "MO-539
    (CONSTRUCTEUR) -- ...". Si la premiere ligne porte un identifiant de mission
    et que ce n est PAS celui de la mission close, le bilan n a pas ete rendu
    pour elle. Mesure du 2026-10-02 : 50 missions closes avec bilan, 1 seule
    atteinte -- MO-527, dont le bilan portait celui de MO-539.

    POURQUOI LA TETE, ET PAS TOUT LE BILAN : un bilan peut legitimement citer une
    autre mission (un precedent, un tooling partage) -- MO-505 commence par un
    titre SANS identifiant et cite MO-504 : il est sain et le detecteur l epargne.
    Ce qui ne pardonne pas est de se presenter comme quelqu un d autre. Reglee
    sur tout le bilan, la regle aurait accuse 2 fois sur 50, dont une a tort.

    CONTRE-TEMOINS : un bilan qui cite son PROPRE identifiant, meme avec d autres
    a cote, est epagne ; un bilan sans aucun identifiant en tete est eparne (il
    se presente par son titre, pas par un nom de mission). Le detecteur ne juge
    pas la QUALITE d un bilan, il verifie une ADRESSE.
    """
    # Motif SANS BARRE OBLIQUE, et c est volontaire. La premiere version
    # ecrivait une frontiere par "\b" : ecrite a travers un remplacement, elle
    # s est retrouvee dans le fichier sous forme d un OCTET RETOUR-ARRIERE
    # (0x08) -- le motif compilait, ne mordait sur RIEN, et le detecteur
    # rendait muet alors que le fait existe. Une classe de caracteres ne peut
    # pas etre mal transportee : elle ne contient aucun caractere special.
    regex_id = re.compile("(^|[^A-Za-z0-9])(MO-[0-9]{3})([^A-Za-z0-9]|$)")
    atteints = []
    for mission in vue.missions():
        if mission.get("statut") != "terminee":
            continue
        bilan = (mission.get("bilan") or "").strip()
        if not bilan:
            continue
        lignes = bilan.splitlines()
        if not lignes:
            continue
        trouves = regex_id.findall(lignes[0])
        # findall rend un TUPLE par motif (frontiere gauche, identifiant,
        # frontiere droite) : c est le DEUXIEME qui est l identifiant. Prendre
        # le premier fit croire 49 missions en faute alors qu il y en a une.
        identifiants = [groupe[1] for groupe in trouves]
        if not identifiants:
            continue
        if mission.get("id") in identifiants:
            continue
        atteints.append((mission.get("id"), lignes[0].strip()[:70]))
    if atteints:
        return ("haute",
                str(len(atteints)) + " mission(s) close(s) dont le bilan s annonce "
                "comme une AUTRE mission",
                "; ".join(m + " <-> " + t for m, t in atteints[:4]),
                "mesure immediate",
                "relire le bilan et le dire au journal (la trace ne se reecrit pas), "
                "puis re-deposer le travail non fait")
    return None


def detecter_round_arme_jamais_pris(vue, declaration, _sortie):
    """EO-360 : le round ARME et JAMAIS PRIS -- la machine a servi, l agent n a pas pris.

    CE QUI SE MESURE : une mission EN COURS porte son injection (`injectee_le`,
    posee par le `fin` precedent ou par un chargement) ; si AUCUNE PRISE (action
    `prise`, notee par le GESTE DE RECEPTION) n a ete tracee DEPUIS cette
    injection, le round n a JAMAIS ete pris. Le seuil est celui de la DECLARATION.

    POURQUOI CE N EST PAS mission-chargee-sans-conduite : la-bas, le fait est la
    CONTRADICTION INTERNE du pilote (en cours SANS aucun debut). Ici le fait est
    plus etroit, et c est celui qui a ETE PAYE : le debut EXISTE (la machine l a
    pose), l injection EXISTE, la file dit en-cours -- les trois traces disent
    d ACCORD que le round a commence, et PERSONNE ne l a pris. C est la famille de
    la cloture fausse de MO-387.

    CONTRE-TEMOIN : un round PRIS (une prise posterieure a l injection) est
    EPARGNE, meme s il dure trente heures -- une mission longue n est pas une
    mission abandonnee. Et la porte ne DEVINE pas : sans aucune prise tracee dans
    le journal, le mecanisme est NEUF et RIEN n est accuse (meme doctrine que la
    charge tracee de MO-388).
    """
    seuil = seuil_de(declaration, "round-arme-jamais-pris")
    if not seuil:
        return None
    if not any(e.get("action") == "prise" for e in vue.evenements):
        return None
    for mission in vue.en_cours():
        injectee = horodate(mission.get("injectee_le"))
        if injectee is None:
            continue
        age = (vue.maintenant - injectee).total_seconds() / 60.0
        if age <= seuil:
            continue
        prises = (vue.dates_par_mission.get(mission.get("id")) or {}).get("prise") or []
        if any(moment and moment >= injectee
               for moment in (horodate(d) for d in prises)):
            continue
        return ("haute", str(mission.get("id")) + " ARME et JAMAIS PRIS depuis "
                + duree_dite(age),
                "le pilote l a servie le " + str(mission.get("injectee_le"))
                + " (seuil declare " + duree_dite(seuil)
                + ") et AUCUNE prise n a ete tracee depuis",
                str(mission.get("injectee_le")),
                "pilote injecter (PRENDRE le round) ou pilote reporter (le parquer)")
    return None


def detecter_round_pris_jamais_conduit(vue, declaration, _sortie):
    """EO-364 : le round PRIS et JAMAIS CONDUIT -- la prise ne blanchit plus le round.

    CE QUI SE MESURE : le DERNIER acte d une mission EN COURS est une PRISE, et rien
    n a suivi. C est le geste de reception lui-meme qui devient le soupcon : une prise
    declare < je conduis ce round > ; si elle reste le DERNIER acte au-dela du seuil,
    soit le round a ete rendu, soit il est mene en silence -- le journal ne voit pas le
    TRAVAIL, cette LIMITE est declaree, et le remede est nomme sur la declaration.

    POURQUOI CE N EST PAS round-arme-jamais-pris : la-bas, le round n a JAMAIS ete
    pris (aucune prise depuis l injection) -- et ce detecteur-la EPARGNE explicitement
    tout round pris, < meme s il dure trente heures >. Une prise tracee suffisait donc
    a FAIRE TAIRE l accusation : c est le trou paye le 2026-09-22, une heure apres la
    pose du premier garde (fin MO-390 20:50:21 -> prise MO-349 20:51:19 -> RIEN),
    alors que la MACHINE avait deja servi le round.

    CONTRE-TEMOIN : un round dont un AUTRE acte suit la prise (intervention, decision,
    cloture) est EPARGNE -- le dernier acte n est plus la prise. Et une prise RECENTE
    l est aussi : le seuil compte.
    """
    seuil = seuil_de(declaration, "round-pris-jamais-conduit")
    if not seuil:
        return None
    for mission in vue.en_cours():
        identifiant = mission.get("id")
        dernier = vue.dernier_fait.get(identifiant)
        if not dernier:
            continue
        moment, date, action = dernier
        if action != "prise":
            continue
        age = (vue.maintenant - moment).total_seconds() / 60.0
        if age >= seuil:
            return ("haute",
                    str(identifiant) + " PRIS il y a " + duree_dite(age)
                    + " : la PRISE est le DERNIER acte du round",
                    "aucun acte depuis la prise du " + str(date)
                    + " (seuil declare " + duree_dite(seuil)
                    + ") : round rendu sans conduite, ou mene en silence (la limite est declaree)",
                    str(date),
                    "pilote conduire (conduire le round) ou suivi-optimus noter "
                    "(declarer l acte de conduite) ou pilote fin (le clore)")
    return None


def dernier_acte_agent(racine):
    """Le moment du DERNIER acte de l AGENT, lu dans le sac-a-dos.

    L ACTIVITE REELLE : chaque invocation d outil est horodatee. La routine
    veille-flux marque ses passes `auto` (mesure du 2026-09-26 : 3025 sur 66022) :
    elles sont EXCLUES, sinon une routine ferait taire le detecteur et la panne
    serait invisible (vert muet, L-163).

    Retourne None si le sac-a-dos est absent ou illisible : un fait non mesurable
    ne s accuse pas.
    """
    chemin = racine / CHEMIN_SAC_A_DOS
    if not chemin.is_file():
        return None
    dernier = None
    try:
        for ligne in chemin.read_text(encoding="utf-8").splitlines():
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                evenement = json.loads(ligne)
            except ValueError:
                continue
            if "auto" in (evenement.get("tags") or []):
                continue
            moment = horodate(evenement.get("date"))
            if moment and (dernier is None or moment > dernier):
                dernier = moment
    except OSError:
        return None
    return dernier


def detecter_bilan_rapport(vue, declaration, _sortie):
    """L HABITUDE < BILAN-RAPPORT ENTRE DEUX ROUNDS > : un round PRIS se CONDUIT.

    Ce n est pas un accident, c est un motif QUI REVIENT : l agent ecrit un long
    rapport jamais demande puis REND LA MAIN, alors que le round suivant est DEJA
    servi et pris par la cloture.

    POURQUOI CE DETECTEUR, ET PAS round-pris-jamais-conduit : ce dernier lit le
    MARBRE, qui ne porte que des actes de mission (p95 = 25.8 min), d ou un seuil
    de 240 min qui crie TROP TARD. Ici la source est le SAC-A-DOS -- l ACTIVITE
    reelle de l agent (p95 = 1.5 min) : un silence y est un vrai silence.

    MORD : une mission EN COURS dont le dernier acte est une `prise`, ET aucun acte
    de l agent (sac-a-dos hors `auto`) posterieur a cette prise, depuis plus que le
    seuil declare.
    EPARGNE : un acte de l agent apres la prise (le round est CONDUIT), une prise
    recente (sous le seuil), un sac-a-dos illisible (le fait n est pas mesurable).
    """
    seuil = seuil_de(declaration, "bilan-rapport-entre-deux-rounds")
    if not seuil:
        return None
    dernier_agent = vue.acte_agent
    if dernier_agent is None:
        return None
    for mission in vue.en_cours():
        identifiant = mission.get("id")
        dernier = vue.dernier_fait.get(identifiant)
        if not dernier:
            continue
        moment, date, action = dernier
        # MO-451 : le FAIT vit au DOMICILE PARTAGE (data/commun/round_servi.py) --
        # le pilote le consomme AUSSI (rappel immediat a la remise, SANS seuil).
        # Une seule regle, deux postures (M-076) : ici on ajoute le SEUIL declare,
        # la-bas le fait NU. La frontiere (un acte agent STRICTEMENT posterieur dit
        # CONDUIT ; un acte egal ne blanchit PAS) est la MEME, par construction.
        if round_servi.servi_non_conduit(action, moment, dernier_agent) is not True:
            continue
        silence = (vue.maintenant - moment).total_seconds() / 60.0
        if silence >= seuil:
            return ("haute",
                    str(identifiant) + " PRIS il y a " + duree_dite(silence)
                    + " et AUCUN outil invoque depuis",
                    "silence d activite (sac-a-dos, hors `auto`) >= seuil declare "
                    + duree_dite(seuil) + " ; prise du " + str(date),
                    str(date),
                    "conduire le round MAINTENANT (poser un acte), ou pilote reporter")
    return None


def detecter_poids_derive(vue, declaration, _sortie):
    """Le sac-a-dos reste borne (plafond de tokens du createur)."""
    seuil = seuil_de(declaration, "poids-qui-derive")
    chemin = vue.racine.joinpath(*MOTIF_OUTBOX)
    if not seuil or not chemin.is_file():
        return None
    plus_lourd = None
    for evenement in lire_jsonl(chemin):
        poids = evenement.get("poids_tokens")
        if isinstance(poids, int) and (plus_lourd is None or poids > plus_lourd[0]):
            plus_lourd = (poids, evenement.get("mission"))
    if plus_lourd and plus_lourd[0] > seuil:
        return ("normale", "une injection depasse le plafond (" + str(plus_lourd[0]) + " > "
                + str(seuil) + ")", "mission " + str(plus_lourd[1]), "mesure immediate",
                "verifier le plafond des lecons et les themes_utiles")
    return None


def charger_decideur_source(racine):
    """Le DECIDEUR de la source < si j etais user >, CONSOMME de son domicile (M-076).

    Le controle permanent ne RECOPIE pas la regle du moment : la re-copier ferait une
    deuxieme verite, et la premiere divergence passerait en silence (L-029 / L-032).
    """
    chemin = racine / DOSSIER_PILOTE / "injection" / "si_j_etais_user.py"
    if not chemin.is_file():
        return None
    import importlib.util
    try:
        specification = importlib.util.spec_from_file_location("si_j_etais_user_suivi", str(chemin))
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError, AttributeError):
        return None
    return module


def detecter_source_non_injectee(vue, declaration, _sortie):
    """LA SOURCE < SI J ETAIS USER > servie AU MOMENT, et sa trace DECLAREE (MO-416).

    Le createur a tranche le 2026-09-25 : la phase n est PAS un crochet -- c est le
    PILOTE qui sert ce genre de source quand on en a besoin, ET LE CONTROLE PERMANENT
    LIT LA TRACE DECLAREE. Ce detecteur est ce controle, et il ne REJOUE pas la
    decision : il CONSOMME le decideur de son domicile pour savoir QUAND la source
    sert, puis il LIT LE JOURNAL pour verifier que l injection l a DECLAREE.

    EPARGNE : une mission injectee AVANT la pose de la source (le seuil `depuis` vit
    dans la declaration, jamais dans le code) et une mission dont l objectif ne
    redemande rien.
    """
    depuis = horodate(seuil_de(declaration, "source-non-injectee", "depuis"))
    if depuis is None:
        return None
    decideur = charger_decideur_source(vue.racine)
    if decideur is None:
        return ("normale", "le DECIDEUR de la source < si j etais user > est INTROUVABLE",
                "injection/si_j_etais_user.py illisible a son domicile",
                "le domicile de la source n a pas pu etre lu",
                "reposer la source : _operateur/optimus-prime/pilote/injection/si_j_etais_user.py")
    tracees = {evenement.get("mission") for evenement in vue.evenements
               if evenement.get("action") == "injection"}
    for mission in vue.missions():
        identifiant = str(mission.get("id") or "")
        moment_injection = horodate(mission.get("injectee_le"))
        if not identifiant or moment_injection is None or moment_injection < depuis:
            continue
        decision = decideur.decider(mission.get("titre") or "", mission.get("objectif") or "")
        if not decision.get("applique") or identifiant in tracees:
            continue
        return ("normale",
                identifiant + " : la source < si j etais user > sert (moment "
                + str(decision.get("moment")) + ") et l injection ne l a PAS declaree",
                str(decision.get("motif")),
                "le pilote a servi la source sans DECLARER sa trace",
                "declarer la source par la porte noter (action `injection`)")
    return None


# Le REGISTRE des detecteurs. Une panne DECLAREE absente d'ici n'est pas accusee --
# elle est NOMMEE < sans detecteur > dans la vue (une couverture muette serait muette).
DETECTEURS = {
    "serie-stricte-violee": detecter_serie_stricte,
    "mission-qui-n-avance-pas": detecter_age_mission,
    "mission-chargee-sans-conduite": detecter_chargee_sans_debut,
    "cloture-fausse": detecter_cloture_fausse,
    "lot-perdu": detecter_lot_sans_tete,
    "enchainement-stop": detecter_stop_sans_suite,
    "brin-perime": detecter_brin_perime,
    "item-qui-dort": detecter_item_dort,
    "pause-oubliee": detecter_pause_contradictoire,
    "bilan-absent": detecter_bilan_absent,
    "bilan-adresse-a-autre": detecter_bilan_adresse_a_autre,
    "cablage-outil-non-enregistre": detecter_cablage_non_enregistre,
    "round-arme-jamais-pris": detecter_round_arme_jamais_pris,
    "round-pris-jamais-conduit": detecter_round_pris_jamais_conduit,
    "bilan-rapport-entre-deux-rounds": detecter_bilan_rapport,
    "poids-qui-derive": detecter_poids_derive,
    "source-non-injectee": detecter_source_non_injectee,
}
# DECLAREES ET NON DETECTABLES, avec la RAISON (mesuree, jamais une excuse) :
SANS_DETECTEUR = {
    "pilote-muet": "couvert par le detecteur serie-stricte-violee (meme lecture : le code de la porte)",
    "injection-refusee": "le refus d injection N EST PAS JOURNALISE (mesure du 2026-09-22 : "
                         "aucun evenement de refus dans l outbox) -- aucune source ne porte le fait",
}


def jouer_detecteurs(vue):
    """(pannes, couverture) -- chaque panne rendue porte son verdict, sa gravite, son silence."""
    sortie_pilote = (None, "")
    try:
        processus = lancer_enfant(
            [sys.executable, str(vue.pilote / "main.py"), "file"],
            cwd=str(vue.pilote), capture_output=True, text=True, timeout=60)
        sortie_pilote = (processus.returncode, (processus.stdout or "") + (processus.stderr or ""))
    except (OSError, subprocess.SubprocessError) as erreur:
        sortie_pilote = (99, type(erreur).__name__ + " : " + str(erreur)[:80])
    declarees = [p.get("id") for p in (vue.declaration.get("pannes") or [])]
    pannes = []
    for identifiant in declarees:
        detecteur = DETECTEURS.get(identifiant)
        if detecteur is None:
            continue
        trouvee = detecteur(vue, vue.declaration, sortie_pilote)
        if trouvee:
            gravite, constat, motif, silence, repare = trouvee
            pannes.append({"id": identifiant, "gravite": gravite, "constat": constat,
                           "motif": motif, "silence": silence, "repare": repare})
    couverture = {"detectees": len(DETECTEURS), "declarees": len(declarees),
                  "sans_detecteur": {identifiant: SANS_DETECTEUR.get(
                      identifiant, "aucun detecteur ecrit pour cette panne declaree")
                      for identifiant in declarees if identifiant not in DETECTEURS}}
    # EXCEPTIONS OUVERTES : une panne CONSTATEE et DEPOSEE (item) reste VISIBLE mais
    # n arrete plus la suite. C est la doctrine des exemptions : NOMMEE et MOTIVEE,
    # jamais muette (MO-075) -- et la declaration seule peut en ouvrir une.
    ouvertes = {p.get("id"): p.get("ouverte") for p in (vue.declaration.get("pannes") or [])
                if isinstance(p.get("ouverte"), dict)}
    for panne in pannes:
        ouverte = ouvertes.get(panne["id"])
        if ouverte:
            panne["ouverte"] = ouverte
    couverture["ouvertes"] = {i: o for i, o in ouvertes.items() if i in {p["id"] for p in pannes}}
    return pannes, couverture


# --- LA VUE ------------------------------------------------------------------

def rendre_vue(vue, pannes, couverture):
    lignes = list(CARTE_VUE) + ["",
                                "# SUIVI DU PILOTE -- la vue derivee",
                                "",
                                "> Regeneree par la porte `suivi-pilote` (T2 de PB-003/SP-003/TD-003).",
                                "> Jamais editee a la main : elle se RECALCULE. Les faits du pilote vivent",
                                "> dans suivi-optimus, file-missions, entonnoir, cycle-historique, outbox et",
                                "> le journal des pauses -- ici, seulement ce que l instrument a JUGE.",
                                "",
                                "Mesure du " + vue.maintenant.strftime("%Y-%m-%d %H:%M:%S")
                                + " | pannes declarees : " + str(couverture["declarees"])
                                + " | detecteurs joues : " + str(couverture["detectees"]) + "."]
    if couverture["sans_detecteur"]:
        lignes += ["", "Pannes DECLAREES sans detecteur (couverture dite, jamais muette) :"]
        for identifiant, raison in sorted(couverture["sans_detecteur"].items()):
            lignes.append("- " + ascii_propre(identifiant) + " : " + ascii_propre(raison))
    lignes += ["", "## Table 0 -- PANNES (la seule qui crie)"]
    if not pannes:
        lignes += ["", "**" + ENCART_VIDE + "** -- les parties lues ci-dessous sont coherentes."]
    else:
        lignes += ["", "| Gravite | Panne | Constat | Silence | Porte qui repare |",
                   "|---|---|---|---|---|"]
        for panne in pannes:
            lignes.append("| " + " | ".join(ascii_propre(panne[cle]) for cle in
                                             ("gravite", "id", "constat", "silence", "repare")) + " |")
        lignes += ["", "Motifs : " + ascii_propre(
            " ; ".join(p["id"] + " -- " + p["motif"] for p in pannes)) + "."]
        if couverture.get("ouvertes"):
            lignes += ["", "OUVERTES (constatees, deposees, suivies -- jamais tues) :"]
            for identifiant, ouverte in sorted(couverture["ouvertes"].items()):
                lignes.append("- " + ascii_propre(identifiant) + " : item "
                              + ascii_propre(ouverte.get("item", "?")) + " -- "
                              + ascii_propre(ouverte.get("motif", "")))

    chemin_outbox = vue.racine.joinpath(*MOTIF_OUTBOX)
    injections = [e for e in lire_jsonl(chemin_outbox) if e.get("type") == "injection"]
    lignes_1 = [(e.get("mission", "?"), e.get("date", MENTION_INCONNU),
                 e.get("poids_tokens", MENTION_INCONNU),
                 len(e.get("lecons_utiles") or []) or MENTION_INCONNU)
                for e in injections[-12:]]
    lignes += rendre_table(1, "INJECTION (partie injection/)",
                           ("Mission", "Injectee le", "Poids (tok)", "Lecons utiles"),
                           lignes_1,
                           "Une injection est un INSTANT : aucune duree. La colonne Refus n EXISTE "
                           "PAS : le refus d injection n est pas journalise (mesure du 2026-09-22) -- "
                           "une colonne toujours < inconnu > serait un placeholder qui ment.")

    lignes_2 = []
    for mission in vue.missions():
        if mission.get("statut") not in ("en-cours", "en-attente"):
            continue
        fait = vue.dernier_fait.get(mission.get("id"))
        age = minutes_ecoulees(mission.get("chargee_le"), vue.maintenant)
        lignes_2.append((mission.get("id", "?"), mission.get("statut", "?"),
                         "oui" if mission.get("id") in vue.lot() else "non",
                         duree_dite(age) if age is not None else MENTION_INCONNU,
                         fait[2] if fait else MENTION_INCONNU,
                         duree_dite((vue.maintenant - fait[0]).total_seconds() / 60.0)
                         if fait else MENTION_INCONNU))
    lignes += rendre_table(2, "FILE (partie file/)",
                           ("Mission", "Statut", "Dans le lot", "En attente depuis",
                            "Dernier fait", "Silence"), lignes_2,
                           "Silence = l ecart entre l ouverture et le dernier fait : la colonne "
                           "qui voit une mission ouverte qui n avance plus.")

    ids = vue.lot()
    par_id = {m.get("id"): m for m in vue.missions()}
    ecoulees = [i for i in ids if par_id.get(i, {}).get("statut") in ("terminee", "retiree")]
    retirees = [i for i in ids if par_id.get(i, {}).get("retiree_le")]
    tete = (vue.en_cours() or [{}])[0].get("id") or (vue.brin()[0].get("id") if vue.brin() else None)
    vertueuses = (vue.entonnoir or {}).get("auto_validees") or []
    suite = MENTION_INCONNU if not tete else str(tete)
    lignes_3 = [("lot-" + str(len(ids)), len(ids), len(ecoulees), len(retirees),
                 tete or MENTION_INCONNU, suite)]
    lignes += rendre_table(3, "LOT (partie file/, a part)",
                           ("Lot", "Portee", "Ecoulees", "Retirees", "Tete", "Enchainement"),
                           lignes_3,
                           "Panne lue : portee sans tete, ou STOP sans motif. Les colonnes Arme le et "
                           "Retour consolide n existent PAS : aucune source ne les porte "
                           "aujourd hui -- une colonne toujours < inconnu > serait un placeholder.")

    entonnoir = vue.entonnoir or {}
    files = entonnoir.get("files") or {}
    lignes_4 = []
    for nom, items in sorted(files.items()):
        items = items or []
        tete_item = items[0] if items else {}
        age = minutes_ecoulees(tete_item.get("deposee_le"), vue.maintenant)
        lignes_4.append((nom, len(items), tete_item.get("id", MENTION_INCONNU),
                         tete_item.get("urgence", MENTION_INCONNU),
                         duree_dite(age) if age is not None else MENTION_INCONNU))
    lignes += rendre_table(4, "ENTONNOIR (files)",
                           ("File", "Items", "Tete", "Urgence de la tete", "Age de la tete"),
                           lignes_4, "Age : un item qui vieillit est un travail qui dort.")

    lignes_5 = []
    for rang, item in enumerate(vue.brin(), 1):
        age = minutes_ecoulees(item.get("deposee_le"), vue.maintenant)
        lignes_5.append((rang, item.get("id", "?"), item.get("urgence", MENTION_INCONNU),
                         item.get("categorie", MENTION_INCONNU),
                         item.get("deposee_le", MENTION_INCONNU),
                         duree_dite(age) if age is not None else MENTION_INCONNU))
    lignes += rendre_table(5, "BRIN", ("Rang", "Item", "Urgence", "Categorie", "Depose le", "Age"),
                           lignes_5, "Coherence : brin = " + str(len(vue.brin())) + " ; files = "
                           + str(sum(len(v or []) for v in files.values())) + ".")

    est_auto, erreur_auto = charger_est_auto(vue.pilote)
    if est_auto is None:
        raison_auto = "verdict non resolu (import du pilote muet : " + erreur_auto + ")"
    else:
        raison_auto = ""
    lignes_6 = []
    fins = sorted([e for e in vue.evenements if e.get("action") == "fin"],
                  key=lambda e: str(e.get("date") or ""))[-12:]
    for evenement in fins:
        mission_id = evenement.get("mission")
        mission = par_id.get(mission_id) or {"id": mission_id}
        if est_auto is None:
            verdict = MENTION_INCONNU
        else:
            verdict = "auto" if est_auto(mission, vertueuses) else "STOP"
        lignes_6.append((mission_id, evenement.get("date", MENTION_INCONNU),
                         "ABSENT" if "TRACE MUETTE" in str(evenement.get("detail") or "") else "pose",
                         verdict))
    lignes += rendre_table(6, "CLOTURES ET ENCHAINEMENT (partie fin/)",
                           ("Mission close", "Fin a", "Bilan", "Enchainement"), lignes_6,
                           "La DUREE d une mission vit dans suivi-optimus : elle n est PAS recopiee ici. "
                           "Le verdict d enchainement vient de la FONCTION du pilote (provenance de "
                           "l item), jamais d une comparaison d ids."
                           + ((" " + raison_auto) if raison_auto else ""))

    lignes_7 = [(item.get("id", "?"), item.get("deposee_le", MENTION_INCONNU),
                 item.get("type", MENTION_INCONNU), "au vrac (non classee)",
                 item.get("urgence", MENTION_INCONNU)) for item in (entonnoir.get("vrac") or [])]
    lignes += rendre_table(7, "DEMANDES FILTREES (vrac)",
                           ("Demande", "Recue le", "Porte visee", "Action posee", "Urgence"),
                           lignes_7,
                           "Panne lue : une demande recue et jamais classee (le vrac ne se vide pas).")

    journal_pauses = lire_jsonl(vue.racine / CHEMIN_PAUSES)
    etat_present = (vue.racine / CHEMIN_ETAT_PAUSE).is_file()
    lignes_8 = [("pause de session", "en pause" if etat_present else "active",
                 journal_pauses[-1].get("date") if journal_pauses else MENTION_INCONNU,
                 (str(journal_pauses[-1].get("type")) + " : "
                  + str(journal_pauses[-1].get("raison") or ""))[:70] if journal_pauses
                 else MENTION_INCONNU)]
    for evenement in lire_jsonl(vue.racine / CHEMIN_DEFCON)[-6:]:
        if evenement.get("niveau") is not None:
            lignes_8.append(("defcon", str(evenement.get("niveau")),
                             evenement.get("date", MENTION_INCONNU),
                             str(evenement.get("motif", MENTION_INCONNU))[:70]))
    lignes += rendre_table(8, "GARDES (pause de session, defcon)",
                           ("Garde", "Etat", "Depuis", "Motif"), lignes_8,
                           "Panne lue : une pause armee et oubliee -- ou le JOURNAL et l ETAT qui "
                           "se contredisent (l agent s arrete et personne ne le voit).")
    return lignes


def tracer(racine, chemin_journal, pannes, signature):
    """N ajoute QUE ce qui n a pas deja ete dit (meme id, meme signature), PAR LA PORTE."""
    deja = {(e.get("id"), e.get("signature")) for e in lire_jsonl(chemin_journal)}
    neuves = [p for p in pannes if (p["id"], signature) not in deja]
    if not neuves:
        return 0, "rien de neuf (les verdicts sont deja traces)"
    contenu = "".join(json.dumps({"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                  "id": p["id"], "gravite": p["gravite"], "constat": p["constat"],
                                  "silence": p["silence"], "signature": signature}) + "\n" for p in neuves)
    mode = "ajouter" if chemin_journal.is_file() else "creer"
    code, sortie = publier(racine, chemin_journal, contenu, mode)
    if code != 0:
        return 0, "REFUS de la porte : " + sortie[-200:]
    return len(neuves), str(len(neuves)) + " verdict(s) trace(s) (" + mode + ")"


# --- L AUTO-TEST (L-032) : le cobaye MORD, le contre-temoin EPARGNE ----------

def auto_test(racine):
    """Eprouve les detecteurs sur des faits FABRIQUES, en memoire : aucun disque touche."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)

    declaration, erreur = lire_json(racine / DOSSIER_SUIVI / NOM_DECLARATION)
    if declaration is None:
        print("REFUS : declaration illisible (" + str(erreur) + ")")
        return 2
    vue = Vue(racine, declaration)
    if not vue.missions():
        print("REFUS : la file du pilote est vide -- aucun cobaye possible.")
        return 2
    cobaye = copy.deepcopy(vue.missions()[0])
    cobaye["id"] = "MO-900"
    cobaye["statut"] = "en-cours"
    cobaye["chargee_le"] = vue.maintenant.replace(year=vue.maintenant.year - 1).strftime("%Y-%m-%d %H:%M:%S")
    # ISOLEMENT : le cobaye est juge SEUL -- la file REELLE (une mission longue
    # legitimement ouverte) ne doit pas colorer le verdict de l epreuve.
    vue.file_missions = {"missions": [cobaye], "compteur": 0, "lot": {"ids": []}}
    trouvee = detecter_age_mission(vue, declaration, (0, ""))
    controler("le detecteur MORD sur une mission en cours hors seuil", trouvee is not None,
              "MO-900 accuse (chargee il y a un an)")
    cobaye["chargee_le"] = vue.maintenant.strftime("%Y-%m-%d %H:%M:%S")
    controler("le detecteur EPARGNE une mission chargee a l instant",
              detecter_age_mission(vue, declaration, (0, "")) is None, "aucune accusation")
    cobaye["statut"] = "terminee"
    cobaye["chargee_le"] = vue.maintenant.strftime("%Y-%m-%d %H:%M:%S")
    controler("le detecteur EPARGNE une mission close (le statut compte)",
              detecter_age_mission(vue, declaration, (0, "")) is None, "aucune accusation")
    # LA REGLE CORRIGEE PAR LA MESURE : une mission < en-attente > du lot n a pas de
    # `debut` (mesure : 31 sur 31) et le lot partage UN SEUL `chargee_le` -- elle est
    # donc EPARGNEE ; seule une mission donned EN COURS sans debut est accusee.
    vue.file_missions = {"missions": [cobaye], "compteur": 0, "lot": {"ids": ["MO-900"]}}
    cobaye["statut"] = "en-attente"
    controler("le detecteur EPARGNE une mission du lot en attente (31 cas reels eprouves)",
              detecter_chargee_sans_debut(vue, declaration, (0, "")) is None,
              "en-attente sans debut : aucune accusation")
    cobaye["statut"] = "en-cours"
    cobaye["chargee_le"] = vue.maintenant.replace(
        year=vue.maintenant.year - 1).strftime("%Y-%m-%d %H:%M:%S")
    controler("le detecteur MORD sur une mission EN COURS sans debut declare",
              detecter_chargee_sans_debut(vue, declaration, (0, "")) is not None,
              "en-cours sans debut : MO-900 accuse")
    # LA CHARGE TRACEE (demande du createur, 2026-09-22) : l acte de charger est
    # desormais une trace, et c est elle qui rend la classe EO-356 MESURABLE.
    vieux = vue.maintenant.replace(year=vue.maintenant.year - 1).strftime("%Y-%m-%d %H:%M:%S")
    vue.file_missions = {"missions": [
        {"id": "MO-901", "statut": "en-attente", "theme": "PILOTE", "chargee_le": vieux},
        {"id": "MO-902", "statut": "en-attente", "theme": "PILOTE", "chargee_le": vieux,
         "lot": "LOT-COBAYE"}],
        "compteur": 0, "lot": {"ids": ["MO-902"]}}
    vue.dates_par_mission = {}
    vue.evenements = [{"action": "charge", "mission": "MO-901", "date": vieux},
                      {"action": "charge", "mission": "MO-902", "date": vieux}]
    controler("le detecteur MORD sur une charge INDIVIDUELLE jamais conduite",
              detecter_chargee_sans_debut(vue, declaration, (0, "")) is not None,
              "MO-901 chargee il y a un an, aucun debut")
    vue.evenements = [{"action": "charge", "mission": "MO-902", "date": vieux}]
    controler("le detecteur EPARGNE une charge de LOT (elle ATTEND son tour)",
              detecter_chargee_sans_debut(vue, declaration, (0, "")) is None,
              "MO-902 appartient a un lot : etat legitime, aucune accusation")
    vue.evenements = [{"action": "charge", "mission": "MO-901", "date": vieux},
                      {"action": "fin", "mission": "MO-902", "date": vieux}]
    controler("le detecteur MORD sur une CLOTURE FAUSSE (la charge close sous un autre nom)",
              detecter_cloture_fausse(vue, declaration, (0, "")) is not None,
              "MO-901 chargee, MO-902 close : la mission ouverte n a jamais ete menee")
    vue.evenements = [{"action": "charge", "mission": "MO-901", "date": vieux},
                      {"action": "fin", "mission": "MO-901", "date": vieux}]
    controler("le detecteur EPARGNE une cloture qui NOMME la mission chargee",
              detecter_cloture_fausse(vue, declaration, (0, "")) is None,
              "charge MO-901 puis cloture MO-901 : la cloture est JUSTE")
    vue.evenements = [{"action": "charge", "mission": "MO-901", "date": vieux},
                      {"action": "report", "mission": "MO-901", "date": vieux},
                      {"action": "fin", "mission": "MO-902", "date": vieux}]
    controler("le detecteur EPARGNE une mission PARQUEE (sortie de round sans cloture)",
              detecter_cloture_fausse(vue, declaration, (0, "")) is None,
              "MO-901 chargee PUIS parquee : la cloture de MO-902 est JUSTE")
    # LE PARQUAGE ANTERIEUR (MO-416, mesure du 2026-09-25) : le round interrompu
    # parque sa mission PUIS charge la suivante ; la mission parquee reprend son
    # round et se close sous son nom. L exemption exige les DEUX faits.
    vue.evenements = [{"action": "report", "mission": "MO-902", "date": vieux},
                      {"action": "charge", "mission": "MO-901", "date": vieux},
                      {"action": "prise", "mission": "MO-902", "date": vieux},
                      {"action": "fin", "mission": "MO-902", "date": vieux}]
    controler("le detecteur EPARGNE la mission PARQUEE AVANT la charge PUIS reprise",
              detecter_cloture_fausse(vue, declaration, (0, "")) is None,
              "MO-902 parquee, MO-901 chargee, MO-902 reprise : sa cloture est JUSTE")
    vue.evenements = [{"action": "charge", "mission": "MO-901", "date": vieux},
                      {"action": "prise", "mission": "MO-902", "date": vieux},
                      {"action": "fin", "mission": "MO-902", "date": vieux}]
    controler("le detecteur MORD sans le PARQUAGE ANTERIEUR (la reprise ne suffit pas)",
              detecter_cloture_fausse(vue, declaration, (0, "")) is not None,
              "MO-902 repris mais jamais parque : la charge de MO-901 est close sous un autre nom")
    vue.evenements = [{"action": "report", "mission": "MO-902", "date": vieux},
                      {"action": "charge", "mission": "MO-901", "date": vieux},
                      {"action": "fin", "mission": "MO-902", "date": vieux}]
    controler("le detecteur MORD sans la REPRISE (le parquage seul ne suffit pas)",
              detecter_cloture_fausse(vue, declaration, (0, "")) is not None,
              "MO-902 parque mais jamais repris : la cloture ne vient pas d un round repris")
    # L ETAT DE PAUSE VIT DANS DEUX FICHIERS REELS (journal + etat) : l epreuve ne peut
    # pas les FABRIQUER sans ecrire sur le disque (interdit ici : "aucun disque touche").
    # Elle CONSTATE donc la paire REELLE -- le detecteur doit se taire quand les deux
    # s accordent (reprise journalisee + etat absent, ou pause + etat present) et MORDRE
    # quand ils se CONTREDISENT (EO-357). MESURE du 2026-09-25 : la paire reelle est
    # coherente (derniere ligne = reprise, etat absent) ; l ANCIENNE epreuve, qui ne
    # lisait QUE l etat, exigeait "MORD" et rendait un KO MENSONGER -- elle accusait un
    # detecteur JUSTE. Le journal est donc lu ICI, comme le fait le detecteur.
    journal_pause = lire_jsonl(racine / CHEMIN_PAUSES)
    en_pause = bool(journal_pause) and journal_pause[-1].get("type") == "pause"
    vrai_etat = (racine / CHEMIN_ETAT_PAUSE).is_file()
    contradiction_reelle = en_pause != vrai_etat
    trouvee_pause = detecter_pause_contradictoire(vue, declaration, (0, ""))
    controler("la pause CONTRADICTOIRE est jugee juste (journal "
              + ("en pause" if en_pause else "en reprise") + ", etat "
              + ("present" if vrai_etat else "absent") + ")",
              (trouvee_pause is not None) == contradiction_reelle,
              "MORD (paire contradictoire)" if contradiction_reelle
              else "EPARGNE (paire coherente)")
    # EO-360 : le round ARME et JAMAIS PRIS (la machine a servi, l agent n a pas pris).
    an_avant = vue.maintenant.replace(
        year=vue.maintenant.year - 1).strftime("%Y-%m-%d %H:%M:%S")
    vue.file_missions = {"missions": [
        {"id": "MO-903", "statut": "en-cours", "theme": "PILOTE",
         "injectee_le": an_avant, "chargee_le": an_avant}], "compteur": 0, "lot": None}
    vue.dates_par_mission = {"MO-903": {"debut": [an_avant]}}
    vue.evenements = [{"action": "prise", "mission": "MO-901", "date": an_avant},
                      {"action": "debut", "mission": "MO-903", "date": an_avant}]
    controler("le detecteur MORD sur un round ARME et JAMAIS PRIS",
              detecter_round_arme_jamais_pris(vue, declaration, (0, "")) is not None,
              "MO-903 servi il y a un an, aucune prise depuis l injection")
    vue.dates_par_mission = {"MO-903": {"debut": [an_avant], "prise": [an_avant]}}
    vue.evenements = [{"action": "debut", "mission": "MO-903", "date": an_avant},
                      {"action": "prise", "mission": "MO-903", "date": an_avant}]
    controler("le detecteur EPARGNE un round PRIS (meme s il dure longtemps)",
              detecter_round_arme_jamais_pris(vue, declaration, (0, "")) is None,
              "la prise est posterieure a l injection : le round a ete pris")
    vue.file_missions["missions"][0]["injectee_le"] = vue.maintenant.strftime("%Y-%m-%d %H:%M:%S")
    vue.dates_par_mission = {"MO-903": {"debut": [an_avant]}}
    vue.evenements = [{"action": "prise", "mission": "MO-901", "date": an_avant}]
    controler("le detecteur EPARGNE un round servi a l instant (le seuil compte)",
              detecter_round_arme_jamais_pris(vue, declaration, (0, "")) is None,
              "injection de maintenant : sous le seuil declare")
    # EO-364 : la PRISE ne BLANCHIT plus le round -- pris, puis RIEN.
    vue.file_missions = {"missions": [
        {"id": "MO-904", "statut": "en-cours", "theme": "PILOTE",
         "injectee_le": an_avant, "chargee_le": an_avant}], "compteur": 0, "lot": None}
    vue.dates_par_mission = {"MO-904": {"debut": [an_avant], "prise": [an_avant]}}
    vue.evenements = [{"action": "prise", "mission": "MO-904", "date": an_avant}]
    vue.dernier_fait = {"MO-904": (horodate(an_avant), an_avant, "prise")}
    controler("le detecteur MORD sur un round PRIS et JAMAIS CONDUIT",
              detecter_round_pris_jamais_conduit(vue, declaration, (0, "")) is not None,
              "MO-904 : dernier acte = prise, il y a un an, RIEN depuis")
    vue.dernier_fait = {"MO-904": (horodate(an_avant), an_avant, "intervention")}
    controler("le detecteur EPARGNE un round dont un ACTE suit la prise",
              detecter_round_pris_jamais_conduit(vue, declaration, (0, "")) is None,
              "dernier acte = intervention : le round est CONDUIT")
    maintenant_texte = vue.maintenant.strftime("%Y-%m-%d %H:%M:%S")
    vue.dernier_fait = {"MO-904": (horodate(maintenant_texte), maintenant_texte, "prise")}
    controler("le detecteur EPARGNE une prise RECENTE (le seuil compte)",
              detecter_round_pris_jamais_conduit(vue, declaration, (0, "")) is None,
              "prise de maintenant : sous le seuil declare")
    # EO-368 : l HABITUDE < bilan-rapport entre deux rounds > -- un round PRIS se
    # CONDUIT. Le signal est le SILENCE d activite (le sac-a-dos, hors `auto`), plus
    # fin que le marbre. Le cobaye FABRIQUE la valeur : aucun disque touche.
    vue.file_missions = {"missions": [
        {"id": "MO-905", "statut": "en-cours", "theme": "PILOTE",
         "injectee_le": an_avant, "chargee_le": an_avant}], "compteur": 0, "lot": None}
    vue.dernier_fait = {"MO-905": (horodate(an_avant), an_avant, "prise")}
    vue.acte_agent = horodate(an_avant)   # le dernier outil invoque AVANT la prise
    controler("le detecteur MORD sur une PRISE suivie d un SILENCE d activite",
              detecter_bilan_rapport(vue, declaration, (0, "")) is not None,
              "MO-905 pris il y a un an, aucun outil invoque depuis")
    vue.acte_agent = vue.maintenant   # un outil vient d etre invoque : round CONDUIT
    controler("le detecteur EPARGNE un acte de l agent APRES la prise",
              detecter_bilan_rapport(vue, declaration, (0, "")) is None,
              "un outil a ete invoque depuis la prise : le round est CONDUIT")
    vue.acte_agent = horodate(an_avant)
    vue.dernier_fait = {"MO-905": (horodate(maintenant_texte), maintenant_texte, "prise")}
    controler("le detecteur EPARGNE une prise RECENTE (le seuil compte)",
              detecter_bilan_rapport(vue, declaration, (0, "")) is None,
              "prise de maintenant : sous le seuil declare")
    vue.acte_agent = horodate(an_avant)
    vue.dernier_fait = {"MO-905": (horodate(an_avant), an_avant, "intervention")}
    controler("le detecteur EPARGNE un dernier acte QUI N EST PAS une prise",
              detecter_bilan_rapport(vue, declaration, (0, "")) is None,
              "dernier acte = intervention : la panne ne s applique pas")
    # EO-362 : LE GARDE DE TRACE VOIT LE FAIT, PAS LA CASSE. Le cobaye est un DOMICILE
    # fabrique en memoire (aucun disque touche). La regle eprouvee est celle du PILOTE,
    # importee -- la recopier serait une copie de plus (L-029).
    fonction_trace, erreur_trace = charger_fichiers_de_la_mission(racine / DOSSIER_PILOTE)
    if fonction_trace is None:
        controler("la regle de derivation est EPROUVABLE (import du pilote)",
                  False, "import muet : " + erreur_trace)
    else:
        domicile_cobaye = {"fichiers": {
            "minuscule.py": {"modifications": [{"detail": "travail", "tags": ["mo-900"]}]},
            "majuscule.py": {"modifications": [{"detail": "travail", "tags": ["MO-900"]}]},
            "mention.py": {"modifications": [{"detail": "MO-900 : mention en tete", "tags": []}]},
            "loin.py": {"modifications": [{"detail": ("x" * 80) + " MO-900", "tags": []}]},
            "voisin.py": {"modifications": [{"detail": "autre mission", "tags": ["MO-901"]}]},
        }}
        controler("le cobaye MORD : un tag en MINUSCULES (mo-900) NOMME la mission MO-900",
                  sorted(fonction_trace("MO-900", domicile_cobaye))
                  == ["majuscule.py", "mention.py", "minuscule.py"],
                  "3 fichiers : deux par TAG, un par MENTION en tete")
        controler("le contre-temoin EPARGNE la mention HORS FENETRE (la casse n elargit rien)",
                  "loin.py" not in fonction_trace("MO-900", domicile_cobaye),
                  "loin.py non retenu : seule la TETE du detail compte")
        controler("le contre-temoin EPARGNE le voisin (MO-901 n herite pas de MO-900)",
                  fonction_trace("MO-901", domicile_cobaye) == ["voisin.py"],
                  "1 fichier, le bon")
        controler("le contre-temoin EPARGNE la mission qui n a RIEN touche",
                  fonction_trace("MO-903", domicile_cobaye) == [],
                  "aucun fichier : la colonne sera muette, et elle le DIRA")
    # EO-420 : l ARRIERE du brin -- la mesure ne porte plus sur la seule tete. Le cobaye
    # porte une TETE FRAICHE et un DORMEUR en arriere : l ancienne regle (brin[0] seul)
    # rendait None sur ce fait, la neuve MORD -- et elle NOMME combien dorment, et lequel
    # est le plus vieux. Le contre-temoin EPARGNE un brin entierement frais, puis un brin VIDE.
    frais = vue.maintenant.strftime("%Y-%m-%d %H:%M:%S")
    vue.entonnoir = {"brin": [{"id": "EO-900", "deposee_le": frais},
                              {"id": "EO-901", "deposee_le": frais},
                              {"id": "EO-902", "deposee_le": an_avant}]}
    trouvee_dort = detecter_item_dort(vue, declaration, (0, ""))
    controler("le detecteur MORD sur un dormeur d ARRIERE alors que la TETE est fraiche",
              trouvee_dort is not None,
              "EO-900 (tete) depose a l instant ; EO-902 dort depuis un an")
    controler("l accusation NOMME le nombre de dormeurs ET le plus vieux",
              bool(trouvee_dort) and "1 item" in trouvee_dort[1] and "EO-902" in trouvee_dort[1],
              "constat : " + (trouvee_dort[1] if trouvee_dort else "AUCUNE ACCUSATION"))
    vue.entonnoir = {"brin": [{"id": "EO-900", "deposee_le": frais},
                              {"id": "EO-901", "deposee_le": frais}]}
    controler("le detecteur EPARGNE un brin ENTIEREMENT frais",
              detecter_item_dort(vue, declaration, (0, "")) is None, "aucune accusation")
    vue.entonnoir = {"brin": []}
    # EO-489 (2026-09-29, decision createur sur la question ouverte depuis MO-460) : le
    # SCAN etait bon (EO-420), mais le REMEDE etait inexecutable. Il nommait "l arriere"
    # et proposait `file verser --lot` -- or verser_tresse verse le brin ENTIER, sans
    # filtre, et un lot n aurait debloque rien (les items sont auto_validation non,
    # bloques par l axe perimetre). MESURE A LA SOURCE : le jour de la decision, les
    # 2 dormeurs accuses portaient position_brin 1 et 2 -- ils etaient les TETES. Le
    # cout n est pas la faute du scan : c est que la sortie NE DISAIT PAS OU elle
    # regardait, donc son lecteur a deduit un arriere inexistant.
    # Le cobaye exige le RANG DIT, et un remede qui ne prescrit plus le lot. Le
    # contre-temoin (le mot "lot" absent SANS que la DETECTION bouge) est ce qui
    # distingue une reparation de texte d une reparation de comportement.
    # La fixture met le DORMEUR EN TETE, car c est precisement le cas qui avait
    # produit la question : un dormeur de rang 1 ne demande rien a vider derriere lui.
    vue.entonnoir = {"brin": [{"id": "EO-902", "deposee_le": an_avant},
                              {"id": "EO-900", "deposee_le": frais}]}
    trouvee_tete = detecter_item_dort(vue, declaration, (0, ""))
    controler("le remede DIT le RANG du dormeur (EO-489 : sans lui, on invente un arriere)",
              bool(trouvee_tete) and "rang 1/2" in trouvee_tete[1]
              and "rang 1/2" in trouvee_tete[4],
              "resume : " + (trouvee_tete[1] if trouvee_tete else "AUCUNE ACCUSATION")
              + " | remede : " + (trouvee_tete[4] if trouvee_tete else "AUCUN REMEDE"))
    vue.entonnoir = {"brin": [{"id": "EO-900", "deposee_le": frais},
                              {"id": "EO-901", "deposee_le": frais},
                              {"id": "EO-902", "deposee_le": an_avant}]}
    trouvee_fond = detecter_item_dort(vue, declaration, (0, ""))
    controler("un dormeur REELLEMENT en fond est dit comme tel (le cas n est pas masque)",
              bool(trouvee_fond) and "rang 3/3" in trouvee_fond[4]
              and "apres les 2 item(s)" in trouvee_fond[4],
              "remede : " + (trouvee_fond[4] if trouvee_fond else "AUCUN REMEDE"))
    sortie_tete = " ".join(str(x) for x in trouvee_tete) if trouvee_tete else ""
    controler("le remede ne prescrit PLUS le lot, qui n est pas selectif (contre-temoin EO-489)",
              "lot" not in sortie_tete and "arriere" not in sortie_tete,
              "sortie : " + (sortie_tete if sortie_tete else "VIDE"))
    controler("malgre ce texte change, la DETECTION reste la MEME (le constat porte toujours)",
              bool(trouvee_tete) and "EO-902" in trouvee_tete[1]
              and trouvee_tete[0] == "normale" and an_avant == trouvee_tete[3],
              "constat : " + (trouvee_tete[1] if trouvee_tete else "AUCUNE ACCUSATION")
              + " | silence : " + (trouvee_tete[3] if trouvee_tete else "AUCUN"))
    # MO-416 (EO-432) : LA SOURCE D INJECTION servie AU MOMENT, et sa trace DECLAREE. Le
    # decideur est CONSOMME de son domicile (jamais recopie) ; le controle LIT le journal.
    maintenant_texte = vue.maintenant.strftime("%Y-%m-%d %H:%M:%S")
    vue.file_missions = {"missions": [
        {"id": "MO-905", "statut": "en-cours", "theme": "BDD", "injectee_le": maintenant_texte,
         "objectif": "il faut refaire le meme geste a la main chaque fois"},
        {"id": "MO-906", "statut": "en-cours", "theme": "BDD", "injectee_le": maintenant_texte,
         "objectif": "corriger le libelle du bouton du formulaire"}], "compteur": 0, "lot": None}
    vue.evenements = []
    controler("le detecteur MORD sur une source NON INJECTEE (le resultat se redemande)",
              detecter_source_non_injectee(vue, declaration, (0, "")) is not None,
              "MO-905 redemande un geste et son injection ne porte AUCUNE trace")
    vue.evenements = [{"action": "injection", "mission": "MO-905", "date": maintenant_texte,
                       "detail": "source si-j-etais-user servie (moment encore)"}]
    controler("le detecteur EPARGNE la source DECLAREE (il LIT ce que le pilote a declare)",
              detecter_source_non_injectee(vue, declaration, (0, "")) is None,
              "la trace nomme la source : le controle lecteur se tait")
    vue.evenements = []
    vue.file_missions["missions"] = [vue.file_missions["missions"][1]]
    controler("le detecteur EPARGNE une mission qui ne redemande RIEN",
              detecter_source_non_injectee(vue, declaration, (0, "")) is None,
              "MO-906 ne redemande aucun geste : la source ne sert pas")
    vue.file_missions["missions"] = [{"id": "MO-907", "statut": "en-cours", "theme": "BDD",
                                      "injectee_le": an_avant,
                                      "objectif": "je dois refaire ca a la main"}]
    controler("le detecteur EPARGNE une mission servie AVANT la pose de la source",
              detecter_source_non_injectee(vue, declaration, (0, "")) is None,
              "injectee avant le seuil `depuis` : aucune accusation retroactive")
    _, omises = garder_colonnes(("Verdict", "Toujours pareil"), [("a", "-"), ("b", "-")])
    controler("une colonne CONSTANTE est omise, une colonne de VERDICT est gardee",
              [nom for nom, _ in omises] == ["Toujours pareil"], "omise : Toujours pareil")
    controler("le seuil se lit dans la DECLARATION (aucun seuil en dur)",
              seuil_de(declaration, "mission-qui-n-avance-pas") is not None,
              "mission-qui-n-avance-pas = " + str(seuil_de(declaration, "mission-qui-n-avance-pas")))
    colonnes = set()
    for ligne in lire_jsonl(racine / DOSSIER_SUIVI / NOM_JOURNAL):
        colonnes |= set(ligne.keys())
    controler("le journal des verdicts ne porte QUE des verdicts",
              colonnes <= set(CLES_JOURNAL),
              "cles : " + ", ".join(sorted(colonnes)) if colonnes else "journal vide (aucun verdict)")
    _, couverture = jouer_detecteurs(vue)
    controler("la couverture des pannes est DITE (aucune panne declaree muette)",
              couverture["declarees"] == couverture["detectees"] + len(couverture["sans_detecteur"]),
              str(couverture["declarees"]) + " declarees = " + str(couverture["detectees"])
              + " detecteurs + " + str(len(couverture["sans_detecteur"])) + " nommees")
    return 0 if all(resultats) else 1


def principal(arguments):
    parseur = argparse.ArgumentParser(description="Porte du suivi du pilote d Optimus (vue derivee).")
    parseur.add_argument("--racine", default=".", help="racine du depot")
    parseur.add_argument("--json", action="store_true", help="la vue en JSON")
    parseur.add_argument("--auto-test", action="store_true", help="eprouve les detecteurs")
    options = parseur.parse_args(arguments)
    racine = trouver_racine(Path(options.racine).resolve())
    if racine is None:
        print("REFUS : racine introuvable (aucun _operateur/optimus-prime/pilote/commun.py).")
        return 2
    if options.auto_test:
        return auto_test(racine)
    declaration, erreur = lire_json(racine / DOSSIER_SUIVI / NOM_DECLARATION)
    if declaration is None:
        print("REFUS : declaration des pannes illisible (" + str(erreur) + ") : "
              + str(racine / DOSSIER_SUIVI / NOM_DECLARATION)
              + " -- sans elle, une porte qui crie crierait au hasard.")
        return 2
    vue = Vue(racine, declaration)
    pannes, couverture = jouer_detecteurs(vue)
    lignes = rendre_vue(vue, pannes, couverture)
    dossier = racine / DOSSIER_SUIVI
    vue_absente = not (dossier / NOM_VUE).is_file()
    code, sortie = publier(racine, dossier / NOM_VUE, "\n".join(lignes) + "\n",
                           "creer" if vue_absente else "remplacer")
    if code != 0:
        print("REFUS de la porte (vue) : " + sortie[-300:])
        return 2
    signature = "|".join(sorted(p["id"] for p in pannes)) or "sain"
    traces, dit = tracer(racine, dossier / NOM_JOURNAL, pannes, signature)
    # Seules les pannes NON ouvertes font rougir : une exception NOMMEE ne gele pas la suite.
    rouges = [p for p in pannes if not p.get("ouverte")]
    if options.json:
        print(json.dumps({"vue": str(dossier / NOM_VUE), "pannes": pannes,
                          "couverture": couverture, "verdicts_traces": traces},
                         ensure_ascii=False, indent=2))
    else:
        print("SUIVI DU PILOTE -- vue recalculee : " + str(dossier / NOM_VUE))
        for panne in pannes:
            print("[KO] " + panne["id"] + " (" + panne["gravite"] + ") : " + panne["constat"]
                  + " | silence : " + str(panne["silence"]) + " | repare par : " + panne["repare"])
        for panne in pannes:
            if panne.get("ouverte"):
                print("[--] " + panne["id"] + " : OUVERTE (item " + str(panne["ouverte"].get("item"))
                      + ") -- " + str(panne["ouverte"].get("motif")))
        for identifiant, raison in sorted(couverture["sans_detecteur"].items()):
            print("[--] " + identifiant + " : declaree SANS detecteur -- " + raison)
        print("couverture : " + str(couverture["detectees"]) + "/" + str(couverture["declarees"])
              + " pannes declarees ont un detecteur | " + dit)
    if rouges:
        print("VERDICT : " + str(len(rouges)) + " PANNE(S) DU PILOTE -- " + ENCART_VIDE + " est FAUX.")
        return 1
    if pannes:
        print("VERDICT : " + str(len(pannes)) + " panne(s) constatee(s), TOUTES OUVERTES (suivies) -- "
              + "aucune panne NOUVELLE.")
        return 0
    print("VERDICT : " + ENCART_VIDE + ".")
    return 0


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
