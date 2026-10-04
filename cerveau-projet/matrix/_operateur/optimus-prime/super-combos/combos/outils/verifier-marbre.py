#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-marbre.py -- Garde : la BORNE du marbre, rejouee sur un journal JETABLE.

POURQUOI (MO-250, racine des doublons MO-202 et MO-240) : la borne `debut` d une
mission avait DEUX ecrivains -- le PILOTE a l injection (mode idempotent,
`--si-absent oui`) et l AGENT sur l ORDRE 4.5 du demarrage
(`suivi-optimus noter --action debut`). L agent qui obeissait fabriquait un
DOUBLON, et `verifier` le comptait en ECART. Le defaut n etait donc pas dans le
journal : il etait dans le CONTRAT (une borne, deux maisons).

CE QUE LE ROUND A TRANCHE : le PILOTE est la SEULE maison qui pose le debut a
l injection ; l agent ne le redeclare que pour une REPRISE (meme mission menee en
DEUX sessions). Cette decision vit dans le demarrage (ORDRE 4.5) -- un TEXTE ne se
mesure pas. Ce garde mesure le COMPORTEMENT : le chemin complet est rejoue sur un
journal JETABLE, dans les deux sens.

CE QU IL EXIGE (1 controle + 10 epreuves rejouees ; la REPRISE est eprouvee dans les
DEUX sens, et le dernier passage mesure que MO-901 reste OUVERTE : une mission en
cours n est pas un ecart, et le journal du cobaye le prouve).

  1. LE CONTRE-TEMOIN : borne du pilote PUIS borne de l agent = 2 debuts, et
     `verifier` ACCUSE. Sans ce sens, un garde vert ne prouve rien : il faut
     d abord que le defaut soit REEL et qu il ne soit pas silencieux ;
  2. MO-202 REPRODUIT : 2 debuts + 1 fin (la signature exacte du defaut mesure)
     est un ECART -- c est ce que le createur a vu le 2026-09-19 ;
  3. LA REPARATION NOMMEE (`archiver --doublons`) : le journal repasse a
     1 debut / 1 fin, le 2e evenement part a l ARCHIVE DEDIEE, et `verifier`
     rend VERT -- la preuve exigee par la mission, mesuree sur piece ;
  4. L IDEMPOTENCE DU PILOTE (`--si-absent oui`) : deux passages ne posent QU UNE
     borne (le pilote COMBLE le trou, il ne double jamais) ;
  5. LA REPRISE LEGITIME : 2 debuts + 2 fins d une mission DECLAREE sont acceptes,
     et les memes 2 debuts + 2 fins d une mission NON declaree sont accuses -- un
     garde qui accepte tout ne garde rien ;
  6. LE GARDE ANTI-FIN-ORPHELINE : une fin declaree SEULE fait naitre un debut
  7. LA FIN A UN SEUL ECRIVAIN (MO-455) : ORDRE 4.5 prescrivait a l agent de poser
     la fin ; mesure du 2026-09-27 -- le geste de l agent joue APRES la cloture pose
     une 2e fin, ACCUSEE par `verifier`. Trois epreuves : le defaut reproduit
     (1 debut / 2 fins, ECART), la reparation qui GARDE la PREMIERE fin (celle du
     pilote), et le chemin CORRIGE (la cloture du pilote seule : 1 debut / 1 fin,
     VERDICT VERT). Le texte du protocole porte desormais la meme regle.
     implicite (le journal n est jamais reecrit) et laisse `verifier` VERT -- le
     chemin de la porte est eprouve en entier, pas seulement ce qui nous occupe.

CE QU IL NE FAIT PAS : il n ecrit RIEN dans la Matrice. Le workspace du cobaye
(AGENTS.md, data/commun, data/outils/suivi-optimus, journal, empreinte, archive)
est entierement une COPIE dans un dossier JETABLE, retire TOUJOURS -- meme si le
bloc leve. L epreuve ne se paie pas d un faux evenement dans le vrai marbre, et un
retrait partiel est DIT au lieu d etre avale.

