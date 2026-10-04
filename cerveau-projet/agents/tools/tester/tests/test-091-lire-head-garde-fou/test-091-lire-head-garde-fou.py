#!/usr/bin/env python3
# -*- coding: ascii -*-
"""test-091-lire-head-garde-fou.py
GARDE-FOU : l'outil lire-head (categorie lire) lit le head (en-tete) d'un
fichier SANS configurer le nombre de lignes : il detecte automatiquement la
fin du head (front-matter YAML, bloc de commentaires, ou premiere ligne
vide, borne --max-lignes 100) et compare plusieurs heads avec
--info-commune MOTIF (PRESENT/ABSENT par fichier).

Contexte (2026-08-18, demande utilisateur) : lire le debut de n'importe
quel fichier sans savoir combien de lignes fait le head, et reperer le
fichier pas a jour parmi plusieurs (information commune manquante).

Invariants verifies :
  1. L'outil existe et compile.
  2. --version v0.1.1 (py + sh parite).
  3. Detection front-matter YAML : fichier .md -> le head s arrete a la
     ligne de fermeture '---'.
  4. Detection bloc de commentaires : fichier .py -> le head couvre le
     bloc d en-tete commente.
  5. Detection premiere ligne vide : fichier sans front-matter -> le head
     va jusqu a la premiere ligne vide.
  6. --lignes N force le nombre de lignes (derogation).
  7. --info-commune present : le motif est trouve (PRESENT + lignes).
  8. --info-commune absent (PREUVE NEGATIVE) : un fichier sans le motif
     est signale ABSENT (reperer le fichier pas a jour).
  9. Fichier introuvable -> code 1.
  10. --dry-run affiche la liste sans lire les fichiers.
  11. Parite .sh : meme version + lecture identique.
  12. Normes : ASCII strict + LF pur (outil + doc + test).

Tags: outils, lecture, garde-fou, preuve-negative
"""
import importlib.util
import io
import os
import py_compile
import subprocess
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

