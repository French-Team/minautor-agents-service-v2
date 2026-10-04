# -*- coding: ascii -*-
"""fonctions/moteur.py - UNE tache : decouvrir et executer les suites NR.

Chaque suite = un dossier <chemin_suites>/nr-<x>/ contenant suite.json :
    {
      "nom": "nr-jarvis",
      "description": "...",
      "actif": true,
      "perimetre": ["cerveau-projet/freelance/tools-commun/jarvis"],
      "tests": [
        {"nom": "aide-jarvis",
         "commande": "python3 {racine}/.../jarvis.py --help",
         "rc_attendu": 0,
         "sortie_contient": ["usage"],
         "fichiers_verifies": [{"chemin": "...", "doit_exister": true}]}
      ]
    }

Securites (config harnais-nr-data.json, D15) : lecture seule par defaut,
.bak + rollback si un test declare une modification, sandbox temporaire
pour les ecrits, hors-perimetre interdit.

Principe NON-REGRESSION : apres la suite, le workspace est IDENTIQUE
(hash avant = hash apres sur le perimetre, sinon ECART signale).
"""

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

_d = os.path.dirname(os.path.abspath(__file__))
# P10 : la racine se DETECTE via os_path, elle ne se compte pas
sys.path.insert(0, os.path.join(_d, "..", "..", "os_path", "fonctions"))
from racine import trouver_racine  # noqa: E402

RACINE = Path(trouver_racine(__file__))
OUTIL_DIR = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
    "harnais-nr"
CONFIG_PATH = OUTIL_DIR / "harnais-nr-data.json"
# la racine DETECTEE EST la racine du workspace (pas son parent !)
WS = str(RACINE)


def charger_config():
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _dossier_suites(cfg):
    nom = cfg.get("chemin_suites", "suites")
    dossier = os.path.join(str(OUTIL_DIR), nom)
    if not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)
    return dossier


def charger_suites(cfg):
    """[(nom_suite, dict_suite)] des suites actives, triees."""
    resultats = []
    for nom in sorted(os.listdir(_dossier_suites(cfg))):
        chemin = os.path.join(_dossier_suites(cfg), nom, "suite.json")
        if not os.path.isfile(chemin):
            continue
        try:
            with open(chemin, encoding="utf-8") as f:
                s = json.load(f)
        except (OSError, ValueError) as e:
            print("[NR] ERREUR suite %s : %s" % (nom, e))
            continue
        if s.get("actif", True):
            resultats.append((nom, s))
    return resultats


def lister(cfg):
    print("[HARNAIS-NR] Suites de non-regression :")
    suites = charger_suites(cfg)
    if not suites:
        print("  (aucune suite - PHASE 1 : le cadre attend les suites)")
        return
    for nom, s in suites:
        tests = [t.get("nom", "?") for t in s.get("tests", [])]
        marqueur = "" if not s.get("temporaire") else " [TEMPORAIRE]"
        exemple = "" if not s.get("exemple") else " [EXEMPLE]"
        print("  %-16s %2d test(s)%s%s - %s" %
              (nom, len(tests), marqueur, exemple,
               s.get("description", "")[:60]))
        for t in tests:
            print("      - %s" % t)


def _hash_perimetre(perimetre):
    """{chemin_relatif: sha256} de tous les fichiers du perimetre."""
    empreintes = {}
    for relatif in perimetre or []:
        base = os.path.join(WS, relatif)
        if not os.path.exists(base):
            continue
        if os.path.isfile(base):
            fichiers = [base]
        else:
            fichiers = []
            for courant, dossiers, noms in os.walk(base):
                dossiers[:] = [x for x in dossiers
                               if x not in ("__pycache__",
                                            ".nr-sandbox")]
                for n in noms:
                    fichiers.append(os.path.join(courant, n))
        for f in fichiers:
            try:
                with open(f, "rb") as fh:
                    empreintes[os.path.relpath(f, WS)] = \
                        hashlib.sha256(fh.read()).hexdigest()
            except OSError:
                pass
    return empreintes


def _hors_perimetre(chemin, perimetre):
    chemin_abs = os.path.abspath(os.path.join(WS, chemin))
    for relatif in perimetre or []:
        base_abs = os.path.abspath(os.path.join(WS, relatif))
        if chemin_abs.startswith(base_abs + os.sep) or \
                chemin_abs == base_abs:
            return False
    return True


