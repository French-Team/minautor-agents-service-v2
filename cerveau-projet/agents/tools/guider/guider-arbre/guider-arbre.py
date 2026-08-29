#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
guider-arbre.py
Piloter un ARBRE DE DECISIONS v2-like (refonte cartes v1 en arbres).

L'arbre est le format cible de la refonte 2026-08-27 : les cartes v1
(parcours-<agent>.json avec cases) sont migrees en ARBRES v2-like :
  arbre-<agent>.json  (racine -> branches vers theme-*.json, regles D*)
  theme-<nom>.json    (but + redirects : besoin -> action/procedure + regle)
  fins.json           (fins CENTRALISEES : redirection/activer/reactiver)

Principe (identique a guider-parcours) : l'agent ne lit JAMAIS l'arbre en
entier. Il recoit LA case courante (racine ou theme), repond/choisit, et
l'outil fournit la suivante. Mode AGENT non-bloquant : jamais d'input()
clavier ; sans --reponses, la question est affichee et l'outil s'arrete.

Usage:
  guider-arbre.py <arbre.json> [--reponses 'A|B'] [--liste] [--valider]

Proprietaire : Vulcain (outils v1)
Version : 0.1.0
Statut : ebauche
"""

import argparse
import json
import os
import sys
from pathlib import Path

VERSION = "0.1.0"
STATUT = "ebauche"

# Racine du projet : guider-arbre -> guider -> tools -> agents -> cerveau-projet -> racine
RACINE = Path(__file__).resolve().parents[5]

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "cyan": "\033[0;36m",
    "magenta": "\033[0;35m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
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
        print(_couleur("ERREUR: Le nom '%s' ne commence pas par le prefixe du dossier '%s'"
                       % (nom_fichier, prefixe), "rouge"), file=sys.stderr)
        sys.exit(1)


# ------------------------------------------------------------------
# Chargement
# ------------------------------------------------------------------

def _charger_json(chemin, obligatoire=True):
    """Charger un JSON (chemin absolu ou relatif a la racine)."""
    p = Path(chemin)
    if not p.is_file():
        p = RACINE / chemin
    if not p.is_file():
        if obligatoire:
            print(_couleur("ERREUR: Fichier introuvable: %s" % chemin, "rouge"), file=sys.stderr)
            sys.exit(1)
        return None
    try:
        with p.open(encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        print(_couleur("ERREUR: JSON invalide dans %s: %s" % (chemin, exc), "rouge"), file=sys.stderr)
        sys.exit(1)


def charger_arbre(chemin):
    """Charge l'arbre et verifie sa structure de base."""
    donnees = _charger_json(chemin)
    if "arbre" not in donnees or "racine" not in donnees:
        print(_couleur("ERREUR: L'arbre doit contenir 'arbre' et 'racine'", "rouge"), file=sys.stderr)
        sys.exit(1)
    return donnees


# ------------------------------------------------------------------
# Validation
# ------------------------------------------------------------------

def valider_arbre(donnees, dossier_base):
    """Valide la structure complete : racine -> themes -> fins centralisees."""
    erreurs = []
    meta = donnees.get("arbre", {})
    racine = donnees.get("racine", {})
    fins = donnees.get("fins", {})

    if not racine.get("branches"):
        erreurs.append("racine: branches manquantes")
    for b in racine.get("branches", []):
        vers = b.get("vers")
        if not vers:
            erreurs.append("racine: branche '%s' sans 'vers'" % b.get("reponse", "?"))
            continue
        p = Path(dossier_base) / vers
        if not p.is_file():
            erreurs.append("racine: theme '%s' introuvable (%s)" % (vers, p))

    # fins centralisees
    nom_fins = fins.get("fichier", "fins.json") if fins else "fins.json"
    p_fins = Path(dossier_base) / nom_fins
    if not p_fins.is_file():
        erreurs.append("fins: '%s' introuvable (%s)" % (nom_fins, p_fins))
    else:
        data_fins = json.loads(p_fins.read_text(encoding="utf-8"))
        liste_fins = (data_fins.get("fins") or {}) if isinstance(data_fins, dict) else {}
        # chaque theme doit avoir une fin qui pointe vers une case existante
        for b in racine.get("branches", []):
            vers = b.get("vers")
            if not vers:
                continue
            p_theme = Path(dossier_base) / vers
            if not p_theme.is_file():
                continue
            try:
                data_theme = json.loads(p_theme.read_text(encoding="utf-8"))
            except ValueError:
                erreurs.append("%s: JSON invalide" % vers)
                continue
            fin = (data_theme.get("fin") or {}) if isinstance(data_theme, dict) else {}
            if fin.get("type") != "lien":
                erreurs.append("%s: fin de theme absente ou non 'lien'" % vers)
            elif fin.get("case") and fin.get("case") not in liste_fins:
                erreurs.append("%s: fin -> case '%s' introuvable dans %s"
                               % (vers, fin.get("case"), nom_fins))

    if erreurs:
        for e in erreurs:
            print(_couleur("ERREUR: " + e, "rouge"), file=sys.stderr)
        sys.exit(1)
    print(_couleur("ARBRE VALIDE : racine -> themes -> fins centralisees", "vert"))
    return True


