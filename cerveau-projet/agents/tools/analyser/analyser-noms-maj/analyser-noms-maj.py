#!/usr/bin/env python3
# -*- coding: ascii -*-
# analyser-noms-maj.py
#
# Analyse la casse et la forme des NOMS references dans les fichiers du
# cerveau-projet : registre-usages-outils, historique, catalogue-commandes,
# index-tools. Deniche les ORPHELINS (nom reference sans cible reelle) et
# les ERREURS DE NOMMAGE (casse min/MAJ incoherente, chemin au lieu d un
# nom d outil normalise, nom de fonction dans une commande).
#
# Contexte (demande utilisateur 2026-08-16) : les conventions de nommage
# existantes (detecter-convention-nommage, corriger-nommage) verifient le
# nommage des FICHIERS mais pas la casse/forme des NOMS REFERENCES dans le
# contenu. Diagnostic Cerberus : 17 entrees du registre ont le champ outil
# = chemin de script temp (tmp-buffy/resync-lock-et-appliquer.py) au lieu
# d un nom kebab-case ; l historique cite des noms de fonctions
# (lancer_protege, charger_protections, detecter_compagnons).
#
# Detections :
#   a. OUTIL_CHEMIN      : registre, champ outil contenant chemin/extension
#                          .py/.sh ou prefixe tmp-/ .tmp- (forme non normalisee)
#   b. OUTIL_ORPHELIN    : nom d outil reference dans catalogue/index/registre
#                          sans dossier reel correspondant (cerveau-projet/
#                          agents/tools/<categorie>/<outil>/)
#   c. OUTIL_CASSE       : occurrence d un nom d outil en casse differente
#                          de la forme canonique (kebab-case minuscule)
#   d. AGENT_INCONNU     : champ agent du registre sans dossier agent reel
#                          (cerveau-projet/agents/<agent>/)
#   e. FONCTION_DANS_COMMANDE : motif snake_case (charger_/lancer_/detecter_/
#                          verifier_/corriger_/valider_/activer_/reactiver_/
#                          enregistrer_/guider_/editer_/generer_/aligner_/
#                          purger_/fusionner_/analyser_/lire_/ecrire_) dans
#                          commandes/raisons (AVERTISSEMENT, non bloquant)
#
# Usage :
#   python3 analyser-noms-maj.py --tous
#   python3 analyser-noms-maj.py --zone registre
#   python3 analyser-noms-maj.py --zone historique
#   python3 analyser-noms-maj.py --zone catalogue
#   python3 analyser-noms-maj.py --zone index
#   python3 analyser-noms-maj.py --tous --rapport rapport-noms-maj.md
#   python3 analyser-noms-maj.py --verbose
#   python3 analyser-noms-maj.py --version
#
# Options :
#   --tous               analyse les 4 zones (registre, historique, catalogue, index)
#   --zone <nom>         zone unique (registre|historique|catalogue|index)
#   --rapport <fichier>  ecrit le rapport markdown
#   --verbose            detail des problemes
#   --no-chrono          coupe le chrono de l outil lui-meme
#   --version            affiche la version
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (analyser-).
# =============================================================================
"""
analyser-noms-maj.py
analyser-noms-maj

Usage:
  analyser-noms-maj.py [OPTIONS]
"""

import argparse
import glob
import io
import json
import os
import re
import sys
import time

VERSION = "0.1.0"
STATUT = "ebauche"

# Triplet chrono (regle immuable des outils)
T_START = time.monotonic()
CHRONO_ACTIF = True

# Motifs de noms de fonctions (snake_case) signales dans les commandes
MOTIFS_FONCTIONS = re.compile(
    r'\b(charger_|analyser_|detecter_|corriger_|verifier_|valider_|lancer_|'
    r'activer_|reactiver_|enregistrer_|guider_|editer_|generer_|aligner_|'
    r'purger_|fusionner_|lire_|ecrire_)[a-z_]+\b')

# Motif d un nom d outil normalise : kebab-case minuscule
RE_NOMMAGE_OK = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')


