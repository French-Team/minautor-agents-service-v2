#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lanceur-non-regression-flux.py -- Non-regression du FLUX (E-095, imperatif 62)

Imperatif 62 : une suite de non-regression ne surveille pas les FICHIERS, elle
surveille le FLUX. Elle doit repondre a : la Matrice demarre ? le pilote
fonctionne ? des processus fantomes ? la file est bloquee ? un fichier manquant
casse-t-il la chaine ?

Cette suite parcourt les MAILLONS de la chaine, dans l'ordre du flux :
  1. PORTE D'ENTREE   : le selecteur de flux repond et un flux est actif
  2. SERVEUR MATRICE  : la Matrice est debout (elle survit aux pauses)
  3. ROUTINES         : chaque routine DECLAREE vit ET journalise la FIN de sa
                        passe (la liste se LIT, elle ne se recopie plus -- MO-478)
  4. PILOTE           : la porte du pilote repond, serie stricte respectee
  5. ENTONNOIR        : vrac/files/brin coherents (pas de brin perime)
  6. INTERCOM         : le dialogue Matrice <-> agent est lisible et valide
  7. FANTOMES         : aucun PID mort, et aucune routine SUPERVISEE declaree
                        ARRET au-dela de sa cadence declaree. Le pid fantome seul
                        ne suffit pas : le nettoyer faisait disparaitre le rouge
                        sans que la routine reparte (EO-404).
  8. RELAIS           : la bank de themes fournit une identite a l'agent
  9. FILE <-> JOURNAL : les DEUX traces d'optimus disent-elles la meme chose ?
                        (le pilote ecrit la file, l'agent declare au journal --
                        marbre L-020 -- donc rien ne les compare sans ce maillon)

Chaque maillon rompu est nomme AVEC son impact sur le flux (ou la chaine
s'arrete, ce qui la bloque, ce qu'elle sert de mort).

Garde L-026 : AUCUNE verification ne peut tuer la suite. Toute porte appelee
est protegee (OSError, timeout) et un maillon casse devient un verdict KO
nomme, jamais un arret silencieux.

Usage: python lanceur-non-regression-flux.py [--racine <path>] [--json]
  code 0 = flux sain, code 1 = flux rompu (maillons listes), code 2 = zone introuvable.
"""

import argparse
import importlib.util
import json
import os
import subprocess

import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-414, vague 4 du lot) -----------------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : on remonte
# jusqu au dossier `matrix`, et on REFUSE plutot que de deviner (garde-foi L-006).
_RACINE_LANCEMENT = Path(__file__).resolve().parent
while _RACINE_LANCEMENT.name != "matrix":
    if _RACINE_LANCEMENT.parent == _RACINE_LANCEMENT:
        raise RuntimeError("racine `matrix` introuvable en remontant depuis " + __file__)
    _RACINE_LANCEMENT = _RACINE_LANCEMENT.parent
_REPERTOIRE_COMMUN_LANCEMENT = _RACINE_LANCEMENT / "matrice" / "data" / "commun"
if not (_REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(_REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(_REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(_REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())

import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# --- SEUILS ET PORTES (aucune valeur en dur dans la logique) ----------------
SECONDES_MAX_PORTE = 60
SEUIL_FIN_MINUTES = 10
# Une routine en mode PASSE (planning, MO-429) est servie puis eteinte : le maillon
# 3 ne peut pas exiger un PID vivant, il exige que le SERVICE l ait reallumee dans
# un delai MEASURE en cadences -- au-dela, c est le service qui manque son tour.
NB_CADENCES_SERVIEES = 3
FORMAT_DATE = "%Y-%m-%d %H:%M:%S"
# Lecture BORNEE de la queue d'un journal (MO-077) : la surveillance d'une
# routine se lit dans ses DERNIERS evenements, jamais dans 87 Mo d'histoire.
# Mesure avant/apres : le dernier `passe` de l'espion etait cherche en balayant
# 540 608 lignes (87,7 Mo) a chaque execution de cette suite ; il est desormais
# lu dans la QUEUE BORNEE, pour un cout constant quelle que soit la taille.
# MO-099 : la FENETRE ne se declare plus ici -- elle vient du moteur PARTAGE
# (data/commun/rotation_journal.py), deduite de la borne declaree du journal lu.

# Maillons : (numero, cle, nom lisible). L'ordre EST l'ordre du flux.
MAILLONS = (
    (1, "selecteur", "PORTE D'ENTREE (selecteur de flux)"),
    (2, "serveur", "SERVEUR MATRICE (la Matrice est-elle debout ?)"),
    (3, "routines", "ROUTINES (les boucles vivent-elles ET finissent-elles ?)"),
    (4, "pilote", "PILOTE (la porte repond-elle ? serie stricte ?)"),
    (5, "entonnoir", "ENTONNOIR (vrac/files/brin coherents ?)"),
    (6, "intercom", "INTERCOM (le dialogue est-il lisible ?)"),
    (7, "fantomes", "FANTOMES ET ROUTINES MUETTES (des PID morts ? une routine declaree ARRET ?)"),
    (8, "relais", "RELAIS (un theme pour prendre une identite ?)"),
    (9, "file-journal", "FILE <-> JOURNAL (les deux traces d'optimus disent-elles la meme chose ?)"),
)

# Impact sur le flux, par etat de maillon.
IMPACTS = {
    "ok": "",
    "rompu": "le flux s'arrete a ce maillon",
    "fantome": "la chaine est annoncee debout alors qu'elle est tombee",
    "muette": "la chaine est annoncee partielle SANS dire qui manque -- une panne qui se lit comme un detail",
    "bloque": "le flux est bloque (la chaine n'avance plus)",
    "perime": "la chaine servirait une donnee morte",
    "flux-porte-morte": "l'entree du flux ne repond plus : personne ne peut demarrer",
    "divergent": "la file et la trace se contredisent : plus rien ne dit ce qui est vraiment fait",
}

# PLUS DE LISTE DE ROUTINES ICI (MO-478). Le maillon 3 lisait TROIS routines ecrites
# en dur quand la Matrice en supervise SEPT (`routines/vie/constants.py`) : les
# quatre autres pouvaient mourir sans que rien ne le voie (EO-404, meme lecon que le
# maillon 7). Il LIT desormais la TABLE DECLAREE et, pour chaque routine, sa
# declaration de FIN DE PASSE (`NOM_JOURNAL` / `EVENEMENT_FIN_PASSE`, lues CHEZ ELLE
# -- M-076 : un seul domicile). Deux listes = deux verites.


# --- OUTILLAGE : lecture seule, jamais d'exception ---------------------------

def processus_vivant(pid):
    """True si le PID designe un processus VIVANT (lecture seule, Windows + POSIX)."""
    try:
        if sys.platform.startswith("win"):
            import ctypes

            noyau = ctypes.windll.kernel32
            poignee = noyau.OpenProcess(0x1000, False, int(pid))  # PROCESS_QUERY_LIMITED_INFORMATION
            if not poignee:
                return False
            noyau.CloseHandle(poignee)
            return True
        os.kill(int(pid), 0)
        return True
    except (OSError, ValueError, TypeError, AttributeError):
        return False


def lire_pid(chemin):
    """Retourne le PID d'un fichier .pid, ou None si absent/illisible."""
    try:
        contenu = chemin.read_text(encoding="utf-8", errors="replace").strip()
        return int(contenu) if contenu else None
    except (OSError, ValueError):
        return None


