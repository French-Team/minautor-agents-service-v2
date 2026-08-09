#!/usr/bin/env python3
# -*- coding: ascii -*-
# cartographier-parcours.py
# Genere la CARTOGRAPHIE d'un parcours de decision (parcours JSON) dans un
# fichier markdown : arbre ASCII des cases (indentation par profondeur, types,
# titres, branches marquees et fins) + sections detaillees (impasses, boucles,
# chemins principaux de la case Mission aux fins).
# Sortie par defaut : <dossier-du-parcours>/cartographie-<agent>.md
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# REGLE IMMUABLE DE NOMMAGE : le nom DOIT commencer par le
# prefixe du dossier de categorie (cartographier-) : controle au demarrage.
# REGLE IMMUABLE : 100% stdlib Python.
# REGLE IMMUABLE : ASCII strict (aucun accent, emoji ou Unicode).
# ============================================================

import argparse
import json
import sys
from collections import deque
from pathlib import Path

VERSION = "0.1.0"
STATUT = "ebauche"

# Racine du projet : 5 remontees depuis ce fichier
# (cartographier-parcours -> cartographier -> tools -> agents -> cerveau-projet -> racine)
RACINE = Path(__file__).resolve().parents[5]

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def verifier_nommage(script_path):
    chemin = Path(script_path)
    nom_fichier = chemin.stem
    if nom_fichier == "outil-template":
        return
    dossier = chemin.parent.name
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


# ------------------------------------------------------------
# Chargement du parcours (lecture seule)
# ------------------------------------------------------------

def charger_parcours(chemin):
    """Charge le parcours JSON et valide sa structure de base (sans modifier)."""
    chemin = Path(chemin)
    if not chemin.exists():
        print(_couleur("ERREUR: Parcours introuvable: %s" % chemin, "rouge"), file=sys.stderr)
        sys.exit(1)
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            donnees = json.load(f)
    except json.JSONDecodeError as e:
        print(_couleur("ERREUR: JSON invalide: %s" % e, "rouge"), file=sys.stderr)
        sys.exit(1)
    if "parcours" not in donnees or "cases" not in donnees:
        print(_couleur("ERREUR: Structure invalide (attendu: parcours + cases)", "rouge"), file=sys.stderr)
        sys.exit(1)
    return donnees


# ------------------------------------------------------------
# Analyse des chemins (BFS, logique generateurs-carte reutilisee)
# ------------------------------------------------------------

def analyser_chemins(donnees):
    """Retourne tous les chemins de case_depart vers les fins (BFS, anti-boucle)."""
    cases = donnees["cases"]
    depart = donnees["parcours"].get("case_depart")
    chemins = []
    file = deque([[depart]])
    limite = 10000
    while file and len(chemins) < limite:
        chemin = file.popleft()
        derniere = chemin[-1]
        case = cases.get(derniere)
        if case is None:
            continue
        if case.get("type") == "fin":
            chemins.append(chemin)
            continue
        suivants = []
        if case.get("suivant"):
            suivants.append(case["suivant"])
        for branche in case.get("branches", []):
            if branche.get("vers"):
                suivants.append(branche["vers"])
        if not suivants:
            chemins.append(chemin + [None])  # impasse
            continue
        for nxt in suivants:
            if nxt in chemin:
                continue  # evite les boucles
            file.append(chemin + [nxt])
    return chemins


# ------------------------------------------------------------
# Construction de l'arbre ASCII
# ------------------------------------------------------------

def construire_arbre(donnees):
    """Construit l'arbre ASCII des cases depuis case_depart (anti-boucle).

    Retourne une liste de lignes. Chaque case est affichee UNE fois (premiere
    occurrence) ; les convergences (case deja affichee) sont marquees
    [convergence] sans descendre. Les branches portent leur reponse et les
    fins leur titre -- lecture rapide du flux de decision.
    """
    cases = donnees["cases"]
    depart = donnees["parcours"].get("case_depart")
    lignes = []
    affichees = set()

    def nom_case(cid):
        c = cases.get(cid, {})
        type_c = c.get("type", "?")
        titre = c.get("titre", c.get("question", "")) or ""
        return "[%s] (%s) %s" % (cid, type_c, titre)

    def descendre(cid, prefixe, lien, contexte):
        """Affiche la case cid avec son lien, puis descend dans ses sorties."""
        if cid is None or cid not in cases:
            return
        if cid in affichees:
            lignes.append("%s%s %s  [convergence]" % (prefixe, lien, nom_case(cid)))
            return
        affichees.add(cid)
        suffixe = "  (%s)" % contexte if contexte else ""
        lignes.append("%s%s %s%s" % (prefixe, lien, nom_case(cid), suffixe))
        case = cases[cid]
        cibles = []
        if case.get("suivant"):
            cibles.append(("suivant", case["suivant"]))
        for b in case.get("branches", []):
            if b.get("vers"):
                cibles.append(("branche " + b.get("reponse", "?"), b["vers"]))
        nb = len(cibles)
        for i, (ctx, dst) in enumerate(cibles):
            dern = (i == nb - 1)
            nlien = "`--" if dern else "|--"
            npre = prefixe + ("    " if dern else "|   ")
            descendre(dst, npre, nlien, ctx)

    descendre(depart, "", "--", None)
    return lignes


# ------------------------------------------------------------
# Generation du rendu markdown
# ------------------------------------------------------------

