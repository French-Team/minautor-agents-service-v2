#!/usr/bin/env python3
# -*- coding: ascii -*-
# guider-parcours.py
# Guide l'agent case par case (jeu de piste) : affiche la case courante
# (question + indices outil/fichier/regle), suit les branches selon la reponse.
# Version : 0.1.0
# Statut : ebauche

# ============================================================
# GUIDE-PARCOURS - OUTIL DE NAVIGATION EN CASES
# ============================================================
# Principe : l'agent ne lit plus les fiches d'avance. L'outil lit un
# parcours JSON et fait avancer l'agent une case a la fois. Chaque case
# donne l'indice exact (outil a lancer, fichier a lire, regle a appliquer)
# et une question. Selon la reponse, l'agent suit une branche.
# ============================================================
# REGLE IMMUABLE DE NOMMAGE : dossier 'guider/' -> prefixe 'guide-'
# ============================================================
# REGLE IMMUABLE : 100% stdlib Python
# ============================================================
# REGLE IMMUABLE : ASCII strict (aucun accent, emoji, caractere Unicode)
# ============================================================

import argparse
import json
import sys
from pathlib import Path

VERSION = "0.1.0"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "cyan": "\033[0;36m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    """Colore le texte si le terminal le supporte, sinon texte brut."""
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def verifier_nommage(script_path):
    """Regle immuable : le nom du fichier commence par le prefixe du dossier."""
    chemin = Path(script_path)
    nom_fichier = chemin.stem
    dossier = chemin.parent.name
    if nom_fichier == "outil-template":
        return
    prefixe = dossier.split("-")[0] + "-"
    if not nom_fichier.startswith(prefixe):
        print(
            _couleur(
                "ERREUR: Le nom '%s' ne commence pas par le prefixe du dossier '%s'"
                % (nom_fichier, prefixe),
                "rouge",
            ),
            file=sys.stderr,
        )
        sys.exit(1)


# ------------------------------------------------------------------
# Lecture et validation du parcours
# ------------------------------------------------------------------

def charger_parcours(chemin):
    """Charge le JSON du parcours et verifie sa structure de base."""
    p = Path(chemin)
    if not p.is_file():
        print(_couleur("ERREUR: Fichier de parcours introuvable: %s" % chemin, "rouge"), file=sys.stderr)
        sys.exit(1)
    try:
        with p.open(encoding="utf-8") as fh:
            donnees = json.load(fh)
    except json.JSONDecodeError as exc:
        print(_couleur("ERREUR: JSON invalide dans %s: %s" % (chemin, exc), "rouge"), file=sys.stderr)
        sys.exit(1)
    if "parcours" not in donnees or "cases" not in donnees:
        print(_couleur("ERREUR: Le parcours doit contenir 'parcours' et 'cases'", "rouge"), file=sys.stderr)
        sys.exit(1)
    return donnees


def valider_parcours(donnees):
    """Valide la structure complete : cases atteignables, branches existantes."""
    meta = donnees.get("parcours", {})
    cases = donnees.get("cases", {})
    depart = meta.get("case_depart")
    erreurs = []
    if not depart:
        erreurs.append("case_depart manquant dans parcours")
    elif depart not in cases:
        erreurs.append("case_depart '%s' introuvable dans cases" % depart)
    for cid, case in cases.items():
        suivant = case.get("suivant")
        branches = case.get("branches")
        if suivant and suivant not in cases:
            erreurs.append("case '%s': suivant '%s' introuvable" % (cid, suivant))
        for b in branches or []:
            vers = b.get("vers")
            if vers and vers not in cases:
                erreurs.append("case '%s': branche vers '%s' introuvable" % (cid, vers))
    if erreurs:
        for e in erreurs:
            print(_couleur("ERREUR: " + e, "rouge"), file=sys.stderr)
        sys.exit(1)
    return True


def lister_cases(donnees):
    """Affiche l'inventaire des cases (id, titre, type)."""
    meta = donnees.get("parcours", {})
    cases = donnees.get("cases", {})
    print("=== Parcours %s v%s ===" % (meta.get("nom", "?"), meta.get("version", "?")))
    print("Agent : %s | Depart : %s" % (meta.get("agent", "?"), meta.get("case_depart", "?")))
    print("")
    for cid, case in cases.items():
        print("  [%s] %-8s %s" % (cid, case.get("type", "?"), case.get("titre", "")))
    return 0


# ------------------------------------------------------------------
# Affichage d'une case
# ------------------------------------------------------------------

def afficher_indices(indices):
    """Affiche les indices de la case (regle / outil / fichier)."""
    if not indices:
        return
    print("")
    for ind in indices:
        typ = ind.get("type", "")
        if typ == "regle":
            print(_couleur("[REGLE] ", "rouge") + ind.get("texte", ""))
        elif typ == "outil":
            nom = ind.get("nom", "?")
            chemin = ind.get("chemin", "")
            print(_couleur("[OUTIL] ", "bleu") + "%s" % nom)
            if chemin:
                print("         chemin: %s" % chemin)
            if ind.get("commande"):
                print(_couleur("         > ", "cyan") + ind.get("commande"))
        elif typ == "fichier":
            print(_couleur("[FICHIER] ", "jaune") + ind.get("chemin", "?"))
            if ind.get("raison"):
                print("         raison: %s" % ind.get("raison"))
        else:
            print("[INDICE] " + str(ind.get("texte", "")))


