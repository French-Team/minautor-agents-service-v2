# -*- coding: utf-8 -*-
"""fonctions/harnais.py - Harnais v2 : mini-test de conformite importable
par CHAQUE outil v2 (decision utilisateur 2026-08-25).

PRINCIPE : plus rien n est fait par un agent v2 sans le harnais. Chaque
outil v2 importe ce module et appelle `verifier_outil()` en debut de
traitement ; chaque script temporaire passe par `verifier_script()`.

SIGNAUX (parite proto-9 v1, adaptes v2) :
  OK    : tout est conforme, tu peux continuer.
  WARN  : anomalie mineure, tu continues mais tu le signales.
  ERR   : erreur detectee, tu STOPPES et tu corriges avant de continuer.
  CRIT  : probleme critique, arret immediat, tout est restaure.

Les messages sont INTUITIFS (aident l agent) : chaque signal dit ce qui
ne va pas ET quoi faire ensuite. L agent n a pas a reflechir pour savoir
comment reagir : le harnais lui donne la reponse.
"""

import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime

_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine

RACINE = trouver_racine(__file__)

VERSION = "0.2.0"

# ------------------------------------------------------------------
# Configuration DYNAMIQUE (D15 : separation code/donnees)
# ------------------------------------------------------------------
# Le harnais est pilote par harnais-data.json : ajouter un import
# obligatoire, une verification, un rappel ou une securite = EDITER
# le JSON, JAMAIS le code. Le harnais lit la config a chaque appel
# et fait le reste (decision utilisateur 2026-08-25).

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "harnais-data.json")