Usage: python verifier-marbre.py [--racine <path>]
  code 0 = sain, 1 = ecart (nomme), 2 = zone introuvable.
"""

import argparse
import importlib.util
import json
import shutil
import subprocess

import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-414, vague 4 du lot) -----------------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : on remonte
# jusqu au dossier `matrix`, et on REFUSE plutot que de deviner (garde-foi L-006).
_RACINE_LANCEMENT = Path(__file__).resolve().parent
while _RACINE_LANCEMENT.name != "matrix":
    if _RACINE_LANCEMENT.parent == _RACINE_LANCEMENT:
        raise RuntimeError("racine `matrix` introuvable en remontant depuis " + __file__)
    _RACINE_LANCEMENT = _RACINE_LANCEMENT.parent
_REPERTOIRE_COMMUN_LANCEMENT = _RACINE_LANCEMENT / "matrice" / "data" / "commun"
if not (_REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(_REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(_REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(_REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())

import sys
from pathlib import Path

# Les deux missions du cobaye : elles n existent QUE dans le journal jetable.
MISSION_DOUBLE = "MO-900"
MISSION_PILOTE = "MO-901"
MISSION_ORPHELINE = "MO-902"
# LE DEFAUT MO-455 (2026-09-27) : ORDRE 4.5 prescrivait `suivi-optimus noter --action
# fin` comme le geste NORMAL de cloture, alors que le PILOTE declare deja la fin
# (idempotent). Le geste de l agent, joue APRES la cloture, pose une 2e FIN.
MISSION_FIN_DEFAUT = "MO-903"
# LE CHEMIN CORRIGE : la cloture du pilote SEULE.
MISSION_FIN_PROPRE = "MO-904"
DETAIL_FIN_PILOTE = "fin declaree par le pilote (cloture)"
DETAIL_FIN_AGENT = "borne redeclaree par l AGENT (ORDRE 4.5)"
DETAIL_PILOTE = "borne posee par le PILOTE (injection)"
DETAIL_AGENT = "borne redeclaree par l AGENT (ORDRE 4.5)"
PREFIXE_FIXTURE = "cobaye-marbre-"
MARQUEUR_FIXTURE = "AGENTS.md"
CONTENU_MARQUEUR = "fixture jetable du garde du marbre (MO-250) : racine du cobaye.\n"
NOM_FABRIQUE = "cobayes_jetables.py"
# Le repertoire du marbre, relatif a la Matrice (racine de resolution des chemins).
RACINE_MATRICE_RELATIVE = ("matrice",)
COMMUN_RELATIF = ("matrice", "data", "commun")
OUTIL_RELATIF = ("matrice", "data", "outils", "suivi-optimus")
CHEMIN_FONCTIONS = ("verifier", "fonctions.py")
NOM_JOURNAL = "suivi-optimus.jsonl"
NOM_ARCHIVE_DOUBLONS = "suivi-optimus-doublons.jsonl"
NOM_MARQUEUR_FIN_ORPHELINE = "Debut implicite"

RESULTATS = []
COBAYE = []


def controler(nom, condition, detail=""):
    """Enregistre et affiche UN controle du garde (nomme, jamais muet)."""
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def cobaye(nom, condition, detail=""):
    """Enregistre et affiche UNE epreuve REJOUEE (la suite les COMPTE et les DIT)."""
    reussie = bool(condition)
    COBAYE.append((nom, reussie))
    print("cobaye " + str(len(COBAYE)) + " : " + nom + " : " + ("OK" if reussie else "KO")
          + (" -- " + detail if detail else ""))
    return reussie


def trouver_matrice(racine):
    """Le dossier `matrice/` (chemin absolu), ou None : les 3 formes du workspace."""
    candidats = [
        racine / "cerveau-projet" / "matrix" / "matrice",
        racine / "matrix" / "matrice",
        racine / "matrice",
        racine,
    ]
    for candidat in candidats:
        if (candidat / "data" / "outils" / "suivi-optimus" / "main.py").is_file():
            return candidat
    return None


def charger_fabrique(matrice):
    """La FABRIQUE DE FIXTURES partagee, chargee PAR CHEMIN (motif L-029/M-076).

    Le module vit dans `data/commun/` et porte un nom importable, mais deux tools
    de la Matrice portent le meme nom de fichier : on le charge donc par CHEMIN,
    comme le prescrit son propre contrat -- et jamais en le recopiant.
    """
    chemin = matrice.joinpath(*COMMUN_RELATIF[1:]) / NOM_FABRIQUE
    if not chemin.is_file():
        return None
    specification = importlib.util.spec_from_file_location("cobayes_jetables", str(chemin))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def charger_fonctions(chemin):
    """Le module `verifier/fonctions.py` de l outil, charge PAR CHEMIN.

    Il ne s agit pas d importer l outil (aucune execution, aucune ecriture) mais de
    lire la REGLE qui juge la trace (`verifier_coherence`) pour la pieger avec des
    evenements fabriques : un controle de coherence ne se prouve pas sur le seul
    journal reel, qui est -- par chance -- deja propre.
    """
    specification = importlib.util.spec_from_file_location("patron_marbre", str(chemin))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def construire_fixture(dossier, source_commun, source_outil):
    """Monte un MINI WORKSPACE jetable et rend (main.py copie, journal de la fixture).

    Pourquoi un `AGENTS.md` de fixture : `racine.detecter_racine` remonte jusqu au
    dossier qui en porte un -- c est le motif UNIQUE du projet, et il ne se
    contourne pas (L-013). La fixture se declare donc ELLE-MEME racine, exactement
    comme le vrai workspace, et tous les chemins de l outil (journal, empreinte,
    archive) se resOLvent DEDANS : rien de la Matrice n est touche.

    Les `__pycache__` et les points de restauration ne sont pas copies : ils ne
    portent aucune regle, et un cobaye qui traine des residus de la veille mesure
    autre chose que ce qu il croit.
    """
    (dossier / MARQUEUR_FIXTURE).write_text(CONTENU_MARQUEUR, encoding="utf-8", newline="\n")
    base = dossier / "cerveau-projet" / "matrix"
    ignorer = shutil.ignore_patterns("__pycache__", "*.pyc", "*.bak.*")
    shutil.copytree(str(source_commun), str(base / "matrice" / "data" / "commun"), ignore=ignorer)
    shutil.copytree(str(source_outil), str(base / "matrice" / "data" / "outils" / "suivi-optimus"),
                    ignore=ignorer)
    outil = base / "matrice" / "data" / "outils" / "suivi-optimus"
    return outil / "main.py", base / "matrice" / "data" / NOM_JOURNAL


def lancer(main_copie, arguments, racine_fixture):
    """Lance la copie de l outil dans la fixture. Rend (code, sortie complete)."""
    resultat = lancer_enfant([sys.executable, str(main_copie)] + list(arguments),
                              capture_output=True, text=True, cwd=str(racine_fixture))
    return resultat.returncode, (resultat.stdout or "") + (resultat.stderr or "")


def noter(main_copie, racine, mission, action, detail, si_absent=False):
    """Un passage par la PORTE `noter` de la fixture (le seul chemin d ecriture)."""
    arguments = ["noter", "--mission", mission, "--theme", "SUIVI", "--action", action,
                 "--detail", detail]
    if si_absent:
        arguments += ["--si-absent", "oui"]
    return lancer(main_copie, arguments, racine)


def verifier(main_copie, racine):
    """Le verdict de la porte `verifier` de la fixture : (code, sortie)."""
    return lancer(main_copie, ["verifier"], racine)


def bornes(journal):
    """(debuts, fins) REELS du journal de la fixture -- mesure, jamais supposee."""
    if not journal.is_file():
        return 0, 0
    debuts = fins = 0
    for ligne in journal.read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        action = json.loads(ligne).get("action")
        if action == "debut":
            debuts += 1
        elif action == "fin":
            fins += 1
    return debuts, fins


def bornes_de(journal, mission):
    """(debuts, fins) d UNE mission -- un total cumule ne dit pas QUI est double."""
    debuts = fins = 0
    for ligne in journal.read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        evenement = json.loads(ligne)
        if evenement.get("mission") != mission:
            continue
        if evenement.get("action") == "debut":
            debuts += 1
        elif evenement.get("action") == "fin":
            fins += 1
    return debuts, fins


def fin_conservee(journal, mission):
    """Le DETAIL de la fin CONSERVEE pour cette mission, ou None (aucune fin).

    Sert au contre-temoin de la reparation : `archiver --doublons` doit GARDER la
    PREMIERE (la borne du pilote), pas la derniere -- une reparation qui garderait
    la derniere REEcrirait l histoire au lieu de la dedoublonner.
    """
    gardee = None
    for ligne in journal.read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        evenement = json.loads(ligne)
        if evenement.get("mission") == mission and evenement.get("action") == "fin":
            gardee = evenement.get("detail")
    return gardee


def evenements_fabriques(mission, debuts, fins):
    """Des evenements SYNTHETIQUES pour pieger la regle de coherence, sans disque."""
    fabriques = []
    for rang in range(debuts):
        fabriques.append({"date": "2026-09-20 0" + str(rang) + ":00:00", "mission": mission,
                          "theme": "SUIVI", "action": "debut", "detail": "fixture",
                          "fichiers": [], "portes": [], "duree_s": ""})
    for rang in range(fins):
        fabriques.append({"date": "2026-09-20 1" + str(rang) + ":00:00", "mission": mission,
                          "theme": "SUIVI", "action": "fin", "detail": "fixture",
                          "fichiers": [], "portes": [], "duree_s": ""})
    return fabriques


def main():
    analyseur = argparse.ArgumentParser(description="Garde : la borne du marbre sur journal jetable")
    analyseur.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = analyseur.parse_args()

    racine = Path(arguments.racine).resolve()
    matrice = trouver_matrice(racine)
    if matrice is None:
        print("Matrice introuvable sous " + str(racine))
        return 2
    source_commun = matrice.joinpath(*COMMUN_RELATIF[1:])
    source_outil = matrice.joinpath(*OUTIL_RELATIF[1:])
    source_fonctions = source_outil.joinpath(*CHEMIN_FONCTIONS)
    if not (source_commun.is_dir() and source_outil.is_dir() and source_fonctions.is_file()):
        print("REFUS : les briques du marbre sont introuvables (data/commun,"
              " data/outils/suivi-optimus, verifier/fonctions.py)")
        return 2
    fabrique = charger_fabrique(matrice)
    if fabrique is None:
        print("REFUS : la fabrique de fixtures est introuvable (" + NOM_FABRIQUE + ")")
        return 1
    regle = charger_fonctions(source_fonctions)

    print("VERIFIER MARBRE -- une borne, un seul ecrivain : le PILOTE a l injection")

    retraits = []
    with fabrique.fixtures(PREFIXE_FIXTURE, retraits) as dossier:
        main_copie, journal = construire_fixture(dossier, source_commun, source_outil)

        # 1. LE CONTRE-TEMOIN (le defaut est REEL, et il est ACCUSE).
        code_pilote, sortie_pilote = noter(main_copie, dossier, MISSION_DOUBLE, "debut",
                                           DETAIL_PILOTE, si_absent=True)
        code_agent, _ = noter(main_copie, dossier, MISSION_DOUBLE, "debut", DETAIL_AGENT)
        debuts, fins = bornes(journal)
        code_ko, sortie_ko = verifier(main_copie, dossier)
        cobaye("2 debuts (pilote + agent) ACCUSES par verifier",
               code_pilote == 0 and code_agent == 0 and (debuts, fins) == (2, 0)
               and code_ko != 0 and "doublon" in sortie_ko,
               "bornes " + str(debuts) + "/" + str(fins) + ", verifier code " + str(code_ko))

        # 2. LA SIGNATURE EXACTE DU DEFAUT MESURE (MO-202 : 2 debuts / 1 fin).
        noter(main_copie, dossier, MISSION_DOUBLE, "fin", "fin de la mission du cobaye")
        debuts, fins = bornes(journal)
        code_ko, sortie_ko = verifier(main_copie, dossier)
        cobaye("MO-202 reproduit (2 debuts / 1 fin) est un ECART",
               (debuts, fins) == (2, 1) and code_ko != 0 and "doublon" in sortie_ko,
               "bornes " + str(debuts) + "/" + str(fins) + ", verifier code " + str(code_ko))

        # 3. LA REPARATION NOMMEE : le journal repasse a 1/1 et verifier rend VERT.
        code_archive, sortie_archive = lancer(main_copie, ["archiver", "--doublons"], dossier)
        debuts, fins = bornes(journal)
        code_vert, sortie_verte = verifier(main_copie, dossier)
        archive = journal.parent / NOM_ARCHIVE_DOUBLONS
        lines_archive = (len([l for l in archive.read_text(encoding="utf-8").splitlines()
                              if l.strip()]) if archive.is_file() else 0)
        cobaye("archiver --doublons repare (1 debut / 1 fin, verifier VERT)",
               code_archive == 0 and (debuts, fins) == (1, 1) and code_vert == 0
               and lines_archive == 1,
               "bornes " + str(debuts) + "/" + str(fins) + ", verifier code " + str(code_vert)
               + ", archive " + str(lines_archive) + " evenement(s)")

        # 4. L'IDEMPOTENCE DU PILOTE : deux passages, UNE borne.
        noter(main_copie, dossier, MISSION_PILOTE, "debut", DETAIL_PILOTE, si_absent=True)
        _, sortie_si_absent = noter(main_copie, dossier, MISSION_PILOTE, "debut", DETAIL_PILOTE,
                                    si_absent=True)
        debuts, fins = bornes(journal)
        cobaye("le mode --si-absent du pilote ne pose QU UNE borne",
               (debuts, fins) == (2, 1) and "RIEN ecrit" in sortie_si_absent
               and MISSION_PILOTE in sortie_si_absent,
               "bornes " + str(debuts) + "/" + str(fins)
               + " (dont celles du cobaye precedent), second passage : "
               + ("RIEN ecrit" if "RIEN ecrit" in sortie_si_absent else "a ECRIT"))

        # 5. LA REPRISE LEGITIME, dans les DEUX sens (un garde qui accepte tout ne
        #    garde rien : la meme FORME doit passer quand elle est reguliere et
        #    crier quand elle ne l est pas).
        #
        #    CE QUE CE COBAYE JOUAIT, ET CE QU IL PROUVAIT (MO-534). Il exigeait
        #    qu une reprise NON DECLAREE soit accusee -- donc la reconnaissance
        #    d une reprise par une liste figee (`REPRISES_DOUBLON_OK`) rendait le
        #    controle AVEUGLE a toute mission reellement rouverte puis re-close :
        #    la forme reguliere [debut, fin, rouverture, fin] etait un ECART sans
        #    remede, alors que la porte `declarer_borne_marbre` (MO-108) ecrit que
        #    deux sessions sont legitimes. La liste disparait : ce qui distingue
        #    une reprise d un doublon se LIT dans la SEQUENCE des bornes.
        #    On joue donc la REGLE, plus son CONTRE-TEMOIN :
        #      - [debut, fin, debut, fin]  -> deux sessions  : ACCEPTE
        #      - [debut, fin, fin]        -> une session, deux fins : ACCUSE
        # ATTENTION : `evenements_fabriques(2, 2)` n est PAS une reprise -- elle
        # EMPILE les debuts ([debut, debut, fin, fin]), donc c est un doublon,
        # et les deux debuts sont precisement ce que les cobayes 1 et 2
        # doivent voir accuses. Une reprise s INTERLACE : chaque debut est suivi
        # de sa fin AVANT le debut suivant (MO-108 -- deux sessions, pas deux
        # ecrivains de la meme borne). On fabrique donc la forme exacte.
        def session(date_debut, date_fin, mission):
            return [{"date": date_debut, "mission": mission, "theme": "SUIVI",
                     "action": "debut", "detail": "fixture", "fichiers": [],
                     "portes": [], "duree_s": ""},
                    {"date": date_fin, "mission": mission, "theme": "SUIVI",
                     "action": "fin", "detail": "fixture", "fichiers": [],
                     "portes": [], "duree_s": ""}]

        ok_reprise, _, _ = regle.verifier_coherence(
            session("2026-09-20 10:00:00", "2026-09-20 11:00:00", MISSION_DOUBLE)
            + session("2026-09-20 12:00:00", "2026-09-20 13:00:00", MISSION_DOUBLE))
        cobaye("une reprise (2 debuts / 2 fins) est acceptee PAR SA FORME",
               ok_reprise, "deux sessions : chaque fin avait son debut")
        ok_doublon, _, stats_doublon = regle.verifier_coherence(
            evenements_fabriques(MISSION_DOUBLE, 1, 2))
        cobaye("la MEME mission, 2 fins pour 1 debut, est ACCUSEE",
               (not ok_doublon) and len(stats_doublon.get("doublons", [])) == 1,
               "une seule session : " + ("accusee" if not ok_doublon else "ACCEPTEE"))
        # La forme ROUVRURE puis RE-CLOSE : c est celle que MO-534 porte au
        # journal reel, et celle que la liste figee ne pouvait pas laisse passer.
        rouvert = [
            {"date": "2026-09-20 10:00:00", "mission": MISSION_DOUBLE, "theme": "SUIVI",
             "action": "debut", "detail": "fixture", "fichiers": [], "portes": [], "duree_s": ""},
            {"date": "2026-09-20 11:00:00", "mission": MISSION_DOUBLE, "theme": "SUIVI",
             "action": "fin", "detail": "fixture", "fichiers": [], "portes": [], "duree_s": ""},
            {"date": "2026-09-20 12:00:00", "mission": MISSION_DOUBLE, "theme": "SUIVI",
             "action": "rouverture", "detail": "fixture", "fichiers": [], "portes": [],
             "duree_s": ""},
            {"date": "2026-09-20 13:00:00", "mission": MISSION_DOUBLE, "theme": "SUIVI",
             "action": "fin", "detail": "fixture", "fichiers": [], "portes": [], "duree_s": ""},
        ]
        ok_rouvert, _, _ = regle.verifier_coherence(rouvert)
        cobaye("rouverte puis RE-CLOSE (la forme reelle de MO-534) est acceptee",
               ok_rouvert, "la rouverture rend A FAIRE sans terminer")

        # 6. LE GARDE ANTI-FIN-ORPHELINE de la porte est aussi dans le chemin : une
        #    fin declaree SEULE (mission jamais commencee) se fait preceder d un
        #    debut implicite -- le journal n est jamais reecrit, et la trace ne
        #    porte pas de trou. Le chemin de la porte est ainsi eprouve en entier.
        code_fin, sortie_fin = noter(main_copie, dossier, MISSION_ORPHELINE, "fin",
                                     "fin d une mission jamais commencee (cobaye)")
        debuts, fins = bornes(journal)
        code_vert, _ = verifier(main_copie, dossier)
        cobaye("une fin seule fait naitre un debut implicite et laisse verifier VERT",
               code_fin == 0 and (debuts, fins) == (3, 2) and code_vert == 0
               and NOM_MARQUEUR_FIN_ORPHELINE in sortie_fin,
               "bornes " + str(debuts) + "/" + str(fins) + ", verifier code " + str(code_vert)
               + ", debut implicite "
               + ("DIT" if NOM_MARQUEUR_FIN_ORPHELINE in sortie_fin else "MUET"))

        # 7. LE DEFAUT MO-455 REPRODUIT : le TEXTE du round prescrivait a l agent de
        #    poser la FIN, alors que le pilote la declare deja. Le geste de l agent,
        #    joue APRES la cloture, pose une 2e fin -- et `verifier` l ACCUSE.
        noter(main_copie, dossier, MISSION_FIN_DEFAUT, "fin", DETAIL_FIN_PILOTE, si_absent=True)
        noter(main_copie, dossier, MISSION_FIN_DEFAUT, "fin", DETAIL_FIN_AGENT)
        debuts_fin, fins_fin = bornes_de(journal, MISSION_FIN_DEFAUT)
        code_ko, sortie_ko = verifier(main_copie, dossier)
        cobaye("MO-455 reproduit : une 2e fin posee APRES la cloture est ACCUSEE",
               (debuts_fin, fins_fin) == (1, 2) and code_ko != 0 and "doublon" in sortie_ko,
               "bornes de " + MISSION_FIN_DEFAUT + " " + str(debuts_fin) + "/" + str(fins_fin)
               + ", verifier code " + str(code_ko))

        # 8. LE CONTRE-TEMOIN DE LA REPARATION : la porte nommee sort la SECONDE et
        #    GARDE LA PREMIERE -- la borne du pilote.
        code_archive, _ = lancer(main_copie, ["archiver", "--doublons"], dossier)
        debuts_fin, fins_fin = bornes_de(journal, MISSION_FIN_DEFAUT)
        code_vert, _ = verifier(main_copie, dossier)
        conservee = fin_conservee(journal, MISSION_FIN_DEFAUT)
        cobaye("archiver --doublons GARDE la PREMIERE fin (celle du pilote)",
               code_archive == 0 and (debuts_fin, fins_fin) == (1, 1) and code_vert == 0
               and conservee == DETAIL_FIN_PILOTE,
               "bornes " + str(debuts_fin) + "/" + str(fins_fin) + ", fin conservee : "
               + repr(conservee))

        # 9. LE CHEMIN CORRIGE (ce que le TEXTE prescrit maintenant) : la cloture du
        #    pilote SEULE rend 1 debut / 1 fin, et `verifier` est VERT -- le chemin
        #    NORMAL d un round, MESURE au lieu d etre cru.
        noter(main_copie, dossier, MISSION_FIN_PROPRE, "fin", DETAIL_FIN_PILOTE, si_absent=True)
        debuts_propre, fins_propre = bornes_de(journal, MISSION_FIN_PROPRE)
        code_vert, _ = verifier(main_copie, dossier)
        cobaye("la cloture du pilote SEULE rend 1 debut / 1 fin et verifier VERT",
               (debuts_propre, fins_propre) == (1, 1) and code_vert == 0,
               "bornes de " + MISSION_FIN_PROPRE + " " + str(debuts_propre) + "/"
               + str(fins_propre) + ", verifier code " + str(code_vert))

    echecs = [(nom, detail) for nom, reussie, detail in RESULTATS if not reussie]
    echecs += [(nom, "") for nom, reussie in COBAYE if not reussie]
    if retraits:
        print("RETRAIT INCOMPLET de la fixture : " + ", ".join(retraits))
        echecs.append(("retrait de la fixture", ""))

    controler("toutes les epreuves du cobaye sont rejouees",
              len(COBAYE) == 10 and all(reussie for _, reussie in COBAYE),
              str(sum(1 for _, reussie in COBAYE if reussie)) + "/" + str(len(COBAYE)))

    print("")
    if echecs:
        print("VERDICT KO : la borne du marbre n est pas tenue (voir les ecarts nommes).")
        return 1
    print("VERDICT OK : le pilote est la SEULE maison du debut, un doublon est ACCUSE,"
          " REPARE par une porte nommee, et la reprise reste possible.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
