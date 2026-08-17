#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-057-marbre-garde-fou.py
GARDE-FOU : le marbre (zones protegees du noyau) reste INTACT dans la
non-regression (demande utilisateur 2026-08-15 : graver dans le marbre des
regles qui ne peuvent plus etre modifiees sans protocole de securite).
Contexte :
  - Le noyau (Constitution dans AGENTS.md, regles-groupes-agents.md, cases
    critiques de Cerberus c0/c0b/c10/c14/c20) est protege par le manifeste
    cerveau-projet/agents/regles-immuables/marbre/marbre.json (empreintes
    SHA-256).
  - proteger-verrou-marbre verifie l integrite (AVANT : les outils du noyau
    appellent le verrou avant d ecrire ; APRES : ce garde-fou).
  - proteger-modifier-marbre est la SEULE porte de modification legitime :
    elle exige une autorisation utilisateur explicite (--autorisation).
Invariants verifies :
  1. Les 2 outils existent, se compilent, --version affiche la version
  2. marbre.json existe, JSON valide, contient les 7 zones attendues
  3. proteger-verrou-marbre --tous -> rc=0 (marbre intact)
  4. Preuve NEGATIVE : violer la case cerberus.c0 -> verrou --zone -> rc=1
     (BLOQUE) puis restauration -> --tous rc=0 (try/finally garanti)
  5. proteger-modifier-marbre SANS --autorisation -> rc=1 (BLOQUE : le
     marbre est immuable pour les agents)
  6. Integration AVANT : activer-agent-principal contient
     verrouiller_constitution + editer-parcours contient
     verifier_cases_protegees
  7. Catalogue : les 2 outils sont declares dans catalogue-commandes.json
  8. Index-tools : les 2 outils sont references dans index-tools.md
  9. Normes : ASCII strict + LF pur (outils, manifeste, protocole, test)
  11. ANTI-CONTOURNEMENT : cartes-lock.json existe (manifeste des empreintes
      des cartes) et couvre les 14 cartes (barrage n3 : aucune carte ne peut
      etre modifiee HORS editer-parcours sans etre detectee)
  12. ANTI-CONTOURNEMENT : editer-parcours BLOQUE une carte modifiee HORS
      editer-parcours (preuve negative avec restauration via git)
  13. ANTI-CONTOURNEMENT : --modifier-case (remplacer le contenu d une case
      SANS ecriture directe) fonctionne en dry-run