def lister_arbre(donnees, dossier_base):
    """Affiche la structure de l'arbre (racine, branches, themes, fins)."""
    meta = donnees.get("arbre", {})
    racine = donnees.get("racine", {})
    print("=== Arbre %s (v%s) ===" % (meta.get("nom", "?"), (meta.get("version") or "?")))
    print("Agent : %s" % meta.get("agent", "?"))
    print("Racine : %s" % racine.get("titre", "?"))
    for b in racine.get("branches", []):
        print("  [%s] -> %s" % (b.get("reponse", "?"), b.get("vers", "?")))
    print("")
    for b in racine.get("branches", []):
        vers = b.get("vers")
        if not vers:
            continue
        p = Path(dossier_base) / vers
        if not p.is_file():
            continue
        data_theme = json.loads(p.read_text(encoding="utf-8"))
        theme = data_theme.get("theme", {})
        print("== THEME %s ==" % theme.get("nom", vers))
        print("But : %s" % theme.get("but", ""))
        for i, r in enumerate(theme.get("redirects", []), 1):
            print("  [%d] %s" % (i, r.get("besoin", "?")))
        print("")
    return 0


# ------------------------------------------------------------------
# Affichage d'un theme
# ------------------------------------------------------------------

def afficher_redirect(redirect, numero):
    """Affiche un besoin du theme (action, description, etapes, regle)."""
    print(_couleur("--- Besoin [%d] : %s ---" % (numero, redirect.get("besoin", "?")), "cyan"))
    if redirect.get("action"):
        print("Action : %s" % redirect.get("action"))
    if redirect.get("description"):
        print("Description : %s" % redirect.get("description"))
    for etape in redirect.get("etapes", []):
        print(_couleur("  > ", "jaune") + etape)
    if redirect.get("regle"):
        print(_couleur("[REGLE] ", "rouge") + redirect.get("regle"))
    print("")


def afficher_theme(data_theme):
    """Affiche un theme : nom, but, liste des besoins (redirects)."""
    theme = data_theme.get("theme", {})
    print("")
    print(_couleur("=== THEME : %s ===" % theme.get("nom", "?"), "vert"))
    if theme.get("but"):
        print("But : %s" % theme.get("but"))
    redirects = theme.get("redirects", [])
    print("")
    for i, r in enumerate(redirects, 1):
        print("  [%d] %s" % (i, r.get("besoin", "?")))
    print("")


# ------------------------------------------------------------------
# Navigation
# ------------------------------------------------------------------

