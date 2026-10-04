#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
evaluer-rating.py
Evalue la qualite et la performance des entites du cerveau-projet (tests,
series, outils, scripts temporaires, fiches) avec une note ponderee /100.

Chaque profil (profils-rating.json) definit des criteres avec POIDS (somme =
100), une source de donnees et un mode de score 0-100. La note finale est la
somme ponderee des scores de critere. Un verdict qualitatif accompagne la note.

Usage:
  evaluer-rating.py --profil <test|serie|outil|script-temp|fiche> --cible <nom>
  evaluer-rating.py --profil test --tous
  evaluer-rating.py --profil serie --tous
  evaluer-rating.py --profil outil --tous
  evaluer-rating.py --profil test --cible test-032-pool-workers.py

Options :
  --profil <nom>       Profil de notation (defaut: test)
  --cible <nom>        Entite a noter (nom de test, serie A-E, chemin d outil,
                       nom de script, nom de fiche)
  --tous               Noter TOUTES les entites du profil + rating general
  --general            Afficher UNIQUEMENT le rating general (rapide)
  --rapport <fichier>  Ecrire le rapport markdown (sans couleurs)
  --verbose            Detail des criteres (score brut + pondere par critere)
  --no-chrono          Couper le chrono de l outil
  --version            Afficher la version
  --aide, -h           Afficher cette aide