OUTIL_DIR = os.path.join(TOOLS_DIR, "lire", "lire-head")
OUTIL_PY = os.path.join(OUTIL_DIR, "lire-head.py")
OUTIL_SH = os.path.join(OUTIL_DIR, "lire-head.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "lire-head.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

# --- options ON/OFF + chrono ---
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
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-091 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  %-38s %6.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
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


def lancer(cmd, timeout=90):
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with io.open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def ecrire(chemin, contenu):
    with io.open(chemin, "w", encoding="ascii", newline="") as fh:
        fh.write(contenu)


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== Garde-fou : lire-head (lecture automatique du head) ===")

    tmp = tempfile.mkdtemp(prefix="tmp-test091-")
    try:
        # Fichiers temoins (ASCII pur, LF ecrit via newline="")
        fm = os.path.join(tmp, "frontmatter.md")
        ecrire(fm, "---\nidentite:\n  type: outil\n  commun: true\n---\n\n"
                   "# Titre\n\ncontenu apres le head.\n")
        com = os.path.join(tmp, "commentaires.py")
        ecrire(com, "#!/usr/bin/env python3\n# -*- coding: ascii -*-\n"
                    "# identite:\n#   type: outil\n#   commun: true\n\n"
                    "print('hello')\n")
        texte = os.path.join(tmp, "texte.md")
        ecrire(texte, "# Titre\n\nparagraphe apres la ligne vide.\n")
        interdit = os.path.join(tmp, "sans-info.md")
        ecrire(interdit, "---\nversion: 1.0\n---\n\n# Autre\n")

        # 1. outil present + compile.
        if point_actif(1):
            t = time.monotonic()
            ok = os.path.isfile(OUTIL_PY) and os.path.isfile(OUTIL_MD)
            try:
                py_compile.compile(OUTIL_PY, doraise=True)
            except Exception:
                ok = False
            verifier("1. outil present + compile", ok)
            chrono_etape("1. outil", t)

        # 2. --version py + parite sh.
        if point_actif(2):
            t = time.monotonic()
            r1 = lancer([PYTHON, OUTIL_PY, "--version"])
            r2 = lancer(["bash", OUTIL_SH, "--version"])
            verifier("2. --version v0.1.1 (py + sh parite)",
                     r1.returncode == 0 and "v0.1.1" in r1.stdout
                     and r2.returncode == 0 and "v0.1.1" in r2.stdout,
                     "%s / %s" % (r1.stdout.strip(), r2.stdout.strip()))
            chrono_etape("2. version", t)

        # 3. detection front-matter YAML : le head s arrete a la fermeture.
        if point_actif(3):
            t = time.monotonic()
            r = lancer([PYTHON, OUTIL_PY, fm])
            sortie = r.stdout
            ok = (r.returncode == 0
                  and "---" in sortie and "type: outil" in sortie
                  and "paragraphe" not in sortie)
            verifier("3. front-matter YAML detecte (head sans le corps)",
                     ok, sortie[-200:])
            chrono_etape("3. front-matter", t)

        # 4. detection bloc de commentaires : head = en-tete commente.
        if point_actif(4):
            t = time.monotonic()
            r = lancer([PYTHON, OUTIL_PY, com])
            sortie = r.stdout
            ok = (r.returncode == 0
                  and "identite:" in sortie and "type: outil" in sortie
                  and "print(" not in sortie)
            verifier("4. bloc de commentaires detecte (sans le code)",
                     ok, sortie[-200:])
            chrono_etape("4. commentaires", t)

        # 5. detection premiere ligne vide : head = titre avant la ligne vide.
        if point_actif(5):
            t = time.monotonic()
            r = lancer([PYTHON, OUTIL_PY, texte])
            sortie = r.stdout
            ok = (r.returncode == 0 and "# Titre" in sortie
                  and "paragraphe" not in sortie)
            verifier("5. premiere ligne vide (titre seul, sans la suite)",
                     ok, sortie[-200:])
            chrono_etape("5. ligne vide", t)

        # 6. --lignes N force le nombre de lignes.
        if point_actif(6):
            t = time.monotonic()
            r = lancer([PYTHON, OUTIL_PY, "--lignes", "2", com])
            sortie = r.stdout
            ok = (r.returncode == 0 and "shebang" not in sortie
                  and "# -*- coding" in sortie)
            verifier("6. --lignes 2 : uniquement les 2 premieres lignes",
                     ok, sortie[-200:])
            chrono_etape("6. lignes forcees", t)

        # 7. --info-commune present (comparaison).
        if point_actif(7):
            t = time.monotonic()
            r = lancer([PYTHON, OUTIL_PY, fm, com, "--info-commune",
                        "commun: true"])
            sortie = r.stdout
            ok = (r.returncode == 0 and "PRESENT" in sortie
                  and "ABSENT" not in sortie
                  and "Tous les heads contiennent" in sortie)
            verifier("7. --info-commune present : PRESENT partout",
                     ok, sortie[-250:])
            chrono_etape("7. info presente", t)

        # 8. PREUVE NEGATIVE : un fichier sans l info = ABSENT (pas a jour).
        if point_actif(8):
            t = time.monotonic()
            r = lancer([PYTHON, OUTIL_PY, fm, interdit, "--info-commune",
                        "identite:"])
            sortie = r.stdout
            ok = (r.returncode == 0 and "PRESENT" in sortie
                  and "ABSENT" in sortie
                  and "fichier probablement pas a jour" in sortie)
            verifier("8. PREUVE NEGATIVE : fichier sans l info = ABSENT",
                     ok, sortie[-250:])
            chrono_etape("8. preuve negative", t)

        # 9. fichier introuvable -> code 1.
        if point_actif(9):
            t = time.monotonic()
            absent = os.path.join(tmp, "n-existe-pas.md")
            r = lancer([PYTHON, OUTIL_PY, absent])
            verifier("9. fichier introuvable -> code 1 + message",
                     r.returncode == 1 and "Fichier non trouve" in r.stdout,
                     "rc=%s %s" % (r.returncode, r.stdout.strip()[-100:]))
            chrono_etape("9. introuvable", t)

        # 10. --dry-run : liste les fichiers sans lire le contenu.
        if point_actif(10):
            t = time.monotonic()
            r = lancer([PYTHON, OUTIL_PY, "--dry-run", fm, texte])
            sortie = r.stdout
            ok = (r.returncode == 0 and "DRY-RUN" in sortie
                  and "Titre" not in sortie)
            verifier("10. --dry-run : liste sans lire le contenu", ok,
                     sortie[-200:])
            chrono_etape("10. dry-run", t)

        # 11. parite .sh : meme lecture (front-matter).
        if point_actif(11):
            t = time.monotonic()
            r = lancer(["bash", OUTIL_SH, fm])
            sortie = r.stdout
            ok = (r.returncode == 0 and "type: outil" in sortie
                  and "paragraphe" not in sortie)
            verifier("11. parite .sh : lecture front-matter identique", ok,
                     sortie[-200:])
            chrono_etape("11. parite sh", t)

        # 12. normes.
        if point_actif(12):
            t = time.monotonic()
            fichiers = [OUTIL_PY, OUTIL_SH, OUTIL_MD,
                        os.path.abspath(__file__)]
            na = sum(ascii_count(f) for f in fichiers)
            crlf = sum(crlf_count(f) for f in fichiers)
            verifier("12. ASCII strict : 0 non-ASCII (outil + doc + test)",
                     na == 0, "total=%d" % na)
            verifier("12b. LF pur : 0 CRLF (outil + doc + test)",
                     crlf == 0, "total=%d" % crlf)
            chrono_etape("12. normes", t)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)

    print("")
    bilan_chrono()
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    PROTECTIONS.afficher_rating("test-091-lire-head-garde-fou")
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