def _couleur(texte, nom="neutre"):
    codes = {"rouge": 31, "vert": 32, "jaune": 33, "bleu": 34, "neutre": 0}
    if not sys.stdout.isatty():
        return texte
    return "\033[%dm%s\033[0m" % (codes.get(nom, 0), texte)


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(d, "AGENTS.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return os.getcwd()
        d = parent


def lire(chemin):
    if not os.path.exists(chemin):
        return ""
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def lister_outils_reels(racine):
    """Ensemble des noms d outils reels (dossiers tools/<categorie>/<outil>/)."""
    outils = set()
    base = os.path.join(racine, "cerveau-projet", "agents", "tools")
    for categorie in os.listdir(base):
        p = os.path.join(base, categorie)
        if not os.path.isdir(p) or categorie in ("__pycache__",):
            continue
        for nom in os.listdir(p):
            if os.path.isdir(os.path.join(p, nom)) and RE_NOMMAGE_OK.match(nom):
                outils.add(nom)
    return outils


def lister_agents_reels(racine):
    """Ensemble des dossiers agents reels (cerveau-projet/agents/<agent>/)."""
    agents = set()
    base = os.path.join(racine, "cerveau-projet", "agents")
    for nom in os.listdir(base):
        p = os.path.join(base, nom)
        if os.path.isdir(p) and RE_NOMMAGE_OK.match(nom) and nom not in (
                "tools", "classeur-variables", "traces", "regles-immuables"):
            agents.add(nom)
    return agents


def lire_registre(chemin):
    """Liste des entrees JSON du registre."""
    entrees = []
    if not os.path.exists(chemin):
        return entrees
    for ligne in io.open(chemin, encoding="utf-8", errors="replace"):
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            entrees.append(json.loads(ligne))
        except ValueError:
            entrees.append({"_invalide": ligne})
    return entrees


# ---------------------------------------------------------------------------
# Zone REGISTRE
# ---------------------------------------------------------------------------
def analyser_registre(racine, verbose=False):
    """Detecte OUTIL_CHEMIN, AGENT_INCONNU, OUTIL_CASSE, OUTIL_ORPHELIN."""
    problemes = []
    agents_reels = lister_agents_reels(racine)
    outils_reels = lister_outils_reels(racine)
    chemin = os.path.join(racine, "cerveau-projet", "agents", "traces",
                          "registre-usages-outils.jsonl")
    entrees = lire_registre(chemin)
    for i, e in enumerate(entrees, 1):
        if "_invalide" in e:
            problemes.append(("REGISTRE_INVALIDE", "L%d" % i, e["_invalide"][:80]))
            continue
        outil = e.get("outil", "")
        agent = e.get("agent", "")
        # a. OUTIL_CHEMIN : chemin/extension/prefixe temp dans le champ outil
        if outil and (("/" in outil) or ("\\" in outil) or
                      outil.endswith((".py", ".sh")) or
                      outil.startswith(("tmp-", ".tmp-", ".zz-"))):
            problemes.append(("OUTIL_CHEMIN", "L%d" % i,
                              "%s -> outil=[%s]" % (e.get("date", ""), outil)))
        # c. OUTIL_CASSE : nom kebab-case attendu, casse differente
        elif outil and not RE_NOMMAGE_OK.match(outil):
            problemes.append(("OUTIL_CASSE", "L%d" % i,
                              "%s -> outil=[%s]" % (e.get("date", ""), outil)))
        # b. OUTIL_ORPHELIN : nom d outil declare sans dossier reel (hors
        #    scripts temporaires declares mode=script-temporaire)
        elif outil and RE_NOMMAGE_OK.match(outil) and \
                outil not in outils_reels and \
                e.get("mode") != "script-temporaire":
            problemes.append(("OUTIL_ORPHELIN", "L%d" % i,
                              "%s -> outil=[%s]" % (e.get("date", ""), outil)))
        # d. AGENT_INCONNU : agent sans dossier reel
        if agent and agent not in agents_reels:
            problemes.append(("AGENT_INCONNU", "L%d" % i,
                              "%s -> agent=[%s]" % (e.get("date", ""), agent)))
        # e. FONCTION_DANS_COMMANDE (avertissement)
        texte = (e.get("commande", "") or "") + " " + \
                (e.get("contexte", "") or "")
        for m in MOTIFS_FONCTIONS.finditer(texte):
            problemes.append(("FONCTION_DANS_COMMANDE", "L%d" % i,
                              "%s -> %s" % (e.get("date", ""), m.group(0))))
    return problemes


# ---------------------------------------------------------------------------
# Zone HISTORIQUE
# ---------------------------------------------------------------------------
def analyser_historique(racine, verbose=False):
    """Detecte FONCTION_DANS_COMMANDE dans les raisons de AGENTS-historique."""
    problemes = []
    chemin = os.path.join(racine, "AGENTS-historique.md")
    texte = lire(chemin)
    for i, ligne in enumerate(texte.splitlines(), 1):
        for m in MOTIFS_FONCTIONS.finditer(ligne):
            problemes.append(("FONCTION_DANS_COMMANDE", "L%d" % i,
                              m.group(0)))
    return problemes


# ---------------------------------------------------------------------------
# Zone CATALOGUE
# ---------------------------------------------------------------------------
def analyser_catalogue(racine, verbose=False):
    """Detecte OUTIL_ORPHELIN (script sans fichier reel) et OUTIL_CASSE."""
    problemes = []
    outils_reels = lister_outils_reels(racine)
    chemin = os.path.join(racine, "cerveau-projet", "agents", "tools",
                          "generateurs", "generateurs-commande",
                          "catalogue-commandes.json")
    if not os.path.exists(chemin):
        return problemes
    try:
        cat = json.loads(lire(chemin))
    except ValueError as e:
        problemes.append(("CATALOGUE_INVALIDE", "", str(e)[:80]))
        return problemes
    for c in cat.get("commandes", []):
        nom = c.get("nom", "")
        script = c.get("script", "")
        # nom de commande : kebab-case attendu
        if nom and not RE_NOMMAGE_OK.match(nom):
            problemes.append(("OUTIL_CASSE", "commande",
                              "nom=[%s] -> %s" % (nom, script[:60])))
        # script : doit pointer vers un fichier reel
        if script and not os.path.exists(os.path.join(racine, script)):
            problemes.append(("OUTIL_ORPHELIN", "commande",
                              "nom=[%s] script=[%s]" % (nom, script[:80])))
    return problemes


# ---------------------------------------------------------------------------
# Zone INDEX
# ---------------------------------------------------------------------------
def analyser_index(racine, verbose=False):
    """Detecte OUTIL_ORPHELIN : lien markdown de index-tools pointant vers
    un dossier ou fichier inexistant (cible reelle resolue)."""
    problemes = []
    chemin = os.path.join(racine, "cerveau-projet", "agents", "tools",
                          "index-tools.md")
    texte = lire(chemin)
    # lien markdown : ](cible)
    liens = re.findall(r'\]\(([^)]+)\)', texte)
    vus = set()
    for cible in liens:
        cible = cible.strip()
        if not cible or cible in vus:
            continue
        vus.add(cible)
        # cibles externes (http) ignorees
        if cible.startswith(('http://', 'https://', 'mailto:')):
            continue
        # retirer ancre eventuelle
        cible_sans_ancre = cible.split('#')[0]
        if not cible_sans_ancre:
            continue
        # les liens de l index sont relatifs au dossier de index-tools.md
        # (cerveau-projet/agents/tools/), pas a la racine du projet
        cible_abs = os.path.join(os.path.dirname(chemin), cible_sans_ancre)
        if not os.path.exists(cible_abs):
            problemes.append(("OUTIL_ORPHELIN", "index-tools", cible))
    return problemes


# ---------------------------------------------------------------------------
# Rapport
# ---------------------------------------------------------------------------
def produire_rapport(par_zone, fichier, racine):
    """Ecrit le rapport markdown."""
    lignes = []
    lignes.append("# Rapport analyser-noms-maj")
    lignes.append("")
    lignes.append("Date : %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    lignes.append("Version outil : %s" % VERSION)
    lignes.append("")
    total = 0
    for zone, problemes in sorted(par_zone.items()):
        lignes.append("## Zone %s" % zone)
        lignes.append("")
        if not problemes:
            lignes.append("PROPRE : 0 probleme.")
        else:
            lignes.append("%d probleme(s) :" % len(problemes))
            lignes.append("")
            lignes.append("| Type | Emplacement | Detail |")
            lignes.append("|---|---|---|")
            for type_p, emp, detail in problemes:
                lignes.append("| %s | %s | %s |" % (type_p, emp, detail))
                total += 1
        lignes.append("")
    lignes.append("## Verdict global")
    lignes.append("")
    if total == 0:
        lignes.append("OK : %d probleme, 0 ecart." % total)
    else:
        lignes.append("KO : %d probleme(s) (%d avertissement(s) inclus)." % (
            total, sum(1 for z, ps in par_zone.items()
                       for t, e, d in ps if t == "FONCTION_DANS_COMMANDE")))
    contenu = "\n".join(lignes) + "\n"
    with io.open(fichier, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)
    return contenu


def main():
    parser = argparse.ArgumentParser(
        description="Analyser la casse et la forme des noms references "
                    "(orphelins, erreurs de nommage min/MAJ)")
    parser.add_argument("--tous", action="store_true",
                        help="analyser les 4 zones")
    parser.add_argument("--zone", choices=["registre", "historique",
                                           "catalogue", "index"],
                        help="zone unique a analyser")
    parser.add_argument("--rapport", metavar="FICHIER",
                        help="ecrit le rapport markdown")
    parser.add_argument("--verbose", action="store_true",
                        help="detail des problemes")
    parser.add_argument("--no-chrono", action="store_true",
                        help="coupe le chrono")
    parser.add_argument("--version", action="store_true",
                        help="affiche la version")
    args = parser.parse_args()

    global CHRONO_ACTIF
    if args.no_chrono:
        CHRONO_ACTIF = False

    if args.version:
        print("analyser-noms-maj %s (%s)" % (VERSION, STATUT))
        return 0

    racine = racine_projet()

    if args.zone:
        zones = [args.zone]
    else:
        zones = ["registre", "historique", "catalogue", "index"]
    if not args.tous and not args.zone:
        zones = ["registre"]

    par_zone = {}
    total = 0
    for zone in zones:
        t0 = time.monotonic()
        if zone == "registre":
            problemes = analyser_registre(racine, args.verbose)
        elif zone == "historique":
            problemes = analyser_historique(racine, args.verbose)
        elif zone == "catalogue":
            problemes = analyser_catalogue(racine, args.verbose)
        elif zone == "index":
            problemes = analyser_index(racine, args.verbose)
        else:
            problemes = []
        par_zone[zone] = problemes
        total += len(problemes)
        if CHRONO_ACTIF:
            print("[chrono] zone %-10s %.2fs" % (zone, time.monotonic() - t0))

    # Affichage
    print("=== analyser-noms-maj %s ===" % VERSION)
    for zone in sorted(par_zone.keys()):
        problemes = par_zone[zone]
        print("")
        print("== Zone %s : %d probleme(s) ==" % (zone, len(problemes)))
        if not problemes:
            print("  %s" % _couleur("PROPRE", "vert"))
            continue
        for type_p, emp, detail in problemes:
            couleur = "jaune" if type_p == "FONCTION_DANS_COMMANDE" else "rouge"
            print("  [%s] %s %s" % (_couleur(type_p, couleur), emp, detail))

    # Verdict
    print("")
    nb_avert = sum(1 for z, ps in par_zone.items()
                   for t, e, d in ps if t == "FONCTION_DANS_COMMANDE")
    if total == 0:
        print("=== VERDICT : %s ===" % _couleur("OK - 0 probleme", "vert"))
    else:
        print("=== VERDICT : %s (%d probleme(s), %d avertissement(s)) ===" % (
            _couleur("KO", "rouge"), total, nb_avert))

    if args.rapport:
        produire_rapport(par_zone, args.rapport, racine)
        print("Rapport ecrit : %s" % args.rapport)

    if CHRONO_ACTIF:
        print("[chrono] analyser-noms-maj total %.2fs" %
              (time.monotonic() - T_START))
    return 1 if total > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
