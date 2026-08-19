#!/usr/bin/env python3
# -*- coding: ascii -*-
# combos-corriger-non-ascii.py
# Combo corriger-non-ascii : detecte et corrige les accents et emojis
# Ressource partagee : utilise par Themis, Buffy, ou tout autre agent
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
combos-corriger-non-ascii.py
combos-corriger-non-ascii

Usage:
  combos-corriger-non-ascii.py [OPTIONS]
  combos-corriger-non-ascii.py [DOSSIER] [OPTIONS]
  combos-corriger-non-ascii.py --full [--dry-run]
"""

VERSION = "0.3.0-py"
STATUT = "prepare"

import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Couleurs ANSI (desactivees si la sortie n'est pas un terminal)
if sys.stdout.isatty():
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"
else:
    RED = GREEN = YELLOW = BLUE = NC = ""

# ---------------------------------------------------------------------------
# Configuration du mode --full (scan du projet entier)
# ---------------------------------------------------------------------------
# Duree de validite de la preuve de dry (en secondes) : au-dela, le wet est
# refuse. Le dry obligatoire doit etre RECENT pour garantir que le rapport
# vu par l'operateur correspond a l'etat reel du projet.
PREUVE_MAX_AGE = 3600

# Extensions des fichiers qui DOIVENT normalement etre en ASCII pur.
EXTENSIONS_FULL = (".md", ".sh", ".py", ".txt", ".json", ".yaml", ".yml", ".js")

# Motifs exclus du scan complet (jamais touches, meme en --full).
MOTIFS_EXCLUS_FULL = [
    ".git",
    ".agents",
    ".backup",
    ".tmp",
    "__pycache__",
    "exemples",
    "corriger-dictionnaire-accents",
    "dictionnaire-emojis",
    "tmp-",
    "node_modules",
]

# Codes des caracteres accentues latins courants (le fichier doit rester
# ASCII pur : on utilise les codes, pas les caracteres).
ACCENTS_LATINS = set(
    [
        0xE0, 0xE1, 0xE2, 0xE3, 0xE4, 0xE5, 0xE7, 0xE8, 0xE9, 0xEA, 0xEB,
        0xEC, 0xED, 0xEE, 0xEF, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF9,
        0xFA, 0xFB, 0xFC, 0xFD, 0xFF, 0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5,
        0xC7, 0xC8, 0xC9, 0xCA, 0xCB, 0xCC, 0xCD, 0xCE, 0xCF, 0xD1, 0xD2,
        0xD3, 0xD4, 0xD5, 0xD6, 0xD9, 0xDA, 0xDB, 0xDC, 0xDD, 0xDF,
    ]
)


def verifier_nommage():
    """Regle immuable : le nom du fichier doit commencer par le prefixe du dossier de categorie."""
    nom = Path(__file__).name
    dossier = Path(__file__).resolve().parent.name
    if not nom.startswith(dossier):
        print(RED + "[ERREUR] Nommage invalide : le fichier doit commencer par '" + dossier + "'" + NC)
        print("  Nom actuel : " + nom)
        sys.exit(2)


def trouver_tools_dir():
    """Combos/combos-corriger-non-ascii/ -> tools/"""
    return Path(__file__).resolve().parent.parent.parent


def trouver_racine_projet():
    """tools/ -> racine du projet (dossier qui contient cerveau-projet/)."""
    return trouver_tools_dir().parent.parent.parent


def executer_bash(script, *args):
    """Executer un script bash avec des arguments et retourner sa sortie."""
    try:
        proc = subprocess.run(
            ["bash", str(script)] + list(args),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        return proc.stdout + proc.stderr
    except subprocess.TimeoutExpired:
        return "[ERREUR] Timeout sur " + script.name + "\n"
    except OSError as e:
        return "[ERREUR] Echec d'execution de " + script.name + " : " + str(e) + "\n"


def compter_problemes(sortie):
    """Compter les lignes de detection au format: deux espaces + [motif]."""
    n = 0
    for ligne in sortie.splitlines():
        if re.match(r"^  \[[a-z]+\]", ligne):
            n += 1
    return n


def extraire_nombre(sortie, motif):
    """Extraire le premier nombre d'une ligne contenant le motif."""
    for ligne in sortie.splitlines():
        if motif in ligne:
            m = re.findall(r"\d+", ligne)
            if m:
                return m[0]
    return "0"


