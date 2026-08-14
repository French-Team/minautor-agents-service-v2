#!/usr/bin/env python3
# -*- coding: ascii -*-
# executer-script-temporaire.py
# ENTONNOIR : point d entree unique pour l execution des scripts temporaires.
# L agent passe son script par l entonnoir au lieu de lancer python3 direct :
#   1. NORMALISE automatiquement (BOM retire, CRLF -> LF, accents corriges
#      via le dictionnaire de corriger-dictionnaire-accents) - transparent
#      pour l agent : il n a pas a penser a la conformite.
#   2. CONTROLE systematiquement (compilation Python) avant execution.
#   3. EXECUTE le script avec les arguments fournis.
# Si le script est deja conforme, l entonnoir l execute tel quel (0 modif).
#
# Usage :
#   python3 executer-script-temporaire.py <script.py> [args...]
#   python3 executer-script-temporaire.py --dry-run <script.py> [args...]
#   python3 executer-script-temporaire.py --version
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

import argparse
import io
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

VERSION = "0.1.0"
STATUT = "ebauche"

# GARDE-FOU ANTI-RESIDUS : fichiers nommes comme des versions semver pures a
# la racine (ex: 0.2.1, v0.2.6) - residus probables de redirections
# accidentelles de sortie d une commande precedente.
import re
REGEX_RESIDU = re.compile(r"^(v?\d+\.\d+(\.\d+)?)$")


# Couleurs ANSI (desactivees si la sortie n est pas un terminal)
if sys.stdout.isatty():
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    NC = "\033[0m"
else:
    RED = GREEN = YELLOW = NC = ""


def verifier_nommage():
    """Regle immuable : le nom du fichier doit commencer par le prefixe du dossier de categorie."""
    nom = Path(__file__).name
    dossier = Path(__file__).resolve().parent.name
    if not nom.startswith(dossier):
        print(RED + "[ERREUR] Nommage invalide : le fichier doit commencer par '" + dossier + "'" + NC)
        print("  Nom actuel : " + nom)
        sys.exit(2)


def verifier_residus_racine():
    """GARDE-FOU ANTI-RESIDUS : detecter dans le repertoire courant les fichiers
    nommes comme des versions semver pures (ex: 0.2.1, v0.2.6). Ces fichiers
    sont des residus probables de redirections accidentelles de sortie d une
    commande precedente. Anti-residu : les supprimer - les sources de verite
    de version vivent dans cerveau-projet/agents/clio/, JAMAIS a la racine."""
    try:
        residus = sorted(n for n in os.listdir(".")
                         if os.path.isfile(n) and REGEX_RESIDU.match(n))
    except OSError:
        return
    if not residus:
        return
    print("=" * 60)
    print("!!! WARNING GARDE-FOU (v%s) !!!" % VERSION)
    print("Des fichiers nommes comme des versions semver sont presents dans le")
    print("repertoire courant (residus probables de redirections accidentelles")
    print("de sortie) :")
    for n in residus[:10]:
        print("    - %s" % n)
    print("ANTI-RESIDU : supprimez-les. Les sources de verite de version vivent")
    print("dans cerveau-projet/agents/clio/ (version-readme.txt,")
    print("statut-projet.txt), JAMAIS a la racine.")
    print("=" * 60)


def chemin_dictionnaire():
    """Chemin vers le dictionnaire d accents de corriger-dictionnaire-accents."""
    base = Path(__file__).resolve().parent.parent.parent / "corriger" / "corriger-dictionnaire-accents"
    return base / "corriger-dictionnaire-accents.txt"


def lire_dictionnaire(dict_file):
    """Lire le dictionnaire (lignes 'accent|remplacement', ignorer # et vides)."""
    replacements = []
    try:
        with io.open(str(dict_file), encoding="utf-8") as df:
            for line in df:
                line = line.rstrip("\n").rstrip("\r")
                if not line or line.startswith("#"):
                    continue
                if "|" in line:
                    accent, repl = line.split("|", 1)
                    if accent:
                        replacements.append((accent, repl))
    except OSError:
        pass
    return replacements