def executer_test(test, cfg, suite, resultat_suite):
    """Executer UN test declare en donnees. Retourne (ok, details)."""
    details = []
    nom = test.get("nom", "?")
    timeout = int(cfg.get("timeout_defaut_secondes", 120))
    commande = test.get("commande", "")
    if not commande:
        return False, ["commande absente"]
    cmd = commande.replace("{racine}", WS).replace("{ws}", WS)
    securites = cfg.get("securites", {})

    # SECURITE : hors perimetre interdit (si le test touche des fichiers)
    perimetre = suite.get("perimetre", [])
    for fv in test.get("fichiers_verifies", []):
        cible = fv.get("chemin", "")
        if cible and securites.get("hors_perimetre_interdit") and \
                _hors_perimetre(cible, perimetre):
            details.append("SECURITE: '%s' hors perimetre declare" % cible)
            return False, details

    # SECURITE : .bak avant toute ecriture declaree + rollback garanti
    sauvegardes = {}
    modification = bool(test.get("modifie_fichier"))
    if modification:
        if securites.get("lecture_seule_par_defaut") and \
                not test.get("ecriture_autorisee"):
            details.append("SECURITE: ecriture non autorisee "
                           "(lecture seule par defaut)")
            return False, details
        for fv in test.get("fichiers_verifies", []):
            src = os.path.join(WS, fv.get("chemin", ""))
            if os.path.isfile(src):
                bak = src + ".bak-nr"
                with open(src, "rb") as fi:
                    contenu = fi.read()
                with open(bak, "wb") as fo:
                    fo.write(contenu)
                sauvegardes[src] = bak

    # Execution (sandbox : cwd = dossier de la suite)
    cwd = os.path.join(_dossier_suites(cfg), suite.get("nom", ""))
    env = dict(os.environ)
    env["NR_SANDBOX"] = os.path.join(cwd, cfg.get("securites", {})
                                     .get("sandbox_temp", ".nr-sandbox"))
    os.makedirs(env["NR_SANDBOX"], exist_ok=True)
    sortie = ""
    rc = -1
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True,
                           text=True, timeout=timeout, cwd=cwd, env=env,
                           creationflags=getattr(subprocess,
                                                 "CREATE_NO_WINDOW", 0))
        rc = p.returncode
        sortie = (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        details.append("TIMEOUT apres %ds" % timeout)
    except OSError as e:
        details.append("ERREUR execution : %s" % e)

    # Verifications DECLAREES
    if "rc_attendu" in test and rc != test["rc_attendu"]:
        details.append("rc=%s attendu %s" % (rc, test["rc_attendu"]))
    for motif in test.get("sortie_contient", []):
        if motif.lower() not in sortie.lower():
            details.append("sortie sans '%s'" % motif[:40])
    for fv in test.get("fichiers_verifies", []):
        cible = os.path.join(WS, fv.get("chemin", ""))
        existe = os.path.exists(cible)
        if fv.get("doit_exister") and not existe:
            details.append("fichier absent : %s" % fv.get("chemin"))
        elif fv.get("doit_exister") is False and existe:
            details.append("fichier ne devrait pas exister : %s"
                           % fv.get("chemin"))

    # ROLLBACK : restauration garantie (.bak -> original)
    for src, bak in sauvegardes.items():
        try:
            with open(bak, "rb") as fi:
                contenu = fi.read()
            with open(src, "wb") as fo:
                fo.write(contenu)
            os.remove(bak)
        except OSError as e:
            details.append("ROLLBACK echoue sur %s : %s" % (src, e))

    ok = not details and rc == test.get("rc_attendu", 0)
    if ok:
        print("    [OK]   %s" % nom)
    else:
        print("    [ECHEC] %s : %s" % (nom, "; ".join(details)[:100]))
        resultat_suite["echecs"].append({"test": nom, "details": details})
    return ok, details


def executer_suite(cfg, nom_suite, filtre_test=None, ecrire_rapport=False):
    suites = dict(charger_suites(cfg))
    if nom_suite not in suites:
        print("[NR] ERREUR : suite '%s' introuvable" % nom_suite)
        return False
    suite = suites[nom_suite]
    print("[NR] Suite %s - %s" % (nom_suite,
                                  suite.get("description", "")[:60]))
    avant = _hash_perimetre(suite.get("perimetre"))
    resultat = {"suite": nom_suite,
                "date": datetime.now().isoformat(timespec="seconds"),
                "total": 0, "passe": 0, "echecs": []}
    tout_ok = True
    for test in suite.get("tests", []):
        nom_test = test.get("nom", "?")
        if filtre_test and nom_test != filtre_test:
            continue
        resultat["total"] += 1
        ok, _ = executer_test(test, cfg, suite, resultat)
        if ok:
            resultat["passe"] += 1
        else:
            tout_ok = False

    # PRINCIPE NR : le workspace doit etre IDENTIQUE apres la suite
    apres = _hash_perimetre(suite.get("perimetre"))
    modifies = sorted(set(apres) ^ set(avant)) + \
        [c for c in set(apres) & set(avant) if apres[c] != avant[c]]
    if modifies:
        tout_ok = False
        print("  [ECART NR] perimetre modifie par la suite : %s"
              % ", ".join(modifies[:5]))
        resultat["echecs"].append(
            {"test": "(perimetre)", "details":
             ["workspace modifie : %s" % m for m in modifies]})

    resume = "%d/%d test(s)" % (resultat["passe"], resultat["total"])
    print("[NR] Suite %s : %s - %s" % (
        nom_suite, "CONFORME" if tout_ok else "NON CONFORME", resume))
    if ecrire_rapport:
        ecrire_rapport_json(cfg, resultat)
    return tout_ok


def executer_toutes(cfg, ecrire_rapport=False):
    suites = charger_suites(cfg)
    if not suites:
        print("[NR] Aucune suite active.")
        return True
    global_ok = True
    for nom, _ in suites:
        if not executer_suite(cfg, nom, ecrire_rapport=ecrire_rapport):
            global_ok = False
    verdict = "CONFORME" if global_ok else "NON CONFORME"
    print("[NR] GLOBAL : %s" % verdict)
    return global_ok


def ecrire_rapport_json(cfg, resultat):
    dossier = os.path.join(str(OUTIL_DIR),
                           cfg.get("dossier_rapports", "rapports"))
    os.makedirs(dossier, exist_ok=True)
    horodatage = datetime.now().strftime("%Y%m%d-%H%M%S")
    chemin = os.path.join(dossier, "%s-%s.json"
                          % (resultat["suite"], horodatage))
    with open(chemin, "w", encoding="ascii", newline="\n") as f:
        json.dump(resultat, f, ensure_ascii=True, indent=2)
    print("[NR] Rapport : %s" % os.path.relpath(chemin, WS))