def lancer(commande, cwd=None):
    """Appelle une porte officielle en sous-processus. Retourne (code, sortie).

    Jamais d'exception : un timeout devient 124, un OSError devient 1 avec son
    message. C'est la garde qui empeche une suite de mourir en silence.
    """
    try:
        resultat = lancer_enfant(
            commande,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=SECONDES_MAX_PORTE,
        )
        return resultat.returncode, (resultat.stdout or "") + (resultat.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "porte tuee par timeout " + str(SECONDES_MAX_PORTE) + "s"
    except OSError as erreur:
        return 1, "porte impossible a lancer : " + str(erreur)


def queue_journal(chemin_journal, octets):
    """Retourne les DERNIERES lignes d'un journal, sans balayer l'historique.

    La premiere ligne lue peut etre TRONQUEE (on a coupe au milieu d'une ligne) :
    elle n'est gardee que si la lecture a commence au debut du fichier.
    """
    if chemin_journal is None or not chemin_journal.is_file():
        return []
    try:
        taille = chemin_journal.stat().st_size
        debut = max(0, taille - octets)
        with open(str(chemin_journal), "rb") as flux:
            flux.seek(debut)
            bloc = flux.read()
    except OSError:
        return []
    lignes = bloc.decode("utf-8", errors="replace").splitlines()
    if debut > 0 and lignes:
        lignes = lignes[1:]
    return [ligne for ligne in lignes if ligne.strip()]


def dernier_evenement(chemin_journal, types_fin):
    """Retourne (date du dernier evenement de type types_fin, duree de lecture).

    Le chronometre est RENDU au maillon, qui l'affiche : la lecture bornee devient
    ainsi une propriete MESUREE a chaque execution, pas une intention.
    """
    debut = time.time()
    moment = None
    from rotation_journal import octets_queue_du_journal  # data/commun installe par main()
    for ligne in reversed(queue_journal(chemin_journal, octets_queue_du_journal(chemin_journal))):
        try:
            evenement = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if evenement.get("type") in types_fin:
            moment = evenement.get("date", "")
            break
    return moment, time.time() - debut


def age_minutes(date_texte):
    """Age en minutes d'une date au format des journaux, ou None si illisible."""
    try:
        return (datetime.now() - datetime.strptime(date_texte, FORMAT_DATE)).total_seconds() / 60.0
    except (ValueError, TypeError):
        return None


# --- LES 8 MAILLONS ---------------------------------------------------------

def maillon_selecteur(m):
    """Le flux a-t-il une porte d'entree qui repond ?"""
    code, sortie = lancer([sys.executable, str(m["selecteur"] / "main.py"), "actuel"])
    if code != 0:
        return "flux-porte-morte", "le selecteur ne repond pas (code " + str(code) + ")"
    if "FLUX1" in sortie:
        return "ok", "flux actif : FLUX1 (CAMELEON, Matrice guide)"
    if "FLUX2" in sortie:
        return "ok", "flux actif : FLUX2 (MAINTENANCE, Optimus seul)"
    return "flux-porte-morte", "aucun flux actif : la Matrice ne sait pas qui elle sert"


def maillon_serveur(m):
    """La Matrice est-elle debout (le serveur qui survit aux pauses) ?"""
    pid = lire_pid(m["pid_serveur"])
    if pid is None:
        return "rompu", "aucun PID serveur : la Matrice n'est pas demarree, rien ne survit aux pauses"
    if not processus_vivant(pid):
        return "fantome", "PID serveur " + str(pid) + " ecrit mais MORT"
    return "ok", "serveur Matrice vivant (PID " + str(pid) + ")"


def maillon_routines(m):
    """Les boucles DECLAREES vivent-elles ET finissent-elles leurs passes (L-026) ?

    La liste ne se RECOPIE pas : elle se LIT dans la table declaree
    (`routines/vie/constants.py`, celle que le serveur importe -- une seule verite,
    EO-404). Pour chacune, sa declaration de fin de passe se lit CHEZ ELLE
    (`NOM_JOURNAL` + `EVENEMENT_FIN_PASSE`) : une routine qui ne journalise pas sa
    fin le DECLARE (`None`), et le maillon le DIT au lieu d'inventer une fin.

    LE MODE (planning, MO-429) change l exigeance : une routine en mode `passe`
    est ETEINTE entre deux passes -- exiger un PID vivant l accuserait a tort a
    chaque tour (mesure du 2026-09-26 : la bascule en passe faisait rougir ce
    maillon sur un etat parfaitement normal). Elle est donc jugee sur sa
    DERNIERE FIN DE PASSE : au-dela de `NB_CADENCES_SERVIEES x sa cadence
    declaree`, personne ne la sert plus -- c est LE SERVICE qui manque son tour,
    et le maillon le dit en nommant le service.
    """
    table = table_des_routines(m)
    if table is None:
        return "rompu", (
            "la table des routines est illisible (routines/vie/constants.py) : "
            "impossible de savoir quelles boucles surveiller"
        )
    _boucles, _pids, lecteur, _modes, cause_mode = table
    if cause_mode:
        # Sans mode lisible, le maillon ne sait plus QUI doit vivre en permanence
        # et QUI doit s eteindre : il le DIT plutot que de juger sur une regle
        # qu il ne connait plus (L-055).
        return "rompu", "table des modes illisible -- " + cause_mode
    a_surveiller = routines_a_surveiller(table)
    rompus = []
    details = []
    journalisees = 0
    passees = 0
    for nom, dossier, nom_pid, mode in a_surveiller:
        pid = lire_pid(dossier / nom_pid)
        vivant = pid is not None and processus_vivant(pid)
        if mode == "passe" and not vivant:
            # ETEINTE entre deux passes = l ETAT NORMAL d une routine en passe :
            # on ne reclame pas de PID, on mesure depuis quand elle n a plus servi.
            passees += 1
            declaration = journal_declare_par_routine(dossier, nom)
            moment = None
            if declaration is not None and declaration[1]:
                moment, _duree = dernier_evenement(
                    dossier / declaration[0] if declaration[0] else None, declaration[1]
                )
            age = age_minutes(moment) if moment else None
            cadence = lire_cadence(lecteur, nom, dossier)
            seuil = SEUIL_FIN_MINUTES
            if isinstance(cadence, int) and cadence > 0:
                seuil = max(SEUIL_FIN_MINUTES, int(NB_CADENCES_SERVIEES * cadence / 60))
            if age is not None and age > seuil:
                rompus.append(
                    nom + " : en PASSE mais non servie depuis " + str(int(age))
                    + " min (> " + str(seuil) + " min = " + str(NB_CADENCES_SERVIEES)
                    + " cadences) -- le SERVICE ne l allume plus"
                )
                continue
            details.append(
                nom + " en PASSE (servie puis eteinte"
                + (", derniere fin il y a " + str(int(age)) + " min" if age is not None
                   else ", jamais servie encore")
                + ")"
            )
            continue
        if pid is None:
            rompus.append(nom + " : aucun PID")
            continue
        if not processus_vivant(pid):
            rompus.append(nom + " : PID " + str(pid) + " mort (fantome)")
            continue
        declaration = journal_declare_par_routine(dossier, nom)
        if declaration is None:
            details.append(nom + " vivant (declaration de fin ILLISIBLE chez la routine)")
            continue
        nom_journal, types_fin = declaration
        if not types_fin:
            details.append(nom + " vivant (ne journalise pas sa fin de passe -- declare)")
            continue
        moment, duree_lecture = dernier_evenement(
            dossier / nom_journal if nom_journal else None, types_fin
        )
        trace = " (journal lu en " + str(round(duree_lecture, 3)) + " s)"
        if moment is None:
            rompus.append(
                nom + " : PID vivant mais AUCUNE fin de passe au journal (lecon L-026)"
                + trace
            )
            continue
        age = age_minutes(moment)
        if age is None:
            details.append(
                nom + " vivant (date de fin illisible : " + str(moment) + ")" + trace
            )
            continue
        if age > SEUIL_FIN_MINUTES:
            rompus.append(
                nom + " : derniere fin il y a " + str(int(age)) + " min (> "
                + str(SEUIL_FIN_MINUTES) + " min) -- boucle qui crashe a chaque passe" + trace
            )
            continue
        journalisees += 1
        details.append(
            nom + " vivant, derniere fin il y a " + str(int(age)) + " min" + trace
        )
    if rompus:
        return "rompu", " | ".join(rompus[:3])
    sans_fin = len(a_surveiller) - journalisees - passees
    resume = (str(len(a_surveiller)) + " routines DECLAREES (lues, pas recopiees) -- "
              + str(journalisees) + " fin(s) de passe journalisee(s) fraiche(s)")
    if passees:
        resume += " ; " + str(passees) + " en passe (servies puis eteintes)"
    if sans_fin:
        resume += (" ; " + str(sans_fin)
                   + " sans fin journalisee declaree (vie suivie par le maillon 7)")
    return "ok", resume + " -- " + " ; ".join(details)


def maillon_pilote(m):
    """Les DEUX pilotes repondent-ils, et la serie stricte tient-elle ?

    Pilote du FLUX (cameleon, matrice/pilote) : c'est lui qui charge les missions
    de la chaine. Pilote de MAINTENANCE (Optimus, _operateur) : c'est lui qui
    porte mes missions. Un seul des deux muet rompt le flux de son cote.
    """
    bilans = []
    for nom, dossier in (("flux", m["pilote_flux"]), ("maintenance", m["pilote_maintenance"])):
        code, sortie = lancer(
            [sys.executable, str(dossier / "main.py"), "file"], cwd=str(dossier)
        )
        if code != 0:
            dernier = sortie.strip().splitlines()[-1] if sortie.strip() else "aucune sortie"
            return "rompu", (
                "pilote " + nom + " MUET (code " + str(code) + ") : " + dernier[:90]
                + " -- plus aucune mission chargeable de ce cote"
            )
        en_cours = sortie.count("[en-cours]")
        if en_cours > 1:
            return "bloque", (
                "pilote " + nom + " : " + str(en_cours)
                + " missions en cours -- la SERIE STRICTE est violee"
            )
        bilans.append(nom + " joignable (" + str(en_cours) + " en cours)")
    return "ok", "pilote " + " ; pilote ".join(bilans)


def maillon_entonnoir(m):
    """Le vrac, les files et le brin sont-ils coherents (brin non perime) ?"""
    chemin = m["entonnoir_etat"]
    try:
        etat = json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as erreur:
        return "rompu", "etat de l'entonnoir illisible (" + str(erreur)[:70] + ") -- aucune mission ne peut entrer"
    files = etat.get("files", {}) or {}
    nb_files = sum(len(v) for v in files.values())
    brin = etat.get("brin", []) or []
    vrac = etat.get("vrac", []) or []
    if brin and nb_files == 0:
        return "perime", (
            "brin a " + str(len(brin)) + " mission(s) alors que TOUTES les files sont vides"
        )
    if len(brin) != nb_files:
        return "perime", (
            "brin (" + str(len(brin)) + ") et files (" + str(nb_files)
            + ") divergent : tissage non refait depuis le dernier classement"
        )
    return "ok", (
        "entonnoir coherent (vrac " + str(len(vrac)) + ", files " + str(nb_files)
        + ", brin " + str(len(brin)) + ")"
    )


def maillon_intercom(m):
    """Le dialogue Matrice <-> agent est-il lisible et valide ligne par ligne ?"""
    soucis = []
    for chemin in m["boites"]:
        if not chemin.is_file():
            soucis.append(chemin.name + " absente")
            continue
        try:
            lignes = chemin.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as erreur:
            soucis.append(chemin.name + " illisible (" + str(erreur)[:40] + ")")
            continue
        for numero, ligne in enumerate(lignes, 1):
            if not ligne.strip():
                continue
            try:
                json.loads(ligne)
            except json.JSONDecodeError:
                soucis.append(chemin.name + " ligne " + str(numero) + " cassee")
                break
    if soucis:
        return "rompu", " | ".join(soucis[:3]) + " -- un message casse bloque le dialogue"
    return "ok", str(len(m["boites"])) + " boite(s) intercom lisibles et valides"


def maillon_fantomes(m):
    """Reste-t-il des PID morts -- ou une routine SUPERVISEE declaree ARRET ?

    Deux mensonges, un seul maillon (EO-404). Le premier est un FICHIER qui ment :
    un `.pid` dont le processus est mort fait croire que la chaine tourne. Le
    second etait plus grave parce qu'il etait INVISIBLE : la Matrice annoncait
    "6/7 routines actives" sans dire LAQUELLE manquait, et il suffisait de nettoyer
    un pid fantome (ce que la porte `vie` fait en rendant son etat) pour que le
    rouge disparaisse sans que la routine reparte. Mesure du 2026-09-23/24 : le
    routeur-maintenance etait mort depuis 19 h 52 la veille, la chaine affichait
    6/7, et la non-regression du flux rendait "FLUX SAIN".

    Le maillon ne juge donc plus le seul FICHIER : il juge la VIE DECLAREE de
    chaque routine supervisee, lue a la source unique
    (`matrice/routines/vie/constants.py`), cadence declaree comprise -- et le
    MODE vient du PLANNING (MO-429) : une routine en mode `passe` est CENSEE
    s eteindre a la fin de chaque passe, son PID residuel n est donc PAS un
    fantome (le signaler sans accuser, c est dire d ou vient le fichier).

    EO-409 : quand la routine NE VIT PAS, l accusation NOMME la CAUSE, lue dans son
    journal de lancement (data/commun/lancement.py, lecture bornee) -- accuser sans
    dire POURQUOI, c est renvoyer le diagnostic a la main. Une routine VIVANTE n en
    recoit pas : sa cause serait du bruit.
    """
    table = table_des_routines(m)
    if table is None:
        return "rompu", (
            "table des routines supervisees ILLISIBLE (matrice/routines/vie/constants.py) : "
            "impossible de dire QUI doit vivre -- un pid mort ne suffit pas a juger la chaine (EO-404)"
        )
    boucles, pid_par_nom, _lecteur, modes, cause_mode = table
    if cause_mode:
        # Sans mode lisible, on ne sait plus QUI est cense vivre en permanence :
        # le refus se DIT plutot qu un jugement silencieux sur la moitie des regles.
        return "rompu", "table des modes illisible -- " + cause_mode
    # ZONE JETABLE (MO-438, mesure MO-363) : un .pid sous un dossier tmp-* est
    # une FIXTURE de cobaye, pas une affirmation sur la chaine -- le rglob
    # balayait les zones jetables comme le reste (copie d arbre portant un
    # vigie-portes.pid mort -> maillon 7 rougit a tort). Le critere vient du
    # DOMICILE PARTAGE (data/commun/zone_tmp.py, PREFIXE_ZONE), jamais recopie
    # ici (M-076) ; la fixture est NOMMEE dans le detail, comme un residu de
    # passe -- jamais d exemption muette. Illisible = rompu NOMME : sans le
    # critere, le faux positif reviendrait en silence.
    zone_tmp = charger_module_par_chemin(
        m["matrix"] / "matrice" / "data" / "commun" / "zone_tmp.py", "zone_tmp_flux")
    if zone_tmp is None or not getattr(zone_tmp, "PREFIXE_ZONE", ""):
        return "rompu", ("domicile partage des zones jetables ILLISIBLE "
                         "(matrice/data/commun/zone_tmp.py) : impossible de "
                         "distinguer une fixture tmp-* d un pid de la chaine (MO-438)")
    prefixe_zone = zone_tmp.PREFIXE_ZONE

    def dans_zone_jetable(chemin):
        # Le NOM des DOSSIERS compte, pas celui du fichier : un .pid qui SE
        # nommerait tmp-* n est pas pour autant depose dans une zone.
        return any(part.startswith(prefixe_zone) for part in chemin.parts[:-1])
    pids_en_passe = set()
    for nom, dossier in boucles:
        if modes.get(nom, "boucle") == "passe":
            pids_en_passe.add(
                (Path(dossier) / (pid_par_nom.get(nom) or nom + ".pid")).resolve()
            )
    fantomes = []
    residus = []
    for chemin_pid in sorted(m["matrix"].rglob("*.pid")):
        if dans_zone_jetable(chemin_pid):
            # FIXTURE en zone jetable : NOMMEE, jamais accusee (MO-438).
            residus.append(chemin_pid.name + "=zone jetable")
            continue
        pid = lire_pid(chemin_pid)
        if pid is None:
            fantomes.append(chemin_pid.name + " illisible")
            continue
        if processus_vivant(pid):
            continue
        if chemin_pid.resolve() in pids_en_passe:
            # Residu NORMAL d une passe : la routine s eteint, c est son mode. Il
            # est NOMME dans le detail (jamais perdu) mais il ne rougit pas le flux.
            residus.append(chemin_pid.name + "=" + str(pid))
            continue
        fantomes.append(chemin_pid.name + "=" + str(pid))
    if fantomes:
        return "fantome", "PID mort(s) : " + ", ".join(fantomes[:5])
    etat, detail, _ = juger_routines_supervisees(table)
    if residus:
        detail += " (PID residuel(s) de passe non accuse(s) : " + ", ".join(residus[:3]) + ")"
    return etat, detail


def maillon_relais(m):
    """Y a-t-il de quoi donner une identite a l'agent (bank de themes) ?"""
    themes = sorted(m["themes"].glob("theme-*.json"))
    if not themes:
        return "rompu", "bank de themes vide : l'agent ne peut prendre AUCUNE identite"
    casses = []
    for theme in themes:
        try:
            json.loads(theme.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            casses.append(theme.name)
    if casses:
        return "rompu", "theme(s) illisible(s) : " + ", ".join(casses[:3]) + " -- le relais de mission casse"
    return "ok", str(len(themes)) + " themes relisibles (identite disponible)"


def maillon_file_journal(m):
    """La file du pilote et le journal suivi-optimus disent-ils la MEME chose ?

    Deux traces qui vivent separement divergent en silence : une mission close
    dans la file mais jamais declaree finie n'apparait nulle part, et un
    compteur en retard reattribue un id deja pris. C'est exactement ce qui est
    reste invisible jusqu'au 2026-09-13 (MO-043 en-cours dans la file alors que
    le journal la donnait finie ; compteur bloque a 44 alors que MO-045 et
    MO-046 existaient).

    Un ECART fait tomber le maillon ; une DETTE (fenetre d'injection, residu
    hors perimetre) est SIGNALEE dans le detail sans bloquer le flux.
    """
    code, sortie = lancer([sys.executable, str(m["outil_suivi"] / "main.py"), "coherence"])
    if code not in (0, 1):
        dernier = sortie.strip().splitlines()[-1] if sortie.strip() else "aucune sortie"
        return "rompu", (
            "la porte de coherence ne repond pas (code " + str(code) + ") : " + dernier[:90]
            + " -- impossible de savoir si la file et la trace sont d'accord"
        )
    ecarts = [l.strip()[len("ECART : "):] for l in sortie.splitlines() if l.strip().startswith("ECART :")]
    dettes = [l.strip()[len("DETTE : "):] for l in sortie.splitlines() if l.strip().startswith("DETTE :")]
    if ecarts:
        return "divergent", str(len(ecarts)) + " ecart(s) : " + " | ".join(ecarts[:2])
    detail = "file et journal d'accord"
    if dettes:
        detail += " (" + str(len(dettes)) + " dette(s) signalee(s) : " + dettes[0][:70] + ")"
    return "ok", detail


MAILLONS_FONCTIONS = {
    "selecteur": maillon_selecteur,
    "serveur": maillon_serveur,
    "routines": maillon_routines,
    "pilote": maillon_pilote,
    "entonnoir": maillon_entonnoir,
    "intercom": maillon_intercom,
    "fantomes": maillon_fantomes,
    "relais": maillon_relais,
    "file-journal": maillon_file_journal,
}


# --- POINT D'ENTREE ---------------------------------------------------------

def trouver_matrix(racine):
    """Retourne le dossier matrix/ (cerveau-projet/matrix prefere), ou None."""
    candidats = [racine / "cerveau-projet" / "matrix", racine / "matrix"]
    if racine.name == "matrix":
        candidats.insert(0, racine)
    return next((c for c in candidats if c.is_dir()), None)


def construire_carte(matrix):
    """Assemble les chemins surveilles (une seule source, lisible en un coup d'oeil)."""
    return {
        "matrix": matrix,
        "matrice": matrix / "matrice",
        "routines": matrix / "matrice" / "routines",
        "pilote_flux": matrix / "matrice" / "pilote",
        "pilote_maintenance": matrix / "_operateur" / "optimus-prime" / "pilote",
        "selecteur": matrix / "matrice" / "data" / "outils" / "selecteur-flux",
        "outil_suivi": matrix / "matrice" / "data" / "outils" / "suivi-optimus",
        "pid_serveur": matrix / "matrice" / "routines" / "vie" / "server" / "server-matrice.pid",
        "entonnoir_etat": matrix / "_operateur" / "optimus-prime" / "pilote" / "entonnoir-files-optimus.json",
        "themes": matrix / "_operateur" / "optimus-prime" / "parcours" / "themes",
        "boites": (
            matrix / "matrice" / "intercom" / "matrice" / "inbox.jsonl",
            matrix / "matrice" / "intercom" / "cameleon" / "inbox.jsonl",
            matrix / "matrice" / "intercom" / "pilote" / "outbox.jsonl",
        ),
    }


def executer_maillons(carte):
    """Parcourt les maillons DANS L'ORDRE DU FLUX. Retourne la liste des resultats."""
    resultats = []
    for numero, cle, nom in MAILLONS:
        fonction = MAILLONS_FONCTIONS[cle]
        try:
            etat, detail = fonction(carte)
        except Exception as erreur:  # garde ultime : un maillon ne tue jamais la suite
            etat, detail = "rompu", "verification impossible (" + type(erreur).__name__ + ") : " + str(erreur)[:80]
        resultats.append({"numero": numero, "cle": cle, "nom": nom, "etat": etat, "detail": detail})
    return resultats


def main():
    parser = argparse.ArgumentParser(description="Non-regression du FLUX (imperatif 62)")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    parser.add_argument("--json", action="store_true", help="Sortie machine")
    parser.add_argument(
        "--autotest",
        action="store_true",
        help="Eprouve le maillon 7 sur des cobayes jetables (mordre, puis epargner)",
    )
    parser.add_argument(
        "--autotest-maillon3",
        action="store_true",
        help="Eprouve l'EVOLUTIVITE du maillon 3 (il LIT sa table, il ne la recopie pas)",
    )
    parser.add_argument(
        "--autotest-pid-serveur",
        action="store_true",
        help="Eprouve la publication du PID du SERVEUR (MO-458 : reparer l efface, jamais ecraser un vivant)",
    )
    args = parser.parse_args()

    if args.autotest:
        return autotest(Path(args.racine).resolve())
    if args.autotest_maillon3:
        return autotest_maillon3(Path(args.racine).resolve())
    if args.autotest_pid_serveur:
        return autotest_pid_serveur(Path(args.racine).resolve())

    racine = Path(args.racine).resolve()
    matrix = trouver_matrix(racine)
    if matrix is None:
        print("Dossier matrix/ introuvable sous " + str(racine))
        return 2

    # MO-099 : le moteur PARTAGE entre dans sys.path -- il porte la FENETRE de
    # lecture des queues (deduite de la borne declaree du journal lu).
    sys.path.insert(0, str(matrix / "matrice" / "data" / "commun"))

    resultats = executer_maillons(construire_carte(matrix))
    rompus = [r for r in resultats if r["etat"] != "ok"]

    if args.json:
        print(json.dumps({"maillons": resultats, "rompus": len(rompus)}, ensure_ascii=True, indent=2))
        return 1 if rompus else 0

    print("== NON-REGRESSION DU FLUX (imperatif 62 : on surveille la chaine, pas les fichiers) ==")
    for r in resultats:
        marque = "OK  " if r["etat"] == "ok" else "KO  "
        print("[" + marque + "] MAILLON " + str(r["numero"]) + "/" + str(len(MAILLONS))
              + " " + r["nom"])
        print("         " + r["etat"] + " -- " + r["detail"])

    if rompus:
        print("")
        print("VERDICT FLUX ROMPU : " + str(len(rompus)) + " maillon(s) sur " + str(len(MAILLONS)))
        for r in rompus:
            print("  - MAILLON " + str(r["numero"]) + " (" + r["cle"] + ") : " + r["etat"]
                  + " -- " + r["detail"])
            print("    IMPACT : " + IMPACTS.get(r["etat"], "flux degrade"))
        return 1

    print("")
    print("VERDICT FLUX SAIN : les " + str(len(MAILLONS)) + " maillons repondent, la chaine peut porter une mission.")
    return 0


# --- MAILLON 7, SECONDE REGLE : la VIE DECLAREE des routines (EO-404) --------
# Tolerance d'une routine jugee : N cadences DECLAREES, avec un plancher (une
# cadence de 30 s ne doit pas accuser au bout de 90 s une routine que le serveur
# ne supervise que toutes les 60 s). Ce sont les deux SEULS nombres de la regle.
NB_CADENCES_TOLEREES = 3
TOLERANCE_MINIMALE_SECONDES = 120

# Ou une routine PUBLIE son battement : les formes des etats, journaux et cadences
# de la Matrice. Le PID en est EXCLU a dessein : un fichier `.pid` se date de son
# ECRITURE (l'allumage), pas de la derniere PASSE -- s'en servir daterait une
# routine de son demarrage (des heures plus tot) et la declarerait muette a tort.
FORMES_TRACE = (
    "*-etat*.json",
    "*-cadence.json",
    "*-log*.jsonl",
    "*-historique*.jsonl",
    "journal-*.txt",
)

# La routine de COBAYE : une cadence COURTE, pour que les temoins se posent en
# quelques secondes au lieu d'attendre des minutes.
CADENCE_COBAYE_SECONDES = 30
PREFIXE_COBAYE = "cobaye-maillon7-"
# Le journal de lancement du COBAYE : le MEME nom que le motif partage
# (data/commun/lancement.py), pour que le temoin eprouve la REGLE de nommage.
NOM_JOURNAL_LANCEMENT_COBAYE = "journal-lancement.log"
# La cause d un plantage d allumage, telle que le cobaye la pose.
CAUSE_PLANTAGE = "NameError: name INTERVALLE_SECONDES is not defined"

_MODULES_CHARGES = {}


def charger_module_par_chemin(chemin, nom_module):
    """Charge un module par son CHEMIN, sous un nom UNIQUE (jamais par son nom).

    Motif du depot : plusieurs fichiers portent le meme nom (un `constants.py` par
    routine, `cobayes_jetables.py` chez chaque garde) : un import par nom les
    masquerait mutuellement. Rend None si le fichier manque ou ne se charge pas --
    l'appelant le DIT alors, il ne devine pas.
    """
    chemin = Path(chemin)
    cle = (str(chemin), nom_module)
    if cle in _MODULES_CHARGES:
        return _MODULES_CHARGES[cle]
    if not chemin.is_file():
        return None
    specification = importlib.util.spec_from_file_location(nom_module, str(chemin))
    if specification is None or specification.loader is None:
        return None
    try:
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except Exception:
        return None
    _MODULES_CHARGES[cle] = module
    return module


def modes_du_planning(matrix):
    """({nom: mode}, cause) -- les modes d allumage lus au PLANNING (MO-429, D1).

    Le planning est la SOURCE de la rotation d allumage : une routine en mode
    `passe` est ETEINTE entre deux passes par conception et servie par le
    service -- le maillon doit le savoir pour ne pas accuser un etat normal.
    Trois sorties honnetes :
      - moteur ABSENT (arborescence sans planning, cobaye, ancien monde) ->
        ({}, None) : aucune pretention sur le mode, le comportement est celui
        d avant ;
      - moteur present et planning LUE -> les modes ;
      - moteur present mais planning REFUSE -> ({}, cause) : la MATRICE REELLE
        ne sait plus qui allumer quoi, et le maillon le DIT (jamais un faux
        vert sur un planning casse).
    """
    if matrix is None:
        return {}, None
    moteur = charger_module_par_chemin(
        matrix / "matrice" / "data" / "commun" / "planning_routines.py", "planning_flux"
    )
    if moteur is None:
        return {}, None
    try:
        donnees = moteur.charger(str(matrix))
    except Exception as erreur:  # noqa: BLE001 -- le refus du planning est une cause dite
        return {}, "planning ILLISIBLE : " + str(erreur)
    modes = {}
    for entree in donnees.get("routines", []):
        if isinstance(entree, dict) and entree.get("nom"):
            modes[str(entree["nom"])] = entree.get("mode")
    return modes, None


def table_des_routines(m):
    """La table UNIQUE des routines supervisees, lue la ou elle vit.

    Rend (BOUCLES, PID_PAR_NOM, lecteur de cadence, MODES, cause de mode). Le
    maillon ne REASSEMBLE pas la liste : il la LIT (`matrice/routines/vie/
    constants.py`, celle que le serveur importe -- deux listes = deux verites).
    C'est exactement l'ecart qui a laisse passer EO-404 : le flux ne surveillait
    que TROIS routines ecrites en dur, la Matrice en supervise SEPT -- les
    quatre autres pouvaient mourir sans que rien ne le voie, et le routeur l'a
    fait pendant une journee. Les MODES viennent du PLANNING (MO-429) : deux
    familles, deux regles de vie, une seule source pour chacune.
    Rend None si la table est illisible : le maillon le DIT, il ne suppose pas.
    """
    dossier_vie = m["routines"] / "vie"
    chemin = dossier_vie / "constants.py"
    if not chemin.is_file():
        return None
    # La table importe ses fichiers FRERES (`constants_suivi_sync`, ...) : leur
    # dossier doit etre joignable pendant le chargement, et seulement pendant lui.
    module = charger_module_vie(dossier_vie, "constants.py", "table_vie_flux")
    if module is None:
        return None
    try:
        boucles = [(nom, Path(dossier)) for nom, dossier in module.BOUCLES]
        pid_par_nom = dict(module.PID_PAR_NOM)
    except (AttributeError, TypeError):
        return None
    # Le LECTEUR de la cadence est celui de la porte `vie` : la voix de la cadence
    # est unique, donc le maillon et `vie etat` lisent la MEME chose par
    # construction (le lire ailleurs serait une seconde verite).
    fonctions_vie = charger_module_vie(dossier_vie, "fonctions.py", "fonctions_vie_flux")
    modes, cause_mode = modes_du_planning(m.get("matrix"))
    return boucles, pid_par_nom, fonctions_vie, modes, cause_mode


def routines_a_surveiller(table):
    """[(nom, dossier, nom_pid, mode)] DERIVEE de la table + du PLANNING (MO-429).

    C'est la seule facon de suivre une routine AJOUTEE a la Matrice : la liste vient
    de `BOUCLES` + `PID_PAR_NOM` (`routines/vie/constants.py`), pas d'un tuple fige
    dans ce fichier. Une routine que la table ne nomme pas retombe sur `<nom>.pid`
    (convention du dossier des routines) : ce repli ne se TAIT pas, il est dans la
    liste rendue. Le MODE (passe | boucle) vient du PLANNING : il dit comment la
    routine VIT -- supervisee en permanence, ou allumee a echeance puis eteinte.
    Un mode absent du planning retombe sur `boucle` (le comportement d avant).
    """
    boucles, pid_par_nom, _lecteur, modes, _cause_mode = table
    return [
        (nom, Path(dossier), pid_par_nom.get(nom) or (nom + ".pid"),
         modes.get(nom, "boucle"))
        for nom, dossier in boucles
    ]


def journal_declare_par_routine(dossier, nom):
    """La declaration de FIN DE PASSE d'une routine, lue CHEZ ELLE. Rend (nom, types) ou None.

    Le domicile de cette declaration est la routine (`constants.py`), pas ce maillon :
    une routine qui change de journal ou de marqueur de fin le change a UN endroit
    (M-076). Rend None quand la declaration est ILLISIBLE -- l'appelant le DIT, il ne
    suppose pas < pas de journal >. Un `EVENEMENT_FIN_PASSE = None` DECLARE
    explicitement que la routine ne journalise pas sa fin : le maillon le dit aussi.
    """
    module = charger_module_par_chemin(
        Path(dossier) / "constants.py", "constants_routine_" + nom.replace("-", "_")
    )
    if module is None:
        return None
    types_fin = getattr(module, "EVENEMENT_FIN_PASSE", None)
    if isinstance(types_fin, str):
        types_fin = (types_fin,)
    elif types_fin:
        types_fin = tuple(types_fin)
    else:
        types_fin = ()
    return getattr(module, "NOM_JOURNAL", None), types_fin


def charger_module_vie(dossier_vie, nom_fichier, nom_module):
    """Charge un fichier de `routines/vie/` par son CHEMIN, dossier joignable.

    Les modules de la vie importent leurs FRERES par leur nom (`constants_suivi_sync`,
    ...) : leur dossier doit etre joignable PENDANT le chargement, et seulement
    pendant lui. Le module charge reste ensuite en memoire (`_MODULES_CHARGES`).
    """
    sys.path.insert(0, str(dossier_vie))
    try:
        return charger_module_par_chemin(Path(dossier_vie) / nom_fichier, nom_module)
    finally:
        if sys.path and sys.path[0] == str(dossier_vie):
            sys.path.pop(0)


def lire_cadence(lecteur_cadence, nom, dossier):
    """Cadence DECLAREE par la routine (secondes), ou None si elle est illisible.

    Le LECTEUR est celui de la porte `vie` (`routines/vie/fonctions.py`,
    `cadence_declaree`) : la cadence se LIT, elle ne s'attend pas, et elle se lit au
    MEME endroit que dans `vie etat`. Une lecture ratee rend None et le detail la
    DIT (`cadence ILLISIBLE`) -- un repli muet ferait accuser a tort les routines a
    cadence longue (900 s, 3600 s).
    """
    if lecteur_cadence is None:
        return None
    try:
        valeur = lecteur_cadence.cadence_declaree(nom, dossier)
    except Exception:
        return None
    return valeur if isinstance(valeur, int) else None


def lire_cause(lecteur_cadence, dossier):
    """La CAUSE du dernier lancement d une routine (EO-409), ou None.

    Le maillon 7 ne se contente plus d accuser : quand une routine NE VIT PAS, il
    NOMME la raison, lue dans son journal de lancement par la MEME porte que l etat
    des routines. Un garde ne meurt jamais d un lecteur absent (L-026) : toute
    erreur rend None et la cause n est pas nommee -- l accusation, elle, tient.
    """
    if lecteur_cadence is None or not hasattr(lecteur_cadence, "cause_du_dernier_lancement"):
        return None
    try:
        return lecteur_cadence.cause_du_dernier_lancement(dossier)
    except Exception:
        return None


class _LecteurCadenceCobaye:
    """Lecteur du COBAYE : le MEME contrat que `vie/fonctions.py`.

    La cadence vient de la constante du cobaye ; la CAUSE, de la derniere ligne non
    vide de son journal de lancement -- la regle du motif partage
    (data/commun/lancement.py), dont le VRAI lecteur est eprouve par ailleurs.
    """

    @staticmethod
    def cadence_declaree(nom, dossier):
        return CADENCE_COBAYE_SECONDES if nom == "cobaye-routine" else None

    @staticmethod
    def cause_du_dernier_lancement(dossier):
        chemin = Path(dossier) / NOM_JOURNAL_LANCEMENT_COBAYE
        if not chemin.is_file():
            return None
        try:
            lignes = chemin.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return None
        for ligne in reversed(lignes):
            if ligne.strip():
                return ligne.strip()
        return None


_LECTEUR_COBAYE = _LecteurCadenceCobaye()


def age_trace_secondes(dossier):
    """Age (s) de la DERNIERE trace de passe d'une routine, ou None s'il n'y en a aucune.

    Une routine qui BAT publie dans son dossier (etat, cadence, journal) : le
    maillon NOMME les formes qu'il lit au lieu de deviner, et rend None quand il
    n'y a RIEN -- une absence de trace est un FAIT, pas un zero (un zero daterait
    la routine de 1970 et la declarerait morte a tort).
    """
    plus_recente = None
    for forme in FORMES_TRACE:
        for chemin in Path(dossier).glob(forme):
            if not chemin.is_file():
                continue
            try:
                moment = chemin.stat().st_mtime
            except OSError:
                continue
            if plus_recente is None or moment > plus_recente:
                plus_recente = moment
    if plus_recente is None:
        return None
    return max(0.0, time.time() - plus_recente)


def juger_routines_supervisees(table):
    """Juge la VIE de chaque routine supervisee. Rend (etat, detail, accuses).

    UNE seule regle de FOND, la meme pour toutes (aucune liste privilegiee) :
      - elle VIT et a publie dans sa tolerance -> EPARGNEE (le contre-temoin) ;
      - elle ne vit pas (PID absent ou mort) au-dela de sa tolerance -> ACCUSEE ;
      - elle vit mais ne publie plus au-dela de sa tolerance -> ACCUSEE (muette) ;
      - aucune trace lisible -> ACCUSEE : un silence ne vaut pas un zero.

    LE MODE change le DIAGNOSTIC, pas la regle (MO-429) : une routine en mode
    `passe` est ETEINTE entre deux passes PAR CONCEPTION -- l absence de PID n est
    alors ni un arret ni un fantome, c'est l etat normal. Elle reste jugee sur son
    AGE DE TRACE (le service DOIT la reallumer a echeance) : un age au-dela de la
    tolerance accuse LE SERVICE (qui ne la sert plus), jamais la routine eteinte.
    """
    boucles, pid_par_nom, lecteur_cadence, modes, _cause_mode = table
    accuses = []
    epargnees = []
    for nom, dossier in boucles:
        mode = modes.get(nom, "boucle")
        cadence = lire_cadence(lecteur_cadence, nom, dossier)
        tolerance = max(TOLERANCE_MINIMALE_SECONDES, NB_CADENCES_TOLEREES * (cadence or 0))
        nom_pid = pid_par_nom.get(nom) or (nom + ".pid")
        pid = lire_pid(dossier / nom_pid)
        vivante = pid is not None and processus_vivant(pid)
        if vivante:
            declare = "vivante (PID " + str(pid) + ")"
        elif mode == "passe":
            declare = "en PASSE (eteinte entre deux passes, allumee par le service)"
        else:
            declare = "declaree ARRET (PID " + ("absent" if pid is None else str(pid) + " mort") + ")"
        fenetre = ("tolerance " + str(int(tolerance)) + " s = " + str(NB_CADENCES_TOLEREES)
                   + " x " + (str(cadence) + " s" if cadence is not None else "cadence ILLISIBLE"))
        age = age_trace_secondes(dossier)
        # EO-409 : une routine qui NE VIT PAS se voit NOMMER sa cause (journal de
        # lancement). Une routine VIVANTE n en recoit pas : son journal ne dirait
        # rien de sa mutite, et une cause hors sujet serait du BRUIT.
        cause = lire_cause(lecteur_cadence, dossier) if not vivante else None
        cause_texte = (" -- CAUSE (dernier lancement) : " + cause) if cause else ""
        # En mode passe, une trace ancienne accuse le SERVICE (il ne reallume plus),
        # pas la routine qui suit exactement son mode : le remede se NOMME.
        service = (" -- le SERVICE ne l allume plus (mode passe)" if mode == "passe" else "")
        if age is None:
            accuses.append(nom + " : " + declare + ", AUCUNE trace de passe lisible ("
                           + fenetre + ")" + cause_texte + service)
            continue
        if age <= tolerance:
            epargnees.append(nom)
            continue
        accuses.append(nom + " : " + declare + ", derniere trace il y a " + str(int(age))
                       + " s (> " + fenetre + ")" + cause_texte + service)
    total = len(boucles)
    if accuses:
        return "muette", ("chaine " + str(len(epargnees)) + "/" + str(total)
                          + " routines saines -- MANQUE : " + " | ".join(accuses[:3])), accuses
    return "ok", (str(total) + "/" + str(total)
                  + " routines supervisees dans leur tolerance (PID vivant et derniere passe recente ;"
                  + " " + str(NB_CADENCES_TOLEREES) + " cadences declarees, plancher "
                  + str(TOLERANCE_MINIMALE_SECONDES) + " s)"), accuses


def autotest(racine):
    """Eprouve le maillon 7 sur une arborescence de COBAYE : mordre, puis epargner.

    Un controle qu'on ne peut pas pieger ne prouve rien (L-032) -- et le maillon 7
    est justement celui qui se taisait. Aucune routine en service n'est touchee :
    tout se passe dans une zone jetable du temporaire systeme, retiree TOUJOURS
    (fabrique PARTAGEE `cobayes_jetables.fixtures`, motif M-076).
    """
    matrix = trouver_matrix(racine)
    if matrix is None:
        print("AUTOTEST IMPOSSIBLE : dossier matrix/ introuvable sous " + str(racine))
        return 2
    chemin_fabrique = matrix / "matrice" / "data" / "commun" / "cobayes_jetables.py"
    fabrique = charger_module_par_chemin(chemin_fabrique, "cobayes_jetables_flux")
    if fabrique is None:
        print("AUTOTEST IMPOSSIBLE : fabrique de cobayes illisible (" + str(chemin_fabrique) + ")")
        return 2

    residus = []
    essais = []
    with fabrique.fixtures(PREFIXE_COBAYE, residus) as zone:
        dossier = zone / "cobaye-routine"
        dossier.mkdir(parents=True, exist_ok=True)
        # La cadence du cobaye vient d un lecteur SYNTHETIQUE (meme contrat que la
        # porte `vie`) : le cobaye eprouve la REGLE de jugement, pas la lecture de
        # la cadence (elle-meme eprouvee par `verifier-sans-attendre`). Le MODE
        # vient du PLANNING (MO-429) : ici `boucle`, la regle d avant, celle que
        # les six temoins ci-dessous eprouvent toujours.
        table = (
            [("cobaye-routine", dossier)],
            {"cobaye-routine": "cobaye-routine.pid"},
            _LECTEUR_COBAYE,
            {"cobaye-routine": "boucle"},
            None,
        )
        tolerance = max(TOLERANCE_MINIMALE_SECONDES, NB_CADENCES_TOLEREES * CADENCE_COBAYE_SECONDES)

        def poser(pid, age_trace, cause=None):
            """Pose (ou retire) le PID, la trace de passe ET le journal de lancement."""
            chemin_trace = dossier / "cobaye-routine-etat.json"
            chemin_pid = dossier / "cobaye-routine.pid"
            chemin_journal = dossier / NOM_JOURNAL_LANCEMENT_COBAYE
            if cause is None:
                if chemin_journal.exists():
                    chemin_journal.unlink()
            else:
                chemin_journal.write_text(cause + "\n", encoding="utf-8")
            if age_trace is None:
                if chemin_trace.exists():
                    chemin_trace.unlink()
            else:
                chemin_trace.write_text("{}\n", encoding="utf-8")
                moment = time.time() - age_trace
                os.utime(str(chemin_trace), (moment, moment))
            if pid is None:
                if chemin_pid.exists():
                    chemin_pid.unlink()
            else:
                chemin_pid.write_text(str(pid) + "\n", encoding="utf-8")

        # EO-409 : la cause d'un plantage d'allumage, telle qu'un journal de
        # lancement la porterait. Les temoins disent AUSSI qui doit la voir, et qui
        # ne doit PAS la voir (une routine vivante : sa cause serait du BRUIT).
        temoins = (
            ("COBAYE  pid ABSENT et trace au-dela de la tolerance", None, tolerance + 60, "muette", CAUSE_PLANTAGE, True),
            ("COBAYE  pid MORT et trace au-dela de la tolerance", 0, tolerance + 60, "muette", None, False),
            ("COBAYE  pid VIVANT mais muette au-dela de la tolerance", os.getpid(), tolerance + 60, "muette", CAUSE_PLANTAGE, False),
            ("COBAYE  aucune trace de passe du tout", None, None, "muette", None, False),
            ("CONTRE-TEMOIN pid ABSENT mais relance recente (tolerance)", None, tolerance - 60, "ok", None, False),
            ("CONTRE-TEMOIN pid VIVANT qui vient de publier sa passe", os.getpid(), 1, "ok", CAUSE_PLANTAGE, False),
        )
        for libelle, pid, age, attendu, cause, cause_attendue in temoins:
            poser(pid, age, cause)
            etat, detail, accuses = juger_routines_supervisees(table)
            nomme = all("cobaye-routine" in accuse for accuse in accuses)
            cause_nommee = ("CAUSE (dernier lancement) : " + CAUSE_PLANTAGE) in detail
            gagne = (etat == attendu
                     and (nomme if attendu == "muette" else not accuses)
                     and cause_nommee == cause_attendue)
            essais.append((libelle, attendu, etat, gagne, detail))

        # --- MODE PASSE (MO-429, decision D2 du createur) --------------------
        # La MEME routine, mais declaree eteinte entre deux passes. Trois cas a
        # PROUVER dans les deux sens : l etat normal n est PAS accuse ; un
        # service qui ne la reallume plus L EST (le remede se nomme) ; et un
        # residu de PID de fin de passe n est pas un fantome.
        table_passe = (
            [("cobaye-routine", dossier)],
            {"cobaye-routine": "cobaye-routine.pid"},
            _LECTEUR_COBAYE,
            {"cobaye-routine": "passe"},
            None,
        )
        temoins_passe = (
            ("COBAYE PASSE eteinte, trace fraiche : l etat NORMAL est epargne",
             None, tolerance - 60, "ok"),
            ("COBAYE PASSE eteinte, trace ancienne : c est le SERVICE qui manque",
             None, tolerance + 60, "muette"),
            ("COBAYE PASSE residu de PID MORT + trace fraiche : epargne",
             0, 1, "ok"),
        )
        for libelle, pid, age, attendu in temoins_passe:
            poser(pid, age, None)
            etat, detail, accuses = juger_routines_supervisees(table_passe)
            if attendu == "muette":
                gagne = (etat == "muette"
                         and any("cobaye-routine" in accuse for accuse in accuses)
                         and "SERVICE ne l allume plus" in detail)
            else:
                gagne = etat == "ok" and not accuses
            essais.append((libelle, attendu, etat, gagne, detail))

        # --- LE RESIDU DE PID N EST PAS UN FANTOME (maillon_fantomes) --------
        # Le maillon lit les pids AVANT de juger : un residu de fin de passe
        # l aurait fait rougir a tort. Cobaye qui mord (mode passe -> epargne)
        # et contre-temoin (mode boucle -> le MEME fichier est accuse).
        import shutil

        # On vide le dossier du cobaye precedent : son propre PID (mort a ce
        # stade) serait sinon lu par le rglob du maillon et melerait les deux preuves.
        poser(None, None, None)

        vie = zone / "matrice" / "routines" / "vie"
        dossier_passe = zone / "matrice" / "routines" / "cobaye-passe"
        vie.mkdir(parents=True, exist_ok=True)
        dossier_passe.mkdir(parents=True, exist_ok=True)
        vrai_moteur = (matrix / "matrice" / "data" / "commun" / "planning_routines.py")
        moteur_zone = zone / "matrice" / "data" / "commun"
        moteur_zone.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(vrai_moteur), str(moteur_zone / "planning_routines.py"))
        # MO-438 : le maillon lit aussi le DOMICILE PARTAGE des zones jetables
        # (critere tmp-*) : la copie de fabrique doit le porter, sinon le cobaye
        # eprouverait un garde qui REFUSE (rompu) au lieu de le juger.
        shutil.copyfile(
            str(matrix / "matrice" / "data" / "commun" / "zone_tmp.py"),
            str(moteur_zone / "zone_tmp.py"))
        (vie / "constants.py").write_text(
            "BOUCLES = (\n    (\"cobaye-passe\", r\"" + str(dossier_passe) + "\"),\n)\n"
            "PID_PAR_NOM = {}\n",
            encoding="utf-8")
        # PID residuel MORT + trace de passe fraiche (l etat normal du cobaye).
        (dossier_passe / "cobaye-passe.pid").write_text("0\n", encoding="utf-8")
        (dossier_passe / "cobaye-passe-etat.json").write_text("{}\n", encoding="utf-8")

        def poser_mode(mode):
            (vie / "planning.json").write_text(
                json.dumps({"routines": [{
                    "nom": "cobaye-passe", "cadence_secondes": 300, "mode": mode,
                    "decalage_initial_secondes": 0, "priorite": 10,
                    "tolerance_cadences": 3,
                    "commande_passe": ["python3", "cobaye.py"],
                }]}, indent=2),
                encoding="utf-8",
            )

        carte = {"matrix": zone, "routines": zone / "matrice" / "routines"}
        poser_mode("passe")
        etat, detail = maillon_fantomes(carte)
        gagne = etat == "ok" and "residuel" in detail
        essais.append(("COBAYE fantomes : residu de PID en mode PASSE epargne (mais NOMME)",
                       "ok", etat, gagne, detail))
        poser_mode("boucle")
        etat, detail = maillon_fantomes(carte)
        gagne = etat == "fantome" and "cobaye-passe.pid" in detail
        essais.append(("CONTRE-TEMOIN fantomes : le MEME pid en mode BOUCLE est accuse",
                       "fantome", etat, gagne, detail))

        # --- LA ZONE JETABLE N EST PAS LA CHAINE (MO-438 / mesure MO-363) ----
        # Le rglob du maillon balayait les zones jetables : une FIXTURE tmp-*
        # (un .pid de cobaye) etait lue comme un pid mort de la chaine.
        # Cobaye qui MORD : un pid mort HORS zone jetable reste accuse.
        # Contre-temoin qui EPARGNE : le MEME pid mort DANS tmp-* ne l est plus,
        # mais il reste NOMME (jamais d exemption muette).
        poser_mode("passe")
        fixture_zone = zone / "_operateur" / "optimus-prime" / "tmp-optimus"
        fixture_zone.mkdir(parents=True, exist_ok=True)
        (fixture_zone / "cobaye-fixture.pid").write_text("0\n", encoding="utf-8")
        dossier_hors = zone / "matrice" / "routines" / "cobaye-hors"
        dossier_hors.mkdir(parents=True, exist_ok=True)
        (dossier_hors / "cobaye-hors.pid").write_text("0\n", encoding="utf-8")
        etat, detail = maillon_fantomes(carte)
        gagne = (etat == "fantome" and "cobaye-hors.pid" in detail
                 and "cobaye-fixture.pid" not in detail)
        essais.append(("COBAYE fantomes MO-438 : pid mort HORS zone jetable toujours accuse",
                       "fantome", etat, gagne, detail))
        (dossier_hors / "cobaye-hors.pid").unlink()
        etat, detail = maillon_fantomes(carte)
        gagne = etat == "ok" and "cobaye-fixture.pid" in detail
        essais.append(("CONTRE-TEMOIN fantomes MO-438 : fixture .pid DANS tmp-* epargnee mais NOMMEE",
                       "ok", etat, gagne, detail))

    for libelle, attendu, obtenu, gagne, detail in essais:
        print(("OK    " if gagne else "ECHEC ") + libelle)
        print("      attendu : " + attendu + " ; obtenu : " + obtenu)
        print("      detail  : " + detail[:150])
    if residus:
        print("RESIDUS de cobaye NON retires : " + ", ".join(residus))
    gagnes = sum(1 for essai in essais if essai[3])
    print("")
    print("AUTOTEST MAILLON 7 : " + str(gagnes) + "/" + str(len(essais)) + " temoins")
    if gagnes != len(essais) or residus:
        print("VERDICT : KO -- le maillon ne mord pas (ou epargne) comme il le dit.")
        return 1
    print("VERDICT : OK -- le maillon MORD sur le mort et EPARGNE le vif.")
    return 0


# --- MAILLON 3, SECONDE REGLE : la table DECLAREE (MO-478) ------------------
# Le maillon 3 lisait trois routines en dur ; il doit desormais LIRE sa table. Ces
# cobayes le prouvent : ils changent la table, pas le code du maillon.
PREFIXE_COBAYE_MAILLON3 = "cobaye-maillon3-"
MARQUEUR_FIN_COBAYE = "passe-fin"


def _poser_cobaye_routine(dossier, age_secondes, declare=True):
    """Pose une routine de COBAYE : ses declarations, son PID, sa fin de passe.

    `declare=False` : la routine declare qu'elle NE journalise PAS sa fin
    (`EVENEMENT_FIN_PASSE = None`). `age_secondes=None` : la fin declaree n'est
    JAMAIS posee (routine muette). Les fichiers naissent DANS la zone jetable.
    """
    dossier.mkdir(parents=True, exist_ok=True)
    nom = dossier.name
    declaration = ('EVENEMENT_FIN_PASSE = "' + MARQUEUR_FIN_COBAYE + '"\n'
                   if declare else "EVENEMENT_FIN_PASSE = None\n")
    (dossier / "constants.py").write_text(
        'NOM_JOURNAL = "' + nom + '-log.jsonl"\n' + declaration, encoding="utf-8"
    )
    (dossier / (nom + ".pid")).write_text(str(os.getpid()) + "\n", encoding="utf-8")
    if age_secondes is None:
        return
    moment = datetime.now() - timedelta(seconds=age_secondes)
    (dossier / (nom + "-log.jsonl")).write_text(
        json.dumps({"type": MARQUEUR_FIN_COBAYE, "date": moment.strftime(FORMAT_DATE)}) + "\n",
        encoding="utf-8",
    )


def _poser_table_cobaye(dossier_vie, noms):
    """Ecrit la table DECLAREE d'un cobaye : BOUCLES + PID_PAR_NOM, rien d'autre."""
    dossier_vie.mkdir(parents=True, exist_ok=True)
    lignes = [repr((nom, str(dossier_vie.parent / nom))) for nom in noms]
    pid = "{" + ", ".join(repr(n) + ": " + repr(n + ".pid") for n in noms) + "}"
    (dossier_vie / "constants.py").write_text(
        "BOUCLES = (\n    " + ",\n    ".join(lignes) + ",\n)\nPID_PAR_NOM = " + pid + "\n",
        encoding="utf-8",
    )


def autotest_maillon3(racine):
    """Eprouve l'EVOLUTIVITE du maillon 3 : il LIT sa table, il ne la recopie pas.

    Trois temps sur des cobayes jetables :
      1. deux routines declarees (une fraiche, une muette) : le maillon MORD sur la
         muette et EPARGNE la fraiche ;
      2. une TROISIEME routine, muette, AJOUTEE a la table de cobaye : le maillon la
         juge SANS qu'on touche a son code -- preuve qu'aucune liste n'est figee ;
      3. une routine qui DECLARE ne pas journaliser sa fin n'est pas accuse pour
         autant (le fait est DIT, il n'est pas invente).
    """
    matrix = trouver_matrix(Path(racine).resolve())
    if matrix is None:
        print("AUTOTEST IMPOSSIBLE : dossier matrix/ introuvable sous " + str(racine))
        return 2
    # Le lecteur borne d'une queue de journal vient du domicile partage : sans lui,
    # `dernier_evenement` echouerait (le cobaye le DIT, il ne se tait pas).
    sys.path.insert(0, str(matrix / "matrice" / "data" / "commun"))
    chemin_fabrique = matrix / "matrice" / "data" / "commun" / "cobayes_jetables.py"
    fabrique = charger_module_par_chemin(chemin_fabrique, "cobayes_jetables_maillon3")
    if fabrique is None:
        print("AUTOTEST IMPOSSIBLE : fabrique de cobayes illisible (" + str(chemin_fabrique) + ")")
        return 2

    residus = []
    essais = []
    # La table est chargee une fois par CHEMIN (cache de modules) : en production
    # elle ne bouge pas du processus. Le cobaye, lui, la REEcrit entre deux temps :
    # il vide donc ce cache pour simuler un processus neuf (sinon il eprouverait sa
    # propre memoire, pas la lecture du maillon).
    with fabrique.fixtures(PREFIXE_COBAYE_MAILLON3, residus) as zone:
        _poser_cobaye_routine(zone / "cobaye-fraiche", 1)
        _poser_cobaye_routine(zone / "cobaye-muette", (SEUIL_FIN_MINUTES + 5) * 60)
        carte = {"routines": zone}

        _poser_table_cobaye(zone / "vie", ("cobaye-fraiche", "cobaye-muette"))
        _MODULES_CHARGES.clear()
        etat, detail = maillon_routines(carte)
        mord = etat == "rompu" and "cobaye-muette" in detail
        epargne = "cobaye-fraiche" not in detail
        essais.append(("MORD sur la routine muette, EPARGNE la fraiche", "rompu",
                       etat, mord and epargne, detail))

        # 2. EVOLUTIVITE : la troisieme routine n'existe que dans la TABLE.
        _poser_cobaye_routine(zone / "cobaye-ajoutee", (SEUIL_FIN_MINUTES + 5) * 60)
        _poser_table_cobaye(zone / "vie",
                            ("cobaye-fraiche", "cobaye-muette", "cobaye-ajoutee"))
        _MODULES_CHARGES.clear()
        etat, detail = maillon_routines(carte)
        suit = etat == "rompu" and "cobaye-ajoutee" in detail
        essais.append(("SUIT sa table : la routine AJOUTEE est jugee sans toucher au code",
                       "rompu", etat, suit, detail))

        # 3. Une fin NON journalisee DECLAREE n'est pas une accusation.
        _poser_cobaye_routine(zone / "cobaye-sans-fin", None, declare=False)
        _poser_table_cobaye(zone / "vie", ("cobaye-sans-fin",))
        _MODULES_CHARGES.clear()
        etat, detail = maillon_routines(carte)
        dit = etat == "ok" and "ne journalise pas sa fin" in detail
        essais.append(("DIT une fin non journalisee declaree (jamais un faux KO)",
                       "ok", etat, dit, detail))

        # 4. MODE PASSE (MO-429, decision D2 du createur) : une routine servie
        #    puis ETEINTE n est pas accusee pour son absence de PID -- c est le
        #    SERVICE qui est juge (elle ne se sert plus d elle). Cobaye qui mord
        #    (non servie depuis 15 min -> SERVICE accuse) + contre-temoin
        #    (fin fraiche -> l etat normal passe).
        import shutil

        plan_vie = zone / "matrice" / "routines" / "vie"
        moteur_dir = zone / "matrice" / "data" / "commun"
        plan_vie.mkdir(parents=True, exist_ok=True)
        moteur_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(
            str(matrix / "matrice" / "data" / "commun" / "planning_routines.py"),
            str(moteur_dir / "planning_routines.py"),
        )

        def poser_mode(nom, mode):
            (plan_vie / "planning.json").write_text(
                json.dumps({"routines": [{
                    "nom": nom, "cadence_secondes": 60, "mode": mode,
                    "decalage_initial_secondes": 0, "priorite": 10,
                    "tolerance_cadences": 3,
                    "commande_passe": ["python3", "cobaye.py"],
                }]}, indent=2),
                encoding="utf-8",
            )

        # La meme zone sert de racine matrice pour le PLANNING (le moteur est
        # copie ci-dessus) et de dossier routines pour la TABLE.
        carte_passe = {"routines": zone, "matrix": zone}

        def cobaye_passe(nom, age_fin_secondes, mode):
            _poser_table_cobaye(zone / "vie", (nom,))
            _poser_cobaye_routine(zone / nom, age_fin_secondes)
            # ETEINTE entre deux passes : aucun PID sur le disque.
            (zone / nom / (nom + ".pid")).unlink()
            poser_mode(nom, mode)
            # PIEGE MESURE (MO-429) : vider le cache de MODULES ne suffit pas --
            # le `.pyc` du fichier recharge rend l ANCIEN contenu quand la meme
            # re-ecriture tombe dans la meme seconde (reproduit, puis repare par
            # la purge). Un cobaye qui simule un processus neuf vide les DEUX
            # caches : le bytecode est au niveau du FICHIER, pas du module.
            shutil.rmtree(str(zone / "vie" / "__pycache__"), ignore_errors=True)
            _MODULES_CHARGES.clear()

        cobaye_passe("cobaye-passe-ok", 1, "passe")
        etat, detail = maillon_routines(carte_passe)
        essais.append(("MODE PASSE : eteinte entre deux passes -> NON accusee (etat normal)",
                       "ok", etat, etat == "ok" and "en PASSE" in detail, detail))

        cobaye_passe("cobaye-passe-vieille", (SEUIL_FIN_MINUTES + 5) * 60, "passe")
        etat, detail = maillon_routines(carte_passe)
        essais.append(("MODE PASSE : non servie depuis 15 min -> le SERVICE est accuse",
                       "rompu", etat,
                       etat == "rompu" and "SERVICE ne l allume plus" in detail, detail))

    for libelle, attendu, obtenu, gagne, detail in essais:
        print(("OK    " if gagne else "ECHEC ") + libelle)
        print("      attendu : " + attendu + " ; obtenu : " + obtenu)
        print("      detail  : " + detail[:200])
    if residus:
        print("RESIDUS de cobaye NON retires : " + ", ".join(residus))
    gagnes = sum(1 for essai in essais if essai[3])
    print("")
    print("AUTOTEST MAILLON 3 : " + str(gagnes) + "/" + str(len(essais)) + " temoins")
    if gagnes != len(essais) or residus:
        print("VERDICT : KO -- le maillon ne LIT pas sa table (ou n'epargne pas).")
        return 1
    print("VERDICT : OK -- le maillon LIT sa table et MORD sur ce qu'elle declare.")
    return 0


# --- LA PUBLICATION DU PID DU SERVEUR (MO-458) -------------------------------
# Mesure du 2026-09-28 : le serveur (re)publiait le PID des ROUTINES
# (`recreer_pid_files`) mais le SIEN, ecrit UNE fois a l allumage, n etait JAMAIS
# repare. Efface a la main, il faisait dire a `vie etat` et au maillon 2 que la
# Matrice est ARRETEE alors que le serveur VIT : un VIVANT lu comme MORT. Le cobaye
# eprouve la regle la ou elle vit, au DOMICILE PARTAGE (matrice/data/commun/
# pid_serveur.py, consomme par le serveur -- M-076), et n ecrit que dans une zone
# jetable : la sonde de vivacite est INJECTEE, aucun processus n est lance ni tue.
PREFIXE_COBAYE_PID_SERVEUR = "cobaye-pid-serveur-"


def autotest_pid_serveur(racine):
    """Eprouve `pid_serveur.publier` : reparer l efface, JAMAIS ecraser un vivant."""
    matrix = trouver_matrix(Path(racine).resolve())
    if matrix is None:
        print("AUTOTEST IMPOSSIBLE : dossier matrix/ introuvable sous " + str(racine))
        return 2
    commun = matrix / "matrice" / "data" / "commun"
    sys.path.insert(0, str(commun))
    module = charger_module_par_chemin(commun / "pid_serveur.py", "pid_serveur_cobaye")
    if module is None:
        print("AUTOTEST IMPOSSIBLE : " + str(commun / "pid_serveur.py") + " illisible")
        return 2
    fabrique = charger_module_par_chemin(commun / "cobayes_jetables.py",
                                         "cobayes_jetables_pid_serveur")
    if fabrique is None:
        print("AUTOTEST IMPOSSIBLE : fabrique de cobayes illisible")
        return 2

    def jamais_vivant(_pid):
        return False

    def toujours_vivant(_pid):
        return True

    residus = []
    essais = []
    with fabrique.fixtures(PREFIXE_COBAYE_PID_SERVEUR, residus) as zone:
        fichier = zone / "server-matrice.pid"

        # 1. COBAYE QUI MORD : le fichier a ete efface a la main -> il est REPUBLIE.
        message, ecrit = module.publier(fichier, 4242, est_vivant=jamais_vivant)
        contenu = fichier.read_text(encoding="utf-8").strip() if fichier.exists() else "(absent)"
        essais.append(("COBAYE PID serveur EFFACE : republie (le vivant redevient lisible)",
                       "present", contenu, ecrit and contenu == "4242", message))

        # 2. COBAYE QUI MORD : le fichier dit un PID MORT (fantome) -> republie.
        fichier.write_text("0\n", encoding="utf-8")
        message, ecrit = module.publier(fichier, 4242, est_vivant=jamais_vivant)
        contenu = fichier.read_text(encoding="utf-8").strip()
        essais.append(("COBAYE PID serveur FANTOME : republie",
                       "present", contenu, ecrit and contenu == "4242", message))

        # 3. CONTRE-TEMOIN QUI EPARGNE : la verite est deja publiee -> rien n est reecrit.
        message, ecrit = module.publier(fichier, 4242, est_vivant=jamais_vivant)
        contenu = fichier.read_text(encoding="utf-8").strip()
        essais.append(("CONTRE-TEMOIN deja publie : rien n est reecrit (idempotent)",
                       "intact", contenu, (not ecrit) and contenu == "4242", message))

        # 4. GARDE : un PID ETRANGER VIVANT n est JAMAIS ecrase (deux serveurs ne
        #    doivent pas se croire seuls) -- le refus est NOMME, jamais silencieux.
        fichier.write_text("777\n", encoding="utf-8")
        message, ecrit = module.publier(fichier, 4242, est_vivant=toujours_vivant)
        contenu = fichier.read_text(encoding="utf-8").strip()
        essais.append(("GARDE PID ETRANGER VIVANT : jamais ecrase, refus NOMME",
                       "intact", contenu,
                       (not ecrit) and contenu == "777" and "ALERTE" in message, message))

    for libelle, attendu, obtenu, gagne, detail in essais:
        print(("OK    " if gagne else "ECHEC ") + libelle)
        print("      attendu : " + attendu + " ; obtenu : " + obtenu)
        print("      detail  : " + detail[:150])
    if residus:
        print("RESIDUS de cobaye NON retires : " + ", ".join(residus))
    gagnes = sum(1 for essai in essais if essai[3])
    print("")
    print("AUTOTEST PID SERVEUR : " + str(gagnes) + "/" + str(len(essais)) + " temoins")
    if gagnes != len(essais) or residus:
        print("VERDICT : KO -- le PID du serveur n est pas repare comme il le dit.")
        return 1
    print("VERDICT : OK -- le serveur repare son PID, et n ecrase jamais un vivant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())




