#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-077-detecter-troncatures.py
GARDE-FOU : l outil detecter-troncatures (v0.2.0, demande utilisateur
2026-08-16, round amelioration) detecte les elements tronques donc
illisibles : fichiers trop longs a lire (FICHIER_TROUQUE), blocs non
fermes (BLOC_NON_FERME : JSON/Python/bash invalides = un fichier tronque
ne compile pas), marqueurs de troncature dans le CONTENU reel
(MARQUEUR_TRONCATURE : [tronque], [cut], [truncated], 'coupe ici',
'contenu tronque').

Contexte :
  - Outil cree par Vulcain apres le bug des fichiers illisibles : la 1ere
    version comptait naivement les delimiteurs (texte.count) et produisait
    355 faux positifs (codes ANSI, chaines, regex). La methode fiable est
    structurelle : json.loads / compile / bash -n.
  - v0.2.0 (round amelioration) : binaires ignores (octets NUL), option
    --exclure, marqueurs des zones de DOCUMENTATION ignores (docstrings,
    blocs de code, commentaires, citations, lignes qui documentent le
    motif) - documenter un marqueur n est pas etre tronque.

Invariants verifies (fichiers temp, jamais le vrai depot) :
  1. detecter-troncatures --version = 0.2.0
  2. L option --tous, --seuil-lignes et --exclure sont presentes dans --aide.
  3. PREUVE RELLE : fichier sain -> PROPRE (0 probleme).
  4. Fichier long (> seuil) -> FICHIER_TROUQUE detecte.
  5. JSON invalide -> BLOC_NON_FERME detecte (fichier tronque ne compile pas).
  6. Marqueur litteral [tronque] -> MARQUEUR_TRONCATURE detecte.
  6b. BINAIRE (octets NUL) -> PROPRE (v0.2.0 : un binaire n a pas de lignes).
  6c. Marqueur cite dans une docstring Python -> NON detecte (zone doc).
  7. PREUVE NEGATIVE : sans marqueur = PROPRE, apres injection d un marqueur
     = detecte (garde-fou anti-recurrence : si l outil ne detectait pas,
     le test KO).
  7b. --exclure <motif> exclut reellement un fichier cible (v0.2.0).
  8. --rapport ecrit le rapport markdown (fichier cree).
  9. Parite .sh : --version identique (0.2.0).
 10. Le dossier temp est SUPPRIME en fin de test (0 trace).
 11. Normes : ASCII strict + LF pur (test + outil py/sh/md).