def generer_rendu(donnees, chemin_source):
    """Construit le contenu markdown complet de la cartographie."""
    cases = donnees["cases"]
    parc = donnees["parcours"]
    depart = parc.get("case_depart")
    agent = parc.get("agent", "inconnu")
    version = parc.get("version", "?")
    nom = parc.get("nom", "?")
    chemins = analyser_chemins(donnees)

    # Boucles detectees : case pointant vers une case deja du chemin courant
    boucles = []
    for cid, case in cases.items():
        cibles = []
        if case.get("suivant"):
            cibles.append(("suivant", case["suivant"]))
        for b in case.get("branches", []):
            if b.get("vers"):
                cibles.append((b.get("reponse", "?"), b["vers"]))
        for src, dst in cibles:
            if dst == cid:
                boucles.append("case %s -> elle-meme (%s)" % (cid, src))

    # Impasses : cases non-fin sans sortie
    impasses = []
    for cid, case in cases.items():
        if case.get("type") != "fin" and not case.get("suivant") and not case.get("branches"):
            impasses.append(cid)

    lignes = []
    lignes.append("# Cartographie du parcours : %s" % nom)
    lignes.append("")
    lignes.append("> Generee par `cartographier-parcours` (v%s) depuis `%s`" % (VERSION, chemin_source))
    lignes.append("")
    lignes.append("| Champ | Valeur |")
    lignes.append("|---|---|")
    lignes.append("| Agent | %s |" % agent)
    lignes.append("| Version du parcours | %s |" % version)
    lignes.append("| Case de depart | %s |" % depart)
    lignes.append("| Nombre de cases | %d |" % len(cases))
    lignes.append("| Nombre de chemins (depart -> fins) | %d |" % len(chemins))
    lignes.append("")
    lignes.append("## Arbre des cases")
    lignes.append("")
    lignes.append("```")
    lignes.extend(construire_arbre(donnees))
    lignes.append("```")
    lignes.append("")

    lignes.append("## Cases sans sortie (impasses)")
    lignes.append("")
    if impasses:
        for cid in impasses:
            lignes.append("- `%s` : %s" % (cid, cases[cid].get("titre", cases[cid].get("question", ""))))
    else:
        lignes.append("- Aucune impasse.")
    lignes.append("")

    lignes.append("## Boucles detectees")
    lignes.append("")
    if boucles:
        for b in boucles:
            lignes.append("- %s" % b)
    else:
        lignes.append("- Aucune boucle.")
    lignes.append("")

    lignes.append("## Chemins principaux (depart -> fins)")
    lignes.append("")
    if chemins:
        for i, chemin in enumerate(chemins, 1):
            fin = chemin[-1]
            fin_label = cases.get(fin, {}).get("titre", "IMPASSE") if fin else "IMPASSE"
            etapes = []
            for c in chemin:
                if c is None:
                    etapes.append("[impasse]")
                else:
                    etapes.append("%s(%s)" % (c, cases[c].get("type", "?")))
            lignes.append("%d. **%s** : %s" % (i, fin_label, " -> ".join(etapes)))
    else:
        lignes.append("- Aucun chemin trouve.")
    lignes.append("")
    return "\n".join(lignes)


def chemin_sortie_defaut(chemin_parcours, agent):
    """Chemin par defaut : meme dossier que le parcours, cartographie-<agent>.md."""
    return Path(chemin_parcours).parent / ("cartographie-%s.md" % agent)


# ------------------------------------------------------------
# Action principale
# ------------------------------------------------------------

def action_cartographier(args):
    donnees = charger_parcours(args.parcours)
    agent = donnees["parcours"].get("agent", "agent")
    sortie = Path(args.sortie) if args.sortie else chemin_sortie_defaut(args.parcours, agent)

    if args.dry_run:
        print(_couleur(
            "[DRY-RUN] Cartographie de '%s' (%s cases) generee a %s"
            % (args.parcours, len(donnees["cases"]), sortie),
            "jaune",
        ))
        return 0

    contenu = generer_rendu(donnees, args.parcours)
    try:
        contenu.encode("ascii")
    except UnicodeEncodeError:
        print(_couleur("ERREUR: Contenu non-ASCII refuse (regle immuable)", "rouge"), file=sys.stderr)
        sys.exit(1)

    sortie.parent.mkdir(parents=True, exist_ok=True)
    with open(sortie, "w", encoding="ascii", newline="\n") as f:
        f.write(contenu)
        f.write("\n")

    nb_chemins = len(analyser_chemins(donnees))
    print(_couleur(
        "[OK] Cartographie generee : %s (%d cases, %d chemins)"
        % (sortie, len(donnees["cases"]), nb_chemins),
        "vert",
    ))
    return 0


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def construire_parser():
    parser = argparse.ArgumentParser(
        prog="cartographier-parcours",
        description="Genere la cartographie (arbre ASCII + chemins + anomalies) d'un parcours de decision dans un fichier markdown.",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("parcours", type=str, help="Chemin du parcours JSON a cartographier")
    parser.add_argument("-o", "--sortie", type=str, default=None,
                        help="Chemin du fichier markdown de sortie (defaut: <dossier-du-parcours>/cartographie-<agent>.md)")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans ecrire le fichier")
    parser.add_argument("--verbose", action="store_true", help="Afficher les details")
    parser.add_argument("--version", action="version", version="cartographier-parcours v%s" % VERSION)
    return parser


def main():
    verifier_nommage(sys.argv[0])
    parser = construire_parser()
    args = parser.parse_args()
    return action_cartographier(args)


if __name__ == "__main__":
    sys.exit(main())
