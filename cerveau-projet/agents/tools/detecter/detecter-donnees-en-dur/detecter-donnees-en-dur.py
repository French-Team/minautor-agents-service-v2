#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-donnees-en-dur.py
#
# Detecte les DONNEES EN DUR qui provoquent des bugs caches : des valeurs
# ecrites directement dans le code (ou les documents) qui deviendront fausses
# quand le projet evolue. La regle d or : ne JAMAIS coder en dur une valeur
# qui peut changer (versions, compteurs, seuils, chemins, URLs, tailles,
# delais). Quand un doute est emis, l agent doit preferer :
#   - une CONSTANTE NOMMEE en haut du fichier (usage local, convention
#     MAJUSCULES) ;
#   - un fichier de CONFIGURATION (JSON) si la valeur est partagee ou change
#     souvent ;
#   - une LISTE / un TABLEAU dans un autre fichier (JSON/CSV) pour les
#     collections ;
#   - la documentation (.md) pour les valeurs purement documentaires.
#
# Detections (par type) :
#   1. NOMBRES_MAGIQUES : constante numerique utilisee dans le code sans nom
#      (seuil, taille, delai, compteur, port). Heuristique : nombre != 0/1/-1
#      dans une comparaison, un calcul ou un parametre.
#   2. CHEMINS_EN_DUR    : chaine ressemblant a un chemin de fichier/dossier
#      (contient / ou \ ou une extension de fichier connue).
#   3. URLS_EN_DUR       : chaine commencant par http://, https://, ftp://.
#   4. VERSIONS_EN_DUR   : chaine vX.Y.Z / X.Y.Z dans un message, un titre ou
#      un en-tete (hors source de verite de version du fichier lui-meme).
#   5. COMPTEURS_SEUILS  : nombre qui devrait etre calcule ou nomme (delai,
#      timeout, limite, total, nb_*, seuil, max, min).
#
# Exclusions legitimes : 0/1/-1/100, valeurs de test (fixtures), exemples de
# documentation, entrees d historique (AGENTS-historique), valeurs deja
# issues d une constante nommee (MAJUSCULES).
#
# Usage :
#   python3 detecter-donnees-en-dur.py <chemin-fichier-ou-dossier> [autres...]
#   python3 detecter-donnees-en-dur.py --tous
#   python3 detecter-donnees-en-dur.py --tous --rapport rapport.md --verbose
#
# Options :
#   --tous              : scanne tout le projet depuis la racine (AGENTS.md)
#   --rapport <fichier> : ecrit le rapport markdown
#   --verbose           : detail des fichiers et des motifs
#   --version
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (detecter-).
# =============================================================================
import argparse
import io
import os
import re
import sys
from datetime import datetime

