#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-troncatures.py
#
# Detecte les elements TRONQUES donc ILLISIBLES au final (demande
# utilisateur 2026-08-16, perimetre valide, round d amelioration
# 2026-08-16) :
#
#   1. FICHIER_TROUQUE   : fichier depassant un seuil de lignes lisible en
#                          une lecture (defaut 2000) - tronque par les
#                          outils de lecture LLM, le contenu devient
#                          partiellement illisible. Les fichiers BINAIRES
#                          sont ignores (pas de lignes lisibles).
#   2. BLOC_NON_FERME    : blocs de code markdown (triple backticks) non
#                          fermes + structure invalide (JSON invalide,
#                          Python qui ne compile pas, bash -n KO) - un
#                          fichier coupe en plein milieu ne compile pas.
#   3. MARQUEUR_TRONCATURE : marqueurs litteraux de coupure dans le CONTENU
#                          reel ([tronque], [cut], [truncated], 'coupe ici',
#                          'contenu tronque', etc.) - les zones de
#                          DOCUMENTATION (docstrings, blocs de code
#                          markdown, commentaires, citations entre quotes,
#                          lignes qui documentent le motif) sont ignorees :
#                          documenter un marqueur n est pas une troncature.
#
# Usage :
#   python3 detecter-troncatures.py <chemin> [autres...]
#   python3 detecter-troncatures.py --tous
#   python3 detecter-troncatures.py --tous --exclure snapshots --exclure rapports
#   python3 detecter-troncatures.py <chemin> --seuil-lignes 500
#
# Options :
#   --tous                : scanne tous les fichiers de cerveau-projet/
#   --seuil-lignes <n>    : seuil de lignes pour FICHIER_TROUQUE (defaut 2000)
#   --exclure <motif>     : exclut les chemins contenant le motif (repeteble)
#   --rapport <fichier>   : ecrit le rapport markdown
#   --verbose             : detail des detections
#   --version
#
# Version : 0.2.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (detecter-).
# =============================================================================
"""
detecter-troncatures.py
detecter-troncatures

Usage:
  detecter-troncatures.py [OPTIONS]
"""

import argparse
import glob
import io
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

VERSION = "0.2.0"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[0;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}

# Nombre d octets lus au debut d un fichier pour detecter un binaire.
_SEUIL_BINAIRE = 1024


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


EXCLUSIONS = ("__pycache__", ".git", "node_modules", ".backup", ".agents")


def est_exclu(chemin, motifs_utilisateur=()):
    """True si le chemin traverse un dossier exclu par defaut OU contient
    un des motifs utilisateur (--exclure)."""
    normalise = chemin.replace("\\", "/")
    parties = normalise.split("/")
    if any(e in parties for e in EXCLUSIONS):
        return True
    for motif in motifs_utilisateur:
        if motif and motif.replace("\\", "/") in normalise:
            return True
    return False


def est_binaire(chemin):
    """True si le fichier est binaire (octets NUL dans les premiers octets).
    Un binaire n a pas de lignes lisibles : le compter FICHIER_TROUQUE
    serait un faux positif massif (ex : une image de 2613 octets devient
    '2613 lignes')."""
    try:
        with open(chemin, "rb") as fh:
            tete = fh.read(_SEUIL_BINAIRE)
        return b"\x00" in tete
    except Exception:
        return False


# Marqueurs litteraux de coupure : un contenu qui les contient a ete
# probablement tronque (volontairement ou accidentellement) - il devient
# partiellement illisible pour un lecteur.
RE_MARQUEURS = re.compile(
    r"(\[\s*(tronqu\w*|cut|truncated|suite\.{3})\s*\]"
    r"|\b(contenu tronqu\w*|texte tronqu\w*|coupe ici|suite ci[- ]dessous)\b"
    r"|(?:^|\s)\.{6,}(?:\s|$))", re.IGNORECASE)

RE_TRIPLE_BACKTICK = re.compile(r"^```")

# Mots qui signalent que la ligne DOCUMENTE le motif (lecon, doc, test) :
# une ligne qui parle du marqueur n est pas elle-meme tronquee.
_MOTS_DOC_MARQUEUR = (
    "marqueur", "troncature", "MARQUEUR_TRONCATURE", "FICHIER_TROUQUE",
    "BLOC_NON_FERME", "regex", "motif", "detecte", "coupe",
)