Retour: 0 toujours (outil d'evaluation, rapport sur stdout).

Proprietaire : Themis (outil partage)
Version : 0.1.0-py
Statut : beta
"""

import argparse
import io
import json
import os
import sys
import time

VERSION = "0.1.0-py"
STATUT = "beta"

# Couleurs ANSI : desactivees si la sortie n'est pas un terminal.
_ANSI = sys.stdout.isatty()
RED = "\033[0;31m" if _ANSI else ""
GREEN = "\033[0;32m" if _ANSI else ""
YELLOW = "\033[1;33m" if _ANSI else ""
NC = "\033[0m" if _ANSI else ""

# Racine du projet : detection par AGENTS.md (modele detecter-usage-scripts-temporaires)
def trouver_racine():
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.exists(os.path.join(d, "AGENTS.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return os.getcwd()
        d = parent

RACINE = trouver_racine()
DOSSIER_OUTIL = os.path.dirname(os.path.abspath(__file__))
PROFILS_PATH = os.path.join(DOSSIER_OUTIL, "profils-rating.json")
REGISTRE_TESTS = os.path.join(RACINE, "cerveau-projet", "agents", "traces",
                              "registre-tests.jsonl")
REGISTRE_USAGES = os.path.join(RACINE, "cerveau-projet", "agents", "traces",
                               "registre-usages-outils.jsonl")
CLASSEUR = os.path.join(RACINE, "cerveau-projet", "agents",
                        "classeur-variables", "stockage", "variables-actuelles.md")
TESTS_DIR = os.path.join(RACINE, "cerveau-projet", "agents", "tools",
                         "tester", "tests")
OUTILS_DIR = os.path.join(RACINE, "cerveau-projet", "agents", "tools")

MARQUEURS_TEST = [
    "charger_protections",
    "point_actif",
    "chrono_etape",
    "bilan_chrono",
    "coding: ascii",
    "#!/usr/bin/env python3",
    "def verifier",
    "[OK]",
    "[KO]",
    "RESULTAT",
]

MARQUEURS_SCRIPT_TEMP = [
    "coding: ascii",
    "#!/usr/bin/env python3",
    "point_actif",
    "chrono_etape",
    "bilan_chrono",
    "no-chrono",
]

MARQUEURS_FICHE = [
    "identite:",
    "type: fiche",
    "PARCOURS",
    "Vue d",
    "REGLES ABSOLUES",
]

MARQUEURS_OUTIL = [
    "coding: ascii",
    "#!/usr/bin/env python3",
    "Usage:",
    "--version",
    "--aide",
]

SERIES = ["a", "b", "c", "d", "e"]


def trouver_fichier_outil(nom):
    """Cherche le fichier principal d un outil dans l arborescence
    tools/<categorie>/<nom>/ (les outils ne vivent pas directement sous
    tools/ : ils sont groupes par categorie d action)."""
    if os.path.exists(nom):
        return nom
    for categorie in os.listdir(OUTILS_DIR):
        chemin_cat = os.path.join(OUTILS_DIR, categorie)
        if not os.path.isdir(chemin_cat) or categorie.startswith("_"):
            continue
        dossier = os.path.join(chemin_cat, nom)
        if os.path.isdir(dossier):
            for ext in (".py", ".sh"):
                candidat = os.path.join(dossier, nom + ext)
                if os.path.exists(candidat):
                    return candidat
    # Recherche recursive en dernier recours
    import glob
    matches = glob.glob(os.path.join(OUTILS_DIR, "*", nom, nom + ".*"))
    return matches[0] if matches else nom


def charger_profils():
    if not os.path.exists(PROFILS_PATH):
        print(RED + "[ERREUR] profils-rating.json introuvable : " + PROFILS_PATH + NC)
        sys.exit(2)
    with io.open(PROFILS_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def charger_jsonl(chemin):
    """Charge un fichier JSONL en listant les lignes valides."""
    entrees = []
    if not os.path.exists(chemin):
        return entrees
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                entrees.append(json.loads(ligne))
            except ValueError:
                continue
    return entrees


def lire_fichier(chemin):
    if not os.path.exists(chemin):
        return ""
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return fh.read()


# --- Modes de score (chacun retourne un score 0-100) ---

def dernier_run(registre, fenetre_minutes=10):
    """Entrees du dernier run : fenetre temporelle autour de la date la plus
    recente (modele analyser-performance-tests). Un run complet de
    non-regression dure ~100 s, une fenetre de 10 minutes l isole proprement."""
    if not registre:
        return []
    fmt = "%Y-%m-%d %H:%M:%S"
    from datetime import datetime, timedelta
    parsees = []
    for e in registre:
        try:
            d = datetime.strptime(e.get("date", ""), fmt)
            parsees.append((d, e))
        except ValueError:
            continue
    if not parsees:
        return registre
    dmax = max(d for d, _ in parsees)
    seuil = dmax - timedelta(minutes=fenetre_minutes)
    return [e for d, e in parsees if d >= seuil]


def score_temps(entree, registre, base_secondes=3.0, mode_serie=False):
    """Mode plus-rapide-mieux : bareme absolu en secondes (configurable dans
    le profil). Score = 100 si duree <= base, decroit ensuite (20 points par
    multiple de base au-dela, plancher 0). Deterministe et comparable entre
    les runs, contrairement a une base statistique (mediane/moyenne) qui
    depend du contenu de la fenetre."""
    run = dernier_run(registre)
    if not run:
        return 50.0
    # Duree de l entite : pour un test, premiere occurrence dans le run ;
    # pour une serie, SOMME des durees des tests de la serie.
    if mode_serie:
        duree_entite = sum(e.get("duree", 0) for e in run
                           if e.get("serie") == entree)
    else:
        duree_entite = 0.0
        for e in run:
            if matcher_entite(entree, e):
                duree_entite = e.get("duree", 0)
                break
    if duree_entite <= 0:
        return 50.0
    if base_secondes <= 0:
        base_secondes = 3.0
    ratio = duree_entite / base_secondes
    # Pente douce : 20 points par multiple de base au-dela (plancher 0).
    # 3s -> 100, 6s -> 80, 9s -> 60, 12s -> 40, 15s -> 20, 18s+ -> 0
    score = 100.0 - (ratio - 1.0) * 20.0
    return max(0.0, min(100.0, score))


def matcher_entite(entree, e, mode_serie=False):
    """Match une entite sur une entree du registre. Pour les series, le match
    se fait sur le champ 'serie' (jamais sur le nom de test : 'a' matcherait
    tous les tests contenant la lettre a)."""
    if mode_serie:
        return e.get("serie", "") == entree
    return entree in e.get("test", "") or e.get("test", "") in entree


def score_fiabilite(entree, registre, mode_serie=False):
    """Mode ko-historique : 0 KO sur les derniers lancements = 100."""
    if not registre:
        return 50.0
    entrees_entite = [e for e in registre
                      if matcher_entite(entree, e, mode_serie)]
    if not entrees_entite:
        return 50.0
    derniers = entrees_entite[-10:]
    nb_ko = sum(1 for e in derniers if e.get("verdict") != "OK")
    total = len(derniers)
    if total == 0:
        return 50.0
    score = 100.0 * (total - nb_ko) / total
    # Penalite supplementaire si le KO est recent
    if derniers and derniers[-1].get("verdict") != "OK":
        score -= 10.0
    return max(0.0, min(100.0, score))


def score_presence(contenu, marqueurs):
    """Mode presence-marqueurs : proportion de marqueurs presents."""
    if not contenu:
        return 0.0
    presents = sum(1 for m in marqueurs if m in contenu)
    return 100.0 * presents / len(marqueurs)


def score_tokens_fichier(chemin, taille_base=30000):
    """Mode moins-tokens-mieux : taille du fichier vs base."""
    if not os.path.exists(chemin):
        return 0.0
    taille = os.path.getsize(chemin)
    if taille <= 0:
        return 50.0
    ratio = taille / taille_base
    score = 100.0 - (ratio - 0.5) * 50.0
    return max(0.0, min(100.0, score))


def score_systeme():
    """Mode environnement : profil-systeme present dans le classeur."""
    contenu = lire_fichier(CLASSEUR)
    if "profil-systeme" in contenu:
        return 100.0
    return 40.0


def score_usage(entree, registre_usages):
    """Mode utilise : presence d entrees au registre des usages."""
    if not registre_usages:
        return 30.0
    nb = sum(1 for e in registre_usages if entree in e.get("outil", ""))
    if nb >= 5:
        return 100.0
    if nb >= 2:
        return 75.0
    if nb >= 1:
        return 50.0
    return 20.0


def score_nettoyage(nom_script):
    """Mode propre : le dossier tmp-<agent> correspondant est-il vide."""
    for d in os.listdir(RACINE):
        if d.startswith("tmp-"):
            # On ne peut pas associer un script a son dossier sans convention :
            # note neutre si des dossiers tmp existent, 100 si aucun residu.
            return 50.0
    return 100.0


def score_synchro(nom_fiche, contenu):
    """Mode synchro : coherence fiche/arbre v2/AGENTS.md (migration v1->v2)."""
    score = 50.0
    base = os.path.join(RACINE, "cerveau-projet", "agents", nom_fiche)
    arbre = os.path.join(base, "parcours", "arbre-%s.json" % nom_fiche)
    if os.path.exists(arbre):
        score += 25.0
    ag = lire_fichier(os.path.join(RACINE, "AGENTS.md"))
    if nom_fiche in ag:
        score += 25.0
    return min(100.0, score)


# --- Score d une entite selon son profil ---

def calculer_entite(profil, criteres, entite, registre, registre_usages):
    """Retourne (scores_criteres, note_totale)."""
    scores = {}
    mode_serie = (profil == "serie")
    for c in criteres:
        mode = c.get("mode", "")
        nom = c.get("nom", "")
        if mode == "plus-rapide-mieux":
            scores[nom] = score_temps(entite, registre,
                                     base_secondes=c.get("base", 3.0),
                                     mode_serie=mode_serie)
        elif mode == "ko-historique":
            scores[nom] = score_fiabilite(entite, registre,
                                         mode_serie=mode_serie)
        elif mode == "presence-marqueurs":
            contenu = ""
            if profil == "test":
                chemin = os.path.join(TESTS_DIR, entite, entite + ".py")
                if not os.path.exists(chemin):
                    # entite peut etre le chemin complet
                    chemin = entite
                contenu = lire_fichier(chemin)
                scores[nom] = score_presence(contenu, MARQUEURS_TEST)
            elif profil == "outil":
                chemin = trouver_fichier_outil(entite)
                contenu = lire_fichier(chemin)
                scores[nom] = score_presence(contenu, MARQUEURS_OUTIL)
            elif profil == "script-temp":
                contenu = lire_fichier(entite)
                scores[nom] = score_presence(contenu, MARQUEURS_SCRIPT_TEMP)
            elif profil == "fiche":
                chemin = os.path.join(RACINE, "cerveau-projet", "agents",
                                      entite, entite + ".md")
                contenu = lire_fichier(chemin)
                scores[nom] = score_presence(contenu, MARQUEURS_FICHE)
            else:
                scores[nom] = 50.0
        elif mode == "moins-tokens-mieux":
            chemin = entite
            if profil == "test":
                chemin = os.path.join(TESTS_DIR, entite, entite + ".py")
            elif profil == "outil":
                chemin = trouver_fichier_outil(entite)
            elif profil == "fiche":
                chemin = os.path.join(RACINE, "cerveau-projet", "agents",
                                      entite, entite + ".md")
            scores[nom] = score_tokens_fichier(chemin)
        elif mode == "environnement":
            scores[nom] = score_systeme()
        elif mode == "utilise":
            scores[nom] = score_usage(entite, registre_usages)
        elif mode == "propre":
            scores[nom] = score_nettoyage(entite)
        elif mode == "synchro":
            contenu = lire_fichier(os.path.join(RACINE, "cerveau-projet",
                                                "agents", entite, entite + ".md"))
            scores[nom] = score_synchro(entite, contenu)
        else:
            scores[nom] = 50.0
    note = sum(scores.get(c.get("nom", ""), 0) * c.get("poids", 0) / 100.0
               for c in criteres)
    return scores, note


def verdict(note, seuils):
    """Verdict qualitatif depuis les seuils du profil."""
    for nom in ("EXCELLENT", "BIEN", "MOYEN", "FAIBLE"):
        if note >= seuils[nom]:
            return nom
    return "FAIBLE"


def lister_entites(profil):
    """Liste les entites du profil demande."""
    if profil == "test":
        if not os.path.isdir(TESTS_DIR):
            return []
        return sorted(d for d in os.listdir(TESTS_DIR)
                      if d.startswith("test-") and os.path.isdir(os.path.join(TESTS_DIR, d)))
    if profil == "serie":
        return list(SERIES)
    if profil == "outil":
        # Les outils vivent au NIVEAU 2 : tools/<categorie>/<outil>/. Une
        # categorie est un dossier de niveau 1 qui contient des sous-dossiers
        # d outils ; un outil est un sous-dossier qui contient un fichier
        # <nom>.py ou <nom>.sh. On ne liste JAMAIS les categories elles-memes
        # (bug corrige 2026-08-15 : le scan notait les categories FAIBLE).
        if not os.path.isdir(OUTILS_DIR):
            return []
        outils = []
        for categorie in sorted(os.listdir(OUTILS_DIR)):
            chemin_cat = os.path.join(OUTILS_DIR, categorie)
            if not os.path.isdir(chemin_cat) or categorie.startswith("__"):
                continue
            for nom in sorted(os.listdir(chemin_cat)):
                dossier = os.path.join(chemin_cat, nom)
                if not os.path.isdir(dossier) or nom.startswith("__"):
                    continue
                if (os.path.exists(os.path.join(dossier, nom + ".py"))
                        or os.path.exists(os.path.join(dossier, nom + ".sh"))):
                    outils.append(nom)
        return sorted(set(outils))
    if profil == "fiche":
        base = os.path.join(RACINE, "cerveau-projet", "agents")
        if not os.path.isdir(base):
            return []
        return sorted(d for d in os.listdir(base)
                      if os.path.isdir(os.path.join(base, d))
                      and os.path.exists(os.path.join(base, d, d + ".md")))
    return []


def afficher_entite(profil, criteres, entite, scores, note, verbose, seuils,
                    prefix=""):
    ligne = "%s%s : %s%.1f/100%s (%s)" % (prefix, entite, GREEN if note >= 70 else
                                          (YELLOW if note >= 50 else RED),
                                          note, NC, verdict(note, seuils))
    print(ligne)
    if verbose:
        for c in criteres:
            nom = c.get("nom", "")
            print("    - %-12s : %5.1f/100 (poids %d)" % (nom,
                                                          scores.get(nom, 0),
                                                          c.get("poids", 0)))


def rapport_markdown(profil, desc, resultats, criteres, note_generale, seuils):
    lignes = []
    lignes.append("# Rapport de rating - profil %s" % profil)
    lignes.append("")
    lignes.append("> %s" % desc)
    lignes.append("")
    lignes.append("| Entite | Note /100 | Verdict |")
    lignes.append("|---|---|---|")
    for entite, note in resultats:
        lignes.append("| %s | %.1f | %s |" % (entite, note,
                                              verdict(note, seuils)))
    if note_generale is not None:
        lignes.append("")
        lignes.append("## Rating general : %.1f/100 (%s)" % (
            note_generale, verdict(note_generale, seuils)))
    lignes.append("")
    lignes.append("Criteres (%d) : %s" % (
        len(criteres),
        ", ".join("%s (poids %d)" % (c.get("nom"), c.get("poids"))
                  for c in criteres)))
    return "\n".join(lignes) + "\n"


def _cli():
    parser = argparse.ArgumentParser(
        prog="evaluer-rating.py",
        description="Evalue la qualite et la performance (note ponderee /100).",
        add_help=False,
    )
    parser.add_argument("--profil", default="test",
                        help="Profil de notation (test|serie|outil|script-temp|fiche)")
    parser.add_argument("--cible", default="",
                        help="Entite a noter (nom de test, serie, chemin d outil...)")
    parser.add_argument("--tous", action="store_true",
                        help="Noter toutes les entites du profil")
    parser.add_argument("--general", action="store_true",
                        help="Afficher UNIQUEMENT le rating general du profil "
                             "(rapide, sans detail par entite)")
    parser.add_argument("--rapport", default="",
                        help="Ecrire le rapport markdown dans ce fichier")
    parser.add_argument("--verbose", action="store_true",
                        help="Detail des criteres")
    parser.add_argument("--no-chrono", action="store_true",
                        help="Couper le chrono")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    args = parser.parse_args()

    if args.version:
        print("evaluer-rating v%s (%s)" % (VERSION, STATUT))
        return 0
    if args.aide:
        print(__doc__)
        return 0

    t0 = time.time()
    profils = charger_profils()
    seuils = profils.get("verdicts", {})
    if args.profil not in profils.get("profils", {}):
        print(RED + "[ERREUR] Profil inconnu : " + args.profil + NC)
        print("  Disponibles : " + ", ".join(sorted(profils["profils"].keys())))
        return 2

    profil_cfg = profils["profils"][args.profil]
    criteres = profil_cfg.get("criteres", [])
    registre = charger_jsonl(REGISTRE_TESTS)
    registre_usages = charger_jsonl(REGISTRE_USAGES)

    if args.general:
        # Rating general seul : moyenne des notes de toutes les entites,
        # sans detail (rapide, destine a l affichage en fin de test).
        entites = lister_entites(args.profil)
        if not entites:
            print("RATING GENERAL (%s) : indisponible (aucune entite)" % args.profil)
            return 0
        notes = [calculer_entite(args.profil, criteres, ent, registre,
                                 registre_usages)[1] for ent in entites]
        note_generale = sum(notes) / len(notes)
        print("RATING GENERAL (%s) : %.1f/100 (%s)" % (
            args.profil, note_generale, verdict(note_generale, seuils)))
        return 0

    if args.tous:
        entites = lister_entites(args.profil)
        resultats = []
        for entite in entites:
            scores, note = calculer_entite(args.profil, criteres, entite,
                                           registre, registre_usages)
            resultats.append((entite, note))
            afficher_entite(args.profil, criteres, entite, scores, note,
                            args.verbose, seuils)
        note_generale = 0.0
        if resultats:
            note_generale = sum(n for _, n in resultats) / len(resultats)
        print("")
        print("=== RATING GENERAL (%s) : %.1f/100 (%s) ===" % (
            args.profil, note_generale, verdict(note_generale, seuils)))
        if args.rapport:
            with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(rapport_markdown(args.profil, profil_cfg.get(
                    "description", ""), resultats, criteres, note_generale, seuils))
            print("Rapport ecrit : %s" % args.rapport)
    elif args.cible:
        scores, note = calculer_entite(args.profil, criteres, args.cible,
                                       registre, registre_usages)
        afficher_entite(args.profil, criteres, args.cible, scores, note,
                        args.verbose, seuils)
        print("")
        print("=== RATING GENERAL (%s) : a calculer avec --tous ===" % args.profil)
    else:
        print(YELLOW + "Precisez --cible <nom> ou --tous" + NC)
        return 2

    if not args.no_chrono:
        print("")
        print("[chrono] evaluer-rating : %.1fs" % (time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
