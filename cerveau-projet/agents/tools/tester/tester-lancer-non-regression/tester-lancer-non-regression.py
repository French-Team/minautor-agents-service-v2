#!/usr/bin/env python3
# -*- coding: ascii -*-
# tester-lancer-non-regression.py
#
# Lance TOUS les tests formels du cerveau-projet (tests/test-0XX/) et
# produit un bilan OK/KO avec comptage robuste des [OK]/[KO].
#
# Pourquoi ? Les agents ecrivaient des scripts temporaires (.zz-nonreg-*.py)
# pour lancer la non-regression a la main. Cet outil remplace ces scripts :
# une commande, un bilan fiable, le registre d usage protege (--no-journal).
#
# Round 10 (series) : la suite est decoupee en 4 SERIES thematiques pour
# rester rapide a mesure que le nombre de tests grandit.
#   --series a|b|c|d : ne lancer qu une serie (bilan dedie)
#   --parallele      : series A/B/C en sous-processus isoles (--journal),
#                      puis serie D (registre et garde-fous) en serie apres.
# Round 10b : le mode parallele est le DEFAUT ; --serial force l ancien mode
# serie complet. Le filtre --tests est herite par les sous-processus.
#   Securite : le registre d usage est archive + efface UNE SEULE fois par le
#   processus parent ; les sous-processus paralleles tournent toujours avec
#   --journal. Un test sans serie affectee est signale et lance en queue
#   (jamais oublie silencieusement).
#
# Options :
#   --series <a|b|c|d|tous> : ne lancer qu une serie (defaut : tous)
#   --parallele            : execution parallele (DEFAUT : A/B/C en sous-
#                            processus isoles puis D en serie)
#   --serial               : force le mode serie complet (ancien comportement)
#   --tests <a,b,c>        : filtrer (noms de dossier, ex : test-013-cerberus-migration)
#   --no-journal           : purge le registre d usage avant, verifie 0 apres (defaut)
#   --journal              : ne touche pas au registre
#   --rapport              : ecrit le bilan dans un fichier markdown
#   --version
#
# Usage:
#   python3 tester-lancer-non-regression.py
#   python3 tester-lancer-non-regression.py --serial
#   python3 tester-lancer-non-regression.py --series a
#   python3 tester-lancer-non-regression.py --parallele
#   python3 tester-lancer-non-regression.py --tests test-013-cerberus-migration,test-016-migration-buffy
#   python3 tester-lancer-non-regression.py --rapport rapport-nonreg.md
#
# Version : 0.1.3
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (tester-).
# =============================================================================
import argparse
import glob
import io
import os
import re
import subprocess
import sys
from datetime import datetime

VERSION = "0.1.3"
STATUT = "ebauche"

# Round 10 : 4 series thematiques. Chaque test appartient a une serie par son
# prefixe test-0XX. Un test trouve sur disque sans prefixe de serie est lance
# en queue avec un avertissement (il n est jamais oublie).
SERIES = {
    "a": ["test-001", "test-002", "test-003", "test-004", "test-019", "test-020"],
    "b": ["test-006", "test-009", "test-012", "test-013", "test-014", "test-015",
          "test-016", "test-018", "test-021", "test-022"],
    "c": ["test-005", "test-007", "test-008", "test-010", "test-011", "test-017"],
    "d": ["test-023", "test-024", "test-025", "test-026", "test-027", "test-028",
          "test-029"],
}
SERIES_NOMS = {
    "a": "Combos et coherence",
    "b": "Parcours et validateurs",
    "c": "Generateurs et catalogue",
    "d": "Registre et garde-fous",
}
SERIES_ORDRE = ["a", "b", "c", "d"]
# La serie D est TOUJOURS lancee en dernier (registre et garde-fous : elle
# verifie l absence de scripts temporaires et l etat du registre - jamais en
# parallele avec les autres series).
SERIES_PARALLELES = ["a", "b", "c"]

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
    """Remonte jusqu'au dossier racine (contenant AGENTS.md)."""
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def registre_defaut(racine):
    return os.path.join(racine, "cerveau-projet", "agents", "traces", "registre-usages-outils.jsonl")


