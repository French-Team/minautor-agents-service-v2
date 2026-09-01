#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
tester-lancer-non-regression.py
Lance la non-regression complete des tests formels (mode barrieres par
defaut, series classees par importance, chrono + reference de temps,
verrou d habilitation : seul janus lance la suite en production ; vulcain
est autorise en liste blanche developpeur (v0.2.2) pour VALIDER ses
modifications du lanceur sans attendre janus).

Usage:
  tester-lancer-non-regression.py --agent janus
  tester-lancer-non-regression.py --agent janus --series a,e
  tester-lancer-non-regression.py --agent janus --tests test-001,test-002
  tester-lancer-non-regression.py --agent janus --profil cartes
  tester-lancer-non-regression.py --agent janus --fichiers README.md,tools/creer/creer-fichier/creer-fichier.py
  tester-lancer-non-regression.py --agent janus --tags securite,conventions
  tester-lancer-non-regression.py --agent janus --categorie performance
  tester-lancer-non-regression.py --agent janus --desactiver-categorie performance
  tester-lancer-non-regression.py --version
  tester-lancer-non-regression.py --aide

Options principales:
  --agent <nom>       OBLIGATOIRE (verrou d habilitation : seul janus lance ;
                      vulcain autorise en liste blanche developpeur pour ses essais)
  --series <a,b,c..>  Series a lancer (defaut: tous)
  --tests <liste>     Filtrer par noms de tests
  --profil <nom>      Forcer un profil (cartes, outils, tests, fiches-agents, docs, registre)
  --fichiers <liste>  Fichiers modifies (virgules) : deduit automatiquement le(s) profil(s)
  --tags <t1,t2>      Ne lancer que les tests portant ces tags (OR, bloc Tags: des docstrings)
  --categorie <nom>   Lancer une categorie predefinie (categories-tests.json)
  --desactiver-categorie <nom>  Desactiver une categorie (persistant)
  --activer-categorie <nom>     Reactiver une categorie (persistant)
  --etat-categories   Afficher les categories et leur etat
  --desactiver <N>    Desactiver des tests par numero (persistant)
  --activer <N>       Reactiver des tests par numero (persistant)
  --etat-tests        Afficher la config persistante des tests
  --rapport <fichier> Ecrire le rapport markdown
  --parallele         Mode pool de workers
  --serial            Mode serie complet
  --version           Afficher la version
  --aide, -h          Afficher cette aide

