#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-113-anti-heredoc-formulaire-garde-fou.py

GARDE-FOU ANTI-HEREDOC + FORMULAIRE D6/D7 + INJECTION OUTIL P2
(decisions utilisateur 2026-08-21 D6/D7 et 2026-09-02 P2 via Socrate) :

A. MODE ANTI-HEREDOC des outils simples : creer-fichier, ecrire-fichier et
   editer-fichier doivent lire le contenu/remplacements depuis un FICHIER
   (jamais de ligne bash geante). Un contenu de plusieurs Ko passe sans
   troncature. Patron : ajouter/inserer --fichier SOURCE (deja present).
B. OUTIL = FORMULAIRE (executer-formulaire v0.1.0) : --schema affiche la
   mini-description + la liste des champs/flags depuis le catalogue ;
   --reponses <fichier.json> valide (refus AVANT execution si requis
   manquant, RC=1) puis compose et execute la commande a la place de
   l agent (D6) ; --dry-run montre la commande composee sans executer.
C. INJECTION OUTIL (P2) : files.py injecte dans la mission un bloc
   [OUTIL] (description + flags) pour chaque outil du catalogue mentionne
   (max 3), et ne touche pas une mission sans outil.

Points verifies :
  1. creer-fichier --contenu-chemin ecrit un contenu long (5 Ko) sans
     troncature (RC=0, contenu identique ecrit).
  2. ecrire-fichier --contenu-chemin ecrit le contenu long (RC=0).
  3. editer-fichier --remplacements-chemin applique plusieurs remplacements
     depuis un fichier JSON (RC=0, les 2 remplacements sont dans le fichier).
  4. executer-formulaire --outil creer-fichier --schema affiche la
     mini-description + le champ REQUIS.
  5. executer-formulaire --outil creer-fichier --reponses invalide (requis
     manquant) -> RC=1, refus AVANT execution (fichier cible ABSENT).
  6. executer-formulaire --outil creer-fichier --reponses valide -> RC=0 et
     fichier cible cree avec le contenu fourni (execution automatique D6).
  7. executer-formulaire --dry-run compose la commande sans executer
     (fichier cible ABSENT).
  8. Injection P2 : une mission mentionnant creer-fichier recoit le bloc
     [OUTIL] avec la mini-description et les flags.
  9. Injection P2 : une mission sans outil n est pas modifiee.
  10. Nettoyage : aucun residu tmp (dossier tmp-hef-* supprime).
  11. Normes : ASCII strict + LF pur (outils + test).

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: anti-heredoc, formulaire, D6, D7, executer-formulaire, injection-outil, P2, vulcain
"""
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

CERVEau = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEau, "agents", "tools")
PYTHON = sys.executable

CREER_PY = os.path.join(TOOLS_DIR, "creer", "creer-fichier", "creer-fichier.py")
ECRIRE_PY = os.path.join(TOOLS_DIR, "ecrire", "ecrire-fichier", "ecrire-fichier.py")
EDITER_PY = os.path.join(TOOLS_DIR, "editer", "editer-fichier", "editer-fichier.py")
FORMULAIRE_PY = os.path.join(TOOLS_DIR, "executer", "executer-formulaire",
                             "executer-formulaire.py")

# Dossier de travail isole pour les fixtures (jamais dans le cerveau).
TMP_BASE = os.path.join(tempfile.gettempdir(), "tmp-hef-test-113")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for i, arg in enumerate(sys.argv):
    if arg == "--isoler" and i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[i + 1])
        except ValueError:
            ISOLE = None
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        DESACTIVES = [int(x) for x in sys.argv[i + 1].split(",")
                      if x.strip().isdigit()]

DEBUT_TEST = time.monotonic()
ETAPES = []


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def point_actif(numero):
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    if CHRONO_ACTIF:
        ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - DEBUT_TEST
    print("")
    print("=== CHRONO test (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-34s %6.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(cmd, timeout=60):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace",
                                      timeout=timeout, cwd=PROJECT_ROOT)


def _ecrire(chemin, contenu):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)


def _lire(chemin):
    try:
        with io.open(chemin, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def _nettoyer():
    shutil.rmtree(TMP_BASE, ignore_errors=True)


def _contenu_long():
    return "\n".join("ligne-%d: contenu long anti-heredoc %s"
                     % (i, "x" * 200) for i in range(30))


def _egal_contenu(lus, attendu):
    """Les outils ajoutent un newline final (comportement historique de
    creer/ecrire-fichier) : comparer apres rstrip, sans perdre de contenu."""
    return lus.rstrip("\n") == attendu


def point_1_creer_chemin():
    base = os.path.join(TMP_BASE, "creer")
    _ecrire(os.path.join(base, "source.txt"), _contenu_long())
    cible = os.path.join(base, "cible.md")
    r = run([PYTHON, CREER_PY, cible, "--contenu-chemin",
             os.path.join(base, "source.txt")])
    ok = (r.returncode == 0 and _egal_contenu(_lire(cible), _contenu_long()))
    verifier("1. creer-fichier --contenu-chemin ecrit le contenu long", ok,
             "RC=%d" % r.returncode)


def point_2_ecrire_chemin():
    base = os.path.join(TMP_BASE, "ecrire")
    _ecrire(os.path.join(base, "source.txt"), _contenu_long())
    cible = os.path.join(base, "cible.md")
    r = run([PYTHON, ECRIRE_PY, cible, "--contenu-chemin",
             os.path.join(base, "source.txt")])
    ok = (r.returncode == 0 and _egal_contenu(_lire(cible), _contenu_long()))
    verifier("2. ecrire-fichier --contenu-chemin ecrit le contenu long", ok,
             "RC=%d" % r.returncode)


def point_3_editer_remplacements():
    base = os.path.join(TMP_BASE, "editer")
    cible = os.path.join(base, "cible.md")
    _ecrire(cible, "old-one\nligne\nold-two\n")
    specs = os.path.join(base, "specs.json")
    _ecrire(specs, json.dumps([
        {"ancien": "old-one", "nouveau": "NEW-UN"},
        {"ancien": "old-two", "nouveau": "NEW-DEUX"},
    ], ensure_ascii=True))
    r = run([PYTHON, EDITER_PY, cible, "--remplacements-chemin", specs])
    contenu = _lire(cible)
    ok = (r.returncode == 0 and "NEW-UN" in contenu and "NEW-DEUX" in contenu
          and "old-1" not in contenu)
    verifier("3. editer-fichier --remplacements-chemin applique les 2 remplacements",
             ok, "RC=%d contenu=%r" % (r.returncode, contenu[:60]))


def point_4_schema():
    r = run([PYTHON, FORMULAIRE_PY, "--outil", "creer-fichier", "--schema"])
    sortie = (r.stdout or "") + (r.stderr or "")
    ok = (r.returncode == 0 and "FORMULAIRE" in sortie
          and "Creer un nouveau fichier" in sortie
          and "REQUIS" in sortie)
    verifier("4. --schema affiche description + champs REQUIS", ok,
             "RC=%d" % r.returncode)


def point_5_refus_avant_execution():
    base = os.path.join(TMP_BASE, "invalide")
    cible = os.path.join(base, "cible.md")
    reponses = os.path.join(base, "reponses.json")
    _ecrire(reponses, json.dumps({"fichier": cible}, ensure_ascii=True))
    r = run([PYTHON, FORMULAIRE_PY, "--outil", "creer-fichier",
             "--reponses", reponses])
    ok = (r.returncode == 1 and not os.path.exists(cible)
          and "refus avant execution" in ((r.stdout or "") + (r.stderr or "")))
    verifier("5. reponses invalides -> refus AVANT execution (RC=1, cible absente)",
             ok, "RC=%d" % r.returncode)


def point_6_execution_reelle():
    base = os.path.join(TMP_BASE, "valide")
    cible = os.path.join(base, "cible.md")
    contenu = _contenu_long()
    reponses = os.path.join(base, "reponses.json")
    _ecrire(reponses, json.dumps({"fichier": cible, "contenu": contenu,
                                  "forcer": False}, ensure_ascii=True))
    r = run([PYTHON, FORMULAIRE_PY, "--outil", "creer-fichier",
             "--reponses", reponses])
    ok = (r.returncode == 0 and _egal_contenu(_lire(cible), contenu))
    verifier("6. formulaire valide -> execution automatique (fichier cree)", ok,
             "RC=%d" % r.returncode)


def point_7_dry_run():
    base = os.path.join(TMP_BASE, "dryrun")
    cible = os.path.join(base, "cible.md")
    reponses = os.path.join(base, "reponses.json")
    _ecrire(reponses, json.dumps({"fichier": cible, "contenu": "x",
                                  "forcer": False}, ensure_ascii=True))
    r = run([PYTHON, FORMULAIRE_PY, "--outil", "creer-fichier",
             "--reponses", reponses, "--dry-run"])
    ok = (r.returncode == 0 and "creer-fichier.py" in (r.stdout or "")
          and not os.path.exists(cible))
    verifier("7. --dry-run compose la commande sans l executer", ok,
             "RC=%d cible_exists=%s" % (r.returncode, os.path.exists(cible)))


def _injecter_bloc_outil(mission):
    """Charger files.py et appeler injecter_bloc_outil (test P2)."""
    chemin = os.path.join(TOOLS_DIR, "oracle", "fonctions", "files.py")
    spec = importlib.util.spec_from_file_location("oracle_files_p2", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.injecter_bloc_outil(mission)


def point_8_injection():
    mission = "Creer le fichier rapport.md avec creer-fichier puis le lire"
    res = _injecter_bloc_outil(mission)
    ok = ("[OUTIL] creer-fichier --" in res
          and "Flags" in res
          and "REQUIS" in res)
    verifier("8. injection P2 : bloc [OUTIL] description + flags dans la mission",
             ok, res[-200:])


def point_9_injection_sans_outil():
    mission = "Coordination pure sans aucun outil d ecriture"
    res = _injecter_bloc_outil(mission)
    verifier("9. injection P2 : mission sans outil NON modifiee", res == mission,
             res[-200:])


def point_10_cleanup():
    _nettoyer()
    verifier("10. aucun residu tmp-hef-*", not os.path.exists(TMP_BASE))


def point_11_normes():
    fichiers = [CREER_PY, ECRIRE_PY, EDITER_PY, FORMULAIRE_PY,
                os.path.abspath(__file__)]
    total_non_ascii = 0
    total_crlf = 0
    for f in fichiers:
        data = open(f, "rb").read()
        total_non_ascii += len([c for c in data if c > 127])
        total_crlf += data.count(b"\r\n")
    ok = total_non_ascii == 0 and total_crlf == 0
    verifier("11. ASCII strict + LF pur (outils + test)", ok,
             "non_ascii=%d crlf=%d" % (total_non_ascii, total_crlf))


def main():
    print("=== test-113 : anti-heredoc + formulaire D6/D7 + injection P2 ===")

    points = [
        ("1. creer-fichier chemin", point_1_creer_chemin),
        ("2. ecrire-fichier chemin", point_2_ecrire_chemin),
        ("3. editer remplacements", point_3_editer_remplacements),
        ("4. schema formulaire", point_4_schema),
        ("5. refus avant execution", point_5_refus_avant_execution),
        ("6. execution automatique", point_6_execution_reelle),
        ("7. dry-run", point_7_dry_run),
        ("8. injection P2", point_8_injection),
        ("9. injection sans outil", point_9_injection_sans_outil),
        ("10. cleanup", point_10_cleanup),
        ("11. normes", point_11_normes),
    ]
    for num, (nom, fn) in enumerate(points, start=1):
        if not point_actif(num):
            continue
        t_debut = time.monotonic()
        fn()
        chrono_etape(nom, t_debut)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())