def registre_historique(racine):
    """Chemin de l historique du registre (append, jamais ecrase)."""
    return os.path.join(racine, "cerveau-projet", "agents", "traces",
                        "registre-usages-outils.historique.jsonl")


def archiver_registre(racine):
    """Deplace les lignes du registre courant vers l historique (round 8 :
    la purge pure perdait la memoire des declarations, le detecteur devenait
    aveugle au passe). Les lignes deja presentes dans l historique ne sont
    pas re-ajoutees (dedoublonnage par ligne exacte)."""
    registre = registre_defaut(racine)
    historique = registre_historique(racine)
    if not os.path.isfile(registre):
        return
    try:
        with io.open(registre, encoding="utf-8") as fh:
            lignes = [l for l in fh if l.strip()]
    except Exception:
        return
    if not lignes:
        return
    deja = set()
    if os.path.isfile(historique):
        try:
            with io.open(historique, encoding="utf-8") as fh:
                deja = set(l for l in fh if l.strip())
        except Exception:
            deja = set()
    nouveaux = [l for l in lignes if l not in deja]
    if not nouveaux:
        return
    dossier = os.path.dirname(historique)
    if dossier and not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)
    with io.open(historique, "a", encoding="utf-8", newline="\n") as fh:
        for l in nouveaux:
            fh.write(l.rstrip("\n") + "\n")


def trouver_tests(racine, filtre=None):
    """Retourne la liste des tests test-0XX (fichiers .py) tries."""
    pattern = os.path.join(racine, "cerveau-projet", "agents", "tools", "tester",
                           "tests", "test-0*", "test-0*.py")
    tests = sorted(glob.glob(pattern))
    if filtre:
        noms_filtres = [f.strip() for f in filtre.split(",") if f.strip()]
        tests = [t for t in tests if any(n in os.path.basename(t) for n in noms_filtres)]
    return tests


def compter_ko(sortie):
    return len(re.findall(r"\[KO\]", sortie))


def assigner_series(tests, serie="tous"):
    """Attribue chaque test a sa serie (par prefixe test-0XX).

    Retourne (par_serie, hors_serie) :
      - par_serie : dict serie -> liste de tests (serie vide si aucun test)
      - hors_serie : tests sans serie affectee (mode tous uniquement)
    """
    par_serie = {s: [] for s in SERIES}
    hors_serie = []
    for t in tests:
        nom = os.path.basename(t)
        affecte = None
        for s in SERIES_ORDRE:
            if any(nom.startswith(p) for p in SERIES[s]):
                affecte = s
                break
        if affecte:
            par_serie[affecte].append(t)
        else:
            hors_serie.append(t)
    if serie != "tous":
        return {serie: par_serie[serie]}, []
    return par_serie, hors_serie


def executer_lot(racine, tests, libelle="", header=True):
    """Execute une liste de tests en serie. Retourne (ok, ko, ko_liste)."""
    if header:
        print(_couleur("=== %s : %d tests ===" % (libelle or "Non-regression", len(tests)), "bleu"))
    ok = ko = 0
    ko_liste = []
    for t in tests:
        try:
            r = subprocess.run([sys.executable, t], capture_output=True, text=True, timeout=180)
            nb_ko = compter_ko(r.stdout)
            if nb_ko == 0 and r.returncode == 0:
                ok += 1
                print("  %-50s %s" % (os.path.basename(t), _couleur("OK", "vert")))
            else:
                ko += 1
                ko_liste.append((os.path.basename(t), nb_ko))
                print("  %-50s %s (%d [KO])" % (os.path.basename(t), _couleur("KO", "rouge"), nb_ko))
        except Exception as e:
            ko += 1
            ko_liste.append((os.path.basename(t), -1))
            print("  %-50s %s (%s)" % (os.path.basename(t), _couleur("ERREUR", "rouge"), str(e)[:40]))
    suffixe = (" %s" % libelle) if libelle else ""
    print("")
    print(_couleur("=== RESULTAT%s : %d OK / %d KO (sur %d tests) ===" % (suffixe, ok, ko, len(tests)),
                   "vert" if ko == 0 else "rouge"))
    return ok, ko, ko_liste