Retour: 0 si tous les tests passent, 1 si KO, 2 si erreur de lancement.
"""
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (tester-).
# =============================================================================
import argparse
import glob
import io
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime

VERSION = "0.6.2"
STATUT = "ebauche"

# Round 18 (2026-08-15) : BARRIERES DE PASSAGE (demande utilisateur) - la
# philosophie de la suite change : les series sont classees par IMPORTANCE
# (FONDATIONS D ABORD) et chaque serie doit etre 100% VERTE pour FRANCHIR la
# barriere vers la suivante. Si une serie a un KO, la barriere appelle la
# protection STOP : la suite s arrete, le rapport de la serie est fourni pour
# constater, analyser et reparer. Quand toutes les barrieres sont passees :
# rapport GLOBAL POSITIF.
# Niveaux (importance decroissante) :
#   a = FONDATIONS (nommage, ASCII/LF, template, protections, structure)
#   b = PARCOURS ET VALIDATEURS (le coeur : valider-cartes, guider, migrations)
#   c = OUTILS ET COMBOS (generateurs, combos, outils utilises souvent)
#   d = REGISTRE ET TRACES (registres usages/tests, sessions, chrono)
#   e = ANTI-RECURRENCE ET GARDE-FOUS SPECIFIQUES
SERIES = {
    "a": ["test-007", "test-029", "test-030", "test-042", "test-043", "test-044",
          "test-049", "test-050", "test-052", "test-054", "test-055", "test-056",
          "test-060", "test-062", "test-063", "test-064", "test-067", "test-068",
          "test-069", "test-070", "test-071", "test-072", "test-073",
          "test-074", "test-075", "test-076", "test-077", "test-078",
          "test-079", "test-080", "test-081", "test-082", "test-083", "test-084",
          "test-085"],
    "b": ["test-009", "test-012", "test-013", "test-014", "test-015", "test-016",
          "test-018", "test-021", "test-026", "test-033", "test-034", "test-037",
          "test-048", "test-058", "test-059", "test-094"],
    "c": ["test-001", "test-002", "test-003", "test-004", "test-005", "test-006",
          "test-008", "test-010", "test-011", "test-017", "test-019", "test-020",
          "test-022", "test-023", "test-040", "test-093", "test-095",
          "test-096"],
    "d": ["test-025", "test-027", "test-031", "test-036", "test-038", "test-039",
          "test-045", "test-046", "test-047", "test-051", "test-061",
          "test-097"],
    "e": ["test-024", "test-028", "test-032", "test-035", "test-041", "test-057", "test-065", "test-066", "test-087", "test-088", "test-089", "test-090", "test-091", "test-092", "test-098", "test-099", "test-100", "test-101", "test-102", "test-103", "test-104", "test-105", "test-106", "test-107", "test-108", "test-109", "test-110", "test-111"],
}
SERIES_NOMS = {
    "a": "Fondations (nommage, ASCII/LF, template, protections)",
    "b": "Parcours et validateurs",
    "c": "Outils et combos",
    "d": "Registre et traces",
    "e": "Anti-recurrence et garde-fous specifiques",
}
SERIES_ORDRE = ["a", "b", "c", "d", "e"]


def afficher_rating_fin_de_run(racine):
    """Affiche le RATING des series et le RATING GENERAL du run (demande
    utilisateur 2026-08-15) via l outil evaluer-rating. No-op silencieux si
    l outil est introuvable ou en echec (jamais bloquant pour la suite)."""
    outil = os.path.join(racine, "cerveau-projet", "agents", "tools",
                         "evaluer", "evaluer-rating", "evaluer-rating.py")
    if not os.path.exists(outil):
        return
    try:
        p = subprocess.run([sys.executable, outil, "--profil", "serie",
                            "--tous", "--no-chrono"],
                           capture_output=True, text=True, timeout=60)
        if p.stdout:
            print(_couleur("=== RATING DES SERIES (evaluer-rating) ===", "bleu"))
            print(p.stdout.rstrip())
        p2 = subprocess.run([sys.executable, outil, "--profil", "test",
                             "--general", "--no-chrono"],
                            capture_output=True, text=True, timeout=60)
        if p2.stdout:
            print(p2.stdout.rstrip())
    except Exception:
        pass


def ordre_series_par_ko(racine, nb_derniers=5):
    """Classe les series par TAUX DE KO DECROISSANT (demande utilisateur
    2026-08-15) : les series qui produisent le plus de KO passent en premier
    pour que les problemes remontent vite. Base : le registre-tests.jsonl
    (chaque test journalise serie + verdict). Si pas assez de donnees
    (moins de nb_derniers lancements complets par serie), garde l ordre fixe.
    Retourne la liste des series dans l ordre choisi."""
    registre = os.path.join(racine, "cerveau-projet", "agents", "traces",
                            "registre-tests.jsonl")
    ko_par_serie = {s: 0 for s in SERIES_ORDRE}
    total_par_serie = {s: 0 for s in SERIES_ORDRE}
    if os.path.isfile(registre):
        for ligne in io.open(registre, encoding="utf-8", errors="replace"):
            try:
                e = json.loads(ligne)
            except (ValueError, TypeError):
                continue
            s = e.get("serie")
            if s not in ko_par_serie:
                continue
            total_par_serie[s] += 1
            if e.get("verdict") == "KO":
                ko_par_serie[s] += 1
    # Seuil de confiance : une serie n est RECLASSEE que si elle a au moins
    # nb_derniers lancements (sinon sa position d origine est conservee - pas
    # assez de donnees pour juger). Les series avec donnees suffisantes sont
    # triees par taux de KO decroissant, les autres restent en place.
    # Seuil de confiance : une serie n est RECLASSEE que si elle a au moins
    # nb_derniers lancements (sinon sa position d origine est conservee - pas
    # assez de donnees pour juger). Les series avec donnees suffisantes sont
    # triees par taux de KO decroissant, les autres restent en place.
    fiables = [s for s in SERIES_ORDRE if total_par_serie[s] >= nb_derniers]
    if not fiables:
        return list(SERIES_ORDRE)
    fiables_tries = sorted(fiables, key=lambda s: (-ko_par_serie[s], s))
    return fiables_tries + [s for s in SERIES_ORDRE if s not in fiables_tries]

# Round 12 : garde-fous GLOBAUX - ils verifient l etat global du projet
# (registre vide, absence de scripts temporaires, sessions) et ne doivent
# JAMAIS tourner en parallele avec d autres tests (faux positifs assures).
# Ils sont toujours lances en serie, apres le pool de workers.
GARDE_FOUS_GLOBAUX = ["test-023", "test-024", "test-025", "test-027",
                     "test-051", "test-052", "test-054", "test-055", "test-056",
                     "test-057"]

# Round 14 (lecon 2026-08-14) : tests qui ECRIVENT des fichiers partages
# (README, catalogue, temps-reference...) et ne doivent JAMAIS tourner en
# parallele avec les tests qui LISENT ces fichiers (ex: test-020 modifie le
# README en reel pendant que test-038 lit le badge ; test-031 supprime/restaure
# temps-reference.json pendant que le lanceur parent la gere -> KO intermittent
# en pool). Ils sont lances en serie finale avec les garde-fous globaux.
# Round 15 (2026-08-15, lecon Janus) : test-061 pose des residus factices dans
# le workspace partage pendant que test-006 (serie b) verifie 'aucun fichier
# residuel dans le workspace' -> course en pool (KO intermittent 5b).
# Round 19 (2026-08-16, lecon Janus) : test-035 (evaluer-processus) ecrit et
# lit le registre des usages pendant que d autres tests lisent/ecrivent le
# meme fichier -> KO intermittent en pool. Ajoute aux exclusifs (serie seule).
TESTS_SERIE_EXCLUSIFS = ["test-020", "test-031", "test-035", "test-061"]

# Round 12 : durees mesurees (profil individuel 2026-08-13, machine 16 coeurs)
# pour le tri decroissant du pool - les tests longs partent en premier sur
# les workers, les courts remplissent les creneaux restants.
DUREES_CONNUES = {
    "test-028": 13, "test-003": 8, "test-031": 5, "test-005": 5,
    "test-017": 4, "test-030": 3, "test-012": 3, "test-027": 2,
    "test-010": 2, "test-009": 2, "test-006": 2, "test-004": 2,
    "test-002": 2, "test-026": 1, "test-025": 1, "test-024": 1,
    "test-022": 1, "test-021": 1, "test-020": 1, "test-019": 1,
    "test-018": 1, "test-016": 1, "test-015": 1, "test-013": 1,
    "test-011": 1, "test-008": 1, "test-007": 1, "test-029": 0,
    "test-033": 0, "test-034": 0, "test-035": 0, "test-036": 0,
    "test-037": 0, "test-038": 0, "test-039": 0, "test-040": 0,
    "test-023": 0, "test-014": 0, "test-001": 0, "test-041": 0, "test-042": 0, "test-043": 0, "test-044": 0, "test-045": 0,    "test-046": 0, "test-061": 0, "test-047": 0, "test-048": 0, "test-051": 5, "test-052": 2, "test-054": 3, "test-055": 1,
    "test-057": 0, "test-058": 0, "test-059": 0,
}

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[0;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    return "%s%s%s" % (_COULEURS.get(nom, _COULEURS["neutre"]), texte, _COULEURS["neutre"])


def verrouiller_habilitation(agent, outil):
    """Verrou d habilitation : appelle proteger-verrou-habilitation et
    retourne (code, message). Le verrou lit les cartes de decision comme
    source de verite - aucune table en dur ici. Code 0 = habilite, 1 =
    bloque, 2 = erreur d utilisation."""
    racine = racine_projet()
    verrou = os.path.join(
        racine, "cerveau-projet", "agents", "tools", "proteger",
        "proteger-verrou-habilitation", "proteger-verrou-habilitation.py")
    if not os.path.isfile(verrou):
        return (2, "[ERREUR] Verrou introuvable : %s" % verrou)
    r = subprocess.run(
        [sys.executable, verrou, "--agent", agent, "--outil", outil],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    message = (r.stdout + r.stderr).strip()
    return (r.returncode, message)


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


def ko_tests_defaut(racine):
    """Chemin du fichier persistant de la serie KO (dossier du lanceur)."""
    return os.path.join(racine, "cerveau-projet", "agents", "tools", "tester",
                        "tester-lancer-non-regression", "ko-tests.json")


def config_environnement_defaut(racine):
    """Chemin du fichier de configuration d environnement adaptative
    (config-environnement.json, gere par configurer-environnement)."""
    return os.path.join(racine, "cerveau-projet", "agents", "tools", "tester",
                        "tester-lancer-non-regression", "config-environnement.json")


def lire_workers_config(racine):
    """CONFIGURATION ADAPTATIVE (demande utilisateur 2026-08-17) : lit le
    nombre de workers recommande depuis config-environnement.json. Si le
    fichier est absent ou illisible, retombe sur min(cpu_count, 16) (comportement
    historique). Retourne (workers, timeout_test) - timeout 0 = defaut."""
    workers_defaut = min(os.cpu_count() or 1, 16)
    timeout_defaut = 0
    chemin = config_environnement_defaut(racine)
    if not os.path.isfile(chemin):
        return workers_defaut, timeout_defaut
    try:
        with io.open(chemin, encoding="utf-8") as fh:
            data = json.load(fh)
        workers = int(data.get("workers_recommandes", workers_defaut))
        timeout = int(data.get("timeout_test_recommande", 0))
        if workers < 1:
            workers = workers_defaut
        return workers, timeout
    except (IOError, ValueError, TypeError):
        return workers_defaut, timeout_defaut


def lire_ko_tests(racine):
    """Lit la liste des tests en KO du fichier persistant ko-tests.json.
    Retourne une liste de noms de tests (test-0XX) - vide si fichier absent
    ou illisible (la serie KO vide est le comportement par defaut)."""
    chemin = ko_tests_defaut(racine)
    if not os.path.isfile(chemin):
        return []
    try:
        with io.open(chemin, encoding="utf-8") as fh:
            data = json.load(fh)
        ko = data.get("ko", [])
        return [k for k in ko if isinstance(k, str) and k.startswith("test-")]
    except (IOError, ValueError):
        return []


def ecrire_ko_tests(racine, noms_ko):
    """Ecrit la liste des tests en KO dans ko-tests.json (persistant).
    Les noms sont tries, dedoublonnes, filtres sur test-0XX. Le fichier est
    cree s il n existe pas (demande utilisateur 2026-08-16 : cree au premier
    lancement)."""
    chemin = ko_tests_defaut(racine)
    noms = sorted(set(n for n in noms_ko if n.startswith("test-")))
    data = {"ko": noms, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    dossier = os.path.dirname(chemin)
    if dossier and not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=True, indent=1)
        fh.write("\n")
    return noms


def rotation_registre(racine, max_usages=100):
    """ROTATION NON DESTRUCTIVE du registre courant (v0.5.4, 2026-08-16) :
    le registre est CUMULATIF (memoire des usages reels des agents) mais
    plafonne a `max_usages` entrees de BRUIT d auto-journalisation.
    Les entrees de VERITE ne sont JAMAIS retirees :
      - mode script-temporaire : memoire des declarations (decision 14/08)
      - mode direct / generateur : declarations manuelles documentees
        (generateurs-amelioration, creation d outils...) - lecon 2026-08-16 :
        la rotation a rogne generateurs-amelioration et casse test-078.
    Seules les entrees mode verrou-auto (bruit d auto-journalisation du
    verrou d habilitation) sont plafonnees : les plus anciennes sont
    retirees pour revenir a `max_usages` (le verrou re-journalise les
    usages recents a chaque appel, la memoire vive reste a jour).
    - registre < 100 entrees verrou-auto : AUCUNE suppression (memoire vit)
    - registre > 100 : les verrou-auto les PLUS ANCIENS sont retires
      pour revenir a 100 (les verites restent).
    Retourne le nombre d entrees verrou-auto conservees."""
    registre = registre_defaut(racine)
    if not os.path.isfile(registre):
        return 0
    try:
        with io.open(registre, encoding="utf-8") as fh:
            lignes = [l.rstrip("\n") for l in fh if l.strip()]
    except Exception:
        return 0
    verites = []
    bruit = []
    for l in lignes:
        try:
            e = json.loads(l)
            if e.get("mode") in ("script-temporaire", "direct", "generateur"):
                verites.append(l)
            else:
                bruit.append(l)
        except ValueError:
            # ligne non-JSON : jamais perdue (philosophie corriger-noms-maj)
            verites.append(l)
    # trier le bruit par date (plus recente d abord) si possible
    def _date(l):
        try:
            return json.loads(l).get("date", "")
        except ValueError:
            return ""
    bruit.sort(key=_date, reverse=True)
    if len(bruit) > max_usages:
        bruit = bruit[:max_usages]
    conservees = verites + bruit
    # Re-tri GLOBAL par date decroissante : la rotation ne doit PAS casser
    # le tri du registre (regle de tri v0.3.0). Les lignes sans
    # date (non-JSON ou date vide) restent en fin.
    conservees.sort(key=_date, reverse=True)
    with io.open(registre, "w", encoding="utf-8", newline="\n") as fh:
        for l in conservees:
            fh.write(l + "\n")
    return len(bruit)


def trouver_tests(racine, filtre=None):
    """Retourne la liste des tests test-0XX (fichiers .py) tries."""
    # v0.6.3 : glob test-* (pas test-0*) - test-100+ n etaient JAMAIS detectes
    # (test-100/101 crees le 2026-08-24 jamais executes par la non-regression)
    pattern = os.path.join(racine, "cerveau-projet", "agents", "tools", "tester",
                           "tests", "test-*", "test-*.py")
    tests = sorted(glob.glob(pattern))
    if filtre:
        noms_filtres = [f.strip() for f in filtre.split(",") if f.strip()]
        tests = [t for t in tests if any(n in os.path.basename(t) for n in noms_filtres)]
    return tests


def lire_tags_test(chemin):
    """Extrait le bloc 'Tags:' de la docstring d un test (demande
    utilisateur 2026-08-16 : chaque test porte des tags de categorisation
    dans son en-tete, source unique lisible par le lanceur).
    Retourne une liste de tags (minuscules, sans doublon). Format attendu
    dans la docstring : 'Tags: securite, conventions, anti-recurrence'.
    """
    tags = []
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as fh:
            tete = fh.read(4096)
    except (IOError, OSError):
        return tags
    # Meme format que le garde-fou test-087 : 'Tags: a, b, c' en docstring
    # OU '# Tags: a, b, c' en commentaire (test-027). Deux formats acceptes.
    m = re.search(r"^#?\s*Tags:\s*(.+)$", tete, re.M)
    if m:
        for t in m.group(1).split(","):
            t = t.strip().lower()
            if t and t not in tags:
                tags.append(t)
    return tags


def tags_par_test(tests):
    """Retourne {chemin: [tags]} pour la liste de tests (lecture une fois)."""
    return {t: lire_tags_test(t) for t in tests}


def chemin_categories_tests(racine):
    """Chemin du fichier categories-tests.json (nom de categorie -> tags)."""
    return os.path.join(racine, "cerveau-projet", "agents", "tools", "tester",
                        "tester-lancer-non-regression", "categories-tests.json")


def charger_categories_tests(racine):
    """Charge categories-tests.json. Format : {"categories": {"securite":
    ["marbre", ...], ...}}. Retourne (dict nom -> [tags], erreur)."""
    chemin = chemin_categories_tests(racine)
    try:
        with io.open(chemin, encoding="utf-8") as fh:
            d = json.load(fh)
        return d.get("categories", {}), None
    except (IOError, OSError, ValueError) as e:
        return {}, "fichier %s illisible: %s" % (chemin, str(e)[-80:])


def filtrer_tests_par_tags(tests, tags_voulus):
    """Filtre la liste de tests : ne garde que ceux portant AU MOINS UN des
    tags voulus (combinaison OR). Tags compares en minuscules."""
    carte = tags_par_test(tests)
    voulus = set(t.lower() for t in tags_voulus)
    gardes = []
    for t in tests:
        if voulus & set(carte.get(t, [])):
            gardes.append(t)
    return gardes, carte


def lire_config_categories(racine):
    """Lit les categories DESACTIVEES persistantes depuis config-tests.json."""
    chemin = chemin_config_tests(racine)
    try:
        with io.open(chemin, encoding="utf-8") as fh:
            d = json.load(fh)
        return [str(x) for x in d.get("desactivees_categories", []) if str(x).strip()]
    except (IOError, OSError, ValueError):
        return []


def ecrire_config_categories(racine, desactivees_categories, desactives=None):
    """Ecrit la config persistante (tests + categories desactivees)."""
    chemin = chemin_config_tests(racine)
    if desactives is None:
        desactives = lire_config_tests(racine)
    try:
        entree = {
            "desactives": sorted(set(desactives)),
            "desactivees_categories": sorted(set(desactivees_categories)),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(entree, ensure_ascii=True, indent=1) + "\n")
        return True
    except (IOError, OSError):
        return False


def compter_ko(sortie):
    """Compte les points KO d une sortie de test : seules les lignes qui
    COMMENCENT par [KO] (apres indentation) sont des echecs. Un libelle
    [OK] contenant la sous-chaine "[KO]" (ex "details [KO] presents")
    n est JAMAIS un echec - lecon du round 16 : test-051 point 9 etait
    compte a tort par l ancienne detection (sous-chaine n importe ou)."""
    return sum(1 for ligne in (sortie or "").splitlines()
               if ligne.strip().startswith("[KO]"))


def extraire_lignes_ko(sortie):
    """Extrait les lignes [KO] detaillees d une sortie de test (avec le
    detail apres '--' si present). Round 16 (demande utilisateur) : le
    rapport de non-regression doit fournir les informations detaillees des
    KO quand la suite est terminee - l agent sait immediatement POURQUOI
    chaque test a echoue, sans relancer les tests individuellement."""
    # Seules les lignes qui COMMENCENT par [KO] (apres indentation) sont
    # des echecs : un libelle [OK] contenant la sous-chaine "[KO]" (ex
    # "details [KO] presents") ne doit jamais etre capture (lecon du
    # round 16 : premier passage capturait les [OK] a tort).
    return [ligne.strip() for ligne in (sortie or "").splitlines()
            if ligne.strip().startswith("[KO]")]


def extraire_lignes_aide(sortie):
    """Extrait les lignes [AIDE] (CARTE DE REPARATION / ou chercher) d une
    sortie de test. Demande utilisateur 2026-08-29 : la non-regression doit
    indiquer OU chercher quand il y a des KO - chaque test emet, a la fin
    et quand il a des KO, une bande [AIDE] donnant les FICHIERS inspectes,
    la COMMANDE de diagnostic a relancer (--isoler N / --no-chrono) et un
    indice de correctif, pour retrouver le probleme sans creuser a la main.
    Ces lignes sont remontees dans DETAILS DES KO et le rapport markdown.
    Seules les lignes COMMENCANT par [AIDE] (apres indentation) comptent."""
    return [ligne.strip() for ligne in (sortie or "").splitlines()
            if ligne.strip().startswith("[AIDE]")]


def serie_du_test(nom):
    """Retourne la serie (a|b|c|d|e) d un test par son prefixe test-0XX."""
    for s in SERIES_ORDRE:
        if any(nom.startswith(p) for p in SERIES[s]):
            return s
    return "hors-serie"


def registre_tests_defaut(racine):
    """Chemin du registre des lancements de tests (distinct du registre
    d usage d outils - jamais melanges)."""
    return os.path.join(racine, "cerveau-projet", "agents", "traces",
                        "registre-tests.jsonl")


PLAFOND_REGISTRE_TESTS = 500


def _ecrire_registre_avec_retry(registre, contenu, max_essais=5):
    """Ecrit le registre avec retry court sur OSError (Errno 22 sur lecteur
    reseau Z: quand un handle concurrent existe - crash recurrent de la
    suite complete, observe 2026-08-30). Sans retry, la suite complete
    s interrompt en plein milieu (journalisation OK des premiers tests puis
    OSError Invalid argument sur open(registre, 'w'))."""
    import time as _time
    for essai in range(max_essais):
        try:
            with io.open(registre, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(contenu)
            return True
        except OSError:
            if essai == max_essais - 1:
                raise
            _time.sleep(0.2 * (essai + 1))
    return False


def trier_registre_tests(registre):
    """Trie le registre-tests par date puis heure, DECROISSANT (le plus recent
    en premier - meme regle que registre-usages-outils, demande utilisateur
    2026-08-14). Les lignes non-JSON sont PRESERVEES (conservees en fin).

    ROTATION (v0.6.2, demande performance 2026-08-17) : le fichier est
    PLAFONNE a PLAFOND_REGISTRE_TESTS entrees valides (les plus recentes
    sont conservees). Sans plafond, le fichier grandissait sans limite
    (12k+ lignes, 1.9 Mo) et le re-tri integral a chaque journalisation
    coutait ~8s par lancement (goulot reel de test-032)."""
    if not os.path.isfile(registre):
        return
    try:
        with io.open(registre, encoding="utf-8") as fh:
            lignes = [l.rstrip("\n") for l in fh if l.strip()]
    except Exception:
        return
    valides = []
    invalides = []
    for l in lignes:
        try:
            e = json.loads(l)
            valides.append((e.get("date", ""), l))
        except ValueError:
            invalides.append(l)
    valides.sort(key=lambda paire: paire[0], reverse=True)
    if len(valides) > PLAFOND_REGISTRE_TESTS:
        valides = valides[:PLAFOND_REGISTRE_TESTS]
    triees = [l for _, l in valides] + invalides
    _ecrire_registre_avec_retry(registre, "\n".join(triees) + "\n")


def journaliser_test(racine, agent, serie, nom_test, verdict, duree, run_id=""):
    """Ajoute UNE entree dans registre-tests.jsonl (date, run_id, agent,
    serie, test, verdict OK/KO/ERREUR, duree secondes). No-op si agent est
    vide (aucune trace sans --agent explicite). Le registre est TRIE par
    date/heure DECROISSANT apres chaque ajout (le plus recent en premier).
    run_id (timestamp du debut du run) identifie le lancement auquel
    appartient chaque test : c est la base de --relancer-ko."""
    if not agent:
        return
    registre = registre_tests_defaut(racine)
    entree = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": agent,
        "serie": serie,
        "test": nom_test,
        "verdict": verdict,
        "duree": round(duree, 3),
    }
    if run_id:
        entree["run_id"] = run_id
    with io.open(registre, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(entree, ensure_ascii=True) + "\n")
    trier_registre_tests(registre)


def ko_du_dernier_run(racine, registre=""):
    """Retourne la liste des tests en KO du DERNIER run journalise (--relancer-ko).

    Methode : le registre-tests.jsonl est trie par date DECROISSANT (le plus
    recent en premier). Le dernier run = le run_id le plus recent present
    (ou, a defaut de run_id, le groupe de la date la plus recente). On
    collecte les tests dont le verdict est KO/ERREUR/TIMEOUT dans CE run.
    Retourne (run_id, liste_noms_tests_ko) - liste vide si le dernier run
    n a aucun KO ou si le registre est illisible. Le parametre registre
    (chemin) permet de tester sur un fichier arbitraire (garde-fou)."""
    if not registre:
        registre = registre_tests_defaut(racine)
    entrees = []
    if os.path.isfile(registre):
        for ligne in io.open(registre, encoding="utf-8", errors="replace"):
            try:
                entrees.append(json.loads(ligne))
            except (ValueError, TypeError):
                continue
    if not entrees:
        return "", []
    # run_id le plus recent (les entrees sont triees par date decroissante)
    run_id = None
    for e in entrees:
        if e.get("run_id"):
            run_id = e.get("run_id")
            break
    if not run_id:
        # Anciennes entrees sans run_id : on prend la date la plus recente
        date_max = max((e.get("date", "") for e in entrees), default="")
        run_id = "date:%s" % date_max
    ko = []
    for e in entrees:
        if e.get("run_id") and e.get("run_id") != run_id:
            continue
        if not e.get("run_id") and not e.get("date", "").startswith(run_id[len("date:"):]):
            continue
        if e.get("verdict") in ("KO", "ERREUR", "TIMEOUT"):
            nom = e.get("test", "")
            if nom and nom not in ko:
                ko.append(nom)
    return run_id, ko


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


def executer_lot(racine, tests, libelle="", header=True, fail_fast=False,
                 agent="", serie="", timeout_test=0, run_id=""):
    """Execute une liste de tests en serie.
    Retourne (ok, ko, ko_liste, non_lances, durees) : durees est une liste de
    couples (nom_test, duree_secondes) pour CHAQUE test execute (round 17 :
    le rapport doit fournir le chrono par test pour aider aux optimisations).

    fail_fast (protection STOP, option --fail-fast) : des le premier test KO
    (ou ERREUR), la suite est STOPPEE - les tests restants ne sont pas lances
    et sont comptes comme non-lances.

    Registre-tests : si agent est fourni (--agent), CHAQUE test execute est
    journalise dans registre-tests.jsonl (verdict + duree).
    """
    if header:
        print(_couleur("=== %s : %d tests ===" % (libelle or "Non-regression", len(tests)), "bleu"))
    ok = ko = 0
    non_lances = 0
    ko_liste = []
    durees = []
    for i, t in enumerate(tests):
        t_debut = time.monotonic()
        try:
            r = subprocess.run([sys.executable, t], capture_output=True, text=True,
                               timeout=timeout_test if timeout_test > 0 else 180)
            nb_ko = compter_ko(r.stdout)
            duree = time.monotonic() - t_debut
            durees.append((os.path.basename(t), round(duree, 2)))
            if nb_ko == 0 and r.returncode == 0:
                ok += 1
                print("  %-50s %s" % (os.path.basename(t), _couleur("OK", "vert")))
                journaliser_test(racine, agent, serie, os.path.basename(t),
                                 "OK", duree, run_id)
            else:
                ko += 1
                ko_liste.append((os.path.basename(t), nb_ko,
                                 extraire_lignes_ko(r.stdout),
                                 extraire_lignes_aide(r.stdout)))
                print("  %-50s %s (%d [KO])" % (os.path.basename(t), _couleur("KO", "rouge"), nb_ko))
                journaliser_test(racine, agent, serie, os.path.basename(t),
                                 "KO", duree, run_id)
                if fail_fast:
                    non_lances = len(tests) - i - 1
                    if non_lances > 0:
                        print(_couleur("  [FAIL-FAST] Test en erreur : la suite est STOPPEE, "
                                       "%d test(s) non lance(s)" % non_lances, "rouge"))
                    break
        except subprocess.TimeoutExpired:
            # PROTECTION ERREUR-SILENCIEUSE (demande utilisateur 2026-08-15) :
            # le timeout a expire SANS reponse ni erreur directe -> ce n est
            # PAS un KO banal mais une ERREUR SILENCIEUSE a trouver/a resoudre,
            # puis l agent RELANCE le script ou fichier corrige.
            duree = time.monotonic() - t_debut
            durees.append((os.path.basename(t), round(duree, 2)))
            ko += 1
            ko_liste.append((os.path.basename(t), -2, [], []))
            print("  %-50s %s" % (os.path.basename(t), _couleur("ERREUR SILENCIEUSE (timeout)", "rouge")))
            journaliser_test(racine, agent, serie, os.path.basename(t),
                             "TIMEOUT", duree, run_id)
            if fail_fast:
                non_lances = len(tests) - i - 1
                if non_lances > 0:
                    print(_couleur("  [FAIL-FAST] Erreur silencieuse : la suite est STOPPEE, "
                                   "%d test(s) non lance(s)" % non_lances, "rouge"))
                break
        except Exception as e:
            duree = time.monotonic() - t_debut
            durees.append((os.path.basename(t), round(duree, 2)))
            ko += 1
            ko_liste.append((os.path.basename(t), -1, [], []))
            print("  %-50s %s (%s)" % (os.path.basename(t), _couleur("ERREUR", "rouge"), str(e)[:40]))
            journaliser_test(racine, agent, serie, os.path.basename(t),
                             "ERREUR", duree, run_id)
            if fail_fast:
                non_lances = len(tests) - i - 1
                if non_lances > 0:
                    print(_couleur("  [FAIL-FAST] Erreur d execution : la suite est STOPPEE, "
                                   "%d test(s) non lance(s)" % non_lances, "rouge"))
                break
    suffixe = (" %s" % libelle) if libelle else ""
    lance_total = len(tests) - non_lances
    print("")
    print(_couleur("=== RESULTAT%s : %d OK / %d KO (sur %d tests, %d non lances) ==="
                   % (suffixe, ok, ko, lance_total, non_lances),
                   "vert" if ko == 0 else "rouge"))
    return ok, ko, ko_liste, non_lances, durees


def executer_pool(racine, tests, workers, fail_fast=False, agent="", serie="",
                  timeout_test=0, run_id=""):
    """Execute une liste de tests sur un pool de workers paralleles.

    Round 12 : les tests sont tries par DUREE DECROISSANTE (les plus longs
    partent en premier sur les workers, les courts remplissent les creneaux
    restants) puis distribues sur `workers` sous-processus simultanes.
    Retourne (ok, ko, ko_liste, non_lances, durees) : durees liste de couples
    (nom_test, duree_secondes) pour CHAQUE test execute (round 17 : chrono
    par test dans le rapport pour aider aux optimisations).

    fail_fast : des le premier KO, le pool est stoppe - les tests restants
    ne sont pas lances (non_lances > 0).

    Registre-tests : si agent est fourni (--agent), CHAQUE test execute est
    journalise dans registre-tests.jsonl (verdict + duree).
    """
    if not tests:
        return 0, 0, [], 0, []
    if workers <= 1:
        return executer_lot(racine, tests, libelle="Serie unique",
                            fail_fast=fail_fast, agent=agent, serie=serie,
                            run_id=run_id)

    def cle(t):
        return -DUREES_CONNUES.get(os.path.basename(t)[:8], 0)

    tries = sorted(tests, key=cle)
    print(_couleur("=== Pool de workers : %d tests sur %d workers (longs d abord) ==="
                   % (len(tries), workers), "bleu"))
    # ANTI-DEADLOCK (lecon 2026-08-13) : jamais de Popen(stdout=PIPE) dans le
    # pool - si un test ecrit plus de 64 Ko, le buffer du pipe se remplit et
    # le sous-processus se bloque en ecrivant (poll() ne passe jamais a None).
    # Chaque test redirige sa sortie vers un FICHIER temp unique, lu apres
    # terminaison : aucun pipe, aucun blocage possible.
    TIMEOUT_POOL = timeout_test if timeout_test > 0 else 300
    # secondes par test (protection anti-blocage : un test qui se bloque
    # (verrou fichier, attente) est tue apres ce delai).
    ok = ko = 0
    non_lances = 0
    ko_liste = []
    durees = []
    actifs = []
    index = 0
    stoppe = False
    while index < len(tries) or actifs:
        # Lancer de nouveaux tests tant que des workers sont libres.
        while len(actifs) < workers and index < len(tries) and not stoppe:
            t = tries[index]
            index += 1
            # Fichier de sortie UNIQUE par test (jamais partage entre workers).
            fic_sortie = os.path.join(racine, "cerveau-projet", "agents", "tools",
                                      "tester", ".pool-%d-%d.out" % (os.getpid(), index))
            with io.open(fic_sortie, "w", encoding="utf-8", newline="\n") as fh:
                p = subprocess.Popen([sys.executable, t], cwd=racine,
                                     stdout=fh, stderr=subprocess.STDOUT)
            # [p, t, debut, fichier_sortie, tue_par_timeout]
            actifs.append([p, t, time.monotonic(), fic_sortie, False])
        # Attendre qu AU MOINS un processus se termine (ou depasse le timeout).
        finis = []
        for a in actifs:
            p = a[0]
            if p.poll() is not None:
                finis.append(a)
            elif time.monotonic() - a[2] > TIMEOUT_POOL:
                try:
                    p.kill()
                except Exception:
                    pass
                a[4] = True  # marque : tue par timeout (erreur silencieuse)
                finis.append(a)
        if not finis:
            if not actifs:
                break  # rien a lancer, rien en cours : c est termine
            time.sleep(0.1)
            continue
        for a in finis:
            actifs.remove(a)
            p, t, _, fic_sortie, tue_timeout = a
            try:
                with io.open(fic_sortie, encoding="utf-8", errors="replace") as fh:
                    sortie = fh.read()
            except Exception:
                sortie = ""
            try:
                os.remove(fic_sortie)
            except Exception:
                pass
            nb_ko = compter_ko(sortie)
            duree = time.monotonic() - a[2]
            durees.append((os.path.basename(t), round(duree, 2)))
            serie_test = serie if serie != "tous" else serie_du_test(os.path.basename(t))
            if tue_timeout:
                # PROTECTION ERREUR-SILENCIEUSE (demande utilisateur 2026-08-15) :
                # timeout expire SANS reponse ni erreur directe -> a trouver/a
                # resoudre, puis l agent RELANCE le script ou fichier corrige.
                ko += 1
                ko_liste.append((os.path.basename(t), -2, [], []))
                print("  %-50s %s" % (os.path.basename(t), _couleur("ERREUR SILENCIEUSE (timeout)", "rouge")))
                journaliser_test(racine, agent, serie_test, os.path.basename(t),
                                 "TIMEOUT", duree, run_id)
                if fail_fast:
                    stoppe = True
            elif nb_ko == 0 and p.returncode == 0:
                ok += 1
                print("  %-50s %s" % (os.path.basename(t), _couleur("OK", "vert")))
                journaliser_test(racine, agent, serie_test, os.path.basename(t),
                                 "OK", duree, run_id)
            else:
                ko += 1
                ko_liste.append((os.path.basename(t), nb_ko,
                                 extraire_lignes_ko(sortie),
                                 extraire_lignes_aide(sortie)))
                print("  %-50s %s (%d [KO])" % (os.path.basename(t), _couleur("KO", "rouge"), nb_ko))
                journaliser_test(racine, agent, serie_test, os.path.basename(t),
                                 "KO", duree, run_id)
                if fail_fast:
                    stoppe = True
    if stoppe:
        non_lances = len(tries) - index
        if non_lances > 0:
            print(_couleur("  [FAIL-FAST] Test en erreur : le pool est STOPPE, "
                           "%d test(s) non lance(s)" % non_lances, "rouge"))
    print("")
    print(_couleur("=== RESULTAT Pool : %d OK / %d KO (sur %d tests, %d non lances) ==="
                   % (ok, ko, len(tries) - non_lances, non_lances),
                   "vert" if ko == 0 else "rouge"))
    return ok, ko, ko_liste, non_lances, durees


def afficher_details_ko(ko_liste):
    """Imprime les DETAILS des tests en echec (lignes [KO] avec leur
    detail) a la fin de la suite : l agent sait immediatement ce qui a
    echoue et pourquoi, sans relancer les tests individuellement (round 16,
    demande utilisateur)."""
    if not ko_liste:
        return
    print("")
    print(_couleur("=== DETAILS DES KO (pour action immediate) ===", "rouge"))
    for entree in ko_liste:
        nom, nb, details, aides = (list(entree) + [None, [], []])[:4]
        if nb == -2:
            print("  %s : ERREUR SILENCIEUSE (timeout) - le test n a ni reussi ni "
                  "echoue directement : a trouver/a resoudre, puis RELANCER le "
                  "script ou fichier corrige" % nom)
            continue
        if nb == -1:
            print("  %s : ERREUR d execution (le test n a pas pu tourner)" % nom)
            continue
        print("  %s : %d [KO]" % (nom, nb))
        if aides:
            print("      [OU CHERCHER] :")
            for aide in aides:
                print("      %s" % aide)
        for ligne in details or []:
            print("      %s" % ligne)
    print("")


def afficher_tests_lents(durees, top=10):
    """Affiche le top des tests les plus lents (chrono par test, round 17,
    demande utilisateur : aider aux optimisations). Trie par duree
    DECROISSANTE. N affiche rien si aucune duree collectee."""
    if not durees:
        return
    tries = sorted(durees, key=lambda paire: paire[1], reverse=True)
    print("")
    print(_couleur("=== TESTS LES PLUS LENTS (top %d, chrono par test) ===" % min(top, len(tries)), "jaune"))
    for nom, duree in tries[:top]:
        print("  %-50s %6.2f s" % (nom, duree))
    print("")


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
    # Les entrees mode script-temporaire sont PRESERVEES par la rotation
    # (decision utilisateur 2026-08-14) et les usages normaux CUMULENT jusqu
    # a 100 (memoire des usages reels) : ce n est pas une pollution.
    ligne_reg = "=== Registre d usage apres : %d lignes (cumul <= 100) ===" % lignes
    print(_couleur(ligne_reg, "vert" if lignes == 0 else "jaune"))
    return lignes


def ecrire_rapport(chemin, titre, bilan, ko_liste, lignes_registre, durees=None):
    """Ecrit le rapport markdown du bilan (+ top des tests les plus lents si
    les durees par test sont fournies - round 17, chrono par test)."""
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Rapport non-regression\n\n")
        fh.write("Titre : %s\n\n" % titre)
        fh.write("Date : %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        fh.write("## Bilan\n\n%s\n\n" % bilan)
        if ko_liste:
            fh.write("## Tests en echec (details)\n\n")
            for entree in ko_liste:
                nom, nb, details, aides = (list(entree) + [None, [], []])[:4]
                if nb == -2:
                    fh.write("- %s : ERREUR SILENCIEUSE (timeout) - a resoudre puis relancer\n" % nom)
                    continue
                if nb == -1:
                    fh.write("- %s : ERREUR d execution (le test n a pas pu tourner)\n" % nom)
                    continue
                fh.write("- %s : %d [KO]\n" % (nom, nb))
                if aides:
                    fh.write("  - OU CHERCHER :\n")
                    for aide in aides:
                        fh.write("    - %s\n" % aide)
                for ligne in details or []:
                    fh.write("  - %s\n" % ligne)
        if durees:
            fh.write("\n## Tests les plus lents (chrono par test, top 10)\n\n")
            for nom, duree in sorted(durees, key=lambda paire: paire[1], reverse=True)[:10]:
                fh.write("- %s : %.2f s\n" % (nom, duree))
        if lignes_registre is not None:
            fh.write("\nRegistre d usage apres : %d lignes\n" % lignes_registre)
    print(_couleur("[OK] Rapport ecrit : %s" % chemin, "vert"))


def chemin_config_tests(racine):
    """Chemin du fichier de configuration persistante des tests actifs/
    desactives (machine-dependante, gitignore, comme temps-reference.json)."""
    return os.path.join(racine, "cerveau-projet", "agents", "tools", "tester",
                        "tester-lancer-non-regression", "config-tests.json")


def lire_config_tests(racine):
    """Lit la configuration persistante des tests desactives (demande
    utilisateur 2026-08-15 : Janus active/desactive des tests par numero et
    demarre au lancement suivant avec les regles de l utilisation
    precedente). Format JSON : {"desactives": ["test-024", ...]}. Retourne
    la liste des noms test-0XX desactives (vide si fichier absent)."""
    chemin = chemin_config_tests(racine)
    try:
        with io.open(chemin, encoding="utf-8") as fh:
            d = json.load(fh)
        desactives = d.get("desactives", [])
        return [str(x) for x in desactives if str(x).strip()]
    except (IOError, OSError, ValueError):
        return []


def ecrire_config_tests(racine, desactives):
    """Ecrit la configuration persistante des tests desactives (JSON, LF,
    ASCII strict). PRESERVE les categories desactivees (desactivees_categories)
    si deja enregistrees. Cree le fichier s il n existe pas."""
    chemin = chemin_config_tests(racine)
    try:
        ancien = {}
        try:
            with io.open(chemin, encoding="utf-8") as fh:
                ancien = json.load(fh)
        except (IOError, OSError, ValueError):
            ancien = {}
        categories = [str(x) for x in ancien.get("desactivees_categories", [])
                      if str(x).strip()]
        entree = {
            "desactives": sorted(set(desactives)),
            "desactivees_categories": sorted(set(categories)),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(entree, ensure_ascii=True, indent=1) + "\n")
        return True
    except (IOError, OSError):
        return False


def appliquer_config_tests(tests, desactives):
    """Retire de la liste les tests desactives (par nom test-0XX). Retourne
    (actifs, desactives_trouves) : la liste des tests a lancer et ceux qui
    ont ete retires (pour affichage distinct NON LANCE)."""
    if not desactives:
        return tests, []
    actifs = []
    retires = []
    for t in tests:
        nom = os.path.basename(t)
        if any(nom.startswith(d) for d in desactives):
            retires.append(nom)
        else:
            actifs.append(t)
    return actifs, retires


def chemin_reference(racine):
    """Chemin du fichier de reference de temps (dossier de l outil)."""
    return os.path.join(racine, "cerveau-projet", "agents", "tools", "tester",
                        "tester-lancer-non-regression", "temps-reference.json")


def lire_reference(racine):
    """Lit la reference persistee. Retourne (secondes, mode, nb_tests, date)
    ou (None, None, None, None) si absente ou illisible."""
    chemin = chemin_reference(racine)
    if not os.path.isfile(chemin):
        return None, None, None, None
    try:
        with io.open(chemin, encoding="ascii") as fh:
            d = json.load(fh)
        return (float(d.get("reference_secondes", 0)),
                d.get("mode", ""), d.get("nb_tests", 0), d.get("date", ""))
    except Exception:
        return None, None, None, None


def ecrire_reference(racine, duree, mode, nb_tests):
    """Persiste la reference de temps (meilleur temps ou rebase force)."""
    chemin = chemin_reference(racine)
    d = {
        "reference_secondes": round(duree, 1),
        "mode": mode,
        "nb_tests": nb_tests,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    with io.open(chemin, "w", encoding="ascii", newline="\n") as fh:
        json.dump(d, fh, ensure_ascii=True, indent=1)
        fh.write("\n")
    return chemin


def afficher_chrono(racine, duree, mode, nb_tests, seuil=25.0,
                    rebase=False, no_reference=False):
    """Affiche le temps ecoule, compare a la reference et met a jour si
    meilleur. Retourne True si un SIGNAL de ralentissement est emis.

    Regles (demande utilisateur) :
      - chrono demarre au debut de la premiere serie, s arrete a la fin de la
        derniere (mode tous) ;
      - pas de reference -> enregistree comme base ;
      - temps ameliore (plus bas) -> reference mise a jour automatiquement ;
      - temps trop eloigne (> seuil %, defaut 25) -> SIGNAL affiche ;
      - --rebase-reference force la mise a jour ;
      - --no-reference : sous-processus paralleles (jamais de course sur le fichier).
    """
    print(_couleur("=== Temps ecoule : %.1f s (%s, %d tests) ===" % (duree, mode, nb_tests), "bleu"))
    if no_reference:
        return False
    ref, ref_mode, ref_nb, ref_date = lire_reference(racine)
    # Nombre de tests different : la comparaison n a pas de sens (la suite a
    # change) -> nouvelle base enregistree sans SIGNAL (anti-faux positif).
    if ref is not None and ref_nb is not None and int(ref_nb) != nb_tests:
        chemin = ecrire_reference(racine, duree, mode, nb_tests)
        print(_couleur("[CHRONO] Nombre de tests change (%d -> %d) : nouvelle base enregistree : %.1f s"
                       % (int(ref_nb), nb_tests, duree), "jaune"))
        return False
    if ref is None or rebase:
        chemin = ecrire_reference(racine, duree, mode, nb_tests)
        print(_couleur("[CHRONO] Reference enregistree : %.1f s (%s) -> %s"
                       % (duree, mode, chemin), "vert"))
        return False
    pct = (duree - ref) / ref * 100.0 if ref else 0.0
    if duree < ref:
        chemin = ecrire_reference(racine, duree, mode, nb_tests)
        print(_couleur("[CHRONO] Temps ameliore : %.1f s (ancienne reference %.1f s) -> reference mise a jour"
                       % (duree, ref), "vert"))
        return False
    if pct > seuil:
        print(_couleur("[SIGNAL] RALENTISSEMENT : %.1f s vs reference %.1f s (%s, +%.0f%% depassement)"
                       % (duree, ref, ref_date, pct), "rouge"))
        print(_couleur("[SIGNAL] La suite est plus lente que la reference - verifier les tests lents"
                       " (la reference reste enregistree : %.1f s)" % ref, "rouge"))
        return True
    print(_couleur("[CHRONO] Conforme a la reference : %.1f s vs %.1f s (%s, +%.0f%%)"
                   % (duree, ref, ref_date, pct), "vert"))
    return False



def detecter_parent_temporaire(racine):
    """Detecte le script .tmp-*/.zz-* a la racine qui a LANCE ce processus
    (le processus parent direct, en cours d execution).

    Anti-artefact (lecon 2026-08-13, demande utilisateur) : quand on lance la
    non-regression DEPUIS un script temporaire legitime (ex .tmp-controle.py
    qui orchestre plusieurs appels), ce script existe a la racine pendant
    l execution et test-024 le detecte comme un residu -> KO a tort. Le
    parent direct est en cours d execution : ce n est PAS un residu, il doit
    etre exclu du scan de test-024. Un vrai residu (script temporaire laisse
    par erreur, plus utilise par aucun processus) n est jamais le parent
    direct : il reste KO (protection intacte).

    Retourne le nom du fichier temporaire parent, ou None.
    """
    try:
        ppid = os.getppid()
        cmdline = ""
        if os.path.exists("/proc"):
            try:
                with io.open("/proc/%d/cmdline" % ppid, "rb") as fh:
                    cmdline = fh.read().decode(errors="replace").replace("\x00", " ")
            except Exception:
                cmdline = ""
        else:
            # Windows : interroger la ligne de commande du processus parent.
            try:
                r = subprocess.run(
                    ["powershell", "-NoProfile", "-Command",
                     "(Get-CimInstance Win32_Process -Filter 'ProcessId=%d').CommandLine"
                     % ppid],
                    capture_output=True, text=True, timeout=10,
                )
                cmdline = (r.stdout or "").strip()
            except Exception:
                cmdline = ""
        for mot in cmdline.split():
            base = os.path.basename(mot.strip("\"'"))
            if base.startswith(".tmp-") or base.startswith(".zz-"):
                chemin = os.path.join(racine, base)
                if os.path.exists(chemin):
                    return base
    except Exception:
        pass
    return None




def chemin_profils_tests(racine):
    """Chemin du fichier de definition des profils de tests."""
    return os.path.join(racine, "cerveau-projet", "agents", "tools", "tester",
                        "tester-lancer-non-regression", "profils-tests.json")


def charger_profils_tests(racine):
    """Charge profils-tests.json. Retourne (liste_profils, erreur)."""
    chemin = chemin_profils_tests(racine)
    if not os.path.isfile(chemin):
        return None, "fichier introuvable : %s" % chemin
    try:
        with io.open(chemin, encoding="utf-8") as fh:
            data = json.load(fh)
    except ValueError as e:
        return None, "JSON invalide : %s" % e
    profils = data.get("profils", [])
    if not profils:
        return None, "aucun profil dans %s" % chemin
    return profils, None


def _normaliser_glob(g):
    """Normalise un glob : separateur /, sans ./ initial, dossier -> prefixe."""
    g = g.replace("\\", "/").lstrip("./")
    if g.endswith("/"):
        g = g[:-1]
    return g


def _matche_glob(chemin, glob_pat):
    """Matche un chemin contre un glob.

    - Glob sans '*' : prefixe de dossier (tout le sous-arbre) ou egalite.
    - Glob avec '*' : fnmatch segment par segment (fnmatch gere * sans /).
    """
    g = _normaliser_glob(glob_pat)
    if "*" not in g:
        return chemin == g or chemin.startswith(g + "/")
    import fnmatch
    return fnmatch.fnmatch(chemin, g)


def deduire_profils(fichiers, profils, racine):
    """Deduit le(s) profil(s) pertinent(s) a partir des fichiers modifies.

    Chaque fichier est matche contre les globs 'fichiers_detectes' de chaque
    profil (chemins relatifs a la racine, separes par /). Les globs sans '*'
    matchent tout le sous-arbre du dossier (ex: 'cerveau-projet/agents/tools/'
    -> tout ce qui est sous tools/). Le champ optionnel 'fichiers_exclus'
    retire un profil quand le fichier matche un de ses globs d exclusion.
    Un fichier peut declencher plusieurs profils ; on retourne la liste
    (ordonnee comme dans le JSON) des profils retenus.
    """
    touches = set()
    for f in fichiers:
        f = f.strip()
        if not f:
            continue
        f_norm = f.replace("\\", "/").lstrip("./")
        base = os.path.basename(f_norm)
        for p in profils:
            # exclusion : si le fichier matche un glob d exclusion, ce profil
            # ne s applique pas (ex: un test .py est 'tests', pas 'outils').
            exclu = False
            for e in p.get("fichiers_exclus", []):
                e_norm = e.replace("\\", "/").lstrip("./")
                if _matche_glob(f_norm, e_norm) or _matche_glob(base, e_norm):
                    exclu = True
                    break
            if exclu:
                continue
            for glob_pat in p.get("fichiers_detectes", []):
                if _matche_glob(f_norm, glob_pat) or _matche_glob(base, glob_pat):
                    touches.add(p["nom"])
                    break
    return [p["nom"] for p in profils if p["nom"] in touches]


def tests_du_profil(noms_profils, profils):
    """Fusionne les tests de plusieurs profils (dedoublonnage, tri)."""
    tests = set()
    for p in profils:
        if p["nom"] in noms_profils:
            tests.update(p.get("tests", []))
    return sorted(tests)


def filtrer_tests_par_profils(tests, profils_choisis, profils_cfg):
    """Retourne les tests (chemins) restreints aux numeros des profils choisis."""
    numeros = tests_du_profil(profils_choisis, profils_cfg)
    return [t for t in tests
            if os.path.basename(t)[:8] in numeros], numeros


def main():
    # AFFICHAGE EN DIRECT (lecon 2026-08-15, demande utilisateur) : en sortie
    # redirigee (pipe, entonnoir, combo) Python bufferise stdout et ne
    # l affiche qu a la fin - on ne voit RIEN pendant des dizaines de
    # secondes. Le line_buffering force chaque ligne a s afficher des qu
    # elle est emise : le passage des barrieres se voit EN DIRECT.
    try:
        sys.stdout.reconfigure(line_buffering=True)
        sys.stderr.reconfigure(line_buffering=True)
    except Exception:
        pass
    parser = argparse.ArgumentParser(description="Lance la non-regression complete des tests formels")
    parser.add_argument("--series", type=str, default="tous",
                        help="Series a lancer (a|b|c|d|e, liste separee par des virgules ex: a,c, ou tous par defaut)")
    parser.add_argument("--workers", type=int, default=0,
                        help="Nombre de workers paralleles (defaut : config-environnement.json, sinon min(cpu_count, 16))")
    parser.add_argument("--parallele", action="store_true",
                        help="Mode pool de workers (defaut : distribue les tests, longs d abord)")
    parser.add_argument("--serial", action="store_true",
                        help="Force le mode serie complet (ancien comportement)")
    parser.add_argument("--fail-fast", action="store_true",
                        help="PROTECTION STOP : des le premier test KO, la suite est stoppee (les tests restants ne sont pas lances)")
    parser.add_argument("--timeout-test", type=int, default=0,
                        help="Timeout INTERNE par test en secondes (defaut : 180 serie / 300 pool) - jamais de timeout exterieur (regle immuable)")
    parser.add_argument("--seuil", type=float, default=25.0,
                        help="Pourcentage de depassement tolere avant SIGNAL de ralentissement (defaut 25)")
    parser.add_argument("--rebase-reference", action="store_true",
                        help="Force la mise a jour de la reference de temps (meme si plus lent)")
    parser.add_argument("--no-reference", action="store_true",
                        help="Ne pas lire ni ecrire la reference de temps (sous-processus paralleles)")
    parser.add_argument("--tests", type=str, default="",
                        help="Filtrer par noms de test separes par des virgules")
    parser.add_argument("--relancer-ko", action="store_true",
                        help="Mecanisation KO (demande utilisateur 2026-08-16) : relancer UNIQUEMENT les tests en KO du DERNIER run journalise (registre-tests.jsonl, run_id) - isole le probleme, valide le test, puis la serie, avant de relancer la suite complete. Combine a --series X, ne relance QUE les KO de la serie X.")
    parser.add_argument("--ko", type=str, default="reprendre", choices=["nouveau", "reprendre"],
                        help="Serie KO persistante prioritaire (demande utilisateur 2026-08-16, revue 2026-08-17) : 'reprendre' (defaut) lance D ABORD la serie KO (tests de ko-tests.json) avec sa barriere - ceux qui passent sortent du fichier et ne sont PAS relances dans leur serie d origine ; 'nouveau' = MODE BALAYAGE COMPLET : vide ko-tests.json puis lance TOUTES les series SANS arret pour collecter la TOTALITE des KO (ils deviendront la serie KO a revalider).")
    parser.add_argument("--etat-ko", action="store_true",
                        help="Affiche le contenu de la serie KO persistante (ko-tests.json) puis quitte sans lancer")
    parser.add_argument("--ko-puis-stop", action="store_true",
                        help="CYCLE RAPIDE KO (demande utilisateur 2026-08-17, revu) : avec --ko reprendre, la suite valide UNIQUEMENT la serie KO persistante puis s ARRETE des que la barriere KO est franchie (100%% verte) - sans relancer les series A-E. Le rapport indique 'SERIE KO VERTE = CONTROLE TERMINE' (la suite complete finale n est relancee que si un code partage a ete touche - decision Janus). Si la barriere KO est bloquee, comportement existant (STOP + retour 1). Si ko-tests.json est vide, l option est ignoree (avertissement) et la suite se lance normalement.")
    parser.add_argument("--fichiers", type=str, default="",
                        help="Liste de fichiers modifies (separes par des virgules) : deduit automatiquement le(s) profil(s) de tests a lancer (mode profil)")
    parser.add_argument("--profil", type=str, default="",
                        help="Forcer un profil de tests (ex: --profil cartes,outils) - profils: cartes, outils, tests, fiches-agents, docs, registre")
    parser.add_argument("--tags", type=str, default="",
                        help="Ne lancer que les tests portant CES tags (ex: --tags securite,performance, combinaison OR). Tags lus dans le bloc 'Tags:' de la docstring de chaque test.")
    parser.add_argument("--categorie", type=str, default="",
                        help="Lancer une categorie predefinie de tests (ex: --categorie securite). Categories definies dans categories-tests.json (nom -> liste de tags).")
    parser.add_argument("--desactiver-categorie", type=str, default="",
                        help="Desactiver une categorie (ex: --desactiver-categorie performance). PERSISTANT : herite au prochain lancement (les tests de la categorie ne sont pas lances).")
    parser.add_argument("--activer-categorie", type=str, default="",
                        help="Reactiver une categorie (ex: --activer-categorie performance). PERSISTANT.")
    parser.add_argument("--etat-categories", action="store_true",
                        help="Affiche les categories (tags) et leur etat actif/desactive puis quitte sans lancer")
    parser.add_argument("--desactiver", type=str, default="",
                        help="Desactiver des tests par numero (ex: --desactiver 24,28 pour test-024,test-028). PERSISTANT : enregistre dans config-tests.json et herite au prochain lancement.")
    parser.add_argument("--activer", type=str, default="",
                        help="Reactiver des tests par numero (ex: --activer 24 pour test-024). PERSISTANT : retire de config-tests.json.")
    parser.add_argument("--etat-tests", action="store_true",
                        help="Affiche la configuration persistante (tests actifs/desactives) puis quitte sans lancer")
    parser.add_argument("--ordre-fixe", action="store_true",
                        help="Forcer l ordre historique des series (a,b,c,d,e) au lieu du classement dynamique par taux de KO")
    parser.add_argument("--no-journal", action="store_true",
                        help="Rotation du registre d usage avant (plafond 100 usages normaux, defaut)")
    parser.add_argument("--journal", action="store_true",
                        help="Ne touche pas au registre d usage")
    parser.add_argument("--rapport", type=str, default="",
                        help="Chemin du rapport markdown (optionnel)")
    parser.add_argument("--agent", type=str, default="",
                        help="Nom de l agent qui lance les tests (journalise chaque test dans registre-tests.jsonl)")
    parser.add_argument("--version", action="version", version="tester-lancer-non-regression v%s" % VERSION)
    parser.add_argument("--aide", action="help", help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    # VERROU D HABILITATION (regle immuable : seul janus lance la
    # non-regression en production ; vulcain a une liste blanche developpeur
    # (verrou v0.2.2) pour valider ses modifications du lanceur).
    # --agent est OBLIGATOIRE : sans lui, impossible de verifier qui appelle
    # (le verrou refuse rc=2). L appel au verrou se fait
    # AVANT toute action : si l agent n est pas habilite, la suite n est pas
    # lancee et le message indique QUI est habilite et COMMENT l activer.
    if not args.agent:
        print(_couleur("[ERREUR] --agent est OBLIGATOIRE : le lanceur doit "
                       "connaitre l agent appelant (verrou d habilitation).", "rouge"))
        return 2
    code, message = verrouiller_habilitation(args.agent, "tester-lancer-non-regression")
    if code != 0:
        print(_couleur(message, "rouge"))
        return 1 if code == 1 else 2

    racine = racine_projet()
    # CONFIGURATION ADAPTATIVE (demande utilisateur 2026-08-17) : lire la
    # config-environnement.json (generee par configurer-environnement) pour
    # auto-regler les workers et le timeout par test selon les ressources
    # reelles de la machine. Les options CLI --workers et --timeout-test
    # restent prioritaires : la config ne s applique que si elles sont
    # absentes (valeur 0 = non fournie).
    workers_config, timeout_config = lire_workers_config(racine)
    if args.timeout_test <= 0 and timeout_config > 0:
        args.timeout_test = timeout_config
    # run_id du run courant (demande utilisateur 2026-08-16) : timestamp du
    # debut, journalise avec CHAQUE test dans registre-tests.jsonl pour
    # identifier le lancement auquel appartient chaque test (base de
    # --relancer-ko : relancer uniquement les KO du dernier run).
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")

    # MECANISATION KO (demande utilisateur 2026-08-16) : --relancer-ko lit le
    # registre-tests.jsonl, trouve le dernier run (run_id le plus recent),
    # recupere les tests en KO de CE run et ne lance QUE ceux-la. Janus n a
    # plus a deduire la liste : l outil la calcule. Le workflow devient :
    #   1. KO detecte -> analyser le rapport
    #   2. --relancer-ko -> rejouer UNIQUEMENT les tests KO (validation du
    #      correctif, pas de relance de la suite complete)
    #   3. une fois vert -> lancer la serie concernee (--series X)
    #   4. puis seulement -> la suite complete
    #   Variante (demande utilisateur 2026-08-16) : --relancer-ko --series X
    #   filtre les KO sur LA serie X seulement (revalider uniquement les KO
    #   d une serie donnee sans toucher aux autres series).
    if args.relancer_ko:
        dern_run, tests_ko = ko_du_dernier_run(racine)
        if args.series and args.series != "tous":
            tests_ko_serie = [t for t in tests_ko
                              if serie_du_test(os.path.basename(t)) == args.series]
            ecartes = [t for t in tests_ko
                       if serie_du_test(os.path.basename(t)) != args.series]
            if ecartes:
                print(_couleur("[RELANCER-KO] Filtre serie %s : %d KO ecartes "
                               "(appartenant a d autres series) :"
                               % (args.series.upper(), len(ecartes)), "jaune"))
                for nom in ecartes:
                    print("  - %s" % nom)
            tests_ko = tests_ko_serie
        if not tests_ko:
            print(_couleur("[RELANCER-KO] Dernier run (%s) : AUCUN KO %s- rien a relancer."
                           % (dern_run,
                              ("en serie %s " % args.series.upper())
                              if args.series and args.series != "tous" else ""),
                           "vert"))
            print(_couleur("[RELANCER-KO] Suite complete disponible (--agent %s)."
                           % args.agent, "jaune"))
            return 0
        print(_couleur("[RELANCER-KO] Dernier run : %s - relance UNIQUEMENT %d test(s) en KO%s :"
                       % (dern_run, len(tests_ko),
                          (" (serie %s)" % args.series.upper())
                          if args.series and args.series != "tous" else ""),
                       "cyan"))
        for nom in tests_ko:
            print("  - %s" % nom)
        args.tests = ",".join(t for t in tests_ko)

    # Anti-artefact test-024 (lecon 2026-08-13) : si le lanceur est execute
    # DEPUIS un script temporaire legitime (.tmp-*/.zz-* parent direct), le
    # declarer en exclusion pour test-024 (via l environnement, herite par
    # tous les sous-processus). Un vrai residu n est jamais le parent direct.
    parent_tmp = detecter_parent_temporaire(racine)
    if parent_tmp:
        os.environ["NON_REGRESSION_EXCLUSIONS"] = parent_tmp
        print(_couleur("[INFO] Script parent temporaire exclu du garde-fou "
                       "test-024 : %s" % parent_tmp, "jaune"))
    tests = trouver_tests(racine, args.tests)
    if not tests:
        print(_couleur("[ERREUR] Aucun test trouve", "rouge"))
        return 2

    # MODE PROFIL (demande utilisateur 2026-08-16) : Janus choisit le profil
    # selon les fichiers modifies (--fichiers, auto) ou manuellement
    # (--profil). Le mode profil PREND LE PAS sur --series/--tests : on ne
    # lance que les tests des profils choisis. Sans --fichiers ni --profil,
    # comportement historique inchange.
    mode_profil = bool(args.fichiers or args.profil)
    profils_choisis = []
    if mode_profil:
        profils_cfg, err = charger_profils_tests(racine)
        if err:
            print(_couleur("[ERREUR] Profils de tests indisponibles : %s" % err, "rouge"))
            return 2
        if args.profil:
            profils_choisis = [x.strip() for x in args.profil.split(",") if x.strip()]
            connus = [p["nom"] for p in profils_cfg]
            inconnus = [n for n in profils_choisis if n not in connus]
            if inconnus:
                print(_couleur("[ERREUR] Profil(s) inconnu(s) : %s (disponibles : %s)"
                               % (", ".join(inconnus), ", ".join(connus)), "rouge"))
                return 2
        else:
            fichiers = [f.strip() for f in args.fichiers.split(",") if f.strip()]
            if not fichiers:
                print(_couleur("[ERREUR] --fichiers est vide : fournir au moins un chemin", "rouge"))
                return 2
            profils_choisis = deduire_profils(fichiers, profils_cfg, racine)
            if not profils_choisis:
                print(_couleur("[ERREUR] Aucun profil ne couvre les fichiers fournis : %s"
                               % ", ".join(fichiers), "rouge"))
                print(_couleur("  Profils disponibles : %s"
                               % ", ".join(p["nom"] for p in profils_cfg), "jaune"))
                return 2
        tests_filtres, numeros_profils = filtrer_tests_par_profils(tests, profils_choisis, profils_cfg)
        if not tests_filtres:
            print(_couleur("[ERREUR] Aucun test trouve pour le(s) profil(s) : %s"
                           % ", ".join(profils_choisis), "rouge"))
            return 2
        print(_couleur("[PROFIL] %s : %d tests couverts / %d total"
                       % (", ".join(profils_choisis), len(tests_filtres), len(tests)), "cyan"))
        tests = tests_filtres

    # FILTRE PAR TAGS / CATEGORIE (demande utilisateur 2026-08-16) : Janus
    # peut lancer uniquement les tests portant certains tags (--tags) ou une
    # categorie predefinie (--categorie, categories-tests.json). Le filtre
    # s applique apres le mode profil, avant la config des tests.
    categories_cfg, err_cat = charger_categories_tests(racine)
    tags_voulus = []
    if args.categorie:
        noms_cat = [c.strip().lower() for c in args.categorie.split(",") if c.strip()]
        inconnues = [c for c in noms_cat if c not in categories_cfg]
        if inconnues:
            print(_couleur("[ERREUR] Categorie(s) inconnue(s) : %s (disponibles : %s)"
                           % (", ".join(inconnues), ", ".join(sorted(categories_cfg))),
                           "rouge"))
            return 2
        for c in noms_cat:
            tags_voulus.extend(categories_cfg[c])
    if args.tags:
        tags_voulus.extend([t.strip().lower() for t in args.tags.split(",") if t.strip()])
    if tags_voulus:
        tests_tags, _carte_tags = filtrer_tests_par_tags(tests, tags_voulus)
        if not tests_tags:
            print(_couleur("[ERREUR] Aucun test ne porte les tags : %s"
                           % ", ".join(tags_voulus), "rouge"))
            return 2
        print(_couleur("[TAGS] %s : %d tests portent les tags / %d total"
                       % (", ".join(sorted(set(tags_voulus))), len(tests_tags), len(tests)),
                       "cyan"))
        tests = tests_tags

    # CATEGORIES DESACTIVEES (persistantes) : les tests des categories
    # desactivees sont retires de la liste (comme la config des tests).
    desactivees_cat = lire_config_categories(racine)
    if desactivees_cat:
        tags_exclus = set()
        for c in desactivees_cat:
            tags_exclus.update(categories_cfg.get(c, [c]))
        if tags_exclus:
            carte = tags_par_test(tests)
            gardes = []
            retires_cat = []
            for t in tests:
                if set(carte.get(t, [])) & tags_exclus:
                    retires_cat.append(os.path.basename(t))
                else:
                    gardes.append(t)
            if retires_cat:
                print(_couleur("[CATEGORIES] Desactivees : %s - %d test(s) NON LANCES"
                               % (", ".join(desactivees_cat), len(retires_cat)), "jaune"))
            tests = gardes

    # CONFIGURATION PERSISTANTE DES TESTS (demande utilisateur 2026-08-15) :
    # Janus peut activer/desactiver des tests par numero (--activer/
    # --desactiver N). La config est PERSISTEE dans config-tests.json et
    # HERITEE au lancement suivant : la suite demarre avec les regles de
    # l utilisation precedente, puis les overrides de la commande courante
    # sont appliques. --etat-tests affiche l etat sans lancer.
    desactives_config = lire_config_tests(racine)
    tests_desactives = []

    if args.etat_tests:
        actifs, retires = appliquer_config_tests(tests, desactives_config)
        print(_couleur("=== ETAT CONFIGURATION DES TESTS (persistante) ===", "cyan"))
        print("Fichier : %s" % chemin_config_tests(racine))
        print(_couleur("Tests ACTIFS (%d) :" % len(actifs), "vert"))
        for t in actifs:
            print("  %s" % os.path.basename(t))
        print(_couleur("Tests DESACTIVES (%d) :" % len(retires), "rouge"))
        for nom in sorted(retires):
            print("  %s (NON LANCE)" % nom)
        return 0

    if args.etat_ko:
        ko_actuels = lire_ko_tests(racine)
        print(_couleur("=== ETAT SERIE KO PERSISTANTE (ko-tests.json) ===", "cyan"))
        print("Fichier : %s" % ko_tests_defaut(racine))
        print(_couleur("Tests en KO (%d) :" % len(ko_actuels), "rouge" if ko_actuels else "vert"))
        if ko_actuels:
            for nom in sorted(ko_actuels):
                print("  %s (serie %s, relance prioritaire au prochain --ko reprendre)"
                      % (nom, serie_du_test(nom).upper()))
        else:
            print("  (aucun - la serie KO est vide, la suite demarre directement par A)")
        print("Mode actuel : %s" % args.ko)
        return 0

    def _normaliser_numero(n):
        """Accepte 24 ou test-024, retourne test-0XX (ou None si invalide)."""
        n = n.strip()
        if n.startswith("test-"):
            n = n[len("test-"):]
        if not n.isdigit():
            return None
        return "test-%03d" % int(n)

    if args.desactiver:
        nums = [_normaliser_numero(n) for n in args.desactiver.split(",") if n.strip()]
        invalides = [n for n in nums if n is None]
        if invalides:
            print(_couleur("[ERREUR] Numero(s) invalide(s) : %s (attendu 24 ou test-024)"
                           % args.desactiver, "rouge"))
            return 2
        for n_clean in nums:
            if n_clean not in desactives_config:
                desactives_config.append(n_clean)
        if ecrire_config_tests(racine, desactives_config):
            print(_couleur("[CONFIG] Tests desactives et persistes : %s"
                           % ", ".join(sorted(set(desactives_config))), "jaune"))
        else:
            print(_couleur("[ERREUR] Impossible d ecrire config-tests.json", "rouge"))
            return 2

    if args.activer:
        nums = [_normaliser_numero(n) for n in args.activer.split(",") if n.strip()]
        invalides = [n for n in nums if n is None]
        if invalides:
            print(_couleur("[ERREUR] Numero(s) invalide(s) : %s (attendu 24 ou test-024)"
                           % args.activer, "rouge"))
            return 2
        for n_clean in nums:
            if n_clean in desactives_config:
                desactives_config.remove(n_clean)
        if ecrire_config_tests(racine, desactives_config):
            print(_couleur("[CONFIG] Tests reactives et persistes : %s"
                           % ", ".join(sorted(set(desactives_config))), "vert"))
        else:
            print(_couleur("[ERREUR] Impossible d ecrire config-tests.json", "rouge"))
            return 2

    # CATEGORIES : desactiver / reactiver une categorie (persistant) +
    # --etat-categories (affichage sans lancer).
    if args.etat_categories:
        print(_couleur("=== ETAT DES CATEGORIES (tags, persistante) ===", "cyan"))
        print("Fichier : %s" % chemin_categories_tests(racine))
        desactivees_cat = lire_config_categories(racine)
        for nom in sorted(categories_cfg):
            etat = "DESACTIVEE" if nom in desactivees_cat else "active"
            couleur = "rouge" if nom in desactivees_cat else "vert"
            print(_couleur("  %-14s [%s] tags: %s"
                           % (nom, etat, ", ".join(categories_cfg[nom])), couleur))
        return 0

    if args.desactiver_categorie:
        noms_cat = [c.strip().lower() for c in args.desactiver_categorie.split(",") if c.strip()]
        inconnues = [c for c in noms_cat if c not in categories_cfg]
        if inconnues:
            print(_couleur("[ERREUR] Categorie(s) inconnue(s) : %s (disponibles : %s)"
                           % (", ".join(inconnues), ", ".join(sorted(categories_cfg))),
                           "rouge"))
            return 2
        desactivees_cat = lire_config_categories(racine)
        for c in noms_cat:
            if c not in desactivees_cat:
                desactivees_cat.append(c)
        if ecrire_config_categories(racine, desactivees_cat):
            print(_couleur("[CATEGORIES] Desactivees et persistees : %s"
                           % ", ".join(sorted(set(desactivees_cat))), "jaune"))
        else:
            print(_couleur("[ERREUR] Impossible d ecrire config-tests.json", "rouge"))
            return 2

    if args.activer_categorie:
        noms_cat = [c.strip().lower() for c in args.activer_categorie.split(",") if c.strip()]
        inconnues = [c for c in noms_cat if c not in categories_cfg]
        if inconnues:
            print(_couleur("[ERREUR] Categorie(s) inconnue(s) : %s (disponibles : %s)"
                           % (", ".join(inconnues), ", ".join(sorted(categories_cfg))),
                           "rouge"))
            return 2
        desactivees_cat = lire_config_categories(racine)
        for c in noms_cat:
            if c in desactivees_cat:
                desactivees_cat.remove(c)
        if ecrire_config_categories(racine, desactivees_cat):
            print(_couleur("[CATEGORIES] Reactivees et persistees : %s"
                           % ", ".join(sorted(set(desactivees_cat))), "vert"))
        else:
            print(_couleur("[ERREUR] Impossible d ecrire config-tests.json", "rouge"))
            return 2

    # Applique la configuration (persistee + overrides) : les tests desactives
    # sont retires AVANT le decoupage en series, affiches distinctement
    # (NON LANCE) dans le bilan. On conserve la liste BRUTE (avant
    # desactivation) pour distinguer plus bas une serie vide par FILTRE
    # (comportement historique rc=2 "Aucun test trouve") d une serie vide
    # uniquement par DESACTIVATION (skip legitime).
    tests_bruts = list(tests)
    tests, tests_desactives = appliquer_config_tests(tests, desactives_config)
    if tests_desactives:
        print(_couleur("[CONFIG] %d test(s) desactive(s) (herite de config-tests.json) : %s"
                       % (len(tests_desactives), ", ".join(sorted(tests_desactives))), "jaune"))
    if not tests:
        print(_couleur("[ERREUR] Aucun test actif apres application de la configuration", "rouge"))
        return 2

    # Round 11 (chrono) : le chrono demarre au debut de la premiere serie et
    # s arrete a la fin de la derniere. En mode mono-serie, il couvre la serie
    # (sans toucher a la reference globale).
    t0 = time.monotonic()

    if args.series != "tous":
        # Mode series selectionnees (demande utilisateur 2026-08-15) :
        # --series accepte une liste (ex: a,c) en plus du mono (a) et de
        # tous. Les series sont lancees dans l ORDRE D IMPORTANCE (A
        # Fondations d abord) ; si une serie a un KO, la suivante ne se
        # lance pas (philosophie barriere entre series). La protection du
        # registre se fait UNE fois (comme --tous).
        series_demandees = [s.strip().lower() for s in args.series.split(",") if s.strip()]
        series_inconnues = [s for s in series_demandees if s not in SERIES]
        if series_inconnues:
            print(_couleur("[ERREUR] Serie(s) inconnue(s) : %s (valides : a,b,c,d,e)"
                           % ", ".join(sorted(series_inconnues)), "rouge"))
            return 2
        # Ordre d importance : trier les demandees selon SERIES_ORDRE
        ordre = [s for s in SERIES_ORDRE if s in series_demandees]
        protege = not args.journal
        if protege:
            rotation_registre(racine)
        if args.timeout_test > 0:
            # Le timeout INTERNE reste le seul delai (jamais de timeout
            # exterieur - regle immuable) : il devient parametrable pour les
            # tests lents ou les preuves rapides.
            TIMEOUT_POOL = args.timeout_test
        total_ok = total_ko = total_non = 0
        ko_liste_globale = []
        durees_globales = []
        libelles = []
        for serie in ordre:
            selection, _ = assigner_series(tests, serie)
            selection = selection[serie]
            if not selection:
                # Serie vide : distinguer la cause.
                # 1) FILTRE --tests : la serie ne contient aucun test du
                #    filtre -> comportement historique rc=2 "Aucun test
                #    trouve pour la serie" (verifie par test-027 6b).
                # 2) DESACTIVATION : tous les tests de la serie sont
                #    desactives par la config -> skip legitime (le but meme
                #    de la desactivation : controle cible sans relancer les
                #    tests inutiles).
                selection_brute, _ = assigner_series(tests_bruts, serie)
                if not selection_brute[serie]:
                    print(_couleur("[ERREUR] Aucun test trouve pour la serie %s"
                                   % serie.upper(), "rouge"))
                    return 2
                print(_couleur("[CONFIG] Serie %s : aucun test actif (tous desactives), serie sautee"
                               % serie.upper(), "jaune"))
                continue
            ok, ko, ko_liste, non_lances, durees = executer_lot(racine, selection,
                                                                libelle="Serie %s (%s)" % (serie.upper(), SERIES_NOMS[serie]),
                                                                fail_fast=args.fail_fast,
                                                                agent=args.agent,
                                                                serie=serie,
                                                                timeout_test=args.timeout_test,
                                                                run_id=run_id)
            total_ok += ok
            total_ko += ko
            total_non += non_lances
            ko_liste_globale.extend(ko_liste)
            durees_globales.extend(durees)
            libelles.append(serie.upper())
            if ko or non_lances:
                break  # fail-fast entre series (philosophie barriere)
        duree = time.monotonic() - t0
        libelle_series = "Series %s" % ",".join(libelles)
        afficher_chrono(racine, duree, "series-%s" % ",".join(libelles).lower(),
                        total_ok + total_ko + total_non + len(tests_desactives),
                        seuil=args.seuil, rebase=args.rebase_reference,
                        no_reference=True)
        if total_ko:
            afficher_details_ko(ko_liste_globale)
        afficher_tests_lents(durees_globales)
        print("")
        if tests_desactives:
            print(_couleur("=== RESULTAT : %d OK / %d KO (sur %d tests, %d desactives NON LANCES) ==="
                           % (total_ok, total_ko, total_ok + total_ko + total_non,
                              len(tests_desactives)), "vert" if total_ko == 0 else "rouge"))
            print(_couleur("Tests desactives (config persistante) : %s"
                           % ", ".join(sorted(tests_desactives)), "jaune"))
        else:
            print(_couleur("=== RESULTAT : %d OK / %d KO (sur %d tests, %d non lances) ==="
                           % (total_ok, total_ko, total_ok + total_ko + total_non - total_non, total_non),
                           "vert" if total_ko == 0 else "rouge"))
        if profils_choisis:
            print(_couleur("[PROFIL] Lance avec le(s) profil(s) : %s"
                           % ", ".join(profils_choisis), "cyan"))
        lignes = None
        if protege:
            lignes = afficher_etat_registre(racine)
        if args.rapport:
            ecrire_rapport(args.rapport,
                           libelle_series,
                           "=== RESULTAT : %d OK / %d KO (sur %d tests, %d non lances) ==="
                           % (total_ok, total_ko, total_ok + total_ko + total_non - total_non, total_non),
                           ko_liste_globale, lignes, durees_globales)
        return 1 if (total_ko or total_non) else 0

    # Mode tous : protection du registre faite UNE fois par le parent.
    # (decision utilisateur 2026-08-14 : plus d archivage historique, purge
    # simple qui PRESERVE les entrees mode script-temporaire, memoire des
    # declarations conservee dans le registre actif).
    protege = not args.journal
    if protege:
        rotation_registre(racine)

    par_serie, hors_serie = assigner_series(tests, "tous")
    ko_liste = []
    tot_ok = tot_ko = 0
    tot_non_lances = 0
    durees_total = []

    # =====================================================================
    # SERIE KO PRIORITAIRE (demande utilisateur 2026-08-16, v0.5.5) :
    # fichier persistant ko-tests.json qui garde les tests en KO entre les
    # lancements. Deux modes :
    #   --ko nouveau   : vide ko-tests.json, lance les series normalement
    #                    (A->E avec barrieres), puis COLLECTE les tests en
    #                    KO dans ko-tests.json pour le prochain run.
    #   --ko reprendre (defaut) : lance D ABORD la serie KO (les tests du
    #                    fichier) avec SA barriere. Les tests KO qui PASSENT
    #                    sont RETIRES du fichier et NE SONT PAS relances dans
    #                    leur serie d origine (marques valides pour ce run).
    #                    Si un test de la serie KO ECHOUE encore, la barriere
    #                    KO est BLOQUEE et la suite s arrete (Janus corrige
    #                    puis relance en --ko reprendre). Une fois la barriere
    #                    KO franchie, les series A->E s executent SANS les
    #                    tests deja valides, et les nouveaux KO rejoignent
    #                    ko-tests.json. Idempotent : un test valide par la
    #                    serie KO ne tourne qu UNE fois par run.
    # La serie KO s applique UNIQUEMENT au mode barrieres (defaut), pas aux
    # modes --serial / --parallele (qui gardent leur comportement historique).
    # =====================================================================
    ko_valides_run = set()      # tests valides par la serie KO (a ne pas relancer)
    ko_fichier = lire_ko_tests(racine)
    ko_restants = []            # tests KO non valides apres la barriere KO
    mode_ko = "barrieres"
    balayage = args.ko == "nouveau" and not (args.serial or args.parallele) and not mode_profil
    if not (args.serial or args.parallele) and not mode_profil:
        if args.ko == "nouveau":
            ecrire_ko_tests(racine, [])
            ko_fichier = []
            print(_couleur("[SERIE KO] Mode NOUVEAU (BALAYAGE COMPLET) : ko-tests.json "
                           "vide - TOUTES les series s executent SANS arret pour "
                           "collecter la TOTALITE des KO, puis la serie KO devient "
                           "la seule a revalider.", "cyan"))
        elif ko_fichier:
            print(_couleur("[SERIE KO] Mode REPRENDRE : %d test(s) en KO du fichier, "
                           "relance prioritaire avant les series A-E :"
                           % len(ko_fichier), "cyan"))
            for nom in sorted(ko_fichier):
                print(_couleur("  - %s (serie %s)" % (nom, serie_du_test(nom).upper()), "jaune"))
        else:
            print(_couleur("[SERIE KO] Mode REPRENDRE : serie KO vide - la suite demarre "
                           "par la serie A.", "cyan"))
            if args.ko_puis_stop:
                print(_couleur("[SERIE KO] --ko-puis-stop IGNORE : ko-tests.json est vide, "
                               "il n y a rien a revalider - la suite complete se lance "
                               "normalement.", "jaune"))
        if ko_fichier:
            # La serie KO a SA propre barriere : tests en parallele (pool),
            # puis serie si KO persistant -> barriere bloquee.
            print(_couleur("[BARRIERE KO] Serie KO persistante : lancement...", "bleu"))
            ko_chemin = [t for t in tests if os.path.basename(t) in ko_fichier]
            manquants = [nom for nom in ko_fichier
                         if nom not in {os.path.basename(t) for t in tests}]
            if manquants:
                print(_couleur("[SERIE KO] %d test(s) du fichier introuvable(s) "
                               "(deplaces, desactives ou supprimes) - retires : %s"
                               % (len(manquants), ", ".join(sorted(manquants))), "jaune"))
            ko_restants = []
            ko_ok = ko_ko = ko_non = 0
            ko_ko_liste = []
            ko_durees = []
            if ko_chemin:
                if args.workers and args.workers > 0:
                    workers = args.workers
                else:
                    workers = workers_config
                ko_pool = [t for t in ko_chemin
                           if not any(os.path.basename(t).startswith(g)
                                      for g in GARDE_FOUS_GLOBAUX + TESTS_SERIE_EXCLUSIFS)]
                ko_exclusifs = [t for t in ko_chemin
                                if any(os.path.basename(t).startswith(g)
                                       for g in GARDE_FOUS_GLOBAUX + TESTS_SERIE_EXCLUSIFS)]
                if ko_pool:
                    ok_k, ko_k, ko_l_k, non_k, dur_k = executer_pool(
                        racine, ko_pool, workers,
                        fail_fast=args.fail_fast, agent=args.agent, serie="ko",
                        timeout_test=args.timeout_test, run_id=run_id)
                    ko_ok += ok_k
                    ko_ko += ko_k
                    ko_non += non_k
                    ko_ko_liste.extend(ko_l_k)
                    ko_durees.extend(dur_k)
                if ko_exclusifs:
                    ok_k, ko_k, ko_l_k, non_k, dur_k = executer_lot(
                        racine, ko_exclusifs,
                        libelle="BARRIERE KO - exclusifs (serie)",
                        fail_fast=args.fail_fast, agent=args.agent, serie="ko",
                        timeout_test=args.timeout_test, run_id=run_id)
                    ko_ok += ok_k
                    ko_ko += ko_k
                    ko_non += non_k
                    ko_ko_liste.extend(ko_l_k)
                    ko_durees.extend(dur_k)
                # Les tests KO qui PASSENT sortent du fichier et sont marques
                # valides (pas de re-lancement dans leur serie d origine).
                noms_ok_ko = [os.path.basename(t) for t in ko_pool + ko_exclusifs
                              if os.path.basename(t) not in {k[0] for k in ko_ko_liste}]
                ko_valides_run.update(noms_ok_ko)
                # ko_restants = KO persistants NON valides (les introuvables
                # ont deja ete retires de la liste manquants).
                noms_ko_lances = {os.path.basename(t) for t in ko_chemin}
                ko_restants = [nom for nom in ko_fichier
                               if nom in noms_ko_lances and nom not in ko_valides_run]
            tot_ok += ko_ok
            tot_ko += ko_ko
            tot_non_lances += ko_non
            ko_liste.extend(ko_ko_liste)
            durees_total.extend(ko_durees)
            if ko_ko > 0 or ko_non > 0:
                ecrire_ko_tests(racine, ko_restants or ko_fichier)
                print(_couleur(
                    "[BARRIERE KO BLOQUEE] La serie KO a encore %d KO : la suite "
                    "est STOPPEE. Reparer puis relancer en --ko reprendre."
                    % (ko_ko + ko_non), "rouge"))
                print(_couleur("[SERIE KO] Reste en KO : %s"
                               % ", ".join(sorted(ko_restants or ko_fichier)), "jaune"))
                barriere_ko_bloquee = True
            else:
                ecrire_ko_tests(racine, ko_restants)
                if ko_restants:
                    print(_couleur("[SERIE KO] KO valides et retires du fichier : %s"
                                   % ", ".join(sorted(ko_valides_run)), "vert"))
                print(_couleur("[BARRIERE KO FRANCHIE] Serie KO : 100%% verte, "
                               "passage aux series A-E.", "vert"))
                barriere_ko_bloquee = False

    # SORTIE ANTICIPEE si la barriere KO est bloquee (STOP avant A-E).
    if not (args.serial or args.parallele) and not mode_profil and \
       args.ko != "nouveau" and "barriere_ko_bloquee" in dir() and barriere_ko_bloquee:
        duree = time.monotonic() - t0
        nb_desactives = len(tests_desactives)
        bilan = "=== RESULTAT GLOBAL : %d OK / %d KO (sur %d tests, %d non lances - STOP barriere KO) ===" \
                % (tot_ok, tot_ko, len(tests) - tot_non_lances, tot_non_lances)
        print("")
        print(_couleur(bilan, "rouge"))
        if tot_ko:
            afficher_details_ko(ko_liste)
        afficher_tests_lents(durees_total)
        if args.rapport:
            ecrire_rapport(args.rapport, "Non-regression globale", bilan, ko_liste,
                           None, durees_total)
        return 1

    # SORTIE ANTICIPEE --ko-puis-stop (cycle rapide KO, demande utilisateur
    # 2026-08-17) : la barriere KO est FRANCHIE (100% verte) et l utilisateur
    # ne veut valider QUE les tests en KO du fichier avant de corriger la
    # suite : la suite s ARRETE ICI, sans relancer les series A-E (gain du
    # temps de correction). Le rapport indique clairement qu une validation
    # FINALE (suite complete) est requise. Le chrono ne touche JAMAIS la
    # reference globale (run partiel).
    if (not (args.serial or args.parallele) and not mode_profil and
            args.ko != "nouveau" and args.ko_puis_stop and
            "barriere_ko_bloquee" in dir() and not barriere_ko_bloquee):
        duree = time.monotonic() - t0
        nb_desactives = len(tests_desactives)
        bilan = ("=== RESULTAT : SERIE KO VALIDEE : %d OK / %d KO - suite "
                 "STOPPEE (--ko-puis-stop) ===\n"
                 "=== SERIE KO VERTE = CONTROLE TERMINE ===\n"
                 "=== Si le correctif a touche du code partage (outil/carte "
                 "pinne par plusieurs tests), relancer la suite complete "
                 "pour la garantie anti-cascade (decision Janus) ==="
                 % (tot_ok, tot_ko))
        print("")
        print(_couleur(bilan, "vert" if tot_ko == 0 else "rouge"))
        print(_couleur("[SERIE KO] %d test(s) valide(s) et retire(s) du fichier : %s"
                       % (len(ko_valides_run), ", ".join(sorted(ko_valides_run))), "vert"))
        if tot_ko:
            afficher_details_ko(ko_liste)
        afficher_tests_lents(durees_total)
        if args.rapport:
            ecrire_rapport(args.rapport, "Serie KO (--ko-puis-stop)", bilan,
                           ko_liste, None, durees_total)
        afficher_chrono(racine, duree, "barriere-ko", len(tests),
                        seuil=args.seuil, rebase=args.rebase_reference,
                        no_reference=True)
        return 0 if tot_ko == 0 else 1

    # Exclusion des tests deja valides par la serie KO : ils ne doivent PAS
    # etre relances dans leur serie d origine (idempotence du run).
    if ko_valides_run:
        noms_a_garder = [t for t in tests
                         if os.path.basename(t) not in ko_valides_run]
        ecartes_ko = len(tests) - len(noms_a_garder)
        if ecartes_ko:
            print(_couleur("[SERIE KO] %d test(s) deja valide(s) par la serie KO, "
                           "non relances dans leur serie : %s"
                           % (ecartes_ko, ", ".join(sorted(ko_valides_run))), "vert"))
        tests = noms_a_garder
        par_serie, hors_serie = assigner_series(tests, "tous")

    # Round 18 : BARRIERES DE PASSAGE = NOUVEAU DEFAUT (demande utilisateur).
    # Les series s executent dans l ORDRE D IMPORTANCE (fondations d abord).
    # Chaque serie doit etre 100% VERTE pour FRANCHIR la barriere vers la
    # suivante. Si une serie a un KO (ou un non-lance), la barriere appelle la
    # protection STOP : la suite s ARRETE, le rapport de la serie est fourni
    # pour constater/analyser/reparer, puis on relance. Quand toutes les
    # barrieres sont passees : rapport GLOBAL POSITIF.
    # --parallele conserve l ancien pool de workers (option) ; --serial force
    # une passe serie simple sans barrieres (ancien comportement de secours).
    if args.serial:
        # Mode serie simple (ancien comportement de secours, sans barrieres).
        ok, ko, ko_liste, non_lances, durees_total = executer_lot(racine, tests, libelle="",
                                                                 fail_fast=args.fail_fast,
                                                                 agent=args.agent,
                                                                 serie="tous",
                                                                 timeout_test=args.timeout_test,
                                                                 run_id=run_id)
        tot_ok, tot_ko = ok, ko
        tot_non_lances = non_lances
    elif args.parallele:
        # POOL DE WORKERS (option --parallele, comportement historique).
        # Les tests hors garde-fous globaux sont tries par duree decroissante
        # et distribues sur N workers ; les garde-fous globaux (registre,
        # sessions, scripts temporaires) tournent en SERIE a la fin.
        if args.workers and args.workers > 0:
            workers = args.workers
        else:
            workers = workers_config
        exclu_ou_global = GARDE_FOUS_GLOBAUX + TESTS_SERIE_EXCLUSIFS
        tests_pool = [t for t in tests
                      if not any(os.path.basename(t).startswith(g)
                                 for g in exclu_ou_global)]
        tests_globaux = [t for t in tests
                         if any(os.path.basename(t).startswith(g)
                                for g in exclu_ou_global)]
        if hors_serie:
            print(_couleur("[AVERTISSEMENT] %d test(s) sans serie affectee, lances avec le pool : %s"
                           % (len(hors_serie), ", ".join(os.path.basename(h) for h in hors_serie)), "jaune"))
        ok_p, ko_p, ko_liste_p, non_lances_p, durees_p = executer_pool(
            racine, tests_pool + hors_serie, workers,
            fail_fast=args.fail_fast, agent=args.agent, serie="tous",
            timeout_test=args.timeout_test, run_id=run_id)
        tot_ok += ok_p
        tot_ko += ko_p
        tot_non_lances += non_lances_p
        ko_liste.extend(ko_liste_p)
        durees_total.extend(durees_p)
        # Garde-fous globaux en serie finale (jamais en parallele).
        if tests_globaux and non_lances_p == 0:
            ok_g, ko_g, ko_liste_g, non_lances_g, durees_g = executer_lot(
                racine, tests_globaux,
                libelle="Garde-fous globaux + exclusifs (registre, sessions, scripts temp, README)",
                fail_fast=args.fail_fast, agent=args.agent, serie="globaux",
                timeout_test=args.timeout_test, run_id=run_id)
            tot_ok += ok_g
            tot_ko += ko_g
            tot_non_lances += non_lances_g
            ko_liste.extend(ko_liste_g)
            durees_total.extend(durees_g)
    else:
        # BARRIERES (NOUVEAU DEFAUT) : chaque serie dans l ordre d importance,
        # barriere 100% verte avant la suivante, STOP au premier KO.
        # FIL DE PROGRESSION EN DIRECT (demande utilisateur 2026-08-15) : la
        # ligne [BARRIERES ...] se complete a CHAQUE barriere franchie - on
        # voit le parcours se construire sans attendre la fin.
        barriere_bloquee = None
        fil = []
        # ORDRE DYNAMIQUE (demande utilisateur 2026-08-15) : les series avec
        # le plus de KO passent en premier (sauf --ordre-fixe). Le classement
        # est affiche pour transparence.
        ordre_execution = (list(SERIES_ORDRE) if args.ordre_fixe
                           else ordre_series_par_ko(racine, nb_derniers=5))
        print(_couleur("[ORDRE SERIES] %s" % " > ".join(s.upper() for s in ordre_execution),
                       "cyan"))
        for s in ordre_execution:
            selection = par_serie[s]
            if not selection:
                continue
            print(_couleur("[BARRIERE %s] %s : lancement..." % (s.upper(), SERIES_NOMS[s]), "bleu"))
            # POOL INTRA-SERIE (round 19, optimisation performance 2026-08-16) :
            # les tests de la serie tournent en parallele sur le pool de
            # workers ; les tests exclusifs (fichiers partages : README,
            # registre, temps-reference) tournent en serie a la fin pour
            # eviter les courses. Gain mesure : 127.8s -> ~57s.
            exclu_ou_global = GARDE_FOUS_GLOBAUX + TESTS_SERIE_EXCLUSIFS
            sel_pool = [t for t in selection
                        if not any(os.path.basename(t).startswith(g)
                                   for g in exclu_ou_global)]
            sel_exclusifs = [t for t in selection
                             if any(os.path.basename(t).startswith(g)
                                    for g in exclu_ou_global)]
            ok_s = ko_s = non_lances_s = 0
            ko_liste_s = []
            durees_s = []
            if sel_pool:
                if args.workers and args.workers > 0:
                    workers = args.workers
                else:
                    workers = workers_config
                ok_p, ko_p, ko_liste_p, non_lances_p, durees_p = executer_pool(
                    racine, sel_pool, workers,
                    fail_fast=args.fail_fast, agent=args.agent, serie=s,
                    timeout_test=args.timeout_test, run_id=run_id)
                ok_s += ok_p
                ko_s += ko_p
                non_lances_s += non_lances_p
                ko_liste_s.extend(ko_liste_p)
                durees_s.extend(durees_p)
            if sel_exclusifs:
                ok_e, ko_e, ko_liste_e, non_lances_e, durees_e = executer_lot(
                    racine, sel_exclusifs,
                    libelle="BARRIERE %s - exclusifs (serie)" % s.upper(),
                    fail_fast=args.fail_fast, agent=args.agent, serie=s,
                    timeout_test=args.timeout_test, run_id=run_id)
                ok_s += ok_e
                ko_s += ko_e
                non_lances_s += non_lances_e
                ko_liste_s.extend(ko_liste_e)
                durees_s.extend(durees_e)
            tot_ok += ok_s
            tot_ko += ko_s
            tot_non_lances += non_lances_s
            ko_liste.extend(ko_liste_s)
            durees_total.extend(durees_s)
            if ko_s > 0 or non_lances_s > 0:
                fil.append("%s X" % s.upper())
                if balayage:
                    # MODE BALAYAGE (--ko nouveau, demande utilisateur
                    # 2026-08-17) : PAS de STOP au premier KO - on continue
                    # TOUTES les series pour collecter la totalite des KO,
                    # qui deviendront la serie KO a revalider ensuite.
                    print(_couleur(
                        "[BALAYAGE] Serie %s : %d KO - suite du balayage "
                        "(collecte totale des KO, pas d arret)."
                        % (s.upper(), ko_s + non_lances_s), "jaune"))
                    print(_couleur("[PROGRESSION] %s" % " > ".join(fil), "jaune"))
                    continue
                barriere_bloquee = s
                print(_couleur(
                    "[BARRIERE BLOQUEE] Serie %s non 100%% verte : la suite est STOPPEE. "
                    "Reparer les KO puis relancer pour franchir la barriere."
                    % s.upper(), "rouge"))
                print(_couleur("[PROGRESSION] %s" % " > ".join(fil), "jaune"))
                break
            fil.append("%s V" % s.upper())
            print(_couleur("[BARRIERE FRANCHIE] Serie %s : 100%% verte, passage autorise."
                           % s.upper(), "vert"))
            print(_couleur("[PROGRESSION] %s" % " > ".join(fil), "vert"))
        if barriere_bloquee is None and hors_serie:
            print(_couleur("[AVERTISSEMENT] %d test(s) sans serie affectee, lances en queue : %s"
                           % (len(hors_serie), ", ".join(os.path.basename(h) for h in hors_serie)), "jaune"))
            ok_h, ko_h, ko_liste_h, non_lances_h, durees_h = executer_lot(
                racine, hors_serie, libelle="Tests hors-serie (queue)",
                fail_fast=args.fail_fast, agent=args.agent, serie="hors-serie",
                timeout_test=args.timeout_test, run_id=run_id)
            tot_ok += ok_h
            tot_ko += ko_h
            tot_non_lances += non_lances_h
            ko_liste.extend(ko_liste_h)
            durees_total.extend(durees_h)

    # COLLECTE DES KO DANS LA SERIE KO PERSISTANTE (fin de run, mode barrieres
    # uniquement) : les tests en KO du run rejoignent ko-tests.json pour le
    # prochain --ko reprendre. En mode NOUVEAU, le fichier a ete vide en debut
    # de run : il ne contient donc que les KO de CE run (comportement attendu :
    # 'nouveau' oublie les KO precedents et collecte les nouveaux). En mode
    # REPRENDRE, les KO restants (non valides par la barriere KO) + les
    # nouveaux KO du run sont fusionnes. Seuls les tests reellement KO ou
    # non lances (STOP) sont collectes - un test valide par la serie KO n y
    # figure pas. Les noms stockes sont les NOMS COMPLETS (basename avec
    # suffixe, ex: test-032-pool-workers.py) pour matcher les chemins.
    if not (args.serial or args.parallele) and not mode_profil:
        noms_ko_run = sorted({k[0] for k in ko_liste})
        # En mode reprendre, on conserve les KO restants du fichier (ceux qui
        # n ont pas passe la barriere KO n existent plus : la suite s est
        # arretee avant) - on repart donc de la collecte du run courant.
        nouveau_fichier_ko = sorted(set(noms_ko_run) | set(ko_restants))
        if noms_ko_run or ko_restants or args.ko == "nouveau":
            ecrire_ko_tests(racine, nouveau_fichier_ko)
            if noms_ko_run:
                print(_couleur("[SERIE KO] %d test(s) en KO collecte(s) dans ko-tests.json "
                               "(relance prioritaire au prochain --ko reprendre) :"
                               % len(noms_ko_run), "jaune"))
                for nom in noms_ko_run:
                    print("  - %s (serie %s)" % (nom, serie_du_test(nom).upper()))
            elif ko_restants:
                print(_couleur("[SERIE KO] ko-tests.json conserve %d test(s) en KO."
                               % len(ko_restants), "jaune"))




    duree = time.monotonic() - t0
    nb_desactives = len(tests_desactives)
    if balayage:
        bilan = ("=== BALAYAGE COMPLET : %d OK / %d KO (totalite des KO "
                 "collectes dans ko-tests.json) ===\n"
                 "=== PASSER A LA REVALIDATION : --ko reprendre valide UNIQUEMENT "
                 "la serie KO (les autres tests restent verts) ==="
                 % (tot_ok, tot_ko))
    elif tot_non_lances:
        bilan = "=== RESULTAT GLOBAL : %d OK / %d KO (sur %d tests, %d non lances - STOP) ===" \
                % (tot_ok, tot_ko, len(tests) - tot_non_lances, tot_non_lances)
    elif nb_desactives:
        bilan = "=== RESULTAT GLOBAL : %d OK / %d KO (sur %d tests, %d desactives NON LANCES) ===" \
                % (tot_ok, tot_ko, len(tests), nb_desactives)
    else:
        bilan = "=== RESULTAT GLOBAL : %d OK / %d KO (sur %d tests) ===" % (tot_ok, tot_ko, len(tests))
    print("")
    print(_couleur(bilan, "vert" if tot_ko == 0 else "rouge"))
    if profils_choisis:
        print(_couleur("[PROFIL] Lance avec le(s) profil(s) : %s"
                       % ", ".join(profils_choisis), "cyan"))
    if nb_desactives:
        print(_couleur("Tests desactives (config persistante) : %s"
                       % ", ".join(sorted(tests_desactives)), "jaune"))
    if tot_ko:
        afficher_details_ko(ko_liste)
    afficher_tests_lents(durees_total)
    # La reference globale n est geree QUE par un run COMPLET sans filtre ET
    # 100% VERT : un run cible (--tests), un appel interne, OU une suite
    # ARRETEE par une barriere (KO) ne doivent jamais la lire ni l ecrire
    # (sinon une reference partielle fausserait la comparaison - lecon
    # 2026-08-15 : une barriere bloquee en B avait enregistre 15.4 s pour
    # 23/55 tests, faussant le SIGNAL suivant a +531%).
    reference_globale = not args.tests and tot_ko == 0 and tot_non_lances == 0
    mode_chrono = "barrieres" if not (args.serial or args.parallele) else \
                  ("pool-%d" % workers if args.parallele else "serie")
    afficher_chrono(racine, duree, mode_chrono, len(tests),
                    seuil=args.seuil, rebase=args.rebase_reference,
                    no_reference=args.no_reference or not reference_globale)

    # RATING DES SERIES ET RATING GENERAL (demande utilisateur 2026-08-15) :
    # le lanceur evalue chaque serie (critere temps + fiabilite) et le run
    # complet via evaluer-rating. Affichage en fin de run, apres le chrono.
    if args.agent:
        afficher_rating_fin_de_run(racine)

    lignes = None
    if protege:
        lignes = afficher_etat_registre(racine)

    if args.rapport:
        ecrire_rapport(args.rapport, "Non-regression globale", bilan, ko_liste,
                       lignes, durees_total)

    return 1 if (tot_ko or tot_non_lances) else 0


if __name__ == "__main__":
    sys.exit(main())