# ---------------------------------------------------------------------------
# Mode --full : detection detaillee (rapport concis mais complet)
# ---------------------------------------------------------------------------
def classifier_caractere(ch):
    """Classer un caractere non-ASCII : accent / emoji / autre."""
    code = ord(ch)
    if code in ACCENTS_LATINS:
        return "accent"
    if code >= 0x1F000 or 0x2600 <= code <= 0x27BF or 0x1F300 <= code <= 0x1FAFF:
        return "emoji"
    return "autre"


def analyser_fichier(fichier):
    """Retourne la liste des lignes non-ASCII (index, nb, caracteres uniques classes)."""
    try:
        with open(fichier, encoding="utf-8") as fh:
            lignes = fh.read().split("\n")
    except Exception:
        return []
    lignes_bad = []
    for i, ligne in enumerate(lignes, 1):
        mauvais = [ch for ch in ligne if ord(ch) > 127]
        if mauvais:
            uniq = {}
            for ch in mauvais:
                cat = classifier_caractere(ch)
                if ch not in uniq:
                    uniq[ch] = {"nb": 0, "cat": cat}
                uniq[ch]["nb"] += 1
            lignes_bad.append((i, len(mauvais), uniq))
    return lignes_bad


def scanner_full(racine):
    """Scanner tous les fichiers ASCII attendus du projet. Retourne la liste
    des rapports (fichier, lignes_bad)."""
    rapports = []
    for r, dossiers, fs in os.walk(racine):
        if any(m in r for m in [".git", ".agents", "__pycache__", "node_modules"]):
            continue
        for f in fs:
            chemin = os.path.join(r, f)
            if any(m in chemin for m in MOTIFS_EXCLUS_FULL):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext not in EXTENSIONS_FULL:
                continue
            lignes_bad = analyser_fichier(chemin)
            if lignes_bad:
                rapports.append((chemin, lignes_bad))
    return rapports


def resumer_rapports(rapports):
    """Statistiques globales : fichiers, lignes, caracteres, repartition par type."""
    nb_fichiers = len(rapports)
    nb_lignes = sum(len(lb) for _, lb in rapports)
    nb_caracteres = sum(n for _, lb in rapports for _, n, _ in lb)
    repartition = {"accent": 0, "emoji": 0, "autre": 0}
    for _, lb in rapports:
        for _, _, uniq in lb:
            for info in uniq.values():
                repartition[info["cat"]] += info["nb"]
    return nb_fichiers, nb_lignes, nb_caracteres, repartition


def afficher_rapport_full(rapports, racine):
    """Rapport concis mais complet : 1 ligne par fichier (tous), + resume."""
    nb_fichiers, nb_lignes, nb_caracteres, repartition = resumer_rapports(rapports)

    print("=== Resume du scan complet ===")
    print("Racine : " + str(racine))
    print("Fichiers non conformes : " + str(nb_fichiers))
    print("Lignes concernees : " + str(nb_lignes))
    print("Caracteres non-ASCII : " + str(nb_caracteres))
    print("Repartition : accents=" + str(repartition["accent"])
          + ", emojis=" + str(repartition["emoji"])
          + ", autres=" + str(repartition["autre"]))
    print("")

    for fichier, lignes_bad in rapports:
        total_lignes = len(lignes_bad)
        total_car = sum(n for _, n, _ in lignes_bad)
        uniq_global = {}
        for _, _, uniq in lignes_bad:
            for ch, info in uniq.items():
                if ch not in uniq_global:
                    uniq_global[ch] = {"nb": 0, "cat": info["cat"]}
                uniq_global[ch]["nb"] += info["nb"]
        detail = ", ".join(
            "U+%04X(x%d,%s)" % (ord(ch), info["nb"], info["cat"])
            for ch, info in list(uniq_global.items())[:8]
        )
        print("  [" + fichier + "] : " + str(total_lignes)
              + " ligne(s), " + str(total_car) + " caractere(s) -- " + detail)

    return nb_fichiers