def charger_config():
    """Charger harnais-data.json (retourne un dict vide si absent/invalide)."""
    try:
        with open(CONFIG_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


# ------------------------------------------------------------------
# Signaux (messages par situation)
# ------------------------------------------------------------------

SIGNAUX = {
    "OK": {
        "code": "SIG OK",
        "emoji": "",
        "message": "tout est conforme - tu peux continuer.",
    },
    "WARN": {
        "code": "SIG WARN",
        "emoji": "",
        "message": "anomalie mineure - tu continues mais tu le signales.",
    },
    "ERR": {
        "code": "SIG ERR",
        "emoji": "",
        "message": "erreur detectee - tu STOPPES et tu corriges avant de continuer.",
    },
    "CRIT": {
        "code": "SIG CRIT",
        "emoji": "",
        "message": "probleme critique - arret immediat, tout est restaure.",
    },
}


def signal(niveau, contexte, detail=""):
    """Emettre un signal du harnais avec un message intuitif."""
    info = SIGNAUX.get(niveau, SIGNAUX["WARN"])
    ligne = "[HARNAIS %s] %s : %s" % (info["code"], contexte,
                                        info["message"])
    if detail:
        ligne += " (%s)" % detail
    print(ligne)
    return niveau


def verifier_ascii(texte):
    """Verifier qu un texte est ASCII strict (regle v1 ; v2 tolere UTF-8
    mais les scripts critiques restent ASCII)."""
    return all(ord(c) < 128 for c in texte)


# ------------------------------------------------------------------
# Mini-test de conformite d un outil v2
# ------------------------------------------------------------------

STRUCTURE_OBLIGATOIRE = ["entry.py", "fonctions"]
EXTENSIONS_PY = (".py",)


def verifier_outil(chemin_outil, agent=""):
    """Mini-test de conformite d un outil v2.

    Verifie :
      1. Structure obligatoire (entry.py + fonctions/ + .md).
      2. Syntaxe Python valide (compile de tous les .py).
      3. Detection de la racine via os_path (P10) presente dans entry.py.
      4. Doc .md presente.
      5. ASCII/LF si fichier critique.

    Retour : 0 si conforme, 1 si erreur (a traiter), 2 si critique.
    """
    if not os.path.isdir(chemin_outil):
        signal("CRIT", "outil introuvable", chemin_outil)
        return 2

    contexte = os.path.basename(chemin_outil.rstrip("/\\"))

    # 1. structure obligatoire
    manquants = [f for f in STRUCTURE_OBLIGATOIRE
                 if not os.path.exists(os.path.join(chemin_outil, f))]
    md = [f for f in os.listdir(chemin_outil) if f.endswith(".md")]
    if manquants:
        signal("ERR", "structure de l outil %s incomplete" % contexte,
               "manque : %s" % ", ".join(manquants))
        return 1
    if not md:
        signal("ERR", "doc .md manquante pour l outil %s" % contexte,
               "un outil v2 DOIT avoir son <outil>.md (template v2)")
        return 1
    signal("OK", "structure de l outil %s complete" % contexte,
           "entry.py + fonctions/ + %s" % md[0])

    # 2. syntaxe python de tous les .py (BOM tolere : les fichiers v2
    #    existants commencent par U+FEFF + coding utf-8 -- Python les
    #    accepte ; on lit en utf-8-sig pour ignorer le BOM)
    erreurs = []
    for racine_dossier, _, fichiers in os.walk(chemin_outil):
        for f in fichiers:
            if f.endswith(EXTENSIONS_PY):
                chemin_py = os.path.join(racine_dossier, f)
                try:
                    brut = open(chemin_py, "rb").read()
                    if brut.startswith(b"\xef\xbb\xbf"):
                        brut = brut[3:]
                    compile(brut.decode("utf-8"), chemin_py, "exec")
                except (SyntaxError, UnicodeDecodeError) as exc:
                    erreurs.append("%s : %s" % (f, exc))
    if erreurs:
        signal("ERR", "syntaxe Python invalide dans %s" % contexte,
               "; ".join(erreurs[:3]))
        return 1
    signal("OK", "syntaxe Python valide dans %s" % contexte,
           "%d fichier(s) compile(s)" % len(erreurs) if False else "compile OK")

    # 3. racine via os_path (P10) dans entry.py
    entry = os.path.join(chemin_outil, "entry.py")
    try:
        contenu_entry = open(entry, encoding="utf-8").read()
    except OSError:
        contenu_entry = ""
    if "trouver_racine" not in contenu_entry and \
            "os_path" not in contenu_entry:
        signal("WARN", "entry.py de %s n utilise pas la detection P10" % contexte,
               "P10 : passer par tools-commun/os_path/ (jamais de ../.. comptes)")
    else:
        signal("OK", "detection racine P10 presente dans entry.py de %s" % contexte)

    # 4. conformite harnais : entry.py importe-t-il le harnais ?
    if "harnais" not in contenu_entry and \
            "verifier_outil" not in contenu_entry:
        signal("WARN", "l outil %s n appelle pas encore le harnais" % contexte,
               "PROTOCOLE 21 : chaque outil v2 DOIT appeler verifier_outil() "
               "en debut de traitement")
    else:
        signal("OK", "l outil %s est harnache (verifier_outil appele)" % contexte)

    signal("OK", "outil %s CONFORME - tu peux l utiliser." % contexte)
    return 0


# ------------------------------------------------------------------
# Protection des scripts temporaires
# ------------------------------------------------------------------

def verifier_script(chemin_script, agent="", raison="", type_script="test"):
    """Proteger un script temporaire (PROTOCOLE 21 + proto-13 v1).

    DYNAMIQUE (v0.2.0, decision utilisateur 2026-08-25) : le harnais est
    pilote par harnais-data.json (D15). Les imports obligatoires, les
    verifications (agent, raison...), les rappels et les securites sont
    lus depuis la config a CHAQUE appel. Ajouter une regle = editer le
    JSON, jamais le code ni les scripts.

    REGLE D ORIGINE (v1, demandee pour la v2 par l utilisateur 2026-08-25) :
      - Chaque agent cree SON dossier temporaire a la RACINE du workspace :
        `tmp-<agent>/` (ex: tmp-stark/, tmp-vision/).
      - Le script vit DANS ce dossier dedie a l agent (jamais dans /tmp
        systeme, jamais a la racine, jamais dans un dossier d outil).
      - Le script ne doit JAMAIS ecrire hors de son dossier (isolation).
      - En fin de mission, le dossier est SUPPRIME (`rm -rf tmp-<agent>`) :
        lifecycle complet, 0 residu.
    """
    config = charger_config()
    bloquant_ko = 0

    # 0. lecture du script
    if not os.path.isfile(chemin_script):
        signal("CRIT", "script temporaire introuvable", chemin_script)
        return 2
    try:
        contenu = open(chemin_script, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        signal("ERR", "script illisible", str(exc))
        return 1

    dossier = os.path.dirname(os.path.abspath(chemin_script))
    nom_dossier = os.path.basename(dossier)
    try:
        chemin_rel = os.path.relpath(dossier, RACINE)
    except ValueError:
        chemin_rel = None
    a_la_racine = chemin_rel is not None \
        and not chemin_rel.startswith("..") and "/" not in chemin_rel \
        and "\\" not in chemin_rel

    # ------------------------------------------------------------------
    # 1. VERIFICATIONS (config : verifications[]) -- agent, raison, ...
    # ------------------------------------------------------------------
    contexte_args = {"agent": agent, "raison": raison}
    for verif in config.get("verifications", []):
        nom = verif.get("nom", "?")
        cle = verif.get("cle", "")
        valeur = contexte_args.get(cle, "")
        bloquant = verif.get("bloquant", True)
        if not valeur:
            signal("ERR" if bloquant else "WARN",
                   "verification %s" % nom, verif.get("message", ""))
            if bloquant:
                bloquant_ko += 1
        else:
            signal("OK", "verification %s" % nom, "%s fourni" % cle)

    # ------------------------------------------------------------------
    # 2. SECURITES (config : securites[])
    # ------------------------------------------------------------------
    for secu in config.get("securites", []):
        nom = secu.get("nom", "?")
        bloquant = secu.get("bloquant", True)
        ok = True
        if nom == "zone_dediee":
            dossier_ok = a_la_racine and nom_dossier.startswith("tmp-") \
                and len(nom_dossier) > 4
            ok = dossier_ok
            if not ok:
                signal("ERR", "securite %s" % nom, secu.get("message", ""))
                signal("WARN", "cree ton dossier dedie a la RACINE : tmp-<agent>/ "
                       "(ex: tmp-stark/, tmp-vision/) puis relance")
                if bloquant:
                    bloquant_ko += 1
        elif nom == "isolation":
            # motifs = SOUS-CHAINE LITTERALE (config D15, pas de regex)
            entrees = []
            for motif in secu.get("motifs", []):
                if motif and motif in contenu:
                    entrees.append(motif)
            if entrees:
                signal("WARN", "securite %s" % nom,
                       secu.get("message", "") + " ; motifs: " + "; ".join(entrees))
                if bloquant:
                    bloquant_ko += 1
            else:
                signal("OK", "securite %s" % nom, "aucun chemin absolu suspect")

    # ------------------------------------------------------------------
    # 3. IMPORTS OBLIGATOIRES (config : imports_obligatoires[])
    # ------------------------------------------------------------------
    for imp in config.get("imports_obligatoires", []):
        motif = imp.get("motif", "")
        bloquant = imp.get("bloquant", False)
        if not motif:
            continue
        # motif = SOUS-CHAINE LITTERALE (config D15, pas de regex)
        if motif in contenu:
            signal("OK", "import obligatoire %s" % imp.get("nom", "?"),
                   "present dans le script")
        else:
            signal("WARN" if not bloquant else "ERR",
                   "import obligatoire manquant : %s" % imp.get("nom", "?"),
                   imp.get("message", ""))
            if bloquant:
                bloquant_ko += 1

    # ------------------------------------------------------------------
    # 4. RAPPELS (config : rappels[]) -- utilisation, commande, ...
    # ------------------------------------------------------------------
    print("")
    print("=== RAPPELS DU HARNAIS ===")
    for rappel in config.get("rappels", []):
        print("  > %s" % rappel.get("message", ""))

    # 5. LECONS APPRISES (BDD v2, D10) -- diffusion des apprentissages
    try:
        from lecons import rappels_lecons
        lecons_msg = rappels_lecons(agent=agent)
    except Exception:
        lecons_msg = []
    if lecons_msg:
        print("")
        print("=== LECONS APPRISES (BDD v2) ===")
        for msg in lecons_msg:
            print("  > %s" % msg)

    # ------------------------------------------------------------------
    # Verdict
    # ------------------------------------------------------------------
    if bloquant_ko:
        signal("ERR", "%d verification(s)/securite(s) bloquante(s)" % bloquant_ko,
               "corrige puis relance le harnais")
        return 1
    signal("OK", "script temporaire %s PROTEGE - tu peux l executer, puis "
           "SUPPRIME-le (lifecycle complet)." % os.path.basename(chemin_script))
    return 0


# ------------------------------------------------------------------
# Execution protegee d un script temporaire (AVANT -> PENDANT -> APRES)
# ------------------------------------------------------------------

def _empreinte(chemin):
    """Empreinte SHA-256 d un fichier (backup AVANT pour detection APRES)."""
    try:
        h = hashlib.sha256()
        with open(chemin, "rb") as fh:
            for bloc in iter(lambda: fh.read(65536), b""):
                h.update(bloc)
        return h.hexdigest()
    except OSError:
        return None


def executer_script(chemin_script, agent="", raison="", timeout=60):
    """Orchestrateur AVANT -> PENDANT -> APRES (transparent pour l agent).

    L agent appelle UNE commande ; le harnais fait tout le reste :

      AVANT  : verifier_script (zone, verifications, imports, securites)
               + syntaxe Python + backup empreinte + journalisation
      PENDANT: execution via subprocess (timeout, captures)
      APRES  : verdict rc + detection d effets (fichiers hors zone)
               + rappels + journalisation finale
    """
    print("")
    print("=== HARNAIS EXEC (script temporaire) ===")
    print("Agent : %s | Raison : %s" % (agent or "-", raison or "-"))

    # ---------- AVANT ----------
    rc_verif = verifier_script(chemin_script, agent=agent, raison=raison)
    if rc_verif != 0:
        signal("ERR", "execution refusee",
               "les verifications AVANT ont echoue (rc=%d)" % rc_verif)
        return rc_verif

    # syntaxe Python (compile) avant de lancer
    try:
        contenu = open(chemin_script, encoding="utf-8",
                       errors="replace").read()
        compile(contenu, chemin_script, "exec")
        signal("OK", "syntaxe Python valide", "compile() reussi AVANT execution")
    except (SyntaxError, OSError) as exc:
        signal("ERR", "syntaxe Python invalide", str(exc))
        return 1

    # backup empreinte (detection des effets APRES)
    empreinte_avant = _empreinte(chemin_script)
    dossier = os.path.dirname(os.path.abspath(chemin_script))
    fichiers_avant = set()
    for racine_d, _, fichiers in os.walk(dossier):
        for f in fichiers:
            fichiers_avant.add(os.path.relpath(os.path.join(racine_d, f),
                                               dossier))
    signal("OK", "backup AVANT", "empreinte + %d fichier(s) dans la zone"
           % len(fichiers_avant))

    journaliser(agent, "script:%s" % os.path.basename(chemin_script),
                "EXEC-AVANT")

    # ---------- PENDANT ----------
    print("")
    print("=== EXECUTION (timeout %ss) ===" % timeout)
    # Environnement prepare : le harnais injecte les chemins v2 dans
    # PYTHONPATH (os_path, bdd-lecons, harnais) -- l agent n a PAS a
    # ecrire de sys.path manuel dans son script (PROTOCOLE 22 : le
    # harnais fait le reste).
    env = os.environ.copy()
    _fonctions_v2 = [
        os.path.join(RACINE, "cerveau-projet", "freelance", "tools-commun",
                     "os_path", "fonctions"),
        os.path.join(RACINE, "cerveau-projet", "freelance", "tools-commun",
                     "bdd-lecons", "fonctions"),
        os.path.join(RACINE, "cerveau-projet", "freelance", "tools-commun",
                     "harnais", "fonctions"),
    ]
    _ancien = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join(
        [p for p in _fonctions_v2 if os.path.isdir(p)]
        + ([_ancien] if _ancien else []))
    try:
        proc = subprocess.run([sys.executable, os.path.abspath(chemin_script)],
                              capture_output=True, text=True,
                              encoding="utf-8", errors="replace",
                              timeout=timeout, cwd=dossier, env=env)
        sortie = proc.stdout
        erreur = proc.stderr
        rc = proc.returncode
        timeout_ko = False
    except subprocess.TimeoutExpired:
        sortie, erreur, rc, timeout_ko = "", "TIMEOUT (%ss)" % timeout, -1, True
    except OSError as exc:
        sortie, erreur, rc, timeout_ko = "", str(exc), -2, False

    if sortie:
        print("--- stdout ---")
        print(sortie.rstrip())
    if erreur:
        print("--- stderr ---")
        print(erreur.rstrip())

    # ---------- APRES ----------
    print("")
    print("=== VERDICT ===")
    if timeout_ko:
        signal("ERR", "timeout depasse (%ss)" % timeout,
               "le script a pris trop de temps")
    elif rc == 0:
        signal("OK", "execution reussie (rc=0)")
    else:
        signal("ERR", "execution en echec (rc=%d)" % rc,
               erreur[:200] if erreur else "")

    # detection d effets : nouveaux fichiers dans la zone / script modifie
    fichiers_apres = set()
    for racine_d, _, fichiers in os.walk(dossier):
        for f in fichiers:
            fichiers_apres.add(os.path.relpath(os.path.join(racine_d, f),
                                               dossier))
    nouveaux = fichiers_apres - fichiers_avant
    empreinte_apres = _empreinte(chemin_script)
    if nouveaux:
        signal("WARN", "le script a cree des fichiers",
               "; ".join(sorted(nouveaux)))
    if empreinte_apres != empreinte_avant:
        signal("WARN", "le script a modifie son propre fichier",
               "contenu change pendant l execution")
    if not nouveaux and empreinte_apres == empreinte_avant:
        signal("OK", "aucun effet hors zone", "script isole (0 nouveau fichier)")

    # rappels (depuis la config)
    config = charger_config()
    print("")
    print("=== RAPPELS DU HARNAIS ===")
    for rappel in config.get("rappels", []):
        print("  > %s" % rappel.get("message", ""))

    # lecons apprises (BDD v2, D10)
    try:
        from lecons import rappels_lecons
        lecons_msg = rappels_lecons(agent=agent)
    except Exception:
        lecons_msg = []
    if lecons_msg:
        print("")
        print("=== LECONS APPRISES (BDD v2) ===")
        for msg in lecons_msg:
            print("  > %s" % msg)

    journaliser(agent, "script:%s" % os.path.basename(chemin_script),
                "EXEC-APRES:rc=%d" % rc)

    return 0 if rc == 0 and not timeout_ko else 1


# ------------------------------------------------------------------
# Journalisation du harnais
# ------------------------------------------------------------------

def journaliser(agent, outil, niveau):
    """Journaliser l usage du harnais (tracabilite)."""
    try:
        dossier_log = os.path.join(RACINE, "cerveau-projet", "freelance",
                                   "classeur")
        if not os.path.isdir(dossier_log):
            return
        ligne = {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 "agent": agent, "outil": outil, "signal": niveau}
        with open(os.path.join(dossier_log, "harnais-log.jsonl"), "a",
                  encoding="utf-8") as f:
            f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    except OSError:
        pass