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
  3. ROUTINES         : les 3 boucles vivent ET FINISSENT leurs passes
  4. PILOTE           : la porte du pilote repond, serie stricte respectee
  5. ENTONNOIR        : vrac/files/brin coherents (pas de brin perime)
  6. INTERCOM         : le dialogue Matrice <-> agent est lisible et valide
  7. FANTOMES         : aucun PID mort qui laisse croire que la chaine tourne
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
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# --- SEUILS ET PORTES (aucune valeur en dur dans la logique) ----------------
SECONDES_MAX_PORTE = 60
SEUIL_FIN_MINUTES = 10
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
    (7, "fantomes", "FANTOMES (des PID morts ?)"),
    (8, "relais", "RELAIS (un theme pour prendre une identite ?)"),
    (9, "file-journal", "FILE <-> JOURNAL (les deux traces d'optimus disent-elles la meme chose ?)"),
)

# Impact sur le flux, par etat de maillon.
IMPACTS = {
    "ok": "",
    "rompu": "le flux s'arrete a ce maillon",
    "fantome": "la chaine est annoncee debout alors qu'elle est tombee",
    "bloque": "le flux est bloque (la chaine n'avance plus)",
    "perime": "la chaine servirait une donnee morte",
    "flux-porte-morte": "l'entree du flux ne repond plus : personne ne peut demarrer",
    "divergent": "la file et la trace se contredisent : plus rien ne dit ce qui est vraiment fait",
}

# Routines surveillees : (nom, fichier PID, journal, types de FIN attendus).
# Un journal absent = maillon sur PID seul (le detail le dit, jamais de faux OK).
ROUTINES = (
    ("veille-flux", "veille-flux.pid", "journal-veille.txt", ("passe-fin",)),
    ("espion-integrite", "espion.pid", "espion-log.jsonl", ("passe",)),
    ("suivi-sync", "suivi-sync.pid", None, ()),
)


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
        resultat = subprocess.run(
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
    """Les boucles vivent-elles ET finissent-elles leurs passes (lecon L-026) ?"""
    rompus = []
    details = []
    for nom, nom_pid, nom_journal, types_fin in ROUTINES:
        dossier = m["routines"] / nom
        pid = lire_pid(dossier / nom_pid)
        if pid is None:
            rompus.append(nom + " : aucun PID")
            continue
        if not processus_vivant(pid):
            rompus.append(nom + " : PID " + str(pid) + " mort (fantome)")
            continue
        if not types_fin:
            details.append(nom + " vivant (pas de journal declare)")
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
        details.append(
            nom + " vivant, derniere fin il y a " + str(int(age)) + " min" + trace
        )
    if rompus:
        return "rompu", " | ".join(rompus[:3])
    return "ok", "3 boucles saines -- " + " ; ".join(details)


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
    """Reste-t-il des PID morts qui laissent croire que la chaine tourne ?"""
    fantomes = []
    for chemin_pid in sorted(m["matrix"].rglob("*.pid")):
        pid = lire_pid(chemin_pid)
        if pid is None:
            fantomes.append(chemin_pid.name + " illisible")
        elif not processus_vivant(pid):
            fantomes.append(chemin_pid.name + "=" + str(pid))
    if fantomes:
        return "fantome", "PID mort(s) : " + ", ".join(fantomes[:5])
    return "ok", "aucun processus fantome (tous les PID repondent)"


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
    args = parser.parse_args()

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


if __name__ == "__main__":
    sys.exit(main())