Tags: securite, marbre, anti-contournement, garde-fou
"""
import glob
import importlib.util
import io
import json
import os
import subprocess
import sys
import time
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable
# Chemins des fichiers verifies
VERROU_DIR = os.path.join(TOOLS_DIR, "proteger", "proteger-verrou-marbre")
VERROU_PY = os.path.join(VERROU_DIR, "proteger-verrou-marbre.py")
MODIF_DIR = os.path.join(TOOLS_DIR, "proteger", "proteger-modifier-marbre")
MODIF_PY = os.path.join(MODIF_DIR, "proteger-modifier-marbre.py")
MARBRE_JSON = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "regles-immuables",
                           "marbre", "marbre.json")
PROTOCOLE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "regles-immuables",
                         "general", "protocole-securite-marbre",
                         "protocole-securite-marbre.001.01.ebauche.md")
CERBERUS_PARCOURS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "cerberus",
                                 "parcours", "parcours-cerberus.json")
ACTIVER_PY = os.path.join(TOOLS_DIR, "activer", "activer-agent-principal",
                          "activer-agent-principal.py")
EDITER_PY = os.path.join(TOOLS_DIR, "editer", "editer-parcours", "editer-parcours.py")
CATALOGUE = os.path.join(TOOLS_DIR, "generateurs", "generateurs-commande",
                         "catalogue-commandes.json")
INDEX = os.path.join(TOOLS_DIR, "index-tools.md")
ZONES_ATTENDUES = ["constitution", "regles-groupes-agents",
                   "cerberus.c0", "cerberus.c0b", "cerberus.c10",
                   "cerberus.c14", "cerberus.c20"]
CARTES_LOCK = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "regles-immuables",
                           "marbre", "cartes-lock.json")
NB_POINTS = 0
NB_OK = 0
NB_KO = 0
# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
# ------------------------------------------------------------------
CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for i, arg in enumerate(sys.argv):
    if arg == "--isoler" and i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[i + 1])
        except ValueError:
            pass
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        for p in sys.argv[i + 1].split(","):
            try:
                DESACTIVES.append(int(p))
            except ValueError:
                pass
ETAPES = []
T_START = time.monotonic()


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def point_actif(numero):
    """True si le point N doit s executer (options on/off du test)."""
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    """Enregistre la duree d une etape (no-op si --no-chrono)."""
    if CHRONO_ACTIF:
        ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    """Affiche le bilan des durees : total + detail par etape."""
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-057 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-34s %6.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    """Enregistre un point OK/KO et affiche le verdict."""
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("[OK] %s" % nom)
    else:
        NB_KO += 1
        print("[KO] %s" % nom)
        if detail:
            print("     %s" % detail)


def lancer(cmd, timeout=60, **kwargs):
    """Lancer une commande avec la protection (stop si erreur silencieuse)."""
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout, **kwargs)


def lire(chemin):
    with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def compter_non_ascii(texte):
    return sum(1 for c in texte if ord(c) > 127)


def main():
    # --- 1. outils : existent, compilent, version
    if point_actif(1):
        t = time.monotonic()
        ok = os.path.isfile(VERROU_PY) and os.path.isfile(MODIF_PY)
        verifier("1. outils marbre presents", ok,
                 "manquant: %s" % (VERROU_PY if not os.path.isfile(VERROU_PY) else MODIF_PY))
        for outil in (VERROU_PY, MODIF_PY):
            r = lancer([PYTHON, "-m", "py_compile", outil])
            verifier("   compile %s" % os.path.basename(os.path.dirname(outil)),
                     r.returncode == 0, r.stderr[-200:])
        r = lancer([PYTHON, VERROU_PY, "--version"])
        verifier("   verrou --version", "0.1.0" in r.stdout, r.stdout[-100:])
        r = lancer([PYTHON, MODIF_PY, "--version"])
        verifier("   modifier --version", "0.1.3" in r.stdout, r.stdout[-100:])
        chrono_etape("1. outils", t)

    # --- 2. manifeste marbre.json
    if point_actif(2):
        t = time.monotonic()
        ok_json = os.path.isfile(MARBRE_JSON)
        verifier("2. marbre.json present", ok_json, MARBRE_JSON)
        if ok_json:
            try:
                m = json.load(io.open(MARBRE_JSON, encoding="utf-8"))
                zones = list(m.get("zones", {}).keys())
                manquantes = [z for z in ZONES_ATTENDUES if z not in zones]
                verifier("   %d zones attendues presentes" % len(ZONES_ATTENDUES),
                         not manquantes, "manquantes: %s" % manquantes)
                verifier("   chaque zone a une empreinte",
                         all(m["zones"][z].get("empreinte") for z in zones),
                         "zones sans empreinte")
            except ValueError as e:
                verifier("   marbre.json JSON valide", False, str(e))
        chrono_etape("2. manifeste", t)

    # --- 3. etat conforme
    if point_actif(3):
        t = time.monotonic()
        r = lancer([PYTHON, VERROU_PY, "--tous"])
        verifier("3. verrou --tous rc=0 (marbre intact)", r.returncode == 0,
                 "rc=%s stdout=%s" % (r.returncode, r.stdout[-200:]))
        chrono_etape("3. etat conforme", t)

    # --- 4. preuve negative (violation c0) avec restauration garantie
    if point_actif(4):
        t = time.monotonic()
        original = None
        try:
            d = json.load(io.open(CERBERUS_PARCOURS, encoding="utf-8"))
            original = json.dumps(d, ensure_ascii=True, indent=1) + "\n"
            d["cases"]["c0"]["titre"] = "VIOLATION TEST MARBRE"
            with io.open(CERBERUS_PARCOURS, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(json.dumps(d, ensure_ascii=True, indent=1) + "\n")
            r = lancer([PYTHON, VERROU_PY, "--zone", "cerberus.c0"])
            verifier("4. preuve negative : c0 violee -> BLOQUE rc=1",
                     r.returncode == 1 and "BLOQUE" in r.stdout,
                     "rc=%s stdout=%s" % (r.returncode, r.stdout[-200:]))
        finally:
            if original is not None:
                with io.open(CERBERUS_PARCOURS, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(original)
        r = lancer([PYTHON, VERROU_PY, "--tous"])
        verifier("   restauration -> marbre intact", r.returncode == 0,
                 "rc=%s" % r.returncode)
        chrono_etape("4. preuve negative", t)

    # --- 5. porte du marbre : sans autorisation -> BLOQUE
    if point_actif(5):
        t = time.monotonic()
        r = lancer([PYTHON, MODIF_PY, "--zone", "cerberus.c0", "--raison", "test"])
        verifier("5. modifier-marbre SANS autorisation -> rc=1 (IMMUABLE)",
                 r.returncode == 1 and "BLOQUE" in r.stdout,
                 "rc=%s stdout=%s" % (r.returncode, r.stdout[-200:]))
        chrono_etape("5. porte du marbre", t)

    # --- 6. integration avant (outils du noyau verrouilles)
    if point_actif(6):
        t = time.monotonic()
        contenu_activer = lire(ACTIVER_PY)
        contenu_editer = lire(EDITER_PY)
        verifier("6. activer-agent-principal verrouille (constitution)",
                 "verrouiller_constitution" in contenu_activer)
        verifier("   editer-parcours verrouille (cases protegees)",
                 "verifier_cases_protegees" in contenu_editer)
        chrono_etape("6. integration", t)

    # --- 7. catalogue
    if point_actif(7):
        t = time.monotonic()
        try:
            cat = json.load(io.open(CATALOGUE, encoding="utf-8"))
            noms = [c["nom"] for c in cat["commandes"]]
            verifier("7. catalogue : 2 outils marbre declares",
                     "proteger-verrou-marbre" in noms and "proteger-modifier-marbre" in noms,
                     "manquants dans catalogue")
        except (ValueError, IOError) as e:
            verifier("7. catalogue : 2 outils marbre declares", False, str(e))
        chrono_etape("7. catalogue", t)

    # --- 8. index-tools
    if point_actif(8):
        t = time.monotonic()
        idx = lire(INDEX)
        verifier("8. index-tools : 2 outils marbre references",
                 "proteger-verrou-marbre" in idx and "proteger-modifier-marbre" in idx,
                 "manquants dans index-tools")
        chrono_etape("8. index-tools", t)

    # --- 9. normes ASCII + LF
    if point_actif(9):
        t = time.monotonic()
        fichiers = [VERROU_PY, MODIF_PY, MARBRE_JSON, PROTOCOLE,
                    CERBERUS_PARCOURS, ACTIVER_PY, EDITER_PY]
        ok_normes = True
        details = []
        for f in fichiers:
            if not os.path.isfile(f):
                details.append("%s absent" % f)
                ok_normes = False
                continue
            brut = open(f, "rb").read()
            na = compter_non_ascii(brut.decode("utf-8", errors="replace"))
            crlf = brut.count(b"\r\n")
            if na or crlf:
                details.append("%s: %d non-ascii / %d CRLF" % (os.path.basename(f), na, crlf))
                ok_normes = False
        verifier("9. normes ASCII strict + LF pur (7 fichiers)", ok_normes,
                 "; ".join(details))
        chrono_etape("9. normes", t)

    # --- 10. anti-recurrence : les marqueurs survivent a une reactivation
    # (bug 2026-08-15 : la boucle de retrait de la section Sessions connues
    # avalait le marqueur DEBUT de la zone constitution)
    if point_actif(10):
        t = time.monotonic()
        import shutil
        import tempfile
        tmp = None
        tmp_hist = None
        tmp_classeur = None
        try:
            fd, tmp = tempfile.mkstemp(suffix=".md")
            os.close(fd)
            shutil.copyfile(os.path.join(PROJECT_ROOT, "AGENTS.md"), tmp)
            fd2, tmp_hist = tempfile.mkstemp(suffix=".md")
            os.close(fd2)
            fd3, tmp_classeur = tempfile.mkstemp(suffix=".md")
            os.close(fd3)
            shutil.copyfile(os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                         "classeur-variables", "stockage",
                                         "variables-actuelles.md"), tmp_classeur)
            env = dict(os.environ)
            env["AGENTS_FILE"] = tmp
            env["AGENTS_HISTORIQUE"] = tmp_hist
            # Le classeur doit lui aussi etre un fichier TEMP : la reactivation
            # reecrit le profil de session (bug 2026-08-16 : pointer vers le
            # VRAI variables-actuelles.md reecrivait agent: Cerberus pendant
            # la non-regression et cassait test-024 point 2b).
            env["CLASSEUR_STOCKAGE"] = tmp_classeur
            r = lancer([PYTHON, ACTIVER_PY, "reactiver", "session-llm-1",
                        "test marbre", "janus"], timeout=90, env=env)
            contenu = lire(tmp)
            ok_debut = "MARBRE:DEBUT" in contenu
            ok_fin = "MARBRE:FIN" in contenu
            verifier("10. anti-recurrence : marqueurs survivent a une reactivation",
                     r.returncode == 0 and ok_debut and ok_fin,
                     "rc=%s debut=%s fin=%s" % (r.returncode, ok_debut, ok_fin))
        finally:
            if tmp:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
            if tmp_hist:
                try:
                    os.unlink(tmp_hist)
                except OSError:
                    pass
            if tmp_classeur:
                try:
                    os.unlink(tmp_classeur)
                except OSError:
                    pass
        chrono_etape("10. anti-recurrence", t)

    # --- 11. anti-contournement : cartes-lock.json couvre les 14 cartes
    if point_actif(11):
        t = time.monotonic()
        ok_json = os.path.isfile(CARTES_LOCK)
        verifier("11. cartes-lock.json present", ok_json, CARTES_LOCK)
        if ok_json:
            try:
                lock = json.load(io.open(CARTES_LOCK, encoding="utf-8"))
                dict_lock = lock.get("cartes", {})
                cles_lock = set(dict_lock.keys())
                reels = set()
                for p in glob.glob(os.path.join(PROJECT_ROOT, "cerveau-projet",
                                                "agents", "*", "parcours", "parcours-*.json")):
                    rel = os.path.relpath(p, PROJECT_ROOT).replace(os.sep, "/")
                    reels.add(rel)
                manquantes = reels - cles_lock
                verifier("   couvre les %d cartes reelles" % len(reels),
                         not manquantes, "non couvertes: %s" % sorted(manquantes))
                verifier("   chaque carte a une empreinte SHA-256",
                         all(len(dict_lock.get(c, "") or "") == 64 for c in cles_lock),
                         "empreintes invalides")
            except ValueError as e:
                verifier("   cartes-lock.json JSON valide", False, str(e))
        chrono_etape("11. cartes-lock", t)

    # --- 12. anti-contournement : ecriture directe -> editer-parcours BLOQUE
    if point_actif(12):
        t = time.monotonic()
        import shutil
        import tempfile
        carte_test = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "themis",
                                  "parcours", "parcours-themis.json")
        tmp_carte = None
        env = None
        try:
            # copie de travail : editer-parcours calcule son lock relatif a la
            # racine projet, on fait donc la preuve sur la VRAIE carte avec
            # restauration garantie (sauvegarde du contenu original)
            original = lire(carte_test)
            d = json.loads(original)
            d["cases"]["cZZ"] = {"type": "question", "titre": "factice",
                                 "question": "preuve", "indice": "factice"}
            with io.open(carte_test, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(json.dumps(d, ensure_ascii=True, indent=1) + "\n")
            r = lancer([PYTHON, EDITER_PY, "--agent", "themis", "--bump", "--wet"])
            verifier("12. anti-contournement : ecriture directe -> BLOQUE",
                     r.returncode == 1 and "ANTI-CONTOURNEMENT" in r.stdout,
                     "rc=%s stdout=%s" % (r.returncode, r.stdout[-200:]))
        finally:
            with io.open(carte_test, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(original)
        # apres restauration, l empreinte est resynchronisee : l
        # anti-contournement est leve, mais le verrou SEUL BUFFY bloque
        # (l agent actif de la non-regression n est pas buffy).
        r = lancer([PYTHON, EDITER_PY, "--agent", "themis", "--bump", "--dry-run"])
        verifier("   restauration -> anti-contournement leve, verrou SEUL BUFFY bloque",
                 r.returncode == 1 and "ANTI-CONTOURNEMENT" not in r.stdout
                 and "BLOQUE" in r.stdout, "rc=%s" % r.returncode)
        chrono_etape("12. anti-contournement preuve", t)

    # --- 13. --modifier-case : verrou SEUL BUFFY bloque hors buffy
    if point_actif(13):
        t = time.monotonic()
        r = lancer([PYTHON, EDITER_PY, "--agent", "themis", "--modifier-case", "c1",
                    "--contenu", '{"type":"action","titre":"t","texte":"t","indice":"i"}'])
        verifier("13. --modifier-case : verrou SEUL BUFFY bloque (hors buffy)",
                 r.returncode == 1 and "BLOQUE" in r.stdout
                 and "ANTI-CONTOURNEMENT" not in r.stdout,
                 "rc=%s stdout=%s" % (r.returncode, r.stdout[-200:]))
        chrono_etape("13. modifier-case", t)

    bilan_chrono()
    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("VERDICT : %s" % ("CONFORME" if NB_KO == 0 else "NON CONFORME"))
    print("BILAN : marbre intact si 0 KO (zones protegees conformes au manifeste)")
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