def normaliser(chemin, dictionnaire=None, dry_run=False, verbose=False):
    """Normalise un fichier : BOM, CRLF, accents.
    Retourne (contenu_normalise, rapports) ou (None, rapports) en cas d erreur."""
    rapports = []

    try:
        brut = Path(chemin).read_bytes()
    except OSError as e:
        return None, [("ERREUR", "lecture impossible: %s" % e)]

    # 1. BOM UTF-8
    if brut.startswith(b"\xef\xbb\xbf"):
        brut = brut[3:]
        rapports.append(("BOM", "BOM UTF-8 retire"))

    # 2. CRLF -> LF
    nb_crlf = brut.count(b"\r\n")
    if nb_crlf:
        brut = brut.replace(b"\r\n", b"\n")
        rapports.append(("CRLF", "%d CRLF -> LF" % nb_crlf))

    # 3. Decodage
    try:
        texte = brut.decode("utf-8")
    except UnicodeDecodeError:
        return None, [("ERREUR", "encodage non UTF-8 (impossible de normaliser)")]

    # 4. Accents via le dictionnaire
    if dictionnaire is None:
        dictionnaire = chemin_dictionnaire()
    replacements = lire_dictionnaire(dictionnaire)
    nb_accents = 0
    for accent, repl in replacements:
        count = texte.count(accent)
        if count:
            texte = texte.replace(accent, repl)
            nb_accents += count
    if nb_accents:
        rapports.append(("ACCENTS", "%d accents/caracteres corriges via dictionnaire" % nb_accents))

    # 5. Non-ASCII restants non couverts par le dictionnaire
    reste = sorted({c for c in texte if ord(c) > 127})
    if reste:
        rapports.append(("ATTENTION", "caracteres non-ASCII restants non couverts: %s" % "".join(reste)))

    if dry_run:
        return texte, rapports

    # 6. Ecriture si modification
    nouveau = texte.encode("ascii", errors="replace")
    if nouveau != brut:
        try:
            with open(chemin, "wb") as fh:
                fh.write(nouveau)
            rapports.append(("ECRIT", "fichier re-ecrit normalise"))
        except OSError as e:
            return None, [("ERREUR", "ecriture impossible: %s" % e)]

    return texte, rapports


def controler_compilation(contenu):
    """Verifie que le script compile (syntaxe Python valide)."""
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="ascii") as tf:
            tf.write(contenu)
            tmp_nom = tf.name
        try:
            import py_compile
            py_compile.compile(tmp_nom, doraise=True)
            return True, ""
        finally:
            try:
                os.unlink(tmp_nom)
            except OSError:
                pass
    except py_compile.PyCompileError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def main():
    verifier_nommage()
    verifier_residus_racine()

    parser = argparse.ArgumentParser(
        prog="executer-script-temporaire",
        description="ENTONNOIR : normalise puis execute un script temporaire (transparent pour l agent).",
    )
    parser.add_argument("script", nargs="?", help="Chemin du script temporaire a normaliser et executer")
    parser.add_argument("args", nargs="*", help="Arguments passes au script")
    parser.add_argument("--dry-run", action="store_true",
                        help="Normaliser et controler SANS executer ni ecrire (affiche les changements)")
    parser.add_argument("--dictionnaire", default=None, help="Chemin vers un dictionnaire alternatif")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--chrono", action="store_true", help="Afficher le temps ecoule (triplet template v0.3.0)")
    parser.add_argument("--version", action="version", version="executer-script-temporaire " + VERSION + " (" + STATUT + ")")
    args = parser.parse_args()

    depart = time.time()

    if not args.script:
        parser.print_help()
        return 2

    script = Path(args.script)
    if not script.is_file():
        print(RED + "[ERREUR] Script non trouve: " + args.script + NC)
        return 1

    print("[ENTONNOIR] " + str(script))
    contenu, rapports = normaliser(script, dictionnaire=args.dictionnaire,
                                   dry_run=args.dry_run, verbose=args.verbose)

    if contenu is None:
        for niveau, msg in rapports:
            print(RED + "[%s] %s" % (niveau, msg) + NC)
        return 1

    if rapports:
        for niveau, msg in rapports:
            if niveau == "ATTENTION":
                print(YELLOW + "[%s] %s" % (niveau, msg) + NC)
            else:
                print(GREEN + "[%s] %s" % (niveau, msg) + NC)
    else:
        print(GREEN + "[CONFORME] script deja normalise (0 modification)" + NC)

    # Controle systematique : compilation
    ok_compil, err = controler_compilation(contenu)
    if not ok_compil:
        print(RED + "[CONTROLE KO] erreur de syntaxe - execution bloquee" + NC)
        print("  " + err)
        return 1
    print(GREEN + "[CONTROLE OK] compilation valide" + NC)

    if args.dry_run:
        print("[DRY-RUN] aucune ecriture ni execution")
        if args.chrono:
            print("[CHRONO] %.2fs" % (time.time() - depart))
        return 0

    # Execution
    cmd = [sys.executable, str(script)] + args.args
    if args.verbose:
        print("[EXEC] " + " ".join(cmd))
    try:
        res = subprocess.run(cmd, timeout=600)
        if args.chrono:
            print("[CHRONO] %.2fs" % (time.time() - depart))
        return res.returncode
    except subprocess.TimeoutExpired:
        print(RED + "[EXEC] timeout (600s)" + NC)
        return 1


if __name__ == "__main__":
    sys.exit(main())
