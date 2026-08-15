#!/usr/bin/env python3
# -*- coding: ascii -*-
# guider-parcours.py
# Guide l'agent case par case (jeu de piste) : affiche la case courante
# (question + indices outil/fichier/regle), suit les branches selon la reponse.
# Version : 0.5.1
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

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

"""
guider-parcours.py
guider-parcours

Usage:
  guider-parcours.py [OPTIONS]
"""

import argparse
import io
import json
import os
import re
import sys
from pathlib import Path

VERSION = "0.5.1"
REGEX_RESIDU = re.compile(r"^v?\d+\.\d+\.\d+$")
STATUT = "ebauche"

# Racine du projet : 6 remontees depuis ce fichier
# (guider-parcours -> guider -> tools -> agents -> cerveau-projet -> racine)
RACINE = Path(__file__).resolve().parents[5]
SPEC_GUIDER = RACINE / "cerveau-projet" / "agents" / "tools" / "guider" / "guider-parcours" / "spec" / "spec-guider-parcours.001.01.ebauche.md"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "magenta": "\033[0;35m",
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
    for cid, case in cases.items():
        # Regle 10 (spec v0.2.10) : AUCUNE BOUCLE D'ATTENTE. Une case dont le
        # titre evoque l'attente (attendre/attente) ne doit JAMAIS avoir une
        # branche vers elle-meme : l'attente est une FIN, pas une boucle.
        titre = (case.get("titre", "") + " " + case.get("question", "")).lower()
        if "attendre" in titre or "attente" in titre:
            for b in case.get("branches") or []:
                if b.get("vers") == cid:
                    erreurs.append(
                        "case '%s': BOUCLE D'ATTENTE interdite (branche '%s' -> elle-meme). "
                        "L'attente est une case fin, pas une boucle (spec v0.2.10 regle 10)" % (cid, b.get("reponse"))
                    )
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

def _chemin_doc_outil(nom, chemin):
    """Deduit le chemin du .md de documentation d'un outil depuis son indice.

    Le .md d'un outil vit dans le MEME dossier que l'outil, avec le meme nom
    (ex: agents/tools/lire/lire-fichier/lire-fichier.md). Le chemin de
    l'indice pointe vers le DOSSIER (se termine par /) ou vers un fichier .py/.sh.
    Retourne le chemin du .md deduit, ou None si non deduisible.
    """
    if not chemin:
        return None
    c = chemin.rstrip("/")
    # Le chemin pointe vers un fichier precis (.py/.sh) : remonter au dossier
    if c.endswith(".py") or c.endswith(".sh"):
        dossier = c.rsplit("/", 1)[0]
    else:
        dossier = c
    return dossier + "/" + nom + ".md"


def resoudre_reference(ref):
    """Resout une reference d indice (spec-refonte 7.1 : cle ref) vers son contenu.

    Formats (alignes sur valider-case --references) :
      - pattern-<N> : extrait le titre + 3 lignes du Pattern N de la spec-guider-parcours ;
      - protocole-<x> / regle-<x> : chemin du fichier/dossier trouve dans regles-immuables ;
      - chemin relatif : chemin + existence du fichier.
    Retourne (titre, corps) ou (None, message) si non resolvable.
    """
    # pattern-<N> : titre + corps depuis la spec-guider-parcours
    m = re.match(r"^pattern-(\d+)$", ref)
    if m:
        try:
            lignes = io.open(SPEC_GUIDER, encoding="utf-8").read().split("\n")
        except Exception:
            return None, "(spec-guider-parcours illisible)"
        cible = "### Pattern %s" % m.group(1)
        for i, l in enumerate(lignes):
            if l.strip().startswith(cible):
                titre = l.strip()
                corps = []
                for j in range(i + 1, min(i + 5, len(lignes))):
                    l2 = lignes[j]
                    if l2.strip().startswith("### ") or not l2.strip():
                        if l2.strip().startswith("### "):
                            break
                        continue
                    corps.append(l2.strip())
                    if len(corps) >= 3:
                        break
                return titre, " ".join(corps)[:260]
        return None, "(pattern %s introuvable dans la spec)" % m.group(1)
    # protocole-<x> / regle-<x> : recherche par nom dans regles-immuables
    if ref.startswith("protocole-") or ref.startswith("regle-"):
        dossier = RACINE / "cerveau-projet" / "agents" / "regles-immuables"
        trouve = None
        if dossier.is_dir():
            for racine, dossiers, fichiers in os.walk(str(dossier)):
                for nom in dossiers + fichiers:
                    if nom.startswith(ref):
                        trouve = os.path.join(racine, nom)
                        break
                if trouve:
                    break
        if trouve:
            rel = os.path.relpath(trouve, str(RACINE)).replace("\\", "/")
            return rel, "(reference de regle immuable)"
        return None, "(reference %s introuvable dans regles-immuables)" % ref
    # chemin relatif : fichier existant
    if os.path.isfile(os.path.join(str(RACINE), ref)):
        return ref, "(fichier existant)"
    return ref, "(reference non resolvable)"