def afficher_case(cid, case, total, position):
    """Affiche une case : titre, indices, question, branches."""
    print("")
    print(_couleur("=== [%s/%s] %s ===" % (position, total, case.get("titre", cid)), "vert"))
    afficher_indices(case.get("indices"))
    question = case.get("question")
    branches = case.get("branches") or []
    if question:
        print("")
        print(_couleur("QUESTION : %s" % question, "cyan"))
    for i, b in enumerate(branches, 1):
        print("  [%d] %s" % (i, b.get("reponse", "?")))
    print("")


def reponse_exacte(branches, reponse):
    """Trouve la branche correspondant a la reponse (numero ou texte)."""
    rep = reponse.strip()
    if rep.isdigit():
        idx = int(rep) - 1
        if 0 <= idx < len(branches):
            return branches[idx]
        return None
    for b in branches:
        if b.get("reponse", "").strip().lower() == rep.lower():
            return b
    return None


# ------------------------------------------------------------------
# Navigation
# ------------------------------------------------------------------

def naviguer(donnees, case_debut, reponses_predefinies):
    """Parcourt le parcours case par case."""
    meta = donnees.get("parcours", {})
    cases = donnees.get("cases", {})
    cid = case_debut
    idx_reponses = 0
    total = len(cases)
    position = 0
    # position de la case de depart dans l'ordre du dictionnaire
    ordre = list(cases.keys())
    try:
        position = ordre.index(cid) + 1
    except ValueError:
        position = 0

    while True:
        case = cases[cid]
        typ = case.get("type", "question")
        if typ == "fin":
            print(_couleur("=== PARCOURS TERMINE ===", "vert"))
            print("Fin de parcours atteinte : case '%s' (%s)" % (cid, case.get("titre", "")))
            if case.get("message"):
                print(case.get("message"))
            return 0

        afficher_case(cid, case, total, position if position else ordre.index(cid) + 1)

        branches = case.get("branches") or []
        if typ == "indice":
            # pas de question : passage automatique
            suivant = case.get("suivant")
            if not suivant:
                print(_couleur("ERREUR: case indice '%s' sans 'suivant'" % cid, "rouge"), file=sys.stderr)
                return 1
            cid = suivant
            position = ordre.index(cid) + 1
            continue

        # Question ou controle : attendre une reponse
        if reponses_predefinies is not None:
            if idx_reponses >= len(reponses_predefinies):
                print(_couleur("ERREUR: plus de reponses fournies que de questions (case '%s')" % cid, "rouge"), file=sys.stderr)
                return 1
            rep = reponses_predefinies[idx_reponses].strip()
            idx_reponses += 1
            if rep == "":
                rep = input("> ").strip()
        else:
            rep = input("> ").strip()

        if not branches:
            suivant = case.get("suivant")
            if not suivant:
                print(_couleur("=== PARCOURS TERMINE ===", "vert"))
                return 0
            cid = suivant
        else:
            b = reponse_exacte(branches, rep)
            if b is None:
                print(_couleur("REPONSE INCONNUE: '%s'. Reponses possibles : %s" % (
                    rep, " / ".join(br.get("reponse", "?") for br in branches)), "rouge"))
                if reponses_predefinies is not None:
                    return 1
                continue
            cid = b.get("vers")
        position = ordre.index(cid) + 1


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def construire_parser():
    parser = argparse.ArgumentParser(
        prog="guider-parcours",
        description="Guide l'agent case par case (jeu de piste) selon un parcours JSON",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("parcours", type=str, help="Chemin du fichier de parcours JSON")
    parser.add_argument("--case", type=str, default=None, help="Case de depart (ex: c3)")
    parser.add_argument("--reponses", type=str, default=None, help="Reponses fournies d'un coup, separees par |")
    parser.add_argument("--liste", action="store_true", help="Lister les cases sans naviguer")
    parser.add_argument("--version", action="version", version="guider-parcours v%s" % VERSION)
    return parser


def main():
    verifier_nommage(sys.argv[0])
    parser = construire_parser()
    args = parser.parse_args()

    donnees = charger_parcours(args.parcours)
    valider_parcours(donnees)

    if args.liste:
        return lister_cases(donnees)

    meta = donnees.get("parcours", {})
    case_debut = args.case or meta.get("case_depart")
    reponses = None
    if args.reponses is not None:
        reponses = [r.strip() for r in args.reponses.split("|")]
    return naviguer(donnees, case_debut, reponses)


if __name__ == "__main__":
    sys.exit(main())
