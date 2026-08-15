#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# generateurs-amelioration.py
#
# Generateur d'amelioration et d'optimisation : pose des LISTES DE QUESTIONS
# par THEME avant toute mission d'amelioration (outil, combo, generateur, carte
# de decision, case, regle...).
#
# POURQUOI :
#   - Quand une demande d'amelioration arrive, l'agent doit se poser les
#     bonnes questions AVANT d'agir pour garantir coherence et meilleure
#     analyse (philosophie : guider sans surcharger les cartes).
#   - Les listes de questions vivent dans themes-amelioration.json : faciles
#     a editer (modifier une question, un ensemble, ajouter un theme).
#
# COMMENT :
#   - Mode interactif (defaut) : --theme <nom> -> pose les questions une par
#     une avec leur RAISON, reponses lues sur l'entree standard.
#   - Mode non-interactif (testable) : --reponses "q1=...;q2=..." -> reponses
#     fournies sans saisie.
#   - --liste : affiche les themes disponibles.
#   - Fin : RECAPITULATIF des questions/reponses (checklist parcourue).
#     AUCUN fichier cree (decision utilisateur : la reflexion reste en session).
# =============================================================================

"""
generateurs-amelioration.py
generateurs-amelioration

Usage:
  generateurs-amelioration.py [OPTIONS]
"""

import io
import json
import os
import sys

VERSION = "2.1.0"
STATUT = "ebauche"

DOSSIER = os.path.dirname(os.path.abspath(__file__))
THEMES = os.path.join(DOSSIER, "themes-amelioration.json")


def couleur(texte, code):
    if not sys.stdout.isatty():
        return texte
    return "\033[%sm%s\033[0m" % (code, texte)


def charger_themes():
    """Charge themes-amelioration.json. Retourne (donnees, erreur)."""
    try:
        with io.open(THEMES, encoding="utf-8") as fh:
            d = json.load(fh)
        themes = d.get("themes", [])
        if not isinstance(themes, list) or not themes:
            return None, "Aucun theme dans %s" % THEMES
        return d, None
    except Exception as e:
        return None, "Impossible de lire %s : %s" % (THEMES, e)


def trouver_theme(themes, nom):
    for t in themes:
        if t.get("nom") == nom:
            return t
    return None


def lister_themes(themes, version_themes="?"):
    print("=== Themes d'amelioration disponibles (%d) - themes v%s ===" % (len(themes), version_themes))
    for t in themes:
        nom = t.get("nom", "?")
        desc = t.get("description", "")
        nb = len(t.get("questions", []))
        print("  - %-24s (%d questions) : %s" % (nom, nb, desc))


def poser(question, numero, total):
    """Affiche la question (avec sa raison) et retourne la reponse."""
    q = question.get("question", "?")
    raison = question.get("raison", "")
    qid = question.get("id", "q%d" % numero)
    print(couleur("[Question %d/%d - %s] %s" % (numero, total, qid, q), "jaune"))
    if raison:
        print(couleur("  (pourquoi : %s)" % raison, "cyan"))
    try:
        reponse = input("> ").strip()
    except EOFError:
        return None
    return reponse


def recapituler(reponses, questions):
    """Affiche la checklist parcourue (question -> reponse)."""
    print("")
    print("=== RECAPITULATIF : checklist d'amelioration parcourue ===")
    for numero, question in enumerate(questions, 1):
        qid = question.get("id", "q%d" % numero)
        reponse = reponses.get(qid, "")
        print("  [%s] %s" % ("X" if reponse else " ", qid))
        if reponse:
            print("       -> %s" % reponse)
    print("=== FIN DU QUESTIONNAIRE : synthetiser les reponses avant d agir ===")


def main():
    args = sys.argv[1:]
    donnees, erreur = charger_themes()
    if erreur:
        # --version ne depend pas du fichier de themes (jamais de blocage)
        if "--version" in args:
            print("generateurs-amelioration v%s (%s) - themes v?" % (VERSION, STATUT))
            return 0
        print("ERREUR : %s" % erreur)
        return 1
    themes = donnees["themes"]
    version_themes = donnees.get("version", "?")

    if "--version" in args:
        print("generateurs-amelioration v%s (%s) - themes v%s" % (VERSION, STATUT, version_themes))
        return 0

    if "--aide" in args or "-h" in args or "--help" in args:
        print("generateurs-amelioration v%s (%s) - themes v%s" % (VERSION, STATUT, version_themes))
        print("USAGE : generateurs-amelioration.py --theme <nom> [--reponses 'q1=...;q2=...']")
        print("        generateurs-amelioration.py --liste")
        print("        generateurs-amelioration.py --aide")
        print("")
        lister_themes(themes, version_themes)
        return 0

    if "--liste" in args:
        lister_themes(themes, version_themes)
        return 0

    # Extraction du theme
    theme_nom = None
    if "--theme" in args:
        idx = args.index("--theme")
        if idx + 1 < len(args):
            theme_nom = args[idx + 1]
    if not theme_nom:
        print("USAGE : generateurs-amelioration.py --theme <nom> [--reponses 'q1=...;q2=...']")
        print("        generateurs-amelioration.py --liste")
        print("        generateurs-amelioration.py --version")
        lister_themes(themes, version_themes)
        return 1

    theme = trouver_theme(themes, theme_nom)
    if theme is None:
        print("ERREUR : theme '%s' inconnu." % theme_nom)
        lister_themes(themes, version_themes)
        return 1

    questions = theme.get("questions", [])
    if not questions:
        print("ERREUR : le theme '%s' n'a aucune question." % theme_nom)
        return 1

    # Reponses fournies (non-interactif, testable)
    reponses_pre = {}
    if "--reponses" in args:
        idx = args.index("--reponses")
        if idx + 1 < len(args):
            for couple in args[idx + 1].split(";"):
                if "=" in couple:
                    cle, valeur = couple.split("=", 1)
                    reponses_pre[cle.strip()] = valeur.strip()

    print("=== Theme : %s ===" % theme.get("nom", theme_nom))
    print(theme.get("description", ""))
    print("")

    reponses = {}
    for numero, question in enumerate(questions, 1):
        qid = question.get("id", "q%d" % numero)
        if qid in reponses_pre:
            reponses[qid] = reponses_pre[qid]
            print("[Question %d/%d - %s] %s" % (numero, len(questions), qid,
                                                question.get("question", "?")))
            print("> %s" % reponses[qid])
            continue
        rep = poser(question, numero, len(questions))
        if rep is None:
            rep = ""
        reponses[qid] = rep

    recapituler(reponses, questions)
    return 0


if __name__ == "__main__":
    sys.exit(main())