def naviguer(donnees, dossier_base, reponses_predefinies):
    """Parcourt l'arbre : racine -> theme -> besoin -> fin centralisee.

    Mode AGENT (defaut) : jamais d'input bloquant. Quand une question est
    atteinte sans reponse predefinie, elle est affichee et l'outil s'arrete
    proprement : l'agent repond puis relance avec --reponses 'REPONSE'.
    """
    meta = donnees.get("arbre", {})
    racine = donnees.get("racine", {})
    fins_cfg = donnees.get("fins", {}) or {}
    nom_fins = fins_cfg.get("fichier", "fins.json")
    data_fins = _charger_json(Path(dossier_base) / nom_fins, obligatoire=True)
    liste_fins = (data_fins.get("fins") or {}) if isinstance(data_fins, dict) else {}

    idx = 0

    def prochaine_reponse():
        nonlocal idx
        if reponses_predefinies is not None and idx < len(reponses_predefinies):
            r = reponses_predefinies[idx].strip()
            idx += 1
            return r
        return None

    # --- Etape 1 : la racine ---
    print(_couleur("=== RACINE : %s ===" % racine.get("titre", "?"), "vert"))
    if racine.get("question"):
        print(_couleur("QUESTION : %s" % racine.get("question"), "cyan"))
    branches = racine.get("branches", [])
    for i, b in enumerate(branches, 1):
        print("  [%d] %s" % (i, b.get("reponse", "?")))
    print("")

    rep = prochaine_reponse()
    if rep is None:
        _question_agent("Choisir une branche (racine)", branches)
        return 0

    branche = _resoudre(branches, rep)
    if branche is None:
        print(_couleur("REPONSE INCONNUE: '%s'. Branches : %s" % (
            rep, " / ".join(b.get("reponse", "?") for b in branches)), "rouge"))
        return 1
    vers = branche.get("vers")
    data_theme = _charger_json(Path(dossier_base) / vers, obligatoire=True)

    # --- Etape 2 : le theme ---
    afficher_theme(data_theme)
    theme = data_theme.get("theme", {})
    redirects = theme.get("redirects", [])
    rep2 = prochaine_reponse()
    if rep2 is None:
        _question_agent("Choisir un besoin du theme %s" % theme.get("nom", "?"),
                        [{"reponse": r.get("besoin", "?")} for r in redirects])
        return 0

    # choisir le besoin par numero ou texte
    redirect = None
    if rep2.isdigit():
        i = int(rep2) - 1
        if 0 <= i < len(redirects):
            redirect = redirects[i]
    else:
        for r in redirects:
            if r.get("besoin", "").strip().lower() == rep2.lower():
                redirect = r
                break
    if redirect is None:
        print(_couleur("BESOIN INCONNU: '%s'. Besoins : %s" % (
            rep2, " / ".join(r.get("besoin", "?") for r in redirects)), "rouge"))
        return 1

    # --- Etape 3 : le besoin (procedure) ---
    afficher_redirect(redirect, 1)

    # --- Etape 4 : la fin du theme -> fins.json ---
    fin_theme = data_theme.get("fin", {})
    case = fin_theme.get("case", "fin-theme")
    fin = liste_fins.get(case)
    if not fin:
        print(_couleur("ERREUR: fin '%s' introuvable dans %s" % (case, nom_fins), "rouge"),
              file=sys.stderr)
        return 1
    print(_couleur("=== FIN : %s ===" % fin.get("titre", case), "magenta"))
    if fin.get("description"):
        print(fin.get("description"))
    if fin.get("action"):
        print("Action : %s" % fin.get("action"))
    if fin.get("commande"):
        print(_couleur("  > ", "cyan") + fin.get("commande"))
    if fin.get("regle"):
        print(_couleur("[REGLE] ", "rouge") + fin.get("regle"))
    print("")
    print(_couleur("=== ARBRE TERMINE ===", "vert"))
    return 0


def _question_agent(titre, choix):
    """Affiche une question pour l'agent et s'arrete proprement (mode agent)."""
    print("")
    print(_couleur("=== QUESTION POUR L'AGENT === ", "cyan") + titre)
    print("Tu es un AGENT, tu vis dans la console : tu ne reponds a aucune")
    print("invite interactive. Reponds selon ton etat reel puis fournis ta")
    print("reponse PAR LA CONSOLE en relancant DEPUIS CETTE ETAPE :")
    print("  guider-arbre <arbre.json> --reponses 'REPONSE'")
    if choix:
        print("Reponses possibles : %s" % " / ".join(c.get("reponse", "?") for c in choix))
    print("")


def _resoudre(choix, reponse):
    """Trouve le choix correspondant (numero ou texte)."""
    rep = reponse.strip()
    if rep.isdigit():
        i = int(rep) - 1
        if 0 <= i < len(choix):
            return choix[i]
        return None
    for c in choix:
        if c.get("reponse", "").strip().lower() == rep.lower():
            return c
    return None


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def construire_parser():
    parser = argparse.ArgumentParser(
        prog="guider-arbre",
        description="Pilote un arbre de decisions v2-like (racine -> themes -> fins centralisees)",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("arbre", type=str, help="Chemin du fichier arbre-<agent>.json")
    parser.add_argument("--reponses", type=str, default=None,
                        help="Reponses fournies d'un coup, separees par | (mode agent)")
    parser.add_argument("--liste", action="store_true", help="Lister la structure sans naviguer")
    parser.add_argument("--valider", action="store_true", help="Valider la structure (liens + fins)")
    parser.add_argument("--version", action="version", version="guider-arbre v%s" % VERSION)
    return parser


def main():
    verifier_nommage(sys.argv[0])
    parser = construire_parser()
    parser.add_argument("--aide", action="help", help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    donnees = charger_arbre(args.arbre)
    dossier_base = os.path.dirname(os.path.abspath(args.arbre))

    if args.liste:
        return lister_arbre(donnees, dossier_base)
    if args.valider:
        return 0 if valider_arbre(donnees, dossier_base) else 1

    reponses = None
    if args.reponses is not None:
        reponses = [r.strip() for r in args.reponses.split("|")]
    return naviguer(donnees, dossier_base, reponses)


if __name__ == "__main__":
    sys.exit(main())