# Lignes de commentaires de code (debut de ligne) : documentation, pas contenu.
_RE_COMMENTAIRE = re.compile(r"^\s*(#|//|;|rem\s|--)")


def _lignes_documentation(lignes):
    """Indices des lignes qui sont de la DOCUMENTATION (docstrings Python,
    blocs de code markdown) - les marqueurs y sont cites, pas subis."""
    doc = set()
    ext = ""
    # docstrings Python (triple quotes)
    dans_docstring = False
    for i, ligne in enumerate(lignes):
        stripped = ligne.strip()
        if stripped.startswith('"""') or stripped.startswith("'''"):
            # ouverture ou fermeture (docstring d une seule ligne = les deux)
            if dans_docstring:
                doc.add(i)
                dans_docstring = False
            else:
                if stripped.count('"""') >= 2 or stripped.count("'''") >= 2:
                    doc.add(i)  # docstring sur une seule ligne
                else:
                    doc.add(i)
                    dans_docstring = True
        elif dans_docstring:
            doc.add(i)
    # blocs de code markdown (triple backticks)
    dans_code = False
    for i, ligne in enumerate(lignes):
        if RE_TRIPLE_BACKTICK.match(ligne.strip()):
            doc.add(i)
            dans_code = not dans_code
        elif dans_code:
            doc.add(i)
    return doc


def _ligne_documente_marqueur(ligne):
    """True si la ligne documente le motif (parle du marqueur) au lieu de
    contenir une veritable coupure : commentaire, citation entre quotes,
    mention explicite du motif."""
    if _RE_COMMENTAIRE.match(ligne):
        return True
    # le marqueur est cite entre guillemets simples ou doubles (documentation)
    if re.search(r"['\"][^'\"]*(tronqu|cut|truncated|coupe ici|contenu tronqu)[^'\"]*['\"]", ligne, re.IGNORECASE):
        return True
    # la ligne parle du marqueur (lecon, doc de test, spec de l outil)
    if "MARQUEUR_TRONCATURE" in ligne or "FICHIER_TROUQUE" in ligne or "BLOC_NON_FERME" in ligne:
        return True
    # la ligne parle du marqueur (lecon, doc de test, spec de l outil) :
    # le mot 'marqueur' + un mot du motif = documentation, pas coupure.
    lowered = ligne.lower()
    if "marqueur" in lowered and any(m in lowered for m in
            ("tronqu", "cut", "coupe", "truncat", "troncature")):
        return True
    # le mot 'troncature' ou 'suspension' (concept) signale une
    # documentation du motif (ex : 'hors points de suspension legitimes').
    if "troncature" in lowered or "suspension" in lowered:
        return True
    # ENUMERATION de motifs (2+ marqueurs differents sur la meme ligne) :
    # c est une liste d exemples documentee, pas une coupure unique.
    motifs_trouves = set()
    for m in RE_MARQUEURS.finditer(ligne):
        t = m.group(0).strip().lower()
        motifs_trouves.add(t[:12])
    if len(motifs_trouves) >= 2:
        return True
    return False