VERSION = "0.1.0"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[0;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    return "%s%s%s" % (_COULEURS.get(nom, _COULEURS["neutre"]), texte, _COULEURS["neutre"])


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


# ---------------------------------------------------------------------------
# Heuristiques de detection
# ---------------------------------------------------------------------------

# Extensions de fichiers connues (pour les chemins en dur)
EXTENSIONS_FICHIER = {
    ".py", ".sh", ".md", ".json", ".jsonl", ".txt", ".csv", ".yml", ".yaml",
    ".toml", ".ini", ".cfg", ".html", ".css", ".js", ".ts", ".png", ".jpg",
    ".jpeg", ".gif", ".svg", ".ico", ".bak", ".orig", ".tmp",
}

# Mots qui signalent une VALEUR PARAMETRABLE (compteur, seuil, delai...)
MOTS_PARAMETRABLES = [
    "delai", "timeout", "seuil", "limite", "limit", "max", "min", "total",
    "compteur", "count", "nb_", "nb ", "taille", "size", "port", "duree",
    "budget", "plafond", "seuils",
]

# Extensions de fichiers a analyser (code + config + docs du projet)
EXTENSIONS_ANALYSEES = {".py", ".sh", ".md", ".json", ".jsonl", ".yml", ".yaml", ".toml", ".txt"}

# Fichiers / dossiers exclus du scan --tous
EXCLUSIONS_SCAN = [
    ".git", "__pycache__", ".agents-tmp", "workspace", "node_modules",
    "dictionnaire-accents", "dictionnaire-emojis", "exemples", "recherches-web",
    "docs-dev-cerveau-projet", "exemples-tests", "pense-betes", "specs", "todos",
]


def nombre_est_banal(n):
    """0/1/-1/100 sont des valeurs banales (index, booleens, pourcentage)."""
    return n in (0, 1, -1, 100)


def mot_est_parametrable(mot):
    m = mot.lower().strip("_")
    return any(k in m for k in MOTS_PARAMETRABLES)


def recommander_format(valeur, type_doute):
    """Recommander le meilleur format de stockage pour eviter la valeur en dur."""
    if type_doute == "NOMBRES_MAGIQUES" or type_doute == "COMPTEURS_SEUILS":
        return ("Constante NOMMEE en haut du fichier (ex: SEUIL_ALERTE = %s, "
                "MAJUSCULES). Si partagee entre plusieurs fichiers : fichier de "
                "configuration JSON." % valeur)
    if type_doute == "CHEMINS_EN_DUR":
        return ("Variable de chemin en haut du fichier ou constantes de "
                "configuration (ex: AGENTS_DIR = \"cerveau-projet/agents\"). "
                "Si partage : JSON de configuration.")
    if type_doute == "URLS_EN_DUR":
        return ("Constante en haut du fichier (ex: URL_API = \"...\") ou JSON de "
                "configuration si l URL peut changer (environnement).")
    if type_doute == "VERSIONS_EN_DUR":
        return ("Version centralisee dans une SOURCE DE VERITE (fichier de "
                "version dedie ou VERSION = \"...\" en tete du fichier) - "
                "jamais repetee dans les messages ou la doc.")
    return "Constante nommee en haut du fichier ou JSON de configuration."


def est_date(extrait):
    """Vrai si l'extrait est une date (2026-08-09, 09/08/2026, 2026 08...)."""
    if re.match(r"^\d{4}-\d{2}-\d{2}$", extrait):
        return True
    if re.match(r"^\d{2}/\d{2}/\d{4}$", extrait):
        return True
    return False


def ressemble_a_un_chemin(s):
    """Vrai si la chaine ressemble a un VRAI chemin de fichier/dossier (pas un
    motif de message du type 'OK / 0 KO' ou '41/41').

    Regles :
      - un chemin reel a au moins une extension de fichier connue en fin, OU
        deux segments separes par '/' sans espace autour (ex: a/b/c) ;
      - les slash entoures d espaces (' / ') sont des motifs de message ;
      - les motifs purement numeriques (41/41) ne sont pas des chemins.
    """
    if " / " in s or "/ " in s or " /" in s:
        return False
    if re.match(r"^[\d\s]+/[\d\s]+$", s):
        return False
    if any(s.endswith(ext) for ext in EXTENSIONS_FICHIER):
        return True
    # >= 2 segments separes par '/' sans espaces, avec au moins un caractere
    # alphabetique par segment (exclut les motifs 41/41, 1/0)
    segments = s.split("/")
    if len(segments) >= 2 and all(any(c.isalpha() for c in seg) for seg in segments):
        return True
    return False


def analyser_contenu(chemin, texte, verbose):
    """Analyse le contenu d'un fichier et retourne la liste des doutes.

    Chaque doute : (type, ligne, extrait, recommandation).
    Les fichiers .md sont traites avec parcimonie : la doc decrit des
    regles/documentaires (les nombres documentaires ne sont pas du code en
    dur) - on ne signale que chemins, URLs et versions repetees.
    """
    est_doc = chemin.lower().endswith(".md")
    # Le code reel (chemins/URLs a surveiller) = .py et .sh. Les .json de
    # parcours/configuration et les .md contiennent des COMMANDES et LIENS
    # documentaires legitimes (python3 .../outil.py, liens relatifs) qui ne
    # sont pas des donnees en dur sources de bugs.
    est_code = chemin.lower().endswith((".py", ".sh"))
    doutes = []
    lignes = texte.split("\n")
    for num, ligne in enumerate(lignes, start=1):
        # --- 1+2. CHEMINS_EN_DUR + URLS_EN_DUR : code reel uniquement (.py/.sh),
        # et seulement si la ligne n est pas un commentaire ni une commande
        # documentaire (python3/bash) de l en-tete.
        if est_code and not ligne.strip().startswith(("#", "//")):
            for m in re.finditer(r"[\"']([^\"']*(?:/|\\\\)[^\"']*)[\"']", ligne):
                s = m.group(1)
                if len(s) < 3 or s.startswith("http"):
                    continue
                # chemin de fichier/dossier typique (forme stricte)
                est_chemin = ("/" in s or "\\" in s) and ressemble_a_un_chemin(s)
                if est_chemin and not s.startswith(("$", "{", "{{")):
                    doutes.append(("CHEMINS_EN_DUR", num, s[:80],
                                   recommander_format(s, "CHEMINS_EN_DUR")))
            for m in re.finditer(r"[\"']((?:https?|ftp)://[^\"']+)[\"']", ligne):
                doutes.append(("URLS_EN_DUR", num, m.group(1)[:80],
                               recommander_format(m.group(1), "URLS_EN_DUR")))
        # --- 3. VERSIONS_EN_DUR : vX.Y.Z ou X.Y.Z hors en-tete du fichier
        if re.match(r"^#.*Version", ligne, re.IGNORECASE):
            continue  # en-tete de version du fichier lui-meme (source de verite)
        for m in re.finditer(r"[\"'](v?\d+\.\d+\.\d+)[\"']", ligne):
            v = m.group(1)
            # exclusion : commentaire de version (VERSION =, version:)
            if re.search(r"(VERSION|version)\s*[:=]", ligne):
                continue
            doutes.append(("VERSIONS_EN_DUR", num, v,
                           recommander_format(v, "VERSIONS_EN_DUR")))
        # --- 4. NOMBRES_MAGIQUES + COMPTEURS_SEUILS (code .py/.sh)
        # Les .md sont documentaires : les nombres y decrivent des regles,
        # pas du code en dur -> exclus (sauf chemins/URLs/versions traites
        # ci-dessus).
        if est_doc or not est_code:
            continue
        if ligne.strip().startswith("#") or ligne.strip().startswith("//"):
            continue  # commentaire : pas une valeur en dur active
        # COMPTEURS_SEUILS : affectation DIRECTE d un nom parametrable a un
        # nombre (ex: timeout = 30, max = 5, nb_agents = 13). Les mots
        # max/min/total dans une phrase quelconque ne sont pas des seuils.
        for m in re.finditer(r"([a-z_]+[a-z_]*)\s*=\s*(\d{2,})", ligne, re.IGNORECASE):
            nom_var = m.group(1)
            val = m.group(2)
            if not nombre_est_banal(int(val)) and mot_est_parametrable(nom_var):
                doutes.append(("COMPTEURS_SEUILS", num, val,
                               recommander_format(val, "COMPTEURS_SEUILS")))
        # NOMBRES_MAGIQUES : nombre dans une COMPARAISON (>) < == !=) sans
        # nom parametrable (les seuils nommes sont deja couverts ci-dessus).
        if any(op in ligne for op in [">", "<", "==", "!=", ">=", "<="]):
            for m in re.finditer(r"(?<![\w.])(\d{2,})(?![\w.])", ligne):
                extrait = m.group(1)
                if est_date(extrait):
                    continue
                n = int(extrait)
                if nombre_est_banal(n):
                    continue
                # ligne de comparaison pure (pas de nom parametrable associe)
                doutes.append(("NOMBRES_MAGIQUES", num, extrait,
                               recommander_format(extrait, "NOMBRES_MAGIQUES")))
    return doutes


def analyser_fichier(chemin, verbose):
    """Analyse un fichier, retourne (chemin, liste de doutes)."""
    try:
        with io.open(chemin, encoding="utf-8", errors="replace", newline="") as fh:
            texte = fh.read()
    except Exception as e:
        return chemin, [("LECTURE", 0, "impossible de lire : %s" % e, "")]
    return chemin, analyser_contenu(chemin, texte, verbose)


def fichiers_du_chemin(chemin):
    """Retourne la liste des fichiers a analyser depuis un chemin fichier ou dossier."""
    resultats = []
    if os.path.isfile(chemin):
        return [chemin]
    if os.path.isdir(chemin):
        for racine, dossiers, fichiers in os.walk(chemin):
            dossiers[:] = [d for d in dossiers
                           if d not in EXCLUSIONS_SCAN and not d.startswith(".git")]
            for f in fichiers:
                ext = os.path.splitext(f)[1].lower()
                if ext in EXTENSIONS_ANALYSEES:
                    resultats.append(os.path.join(racine, f))
    return resultats


def scan_tous(racine):
    """Scanne tout le projet depuis la racine (fichiers analysables)."""
    fichiers = []
    for dossier in ["cerveau-projet", "README.md", "AGENTS.md", "demarrer.md"]:
        chemin = os.path.join(racine, dossier)
        if os.path.isfile(chemin):
            fichiers.append(chemin)
        elif os.path.isdir(chemin):
            fichiers.extend(fichiers_du_chemin(chemin))
    return fichiers


def ecrire_rapport(chemin_rapport, resultats, total_doutes, verbose):
    """Ecrit le rapport markdown (LF pur, ASCII)."""
    with io.open(chemin_rapport, "w", encoding="utf-8", newline="") as fh:
        fh.write("# Rapport detecter-donnees-en-dur\n\n")
        fh.write("**Date** : %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M"))
        fh.write("**Total doutes** : %d\n\n" % total_doutes)
        fh.write("## Details\n\n")
        for chemin, doutes in resultats:
            if not doutes:
                continue
            fh.write("### %s\n\n" % chemin)
            fh.write("| Type | Ligne | Valeur | Recommandation |\n")
            fh.write("|---|---|---|---|\n")
            for type_d, num, extrait, reco in doutes:
                fh.write("| %s | %d | `%s` | %s |\n" % (type_d, num, extrait.replace("|", "/"), reco))
            fh.write("\n")
        fh.write("---\n")
        fh.write("Verdict : %s\n" % ("OK - aucun doute" if total_doutes == 0 else
                                     "SIGNAL - %d doutes de donnees en dur" % total_doutes))


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="detecter-donnees-en-dur",
        description="Detecte les donnees en dur (nombres magiques, chemins, "
                    "URLs, versions, compteurs) sources de bugs caches.")
    parser.add_argument("chemins", nargs="*", help="Fichiers ou dossiers a analyser")
    parser.add_argument("--tous", action="store_true",
                        help="Scan complet du projet depuis la racine (AGENTS.md)")
    parser.add_argument("--rapport", metavar="FICHIER",
                        help="Ecrit le rapport markdown dans FICHIER")
    parser.add_argument("--verbose", action="store_true",
                        help="Detail des fichiers et motifs")
    parser.add_argument("--version", action="store_true",
                        help="Affiche la version")
    args = parser.parse_args(argv)

    if args.version:
        print("detecter-donnees-en-dur v%s (%s)" % (VERSION, STATUT))
        return 0

    if args.tous:
        racine = racine_projet()
        fichiers = scan_tous(racine)
        if args.verbose:
            print("Racine projet : %s" % racine)
            print("Fichiers analyses : %d" % len(fichiers))
    elif args.chemins:
        fichiers = []
        for c in args.chemins:
            fichiers.extend(fichiers_du_chemin(c))
    else:
        parser.print_help()
        return 1

    if not fichiers:
        print("Aucun fichier a analyser.")
        return 1

    resultats = []
    total_doutes = 0
    nb_fichiers_douteux = 0
    for f in sorted(fichiers):
        chemin, doutes = analyser_fichier(f, args.verbose)
        if doutes:
            total_doutes += len(doutes)
            nb_fichiers_douteux += 1
            if args.verbose:
                print(_couleur("[DOUTE] %s : %d" % (chemin, len(doutes)), "jaune"))
        resultats.append((chemin, doutes))

    # Affichage par type
    comptes_types = {}
    for chemin, doutes in resultats:
        for type_d, num, extrait, reco in doutes:
            comptes_types[type_d] = comptes_types.get(type_d, 0) + 1

    print("=== RESULTAT detecter-donnees-en-dur v%s ===" % VERSION)
    print("Fichiers analyses : %d | fichiers avec doutes : %d | total doutes : %d"
          % (len(fichiers), nb_fichiers_douteux, total_doutes))
    if comptes_types:
        print("Doutes par type :")
        for type_d in sorted(comptes_types):
            print("  %-18s : %d" % (type_d, comptes_types[type_d]))
    print("")
    for chemin, doutes in resultats:
        if not doutes:
            if args.verbose:
                print(_couleur("  [OK] %s" % chemin, "vert"))
            continue
        print(_couleur("=== %s (%d doutes) ===" % (chemin, len(doutes)), "rouge"))
        for type_d, num, extrait, reco in doutes:
            print("  [%s] ligne %d : %s" % (type_d, num, extrait))
            if args.verbose and reco:
                print("      -> %s" % reco)

    print("")
    if total_doutes == 0:
        print(_couleur("VERDICT : OK - aucun doute de donnee en dur.", "vert"))
    else:
        print(_couleur("VERDICT : SIGNAL - %d doutes de donnees en dur a "
                       "examiner (preferer une constante nommee, un JSON de "
                       "configuration ou une liste dediee)." % total_doutes, "rouge"))

    if args.rapport:
        ecrire_rapport(args.rapport, resultats, total_doutes, args.verbose)
        print(_couleur("Rapport ecrit : %s" % args.rapport, "bleu"))

    return 0 if total_doutes == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