Tags: outils, detecter, troncatures, garde-fou
"""
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

OUTIL_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                         "detecter", "detecter-troncatures")
OUTIL_PY = os.path.join(OUTIL_DIR, "detecter-troncatures.py")
OUTIL_SH = os.path.join(OUTIL_DIR, "detecter-troncatures.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "detecter-troncatures.md")

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []
NB_OK = 0
NB_KO = 0
NB_POINTS = 15


def point_actif(numero):
    return True


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO test-077 (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  [chrono] %-35s %.2fs" % (nom, duree))


def verifier(nom, condition, detail=""):
    global NB_OK, NB_KO
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s -- %s" % (nom, str(detail)[-100:]))


def charger_protections():
    chemin = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                          "tester", "tester-protections", "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def run(cmd, timeout=120):
    # PROTECTION : toute execution passe par lancer_protege (jamais de
    # subprocess.run brut - test-030 verifie cette regle).
    try:
        r = PROTECTIONS.lancer_protege(cmd, timeout=timeout,
                                       capture_output=True, text=True)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, "ERREUR: %s" % str(e)[-80:]


def compter_non_ascii(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for ch in fh.read() if ord(ch) > 127)


def main():
    print("=== Garde-fou : detecter-troncatures v0.2.0 (elements tronques / illisibles) ===")

    # 1. Version 0.2.0
    t0 = time.monotonic()
    code, out = run([sys.executable, OUTIL_PY, "--version"])
    verifier("1. --version = 0.2.0",
             code == 0 and "0.2.0" in out, out.strip()[-40:])
    chrono_etape("1. version", t0)

    # 2. Options --tous, --seuil-lignes et --exclure presentes dans --aide
    t0 = time.monotonic()
    code, out = run([sys.executable, OUTIL_PY, "--aide"])
    verifier("2. --aide liste --tous, --seuil-lignes et --exclure",
             "--tous" in out and "--seuil-lignes" in out and "--exclure" in out,
             out[-160:] if ("--tous" not in out or "--seuil-lignes" not in out or "--exclure" not in out) else "")
    chrono_etape("2. option --aide", t0)

    tmp = tempfile.mkdtemp(prefix="tmp-test077-")
    try:
        # 3. PREUVE RELLE : fichier sain -> PROPRE
        t0 = time.monotonic()
        sain = os.path.join(tmp, "sain.md")
        with io.open(sain, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("ligne 1\nligne 2\nligne 3\n")
        code, out = run([sys.executable, OUTIL_PY, sain])
        verifier("3. fichier sain -> PROPRE (0 probleme)",
                 code == 0 and "PROPRE" in out,
                 "rc=%d out=%s" % (code, out[-80:]))
        chrono_etape("3. fichier sain", t0)

        # 4. Fichier long (> seuil) -> FICHIER_TROUQUE
        t0 = time.monotonic()
        longf = os.path.join(tmp, "long.md")
        with io.open(longf, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join("ligne %d" % i for i in range(10)) + "\n")
        code, out = run([sys.executable, OUTIL_PY, longf, "--seuil-lignes", "5"])
        # rc=1 = problemes detectes (comportement prevu de l outil)
        verifier("4. fichier 10 lignes (seuil 5) -> FICHIER_TROUQUE",
                 code in (0, 1) and "FICHIER_TROUQUE" in out,
                 "rc=%d out=%s" % (code, out[-80:]))
        chrono_etape("4. fichier long", t0)

        # 5. JSON invalide -> BLOC_NON_FERME
        t0 = time.monotonic()
        badjson = os.path.join(tmp, "bad.json")
        with io.open(badjson, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("{ pas un json valide")
        code, out = run([sys.executable, OUTIL_PY, badjson])
        verifier("5. JSON invalide -> BLOC_NON_FERME",
                 code in (0, 1) and "BLOC_NON_FERME" in out,
                 "rc=%d out=%s" % (code, out[-80:]))
        chrono_etape("5. json invalide", t0)

        # 6. Marqueur litteral -> MARQUEUR_TRONCATURE
        t0 = time.monotonic()
        marq = os.path.join(tmp, "marq.md")
        with io.open(marq, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("contenu\n[tronque] ici le reste manque\n")
        code, out = run([sys.executable, OUTIL_PY, marq])
        verifier("6. marqueur [tronque] -> MARQUEUR_TRONCATURE",
                 code in (0, 1) and "MARQUEUR_TRONCATURE" in out,
                 "rc=%d out=%s" % (code, out[-80:]))
        chrono_etape("6. marqueur", t0)

        # 6b. BINAIRE (octets NUL) -> PROPRE (v0.2.0)
        t0 = time.monotonic()
        binf = os.path.join(tmp, "image.bin")
        with open(binf, "wb") as fh:
            fh.write(b"\x00\x01\x02\x03image binaire sans lignes lisibles\x00\x00\n" * 3000)
        code, out = run([sys.executable, OUTIL_PY, binf])
        verifier("6b. binaire (octets NUL) -> PROPRE (v0.2.0)",
                 code == 0 and "PROPRE" in out,
                 "rc=%d out=%s" % (code, out[-80:]))
        chrono_etape("6b. binaire", t0)

        # 6c. Marqueur cite dans une docstring Python -> NON detecte (zone doc)
        t0 = time.monotonic()
        docpy = os.path.join(tmp, "doc.py")
        with io.open(docpy, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\"\"\"" + "\n" + "Documente les marqueurs : [tronque], coupe ici." + "\n" + "\"\"\"" + "\n" + "x = 1\n")
        code, out = run([sys.executable, OUTIL_PY, docpy])
        verifier("6c. marqueur cite dans une docstring -> NON detecte",
                 code == 0 and "PROPRE" in out,
                 "rc=%d out=%s" % (code, out[-80:]))
        chrono_etape("6c. docstring", t0)

        # 7. PREUVE NEGATIVE : sans marqueur = PROPRE, apres injection = detecte
        t0 = time.monotonic()
        neg = os.path.join(tmp, "neg.md")
        with io.open(neg, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("contenu sain\n")
        code, out = run([sys.executable, OUTIL_PY, neg])
        propre_avant = "PROPRE" in out
        with io.open(neg, "a", encoding="utf-8", newline="\n") as fh:
            fh.write("coupe ici - le rapport est incomplet\n")
        code, out = run([sys.executable, OUTIL_PY, neg])
        detecte_apres = "MARQUEUR_TRONCATURE" in out
        verifier("7. preuve negative : sans marqueur PROPRE, avec marqueur detecte",
                 propre_avant and detecte_apres,
                 "avant=%s apres=%s" % (propre_avant, detecte_apres))
        chrono_etape("7. preuve negative", t0)

        # 8. --rapport ecrit le rapport markdown
        t0 = time.monotonic()
        rapport = os.path.join(tmp, "rapport.md")
        code, out = run([sys.executable, OUTIL_PY, sain, "--rapport", rapport])
        ecrit = os.path.isfile(rapport) and os.path.getsize(rapport) > 0
        verifier("8. --rapport ecrit le rapport markdown",
                 code in (0, 1) and ecrit, "rc=%d ecrit=%s" % (code, ecrit))
        chrono_etape("8. rapport", t0)

        # 7b. --exclure <motif> exclut reellement un fichier cible (v0.2.0)
        #    Dossier DEDIE (les fichiers des points 3-7 ont deja des marqueurs)
        t0 = time.monotonic()
        dossier_excl = os.path.join(tmp, "dedie-excl")
        os.makedirs(dossier_excl, exist_ok=True)
        exclu = os.path.join(dossier_excl, "cache", "rapport.md")
        os.makedirs(os.path.dirname(exclu), exist_ok=True)
        with io.open(exclu, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("contenu\n[tronque] le reste manque\n")
        sain_excl = os.path.join(dossier_excl, "sain.md")
        with io.open(sain_excl, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("ligne saine\n")
        # sans --exclure : le marqueur est DETECTE (rc=1)
        code, out = run([sys.executable, OUTIL_PY, dossier_excl])
        detecte_sans_excl = code in (0, 1) and "MARQUEUR_TRONCATURE" in out
        # avec --exclure cache : le fichier marque est EXCLU -> PROPRE (rc=0)
        code, out = run([sys.executable, OUTIL_PY, dossier_excl, "--exclure", "cache"])
        propre_avec_excl = code == 0 and "PROPRE" in out
        verifier("7b. --exclure exclut reellement la cible (detecte sans, PROPRE avec)",
                 detecte_sans_excl and propre_avec_excl,
                 "sans=%s avec=%s rc=%d" % (detecte_sans_excl, propre_avec_excl, code))
        chrono_etape("7b. exclure", t0)

        # 9. Parite .sh : --version identique
        t0 = time.monotonic()
        code, out = run(["bash", OUTIL_SH, "--version"])
        verifier("9. parite .sh : --version = 0.2.0",
                 code == 0 and "0.2.0" in out, out.strip()[-40:])
        chrono_etape("9. parite sh", t0)
    finally:
        # 10. Purge : le dossier temp est SUPPRIME (0 trace)
        t0 = time.monotonic()
        shutil.rmtree(tmp, ignore_errors=True)
        verifier("10. dossier temp SUPPRIME en fin de test (0 trace)",
                 not os.path.exists(tmp), "residu : %s" % tmp)
        chrono_etape("10. purge", t0)

    # 11. Normes ASCII + LF (test + outil py/sh/md)
    t0 = time.monotonic()
    na_total = 0
    crlf_total = 0
    for f in [os.path.abspath(__file__), OUTIL_PY, OUTIL_SH, OUTIL_MD]:
        d = io.open(f, encoding="utf-8", errors="replace").read()
        na_total += sum(1 for ch in d if ord(ch) > 127)
        b = io.open(f, "rb").read()
        crlf_total += b.count(b"\r\n")
    verifier("11. normes : 0 non-ASCII (test + outil py/sh/md)",
             na_total == 0, "non-ascii=%d" % na_total)
    verifier("11b. normes : 0 CRLF (test + outil py/sh/md)",
             crlf_total == 0, "crlf=%d" % crlf_total)
    chrono_etape("11. normes", t0)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    print("=== VERDICT : %s ===" % (
        "PROPRE (detecter-troncatures verrouille)" if NB_KO == 0 else "KO A CORRIGER"))
    return 0 if NB_KO == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