def extraire_bilan(sortie):
    """Extrait (ok, ko) du bilan RESULTAT d une sortie de sous-processus.
    Le libelle d une serie ne contient jamais de deux-points, le premier ':'
    est donc le separateur du bilan."""
    m = re.search(r"RESULTAT[^:]*: (\d+) OK / (\d+) KO", sortie)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def afficher_etat_registre(racine):
    """Affiche l etat du registre apres une passe protegee (round 8)."""
    registre = registre_defaut(racine)
    if os.path.exists(registre):
        with io.open(registre, encoding="utf-8") as fh:
            lignes = sum(1 for l in fh if l.strip())
    else:
        lignes = 0
    hist = registre_historique(racine)
    n_hist = 0
    if os.path.isfile(hist):
        with io.open(hist, encoding="utf-8") as fh:
            n_hist = sum(1 for l in fh if l.strip())
    ligne_reg = "=== Registre d usage apres : %d lignes (archive dans l historique : %d) ===" % (lignes, n_hist)
    print(_couleur(ligne_reg, "vert" if lignes == 0 else "jaune"))
    if lignes != 0:
        print(_couleur("[AVERTISSEMENT] Des tests polluent le registre : "
                       "ajouter --no-journal a leurs appels generateurs-commande", "jaune"))
    return lignes