def afficher_indices(indices):
    """Affiche les indices de la case (regle / ref / outil / fichier)."""
    if not indices:
        return
    print("")
    for ind in indices:
        typ = ind.get("type", "")
        if typ == "regle":
            print(_couleur("[REGLE] ", "rouge") + ind.get("texte", ""))
        elif typ == "ref":
            ref = ind.get("ref", "")
            titre, corps = resoudre_reference(ref)
            print(_couleur("[REFERENCE] ", "magenta" if "magenta" in _COULEURS else "rouge") + ref)
            if titre:
                print("         -> %s" % titre)
            if corps:
                print("         %s" % corps)
        elif typ == "outil":
            nom = ind.get("nom", "?")
            chemin = ind.get("chemin", "")
            print(_couleur("[OUTIL] ", "bleu") + "%s" % nom)
            if chemin:
                print("         chemin: %s" % chemin)
            if ind.get("commande"):
                print(_couleur("         > ", "cyan") + ind.get("commande"))
            # Piste C (spec v0.2.20) : reference catalogue optionnelle -- compose la
            # commande via generateurs-commande --commande <catalogue> au lieu de l'ecrire en dur
            if ind.get("catalogue"):
                print(_couleur("         catalogue: ", "cyan") + ind.get("catalogue"))
                print(_couleur("         PASSE PAR LE GENERATEUR: ", "cyan") +
                      "python3 cerveau-projet/agents/tools/generateurs/generateurs-commande/generateurs-commande.py --commande " + ind.get("catalogue"))
            # Pattern 9 (spec v0.2.16) : lire le .md de l'outil AVANT de l'executer
            doc = _chemin_doc_outil(nom, chemin)
            if doc:
                if Path(doc).is_file():
                    print(_couleur("         LIRE AVANT USAGE: ", "jaune") + doc)
                else:
                    print(_couleur("         LIRE AVANT USAGE (doc a verifier): ", "jaune") + doc)
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