def analyser_fichier(chemin, seuil_lignes, motifs_exclure=()):
    """Analyse un fichier. Retourne (problemes, nb_lignes)."""
    problemes = []
    nb_lignes = 0

    # Binaire : pas de lignes lisibles, on ne compte pas FICHIER_TROUQUE.
    if est_binaire(chemin):
        return [], 0

    try:
        with io.open(chemin, encoding="utf-8", errors="replace", newline="") as fh:
            lignes = fh.readlines()
    except Exception as e:
        return [("LECTURE", "fichier illisible : %s" % e)], 0
    nb_lignes = len(lignes)

    # --- 1. FICHIER_TROUQUE : trop de lignes pour une lecture complete
    if nb_lignes > seuil_lignes:
        problemes.append(("FICHIER_TROUQUE",
                          "%d lignes (seuil %d) - tronque par les lecteurs" % (nb_lignes, seuil_lignes)))

    # --- 2. BLOC_NON_FERME : triple backticks dans les .md
    ext = os.path.splitext(chemin)[1].lower()
    if ext in (".md", ".markdown"):
        ouvertures = 0
        for ligne in lignes:
            if RE_TRIPLE_BACKTICK.match(ligne.strip()):
                ouvertures += 1
        # chaque fermeture est aussi une ouverture de triple backtick :
        # un nombre PAIR = blocs fermes ; un nombre IMPAIR = bloc ouvert.
        if ouvertures % 2 != 0:
            problemes.append(("BLOC_NON_FERME",
                              "bloc de code markdown non ferme (%d backticks impairs)" % ouvertures))

    # --- 2b. BLOC_NON_FERME : structure invalide = fichier tronque probable.
    if ext == ".json":
        try:
            import json as _json
            _json.loads("".join(lignes))
        except Exception as e:
            problemes.append(("BLOC_NON_FERME",
                              "JSON invalide (fichier possiblement tronque) : %s" % str(e)[:70]))
    elif ext == ".py":
        try:
            compile("".join(lignes), chemin, "exec")
        except Exception as e:
            problemes.append(("BLOC_NON_FERME",
                              "syntaxe Python invalide (fichier possiblement tronque) : %s" % str(e)[:70]))
    elif ext == ".sh":
        import subprocess
        try:
            r = subprocess.run(["bash", "-n", chemin], capture_output=True,
                               text=True, timeout=30)
            if r.returncode != 0:
                problemes.append(("BLOC_NON_FERME",
                                  "bash -n KO (fichier possiblement tronque) : %s" % r.stderr.strip()[:70]))
        except Exception:
            pass  # bash indisponible : on saute cette verification

    # --- 3. MARQUEUR_TRONCATURE : marqueurs dans le CONTENU reel uniquement.
    #    Les zones de documentation (docstrings, blocs de code, commentaires,
    #    citations) citent les marqueurs sans etre elles-memes tronquees.
    doc = _lignes_documentation(lignes)
    for i, ligne in enumerate(lignes, start=1):
        if (i - 1) in doc:
            continue
        if _ligne_documente_marqueur(ligne):
            continue
        if RE_MARQUEURS.search(ligne):
            extrait = ligne.strip()[:80]
            problemes.append(("MARQUEUR_TRONCATURE",
                              "ligne %d : %s" % (i, extrait)))

    return problemes, nb_lignes


def collecter_fichiers(cibles, tous, racine, motifs_exclure=()):
    """Liste des fichiers a analyser (fichiers directs + dossiers recursifs).
    Le dossier de l outil lui-meme est EXCLU : son en-tete et sa doc
    documentent les motifs de marqueurs (auto-detection parasite)."""
    outil_dir = os.path.dirname(os.path.abspath(__file__))
    fichiers = []
    if tous:
        base = os.path.join(racine, "cerveau-projet")
        for p in glob.glob(os.path.join(base, "**", "*"), recursive=True):
            if (os.path.isfile(p) and not est_exclu(p, motifs_exclure)
                    and not _dans_dossier_outil(p, outil_dir)):
                fichiers.append(p)
        return fichiers
    for c in cibles:
        chemin = c if os.path.isabs(c) else os.path.join(racine, c)
        if os.path.isfile(chemin) and not _dans_dossier_outil(chemin, outil_dir):
            fichiers.append(chemin)
        elif os.path.isdir(chemin):
            for p in glob.glob(os.path.join(chemin, "**", "*"), recursive=True):
                if (os.path.isfile(p) and not est_exclu(p, motifs_exclure)
                        and not _dans_dossier_outil(p, outil_dir)):
                    fichiers.append(p)
        else:
            print(_couleur("  [ERREUR] Cible non trouvee : %s" % c, "rouge"))
    return fichiers


def _dans_dossier_outil(chemin, outil_dir):
    """True si le fichier est dans le dossier de l outil lui-meme."""
    try:
        return os.path.abspath(chemin).startswith(outil_dir + os.sep)
    except Exception:
        return False