def ecrire_preuve_dry(racine, rapports):
    """Ecrire la preuve de dry (fichier json date) dans tmp-combos-full/."""
    nb_fichiers, nb_lignes, nb_caracteres, repartition = resumer_rapports(rapports)
    dossier_preuve = Path(str(racine)) / "tmp-combos-full"
    dossier_preuve.mkdir(parents=True, exist_ok=True)
    fichier_preuve = dossier_preuve / "preuve-dry-full.json"
    preuve = {
        "date": datetime.datetime.now().isoformat(),
        "racine": str(racine),
        "nb_fichiers": nb_fichiers,
        "nb_lignes": nb_lignes,
        "nb_caracteres": nb_caracteres,
        "repartition": repartition,
    }
    try:
        fichier_preuve.write_text(
            json.dumps(preuve, ensure_ascii=True, indent=1) + "\n",
            encoding="utf-8",
            newline="",
        )
        print(GREEN + "[OK] Preuve de dry ecrite : " + str(fichier_preuve) + NC)
        print("    (le wet --full est maintenant autorise pendant "
              + str(PREUVE_MAX_AGE // 60) + " minutes)")
        return True
    except OSError as e:
        print(RED + "[ERREUR] Impossible d'ecrire la preuve de dry : " + str(e) + NC)
        return False


def verifier_preuve_dry(racine):
    """Verifier la preuve de dry : presente, recente, meme racine."""
    fichier_preuve = Path(str(racine)) / "tmp-combos-full" / "preuve-dry-full.json"
    if not fichier_preuve.is_file():
        print(RED + "[REFUS] Wet --full sans dry prealable." + NC)
        print("  Le dry est OBLIGATOIRE avant le wet (regle utilisateur).")
        print("  Lancez d'abord : combos-corriger-non-ascii.py --full --dry-run")
        print("  puis examinez le rapport, puis relancez sans --dry-run.")
        return False
    try:
        preuve = json.loads(fichier_preuve.read_text(encoding="utf-8"))
    except (ValueError, OSError) as e:
        print(RED + "[REFUS] Preuve de dry illisible : " + str(e) + NC)
        return False
    date_preuve = preuve.get("date", "")
    try:
        dt = datetime.datetime.fromisoformat(date_preuve)
    except ValueError:
        print(RED + "[REFUS] Preuve de dry date invalide : " + date_preuve + NC)
        return False
    age = (datetime.datetime.now() - dt).total_seconds()
    if age > PREUVE_MAX_AGE:
        print(RED + "[REFUS] Preuve de dry trop ancienne (" + str(int(age))
              + " s, max " + str(PREUVE_MAX_AGE) + " s)." + NC)
        print("  Relancez : combos-corriger-non-ascii.py --full --dry-run")
        return False
    if preuve.get("racine") != str(racine):
        print(RED + "[REFUS] Preuve de dry pour une autre racine." + NC)
        return False
    print(GREEN + "[OK] Preuve de dry validee (age " + str(int(age)) + " s)." + NC)
    return True


def mode_full(dry_run):
    """Mode --full : scan du projet entier. Dry obligatoire avant wet."""
    racine = trouver_racine_projet()
    print(BLUE + "=== combos-corriger-non-ascii --full v" + VERSION + " ===" + NC)
    print("Mode : " + ("DRY-RUN" if dry_run else "APPLICATION (wet)"))
    print("Racine : " + str(racine))
    print("Date : " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("")

    if not dry_run:
        if not verifier_preuve_dry(racine):
            return 2

    # Detection detaillee sur TOUT le projet
    print(BLUE + "--- Detection (projet entier) ---" + NC)
    rapports = scanner_full(racine)
    nb_fichiers = afficher_rapport_full(rapports, racine)
    print("")

    if dry_run:
        if nb_fichiers == 0:
            print(GREEN + "[OK] Aucun caractere non-ASCII detecte : rien a corriger." + NC)
            return 0
        print("")
        print(YELLOW + "[ATTENTION] " + str(nb_fichiers)
              + " fichier(s) non conforme(s) detecte(s)." + NC)
        print("Examinez le rapport ci-dessus : il liste TOUS les fichiers concernes.")
        print("Si vous validez, relancez SANS --dry-run pour appliquer (wet).")
        ecrire_preuve_dry(racine, rapports)
        return 1

    # Wet : corriger UNIQUEMENT les fichiers detectes par le dry (le scan
    # Python est rapide ; lancer corriger-accents --recursive sur TOUT le
    # projet prendrait des minutes). Mode fichier direct : couvre toutes les
    # extensions et reste sous la seconde par fichier.
    tools_dir = trouver_tools_dir()
    corriger_emojis = tools_dir / "corriger" / "corriger-emojis" / "corriger-emojis.sh"
    corriger_accents = tools_dir / "corriger" / "corriger-accents-zones-sensibles" / "corriger-accents-zones-sensibles.sh"

    print(BLUE + "--- Correction ciblee (fichiers du dry, mode fichier direct) ---" + NC)
    nb_fichiers = len(rapports)
    for i, (fichier, _) in enumerate(rapports, 1):
        print("  [" + str(i) + "/" + str(nb_fichiers) + "] " + fichier)
        executer_bash(corriger_emojis, fichier)
        executer_bash(corriger_accents, "--all", fichier)
    print("")

    print(BLUE + "--- Verification (projet entier) ---" + NC)
    rapports_apres = scanner_full(racine)
    nb_apres = len(rapports_apres)
    nb_avant = len(rapports)
    print("Fichiers non conformes : avant=" + str(nb_avant) + ", apres=" + str(nb_apres))
    if nb_apres == 0:
        print(GREEN + "[OK] Projet entier ASCII pur : " + str(nb_avant)
              + " fichier(s) corrige(s)." + NC)
        return 0
    print(YELLOW + "[ATTENTION] " + str(nb_apres)
          + " fichier(s) restent non conformes (voir rapport dry)." + NC)
    return 1


def main():
    verifier_nommage()

    import argparse

    parser = argparse.ArgumentParser(
        prog="combos-corriger-non-ascii",
        description="Combo : detecte et corrige les accents et emojis.",
    )
    parser.add_argument("dossier", nargs="?", default=".", help="Dossier cible (defaut: .)")
    parser.add_argument("--dry-run", action="store_true", help="Afficher les changements sans les appliquer")
    parser.add_argument("--all", action="store_true", help="Corriger TOUS les accents (texte francais et titres)")
    parser.add_argument("--full", action="store_true",
                        help="Scanner et corriger TOUT le projet d'un coup (dry obligatoire avant wet)")
    parser.add_argument("--rapport", action="store_true", help="Sauvegarder un rapport dans themis/rapports/")
    parser.add_argument("--version", action="version", version="combos-corriger-non-ascii " + VERSION + " (" + STATUT + ")")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    if args.full:
        return mode_full(args.dry_run)

    dossier = args.dossier.rstrip("/")
    if "cerveau-projet" in dossier:
        cible = dossier
    else:
        cible = os_join(dossier, "cerveau-projet")

    mode = "DRY-RUN" if args.dry_run else "APPLICATION"

    print(BLUE + "=== combos-corriger-non-ascii v" + VERSION + " ===" + NC)
    print("Cible : " + dossier)
    print("Mode : " + mode)
    print("Date : " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("")

    if not Path(dossier).is_dir():
        print(RED + "[ERREUR] Le dossier n'existe pas : " + dossier + NC)
        return 1

    tools_dir = trouver_tools_dir()
    rechercher = tools_dir / "rechercher" / "rechercher-accents-sensibles" / "rechercher-accents-sensibles.sh"
    corriger_emojis = tools_dir / "corriger" / "corriger-emojis" / "corriger-emojis.sh"
    corriger_accents = tools_dir / "corriger" / "corriger-accents-zones-sensibles" / "corriger-accents-zones-sensibles.sh"

    # Etape 1 : Detection
    print(BLUE + "--- Etape 1/4 : Detection des problemes ---" + NC)
    avant = compter_problemes(executer_bash(rechercher, dossier))
    print("Lignes detectees avant correction : " + str(avant))
    print("")

    # Etape 2 : Correction des emojis
    print(BLUE + "--- Etape 2/4 : Correction des emojis ---" + NC)
    if args.dry_run:
        sortie_emojis = executer_bash(corriger_emojis, "--dry-run", dossier)
    else:
        sortie_emojis = executer_bash(corriger_emojis, dossier)
    for ligne in sortie_emojis.splitlines()[-5:]:
        if ligne.strip():
            print(ligne)
    print("")

    # Etape 3 : Correction des accents (mode dossier recursif, un seul appel)
    print(BLUE + "--- Etape 3/4 : Correction des accents ---" + NC)
    accents_args = ["--recursive"]
    if args.all:
        accents_args.append("--all")
    if args.dry_run:
        accents_args.append("--dry-run")
    accents_args.append(cible)
    resultat_accents = executer_bash(corriger_accents, *accents_args)

    nb_accents = extraire_nombre(resultat_accents, "Fichiers analys")
    total_corr = extraire_nombre(resultat_accents, "Corrections appliqu")
    total_cons = extraire_nombre(resultat_accents, "Accents fran")
    print("Fichiers analyses : " + nb_accents)
    print("Corrections zones sensibles : " + total_corr)
    print("Accents francais conserves : " + total_cons)
    print("")

    # Etape 4 : Verification
    print(BLUE + "--- Etape 4/4 : Verification ---" + NC)
    apres = compter_problemes(executer_bash(rechercher, dossier))
    print("Lignes detectees apres correction : " + str(apres))

    if apres < avant:
        print(GREEN + "[OK] Reduction : " + str(avant) + " -> " + str(apres) + " (" + str(avant - apres) + " lignes corrigees)" + NC)
    elif avant == 0 and apres == 0:
        print(GREEN + "[OK] Aucun probleme detecte" + NC)
    else:
        print(YELLOW + "[ATTENTION] " + str(apres) + " lignes restantes : relancez avec --all (regle immuable : aucun accent tolere)" + NC)
        print(YELLOW + "Les seules exceptions admises : exemples/ et dictionnaires fonctionnels." + NC)

    # Rapport
    if args.rapport:
        rapport_dir = Path(cible) / "agents" / "themis" / "rapports"
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        rapport_file = rapport_dir / ("corriger-non-ascii-" + date + ".md")
        rapport_dir.mkdir(parents=True, exist_ok=True)

        contenu = [
            "# Rapport corriger-non-ascii -- " + date,
            "",
            "## Contexte",
            "- Cible : " + dossier,
            "- Mode : " + mode,
            "",
            "## Resultats",
            "- Lignes avant : " + str(avant),
            "- Lignes apres : " + str(apres),
            "- Reduction : " + str(avant - apres) + " lignes",
            "- Fichiers accents corriges : " + nb_accents,
        ]
        try:
            rapport_file.write_text("\n".join(contenu) + "\n", encoding="utf-8", newline="")
            print("")
            print(GREEN + "Rapport sauvegarde : " + str(rapport_file) + NC)
        except OSError as e:
            print(RED + "[ERREUR] Impossible de sauvegarder le rapport : " + str(e) + NC)

    return 0


def os_join(a, b):
    """Joindre 2 chemins en gardant le separateur du systeme."""
    return str(Path(a) / b)


if __name__ == "__main__":
    sys.exit(main())