def ecrire_rapport(chemin, titre, bilan, ko_liste, lignes_registre):
    """Ecrit le rapport markdown du bilan."""
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Rapport non-regression\n\n")
        fh.write("Titre : %s\n\n" % titre)
        fh.write("Date : %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        fh.write("## Bilan\n\n%s\n\n" % bilan)
        if ko_liste:
            fh.write("## Tests en echec\n\n")
            for nom, nb in ko_liste:
                fh.write("- %s : %d [KO]\n" % (nom, nb))
        if lignes_registre is not None:
            fh.write("\nRegistre d usage apres : %d lignes\n" % lignes_registre)
    print(_couleur("[OK] Rapport ecrit : %s" % chemin, "vert"))


def main():
    parser = argparse.ArgumentParser(description="Lance la non-regression complete des tests formels")
    parser.add_argument("--series", type=str, default="tous",
                        choices=["a", "b", "c", "d", "tous"],
                        help="Ne lancer qu une serie (a|b|c|d) ou toutes (tous, defaut)")
    parser.add_argument("--parallele", action="store_true",
                        help="Series A/B/C en parallele puis D en serie (defaut)")
    parser.add_argument("--serial", action="store_true",
                        help="Force le mode serie complet (ancien comportement)")
    parser.add_argument("--tests", type=str, default="",
                        help="Filtrer par noms de test separes par des virgules")
    parser.add_argument("--no-journal", action="store_true",
                        help="Purge le registre d usage avant et verifie 0 apres (defaut)")
    parser.add_argument("--journal", action="store_true",
                        help="Ne touche pas au registre d usage")
    parser.add_argument("--rapport", type=str, default="",
                        help="Chemin du rapport markdown (optionnel)")
    parser.add_argument("--version", action="version", version="tester-lancer-non-regression v%s" % VERSION)
    args = parser.parse_args()

    racine = racine_projet()
    tests = trouver_tests(racine, args.tests)
    if not tests:
        print(_couleur("[ERREUR] Aucun test trouve", "rouge"))
        return 2

    if args.series != "tous":
        # Mode mono-serie : une passe en serie (comportement historique),
        # avec protection du registre si demandee.
        selection, _ = assigner_series(tests, args.series)
        selection = selection[args.series]
        if not selection:
            print(_couleur("[ERREUR] Aucun test trouve pour la serie %s" % args.series, "rouge"))
            return 2
        protege = not args.journal
        if protege:
            archiver_registre(racine)
            if os.path.exists(registre_defaut(racine)):
                with io.open(registre_defaut(racine), "w", encoding="utf-8", newline="\n") as fh:
                    fh.write("")
        ok, ko, ko_liste = executer_lot(racine, selection,
                                        libelle="Serie %s (%s)" % (args.series.upper(), SERIES_NOMS[args.series]))
        lignes = None
        if protege:
            lignes = afficher_etat_registre(racine)
        if args.rapport:
            ecrire_rapport(args.rapport,
                           "Serie %s (%s)" % (args.series.upper(), SERIES_NOMS[args.series]),
                           "=== RESULTAT : %d OK / %d KO (sur %d tests) ===" % (ok, ko, len(selection)),
                           ko_liste, lignes)
        return 1 if ko else 0

    # Mode tous : protection du registre faite UNE fois par le parent.
    protege = not args.journal
    if protege:
        archiver_registre(racine)
        if os.path.exists(registre_defaut(racine)):
            with io.open(registre_defaut(racine), "w", encoding="utf-8", newline="\n") as fh:
                fh.write("")

    par_serie, hors_serie = assigner_series(tests, "tous")
    ko_liste = []
    tot_ok = tot_ko = 0

    # Round 10b : le mode parallele est le DEFAUT (--serial force l ancien mode).
    parallele = args.parallele or not args.serial
    if parallele:
        # Series A/B/C en sous-processus isoles (--journal : ils ne touchent
        # pas au registre), serie D + hors-serie en serie dans le parent.
        # Le filtre --tests est herite par les sous-processus : un filtre
        # cible ne doit jamais lancer une serie complete a la place.
        procs = []
        for s in SERIES_PARALLELES:
            if par_serie[s]:
                cmd = [sys.executable, os.path.abspath(__file__), "--series", s, "--journal"]
                if args.tests:
                    cmd += ["--tests", args.tests]
                procs.append((s, subprocess.Popen(cmd, cwd=racine,
                                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                  text=True, encoding="utf-8", errors="replace")))
        for s, p in procs:
            try:
                sortie, _ = p.communicate(timeout=600)
            except Exception as e:
                sortie = "[ERREUR serie %s : %s]" % (s, str(e)[:60])
            print(sortie)
            bilan = extraire_bilan(sortie)
            if bilan:
                tot_ok += bilan[0]
                tot_ko += bilan[1]
            else:
                tot_ko += 1
                ko_liste.append(("serie-%s" % s, -1))
        suite = par_serie["d"] + hors_serie
        if hors_serie:
            print(_couleur("[AVERTISSEMENT] %d test(s) sans serie affectee, lances en queue : %s"
                           % (len(hors_serie), ", ".join(os.path.basename(h) for h in hors_serie)), "jaune"))
        if suite:
            ok_d, ko_d, ko_liste_d = executer_lot(racine, suite,
                                                  libelle="Serie D (%s)%s" % (SERIES_NOMS["d"],
                                                                              " + hors-serie" if hors_serie else ""))
            tot_ok += ok_d
            tot_ko += ko_d
            ko_liste.extend(ko_liste_d)
    else:
        # Mode serie complet (comportement historique, une seule passe).
        ok, ko, ko_liste = executer_lot(racine, tests, libelle="")
        tot_ok, tot_ko = ok, ko

    bilan = "=== RESULTAT GLOBAL : %d OK / %d KO (sur %d tests) ===" % (tot_ok, tot_ko, len(tests))
    print("")
    print(_couleur(bilan, "vert" if tot_ko == 0 else "rouge"))

    lignes = None
    if protege:
        lignes = afficher_etat_registre(racine)

    if args.rapport:
        ecrire_rapport(args.rapport, "Non-regression globale", bilan, ko_liste, lignes)

    return 1 if tot_ko else 0


if __name__ == "__main__":
    sys.exit(main())
