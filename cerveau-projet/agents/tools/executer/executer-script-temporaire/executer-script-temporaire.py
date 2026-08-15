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

"""
executer-script-temporaire.py
executer-script-temporaire

Usage:
  executer-script-temporaire.py [OPTIONS]
"""

import argparse
import io
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

VERSION = "0.1.2"
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

    # 2. CRLF -> LF (brut_original conserve pour la comparaison d ecriture)
    brut_original = brut
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

    # 6. Ecriture si modification (comparaison sur le brut ORIGINAL)
    nouveau = texte.encode("ascii", errors="replace")
    if nouveau != brut_original:
        try:
            with open(chemin, "wb") as fh:
                fh.write(nouveau)
            rapports.append(("ECRIT", "fichier re-ecrit normalise"))
        except OSError as e:
            return None, [("ERREUR", "ecriture impossible: %s" % e)]

    return texte, rapports


EXTENSIONS_TEXTE = {".md", ".py", ".sh", ".json", ".jsonl", ".txt"}


def controler_triplet(texte):
    """Controle la presence du TRIPLET (regle immuable protocole-
    creation-scripts-temporaires v0.2.6, demande utilisateur 2026-08-15) :
    PROTECTIONS (--dry-run / gestion erreur), OPTIONS ON/OFF (--isoler /
    --desactiver), CHRONO (--no-chrono / chrono_etape / bilan_chrono).

    Retourne la liste des manquants (vide si le script est conforme).
    Le script ne bloque PAS l execution (les scripts de mission legitimes
    peuvent etre simples) mais SIGNALE le manque pour action ulterieure.
    """
    manquants = []
    if "--dry-run" not in texte and "--dry" not in texte:
        manquants.append("protections (--dry-run)")
    if "--isoler" not in texte and "--desactiver" not in texte:
        manquants.append("options on/off (--isoler/--desactiver)")
    if "chrono_etape" not in texte and "bilan_chrono" not in texte \
            and "--no-chrono" not in texte and "CHRONO" not in texte:
        manquants.append("chrono (--no-chrono)")
    return manquants


def racine_projet():
    """Detecte la racine du projet en remontant jusqu a trouver AGENTS.md."""
    courant = Path(__file__).resolve().parent
    for ancetre in courant.parents:
        if (ancetre / "AGENTS.md").is_file():
            return ancetre
    return Path.cwd()


def normaliser_fichiers_modifies(depart, racine, verbose=False):
    """Protection de sortie LF : normalise les fichiers du projet modifies
    pendant la fenetre d execution du script (mtime >= depart).

    Cause racine : un append direct (open en mode a sans newline="") traduit
    LF en CRLF sur Windows. L entonnoir normalisait le script AVANT execution
    mais pas les fichiers ecrits PAR le script au runtime. Cette protection
    ferme la boucle : apres execution, tout fichier du projet touche est
    re-normalise (CRLF -> LF, BOM, accents).

    Retourne la liste des fichiers re-ecrits normalises.
    """
    reecrits = []
    try:
        fichier_racine = racine_projet()
    except OSError:
        fichier_racine = Path.cwd()
    try:
        for chemin in fichier_racine.rglob("*"):
            if not chemin.is_file():
                continue
            if chemin.suffix.lower() not in EXTENSIONS_TEXTE:
                continue
            if "__pycache__" in chemin.parts or ".git" in chemin.parts:
                continue
            try:
                if chemin.stat().st_mtime < depart:
                    continue
            except OSError:
                continue
            texte, rapports = normaliser(chemin, verbose=verbose)
            if texte is None:
                continue
            for niveau, msg in rapports:
                if niveau == "ECRIT":
                    reecrits.append(str(chemin))
                    if verbose:
                        print(GREEN + "[SORTIE-LF] %s : %s" % (chemin, msg) + NC)
    except OSError:
        pass
    return reecrits


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
    parser.add_argument("--chrono", action="store_true",
                        help="(compat) Afficher le temps ecoule - desormais AFFICHE PAR DEFAUT")
    parser.add_argument("--no-chrono", action="store_true",
                        help="Desactiver le chrono (affichage par defaut)")
    parser.add_argument("--version", action="version", version="executer-script-temporaire " + VERSION + " (" + STATUT + ")")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    # CHRONO AFFICHE PAR DEFAUT (demande utilisateur 2026-08-15 : le chrono
    # doit etre visible en haut, a chaque execution) - --no-chrono le coupe.
    chrono_actif = not args.no_chrono
    depart = time.time()
    if chrono_actif:
        print(GREEN + "[CHRONO] %.2fs (entonnoir)" % (time.time() - depart) + NC)

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

    # CONTROLE TRIPLET (regle immuable v0.2.6) : protections + options + chrono
    manquants = controler_triplet(contenu)
    if manquants:
        print(YELLOW + "[TRIPLET] WARNING : le script n embarque pas le triplet complet" + NC)
        print(YELLOW + "  manquants : " + ", ".join(manquants) + NC)
        print(YELLOW + "  regle : protocole-creation-scripts-temporaires v0.2.6" + NC)
        print(YELLOW + "  (--dry-run / --isoler / --desactiver / --no-chrono, chrono_etape, bilan_chrono)" + NC)

    if args.dry_run:
        print("[DRY-RUN] aucune ecriture ni execution")
        if chrono_actif:
            print("[CHRONO] %.2fs (total)" % (time.time() - depart))
        return 0

    # Execution
    cmd = [sys.executable, str(script)] + args.args
    if args.verbose:
        print("[EXEC] " + " ".join(cmd))
    try:
        res = subprocess.run(cmd, timeout=600)
        # PROTECTION DE SORTIE LF : normalise les fichiers du projet modifies
        # par le script pendant la fenetre d execution (CRLF -> LF).
        reecrits = normaliser_fichiers_modifies(depart, Path.cwd(), verbose=args.verbose)
        if reecrits:
            print(GREEN + "[SORTIE-LF] %d fichier(s) re-normalise(s) en LF pur" % len(reecrits) + NC)
        if chrono_actif:
            print(GREEN + "[CHRONO] %.2fs (total)" % (time.time() - depart) + NC)
        return res.returncode
    except subprocess.TimeoutExpired:
        print(RED + "[EXEC] timeout (600s)" + NC)
        return 1


if __name__ == "__main__":
    sys.exit(main())