def naviguer(donnees, case_debut, reponses_predefinies, interactif=False):
    """Parcourt le parcours case par case.

    Mode AGENT (defaut) : jamais d'input bloquant. Quand une question est
    atteinte sans reponse predefinie disponible, la question est affichee et
    l'outil s'arrete proprement : l'agent repond selon son etat reel puis
    relance avec --reponses 'REPONSE'. Les questions sont destinees a
    l'AGENT, jamais a une saisie clavier.
    Mode --interactif : input() clavier, reserve a l'usage humain (tests).
    """
    meta = donnees.get("parcours", {})
    cases = donnees.get("cases", {})
    cid = case_debut
    idx_reponses = 0
    total = len(cases)
    position = 0
    # position de la case de depart dans l'ordre du dictionnaire
    ordre = list(cases.keys())
    # round 9 : une case de depart inexistante (--case c999) provoquait un
    # KeyError traceback brut - l agent perdu doit etre GUIDE, pas crash.
    if cid not in cases:
        dispo = ", ".join(list(cases.keys())[:12])
        if len(cases) > 12:
            dispo += ", ..."
        print(_couleur("ERREUR: la case de depart '%s' n'existe pas dans le parcours" % cid, "rouge"),
              file=sys.stderr)
        print("Cases disponibles : %s" % dispo, file=sys.stderr)
        return 1
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
        if typ in ("indice", "action"):
            # pas de question : passage automatique
            # (action = NOUVEAU type, spec-refonte critere 7 : s execute sans
            #  question et enchaine sur la case suivante, identique a indice)
            suivant = case.get("suivant")
            if not suivant:
                print(_couleur("ERREUR: case %s '%s' sans 'suivant'" % (typ, cid), "rouge"), file=sys.stderr)
                return 1
            cid = suivant
            position = ordre.index(cid) + 1
            continue

        # Question ou controle : reponse de l'agent (jamais d'input bloquant)
        if interactif:
            try:
                rep = input("> ").strip()
            except EOFError:
                print("=== PARCOURS INTERROMPU (fin d'entree) ===")
                return 0
        elif reponses_predefinies is not None and idx_reponses < len(reponses_predefinies):
            rep = reponses_predefinies[idx_reponses].strip()
            idx_reponses += 1
        else:
            # Mode agent : la question est destinee a l'agent. Un agent vit
            # dans la console : il ne repond JAMAIS a une invite interactive.
            # Il repond selon son etat reel puis fournit sa reponse PAR LA
            # CONSOLE en relancant avec --reponses 'REPONSE'.
            print("")
            print(_couleur("=== QUESTION POUR L'AGENT ===", "cyan"))
            print("Tu es un AGENT, tu vis dans la console : tu n'es pas un humain,")
            print("tu ne reponds a aucune invite interactive. Reponds a la question")
            print("ci-dessus selon ton etat reel, puis fournis ta reponse PAR LA CONSOLE")
            print("en relancant DEPUIS CETTE CASE (pour ne pas rejouer c0) :")
            print("  guider-parcours <parcours.json> --case %s --reponses 'REPONSE'" % cid)
            if branches:
                print("Reponses possibles : %s" % " / ".join(b.get("reponse", "?") for b in branches))
            print("")
            return 0

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
    parser.add_argument("--reponses", type=str, default=None, help="Reponses fournies d'un coup, separees par | (mode agent)")
    parser.add_argument("--interactif", action="store_true", help="Mode interactif (input clavier) pour usage humain")
    parser.add_argument("--liste", action="store_true", help="Lister les cases sans naviguer")
    parser.add_argument("--version", action="version", version="guider-parcours v%s" % VERSION)
    return parser


def verifier_residus_racine():
    """GARDE-FOU ANTI-RESIDUS : detecter dans le repertoire courant les fichiers
    nommes comme des versions semver pures (ex: 0.2.1, v0.2.6). Ces fichiers
    sont des residus probables de redirections accidentelles de sortie d une
    commande precedente (souvent la sortie d un outil du cerveau). Anti-residu :
    les supprimer - les sources de verite de version vivent dans
    cerveau-projet/agents/clio/ (version-readme.txt, statut-projet.txt),
    JAMAIS a la racine."""
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


def main():
    verifier_nommage(sys.argv[0])
    parser = construire_parser()
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    verifier_residus_racine()

    donnees = charger_parcours(args.parcours)
    valider_parcours(donnees)

    if args.liste:
        return lister_cases(donnees)

    meta = donnees.get("parcours", {})
    case_debut = args.case or meta.get("case_depart")
    reponses = None
    if args.reponses is not None:
        reponses = [r.strip() for r in args.reponses.split("|")]
    return naviguer(donnees, case_debut, reponses, args.interactif)


if __name__ == "__main__":
    sys.exit(main())