def _relatif(chemin, racine):
    """Chemin d affichage relatif a la racine projet ; si le fichier est
    hors projet (autre lecteur, dossier temp), fallback sur le chemin
    absolu (os.path.relpath leve ValueError entre lecteurs differents)."""
    try:
        return os.path.relpath(chemin, racine).replace("\\", "/")
    except ValueError:
        return os.path.abspath(chemin).replace("\\", "/")


def main():
    parser = argparse.ArgumentParser(
        prog="detecter-troncatures",
        description="Detecte les elements tronques donc illisibles (fichiers trop longs, blocs non fermes, marqueurs de troncature).",
    )
    parser.add_argument("cibles", nargs="*", help="Fichier(s) ou dossier(s) a analyser")
    parser.add_argument("--tous", action="store_true", help="Scanne tous les fichiers de cerveau-projet/")
    parser.add_argument("--seuil-lignes", type=int, default=2000,
                        help="Seuil de lignes pour FICHIER_TROUQUE (defaut 2000)")
    parser.add_argument("--exclure", action="append", default=[],
                        metavar="MOTIF",
                        help="Exclut les chemins contenant le motif (repeteble, ex: --exclure snapshots)")
    parser.add_argument("--rapport", type=str, default="", help="Chemin du rapport markdown")
    parser.add_argument("--verbose", action="store_true", help="Detail des detections")
    parser.add_argument("--version", action="version", version="detecter-troncatures %s (%s)" % (VERSION, STATUT))
    parser.add_argument("--aide", action="help", help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    racine = racine_projet()
    if not args.cibles and not args.tous:
        parser.print_help()
        return 2

    fichiers = collecter_fichiers(args.cibles, args.tous, racine, args.exclure)
    fichiers = sorted(set(fichiers))
    if not fichiers:
        print(_couleur("  [ERREUR] Aucun fichier a analyser", "rouge"))
        return 2

    # Analyse PARALLELE (ThreadPoolExecutor) : les verifications par fichier
    # sont independantes. Le scan --tous (976 fichiers, dont ~134 bash -n)
    # passe de ~3.7s a ~2.2s (le bash -n est un sous-processus, les
    # json.loads/compile sont CPU-bound sous GIL : 16 workers suffisent).
    resultats = {}
    with ThreadPoolExecutor(max_workers=16) as pool:
        futurs = {pool.submit(analyser_fichier, f, args.seuil_lignes): f for f in fichiers}
        for fut in futurs:
            f = futurs[fut]
            try:
                resultats[f] = fut.result()
            except Exception as e:
                resultats[f] = ([("LECTURE", "erreur analyse : %s" % str(e)[:70])], 0)

    tous_problemes = []
    lignes_rapport = []
    for f in fichiers:
        rel = _relatif(f, racine)
        problemes, nb = resultats[f]
        if problemes or args.verbose:
            print("== %s (%d lignes)" % (rel, nb))
            for typ, msg in problemes:
                couleur = "rouge" if typ != "MARQUEUR_TRONCATURE" else "jaune"
                print(_couleur("  [%s] %s" % (typ, msg), couleur))
            if not problemes:
                print(_couleur("  OK : aucun probleme de troncature", "vert"))
        tous_problemes.append((rel, problemes))
        lignes_rapport.append((rel, problemes, nb))

    total = sum(len(p) for _, p in tous_problemes)
    print("")
    print("Fichiers analyses : %d" % len(fichiers))
    verdict = "PROPRE" if total == 0 else "%d PROBLEME(S) DE TRONCATURE DETECTE(S)" % total
    print(_couleur("Verdict global : %s" % verdict, "vert" if total == 0 else "rouge"))

    if args.rapport:
        with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Rapport : troncatures detectees\n\n")
            fh.write("Date : %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            fh.write("Fichiers analyses : %d\n" % len(fichiers))
            fh.write("Problemes : %d\n\n" % total)
            for rel, problemes, nb in lignes_rapport:
                fh.write("## %s (%d lignes)\n\n" % (rel, nb))
                if problemes:
                    for typ, msg in problemes:
                        fh.write("- **[%s]** %s\n" % (typ, msg))
                else:
                    fh.write("- OK : aucun probleme de troncature\n")
                fh.write("\n")
            fh.write("Verdict : %s\n" % verdict)
        print(_couleur("[OK] Rapport ecrit : %s" % args.rapport, "vert"))

    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
