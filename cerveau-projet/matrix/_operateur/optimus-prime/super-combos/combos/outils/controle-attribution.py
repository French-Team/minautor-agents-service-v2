#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
controle-attribution.py -- DESCENDRE ORDRE 3.2 (M-153, MO-357)

LA QUESTION A LAQUELLE RIEN NE REPONDAIT : une source a CHANGE -- par quelle PORTE ?

L'empreinte d'integrite dit QU'il y a eu ecriture ; elle ne dit pas QUI l'a faite.
Un outil natif, un script de passage ou une commande du shell laissent la MEME
trace qu'une porte : un fichier modifie. Le seul temoin d'une ecriture PAR LA
PORTE est la NOTE laissee au domicile des modifications (bdd-modifications), et
cette note porte une DATE.

LE CONTROLE, EN DEUX PIECES :
  (a) UN DOMICILE DE REFERENCE -- les empreintes sha256 des sources, posees avec
      leur DATE de pose (`poser`), comme l'espion d'integrite de la zone ;
  (b) UN CONTROLE PERMANENT (`verifier`) -- pour chaque source dont l'empreinte a
      change depuis la pose, il faut une NOTE TRACEE posterieure a la pose QUI PORTE
      l'empreinte DU CONTENU MESURE. Sans note : ECRITURE HORS DE SA PORTE, accusee
      nommement (fichier + empreinte attendue + empreinte mesuree). Code 1.

LA NOTE DOIT PROUVER, PAS SEULEMENT DATER (friction du 2026-09-23) : une note
n'etait lue que par sa DATE, alors qu'une note est ecrite pour UNE ecriture. Une
note PERIMEE -- posee pour un autre contenu -- blanchissait donc n'importe quel
changement posterieur ; et ce controle, qui IMPRIMAIT les deux empreintes sans
jamais les comparer, ne pouvait pas le voir. Depuis, la note porte l'empreinte du
contenu qu'elle atteste (champ consomme chez la porte `noter`) : le verdict est la
COMPARAISON, la date n'en est que la seconde condition. Les notes anterieures a
cette mesure ne peuvent plus attester : elles sont COMPTEES et DITES, a la pose
comme a la verification (L-286) -- jamais decouvertes au premier refus.

CE QUE LE CONTROLE NE JUGE PAS (declare, jamais muet) : les formes d'ETAT --
journaux append-only, empreintes temoins, marqueurs de processus, etats des
routines -- les PRODUCTIONS qu'une routine DECLARE siennes (`PRODUCTIONS` dans ses
propres constantes : un rapport, un inventaire, la memoire d'une passe -- sa porte
est la routine, ce n'est pas une source) -- les DRAPEAUX D'ARRET, dont le nom REEL
est declare par la table unique du serveur (un drapeau ne vit que le temps d'un
arret : le juger accuserait une porte pour un geste qu'elle a elle-meme demande) --
les TEMPORAIRES d'ecriture atomique (forme declaree par le domicile `ecrire`) -- et
les zones jetables ou d'archive : elles sont ecrites par LEURS PROPRES portes.
Chaque exclusion a son motif et son COMPTE, imprimes a chaque passe : une exclusion
muette serait un angle mort (L-104).

AUDIT DES ECRITURES DE ROUTINE (2026-09-23) : les NEUF routines de la Matrice ont
ete recensees, ecriture par ecriture, contre ces exclusions. Resultat mesure : trois
familles etaient JUGEES faute d'etre declarees -- l'etat anti-spam de veille-flux
(nom anterieur a la convention des etats, desormais DECLARE par sa routine), les
HUIT marqueurs d'arret (desormais consommes depuis la table unique du serveur) et
les temporaires d'ecriture atomique (forme consommee chez `ecrire`). Chaque famille
a son cobaye : la revue est un fait mesure, pas une promesse.

LA PORTEE SE MESURE AVANT DE REFUSER (L-286) : a la pose, tout est pardonne (la
reference est le PRESENT) et la dette est DITE ; a la verification, seuls les
changements POSTERIEURS a la pose sont juges.

Usage:
  python controle-attribution.py poser        (pose la reference + la date)
  python controle-attribution.py verifier     (code 0 = chaque changement est attribue)
  python controle-attribution.py --auto-test  (les cobayes, sur des faits fabriques)
"""

import sys
import re
import json
import hashlib
import argparse
import importlib.util
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parent
MATRICE = next(p for p in [BASE, *BASE.parents] if p.name == "matrix")
COMMUN = MATRICE / "matrice" / "data" / "commun"
if str(COMMUN) not in sys.path:
    sys.path.insert(0, str(COMMUN))

from cible import forme_canonique, racine_matrice_stricte  # noqa: E402
from passerelle_user import est_passerelle_user, MOTIF_PASSERELLE_USER  # noqa: E402
from zone_sources import est_zone_sources, MOTIF_ZONE_SOURCES  # noqa: E402
from zone_runtime import est_zone_runtime, MOTIF_ZONE_RUNTIME  # noqa: E402

# Le registre de reference vit A COTE de son outil (un etat, pas une source).
REGISTRE = BASE / "attribution-registre.json"
# Le domicile des NOTES : la porte qui ecrit et note les modifications.
DOMICILE_MODIFICATIONS = MATRICE / "matrice" / "data" / "outils" / "bdd-modifications"
# Le domicile de la FORME du point de restauration (consomme, jamais recopie).
DOMICILE_FORME_BAK = MATRICE / "matrice" / "data" / "outils" / "ecrire" / "constants.py"
# Le domicile de la ZONE JETABLE du voisin (consomme, jamais recopie).
DOMICILE_ZONE_TMP = COMMUN / "zone_tmp.py"
# Le domicile de l'ARCHIVE de rotation (consomme, jamais recopie).
DOMICILE_ARCHIVES = MATRICE / "matrice" / "data" / "outils" / "bdd-conservation" / "constants.py"
# Le domicile des VUES RECALCULEES : une vue se REECRIT a chaque passe par sa
# propre porte -- ce n'est pas une source, c'est un affichage (L-162). Mesure du
# 2026-09-22 : la vue du suivi du pilote a ete accusee des sa premiere pose.
DOMICILE_VUE_SUIVI = BASE / "suivi-pilote.py"
# Les AUTRES vues declarees par leur porte (meme regle, domiciles differents).
DOMICILES_VUES = (MATRICE / "matrice" / "data" / "outils" / "suivi-optimus" / "constants.py",
                    # MO-576 : la porte des CINQ PARTIES MAITRESSES. Elle n etait pas
                    # declaree, alors qu elle ecrit plus de vues que les trois autres
                    # reunies : le controle ne lisait qu UNE vue par porte
                    # (`CHEMIN_VUE` ou `NOM_VUE`), donc quatre de ses vues restaient
                    # accusees comme des sources a chaque rafraichissement.
                    BASE / "suivi-parties-maitresses.py")
# LA VUE DU SUIVI DU CAMELEON (MO-534). Elle est listee A PART parce qu elle ne
# vit pas dans la zone de l operateur comme les autres : la porte `suivi-cameleon`
# la publie dans `matrice/data/`, ou le createur l ouvre avec les autres vues. Le
# chemin est lai chez SA PORTE (`CHEMIN_VUE`) : ici on ne fait que le LIRE, sinon
# une vue deplacee serait exclue par un nom devenu faux.
DOMICILE_VUE_SUIVI_CAMELEON = (MATRICE / "_operateur" / "optimus-prime"
                               / "super-combos" / "combos" / "outils" / "suivi-cameleon.py")
# Le domicile du PILOTE : il DECLARE ses propres etats (file, entonnoir, themes,
# etat de pause) -- ces fichiers sont ecrits par SA porte a chaque round, ils ne
# sont pas des sources. Mesure du 2026-09-22 : six d'entre eux ont ete accuses en
# une seule passe (file, entonnoir, archive, marbre, activites, conservation).
DOMICILE_PILOTE = MATRICE / "_operateur" / "optimus-prime" / "pilote" / "constants.py"

# LE DOMICILE DES ROUTINES DE LA MATRICE : chacune DECLARE ses PRODUCTIONS dans ses
# propres constantes (`PRODUCTIONS = (CHEMIN_...,)`). Une PRODUCTION est un fichier
# que la routine ECRIT a chaque passe et qui n'est PAS un etat court : un rapport,
# un inventaire, une vue. Ce n'est donc pas une source -- personne ne l'ecrit a la
# main, sa porte est la routine.
# Mesure du 2026-09-23 : sans cette declaration, `rapport-liens.json` (reecrit a
# chaque passe) etait accuse comme une source -- et l'accusation serait revenue a
# CHAQUE passe, sans fin. Le domicile est CONSOMME (M-076) : le jour ou une routine
# declare une production, le controle la connait sans liste a retoucher.
DOMICILE_ROUTINES = MATRICE / "matrice" / "routines"
# LA ZONE DE L OPERATEUR declare ses productions AU MEME TITRE (MO-534). Mesure :
# le scan ne regardait que `matrice/routines/`, donc une porte hors Matrice ne
# pouvait meme pas se declarer -- sa production etait accusee comme une ecriture
# non attribuee, sans remede possible cote outil. Le titre est celui des
# routines, la DECLARATION est dans le fichier de l outil lui-meme (une porte a
# un seul script et pas de `constants.py`) : c est la meme convention, lue la ou
# elle vit.
DOMICILE_OUTILS_OPERATEUR = MATRICE / "_operateur" / "optimus-prime" / "remorque"
NOM_DECLARATION_PRODUCTIONS = "PRODUCTIONS"
# LE MEME TITRE POUR LES VUES D UNE PORTE A UN SEUL SCRIPT (MO-576). Une vue se
# RECALCULE a chaque passe : elle ne peut pas porter une note attestant son contenu
# AVANT l ecriture, donc une vue ne s atteste pas elle-meme. Une porte qui en pose
# plusieurs les DECLARE, et le controle les lit -- il ne les devine pas.
NOM_DECLARATION_VUES_PRODUITES = "VUES_PRODUITES"
# LE NOM DU CHAMP D'EMPREINTE D'UNE NOTE vit chez la porte qui l'ECRIT
# (bdd-modifications, friction du 2026-09-23) : ici on le CONSOMME. Un nom recopie
# divergerait en silence -- et un controle qui lit un champ que personne n'ecrit
# accuserait tout le corpus sans jamais dire pourquoi.
DOMICILE_CONSTANTES_NOTES = (MATRICE / "matrice" / "data" / "outils"
                             / "bdd-modifications" / "constants.py")
NOM_CHAMP_EMPREINTE = "CHAMP_EMPREINTE"

# LE DOMICILE DES DRAPEAUX D'ARRET : la table UNIQUE du serveur dit, pour chaque
# routine supervisee, le NOM REEL de son drapeau (`DRAPEAU_PAR_NOM`), et le sien
# (`NOM_DRAPEAU_SERVER`). Un drapeau ne vit que le temps d'un arret -- sa boucle le
# voit (2 s) et l'OTE -- mais celui qu'une routine ARRETEE n'a jamais vu reste sur
# le disque : le juger accuserait une porte pour le geste qu'elle a demande, et
# l'accusation reviendrait A CHAQUE PASSE. L'anomalie d'un drapeau oublie a son
# propre juge (le garde `pause-oubliee` du suivi du pilote) : ici on ne juge pas la
# porte, on juge la SOURCE. Les noms sont CONSOMMES, jamais recopies (M-076) : le
# jour ou une routine arrive, sa ligne dans la table suffit.
DOMICILE_TABLE_DRAPEAUX = MATRICE / "matrice" / "routines" / "vie" / "constants.py"
NOM_TABLE_DRAPEAUX = "DRAPEAU_PAR_NOM"
NOM_DRAPEAU_SERVEUR = "NOM_DRAPEAU_SERVER"
DOSSIER_ROUTINES = MATRICE / "matrice" / "routines"
DOSSIER_SERVEUR = DOSSIER_ROUTINES / "vie" / "server"

DOSSIERS_EXCLUS = {"__pycache__", ".git"}
# LA PASSERELLE USER (decision du createur, 2026-09-26 ; domicile MO-492) : le
# dossier `user-demandes/` porte le fichier que l'USER ecrit LUI-MEME, en continu,
# hors de toute porte de la Matrice, et dans SA langue. Ce n'est pas une SOURCE
# (aucune porte ne le produit ni ne le repare) : le juger accusait une ecriture
# LEGITIME a CHAQUE passe et faisait rougir la non-regression en permanence (mesure
# du 2026-09-26 : le fichier est reecrit toutes les quelques secondes pendant la
# session). La declaration a UN DOMICILE (`matrice/data/commun/passerelle_user.py`)
# et se CONSOMME ici (M-076) : la recopier ferait diverger en silence les
# instruments de la maison -- ce qui s'etait produit (mesure MO-492 du 2026-09-29 :
# `garde-ascii` ignorait la decision et accusait la MEME zone). Elle reste COMPTE
# par `perimetre()` : une exclusion muette serait un angle mort (L-104).
# FORMES D'ETAT : ecrites par leurs propres portes, jamais par la porte ecrire.
#   - `.jsonl` : journaux en ajout seul (rotation partagee, boites du pilote) ;
#   - `.sha256` : empreintes temoins des BDD (la porte de la BDD les repose) ;
#   - `.pid` : marqueurs de processus des espions.
FORMES_ETAT = (".jsonl", ".sha256", ".pid")
# REGISTRES D'UN CONTROLE : un fichier de reference POSE par sa propre porte (le
# registre du garde des versions, la reference d'un controle). Il change A CHAQUE
# POSE et ne peut pas etre note par lui-meme : le motif est une FORME, DITE avec
# son compte, jamais un silence (mesure du 2026-09-22 : le premier garde de ce
# genre a ete accuse par lui-meme des sa deuxieme pose).
FORME_REGISTRE = "-registre.json"
# ETATS DES ROUTINES : un etat qui se reecrit a chaque passe (mesure du
# 2026-09-22 : `routeur-etat.json`, `vigie-portes-etat-passes.json`... portent
# une note ANCIENNE et changent a chaque tour -- les accuser serait accuser une
# porte LEGITIME, celle de la routine qui les possede).
# Mesure du 2026-09-22 (faux positif attrape en direct) : le premier motif
# `-etat(-passes)?\.json` n'attrapait PAS `espion-etat-bdds.json` -- l'etat du
# tableau des BDD de l'espion. Le controle a donc accuse une source SAINE des la
# premiere passe : c'est exactement ce que L-286 demande de mesurer AVANT de
# refuser. Un etat de routine se nomme `<routine>-etat[-<qualificatif>]*.json` :
# le motif le dit en ENTIER, et le cobaye des exclusions mord dessus.
# DEUXIEME TROU, MEME FAMILLE (mesure du 2026-09-23) : la CADENCE qu'une routine
# PUBLIE a son demarrage s'ecrit `<routine>-cadence.json` et n'etait couverte par
# AUCUNE branche -- redemarrer la Matrice (le geste de reprise normal) faisait donc
# accuser QUATRE etats de routine legitimes. Un etat publie par sa propre porte se
# nomme `<routine>-etat|-log|-cadence[-<qualificatif>]*.json`.
MOTIF_ETAT = re.compile(r"(-etat|-log|-cadence)(-[a-z0-9]+)*\.json$")


def charger_module(chemin, nom, dossier_local=False):
    """Importe un module par son CHEMIN, sans dependre du repertoire courant.

    `dossier_local` : certains domiciles importent leurs VOISINS par leur nom
    (`vie/constants.py` : `from constants_suivi_sync import ...`). Python ne pose
    PAS le dossier d'un module charge par chemin sur `sys.path` : sans ce drapeau,
    la table des drapeaux serait un SILENCE -- `charger_module` rend None et le
    controle ne saurait meme pas qu'il ne l'a pas lue. Le dossier est pose le temps
    de l'execution puis OTE : un nom aussi generique que `constants` ne doit pas
    rester atteignable par les chargements suivants.
    """
    if not chemin.is_file():
        return None
    dossier = str(Path(chemin).resolve().parent) if dossier_local else None
    if dossier is not None:
        sys.path.insert(0, dossier)
    try:
        spec = importlib.util.spec_from_file_location(nom, str(chemin))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except (ImportError, OSError, SyntaxError, AttributeError):
        return None
    finally:
        if dossier is not None and dossier in sys.path:
            sys.path.remove(dossier)


def domiciles():
    """Le domicile des notes, la forme du point de restauration, la zone jetable.

    AUCUNE de ces valeurs n'est recopiee (M-076) : chacune est CONSOMMEE chez la
    porte qui la produit. Un domicile illisible est rendu None : le controle le
    DIT et continue -- il ne devine jamais.
    """
    porte = charger_module(DOMICILE_MODIFICATIONS / "constants.py", "domicile_modifications")
    ecrire = charger_module(DOMICILE_FORME_BAK, "domicile_forme_bak")
    zone = charger_module(DOMICILE_ZONE_TMP, "domicile_zone_tmp")
    archives = charger_module(DOMICILE_ARCHIVES, "domicile_archives")
    motif_bak = None
    if ecrire is not None and getattr(ecrire, "MOTIF_BAK_HORODATE", None):
        try:
            motif_bak = re.compile(ecrire.MOTIF_BAK_HORODATE)
        except re.error:
            motif_bak = None
    zone_optimus = ""
    if zone is not None:
        morceaux = getattr(zone, "DOMICILE_ZONE_OPTIMUS", None)
        if morceaux:
            zone_optimus = "/".join(str(morceau) for morceau in morceaux)
    vues = []
    vue = charger_module(DOMICILE_VUE_SUIVI, "domicile_vue_suivi")
    if vue is not None:
        dossier = getattr(vue, "DOSSIER_SUIVI", None)
        nom = getattr(vue, "NOM_VUE", None)
        if dossier and nom:
            vues.append((str(dossier).replace(chr(92), "/") + "/" + str(nom),
                         "vue recalculee par sa propre porte (domicile suivi-pilote)"))
    for chemin_module in DOMICILES_VUES + (DOMICILE_VUE_SUIVI_CAMELEON,):
        module_vue = charger_module(chemin_module, "domicile_vue")
        if module_vue is None:
            continue
        # MESURE MO-534 : la vue se DIT la ou elle est, pas la ou on suppose
        # qu elle est. Ce bloc recomposait le chemin depuis le seul NOM_VUE, ce
        # qui est vrai pour la vue du suivi d Optimus (elle vit a cote de son
        # outil, dans `_operateur/`) et FAUX pour celle du cameleon (publiee
        # dans `matrice/data/`) : le chemin recompose ne designait aucun fichier,
        # donc la vue reelle etait accusee comme une source neuve. On lit
        # `CHEMIN_VUE` quand la porte l expose, et on ne TOMBE sur le nom que si
        # elle ne l expose pas.
        relatif = None
        chemin_vue = getattr(module_vue, "CHEMIN_VUE", None)
        if chemin_vue is not None:
            try:
                relatif = forme_canonique(chemin_vue, BASE)
            except (ValueError, OSError, TypeError):
                relatif = None
        # MO-576 : une porte qui pose PLUSIEURS vues les declare. La liste est lue
        # la ou elle est ecrite -- aucun nom de vue n est recopie ici (M-076).
        produites = getattr(module_vue, NOM_DECLARATION_VUES_PRODUITES, None) or ()
        if produites:
            for chemin_produit in produites:
                try:
                    produit = forme_canonique(chemin_produit, BASE)
                except (ValueError, OSError, TypeError):
                    continue
                if produit:
                    vues.append((produit, "vue recalculee par sa propre porte ("
                                 + chemin_module.stem + ")"))
            continue
        if not relatif:
            nom = getattr(module_vue, "NOM_VUE", None)
            if not nom:
                continue
            # Repli : le dossier de l OPERATEUR, convention historique.
            relatif = "_operateur/optimus-prime/" + str(nom)
        vues.append((relatif, "vue recalculee par sa propre porte (domicile suivi-optimus)"))
    # LES ETATS DU PILOTE : il les DECLARE lui-meme (CHEMIN_* et NOM_* joints a
    # ses dossiers). Consommer sa declaration vaut mieux que recopier six noms :
    # le jour ou il en ajoute un, le controle le suit.
    pilote = charger_module(DOMICILE_PILOTE, "domicile_pilote")
    etats_pilote = []
    if pilote is not None:
        dossier_pilote = getattr(pilote, "REPERTOIRE_PILOTE", None)
        for attribut in dir(pilote):
            if not attribut.startswith("CHEMIN_"):
                continue
            valeur = getattr(pilote, attribut, None)
            if isinstance(valeur, Path) and valeur.is_file():
                try:
                    etats_pilote.append(valeur.resolve().relative_to(Path(MATRICE).resolve()).as_posix())
                except ValueError:
                    continue
        for attribut in dir(pilote):
            if not attribut.startswith("NOM_") or not dossier_pilote:
                continue
            nom = getattr(pilote, attribut, None)
            if not isinstance(nom, str) or "." not in nom:
                continue
            candidat = Path(dossier_pilote) / nom
            if candidat.is_file():
                try:
                    etats_pilote.append(candidat.resolve().relative_to(Path(MATRICE).resolve()).as_posix())
                except ValueError:
                    continue
    # LES PRODUCTIONS DECLAREES PAR LES ROUTINES : chacune dit ce qu'elle ecrit.
    # Aucun nom n'est recopie ici -- on LIT la declaration (M-076). Une routine dont
    # les constantes ne sont pas importables est simplement absente de la liste : le
    # controle ne devine pas ses productions, et le compte des exclusions le dira.
    productions = []
    # LES PRODUCTIONS DES OUTILS DE L OPERATEUR : meme titre `PRODUCTIONS`, lu
    # dans le script de l outil (une porte a un seul fichier, pas de module de
    # constantes). Le nom du fichier porte le nom de l outil : le controle
    # n invente rien, il lit la declaration la ou elle est ecrite.
    for script in sorted(DOMICILE_OUTILS_OPERATEUR.glob("*.py")):
        module_outil = charger_module(script, "productions_" + script.stem.replace("-", "_"),
                                      dossier_local=True)
        if module_outil is None:
            continue
        for production in (getattr(module_outil, NOM_DECLARATION_PRODUCTIONS, None) or ()):
            try:
                relatif_production = Path(production).resolve().relative_to(
                    Path(MATRICE).resolve()).as_posix()
            except (ValueError, OSError, TypeError):
                continue
            productions.append((relatif_production, script.stem))
    # LES ROUTINES DONT AUCUNE DECLARATION N'EST LISIBLE : celles qui n'ont pas de
    # constantes, et celles dont les constantes importent leurs VOISINS par leur nom
    # -- ce que `charger_module` ne permet pas sans `dossier_local` (mesure du
    # 2026-09-23 : `vie/constants.py` etait la SEULE muette des neuf). Le controle ne
    # devine PAS leurs productions, mais il ne le TAIT plus : la liste est rendue et
    # DITE, donc une routine neuve qui oublie sa case est VUE (L-104).
    declarations_muettes = []
    if DOMICILE_ROUTINES.is_dir():
        for dossier in sorted(DOMICILE_ROUTINES.iterdir()):
            if not dossier.is_dir():
                continue
            module_routine = charger_module(
                dossier / "constants.py", "productions_" + dossier.name.replace("-", "_"),
                dossier_local=True)
            if module_routine is None:
                declarations_muettes.append(dossier.name)
                continue
            for production in (getattr(module_routine, NOM_DECLARATION_PRODUCTIONS, None) or ()):
                try:
                    relatif_production = Path(production).resolve().relative_to(
                        Path(MATRICE).resolve()).as_posix()
                except (ValueError, OSError, TypeError):
                    continue
                productions.append((relatif_production, dossier.name))
    # LES DRAPEAUX D'ARRET : une SEULE table les declare (celle du serveur de vie),
    # et elle nomme le fichier REEL de chacune -- y compris les deux qui echappent
    # a la convention (l'espion garde `boucle-arret.txt`, le routeur un `.flag`) :
    # la table le DIT, le controle ne le devine pas. Son dossier est pose le temps
    # du chargement : ce domicile importe ses voisins par leur nom.
    drapeaux = []
    table_drapeaux = charger_module(DOMICILE_TABLE_DRAPEAUX, "domicile_table_drapeaux",
                                    dossier_local=True)
    if table_drapeaux is not None:
        for nom_routine, fichier in (getattr(table_drapeaux, NOM_TABLE_DRAPEAUX,
                                             None) or {}).items():
            candidat = DOSSIER_ROUTINES / str(nom_routine) / str(fichier)
            relatif = forme_canonique(candidat, BASE)
            if relatif and not relatif.startswith(".."):
                drapeaux.append((relatif, "drapeau d'arret (nom declare par la table"
                                          " unique du serveur)"))
        nom_serveur = getattr(table_drapeaux, NOM_DRAPEAU_SERVEUR, None)
        if nom_serveur:
            relatif_serveur = forme_canonique(DOSSIER_SERVEUR / str(nom_serveur), BASE)
            if relatif_serveur and not relatif_serveur.startswith(".."):
                drapeaux.append((relatif_serveur, "drapeau d'arret du serveur (declare"
                                                   " par son propre domicile)"))
    # LE NOM DU CHAMP D'EMPREINTE : consomme chez la porte qui l'ecrit (M-076).
    constantes_notes = charger_module(DOMICILE_CONSTANTES_NOTES, "domicile_champ_empreinte")
    champ_empreinte = str(getattr(constantes_notes, NOM_CHAMP_EMPREINTE, "") or "")
    return {
        "bdd": Path(getattr(porte, "CHEMIN_BDD", "")) if porte is not None else None,
        "motif_bak": motif_bak,
        "zone_cameleon": getattr(zone, "est_dans_zone_cameleon", None) if zone is not None else None,
        "zone_optimus": zone_optimus,
        "vues": tuple(vues),
        "etats_pilote": tuple(sorted(set(etats_pilote))),
        "productions": tuple(sorted(set(productions))),
        "declarations_muettes": tuple(declarations_muettes),
        "drapeaux": tuple(sorted(set(drapeaux))),
        # LA FORME DU TEMPORAIRE D'ECRITURE ATOMIQUE : consommee chez le MEME
        # domicile que la forme du point de restauration (`ecrire`), jamais recopiee.
        "suffixe_tmp": str(getattr(ecrire, "SUFFIXE_TMP", "") or "") if ecrire is not None else "",
        "champ_empreinte": champ_empreinte,
        "archives": (str(getattr(archives, "REPERTOIRE_ARCHIVES", "")) if archives is not None else ""),
    }


def empreinte(chemin):
    """sha256 d'un fichier, ou None s'il est illisible (jamais devine)."""
    try:
        digest = hashlib.sha256()
        with open(chemin, "rb") as fichier:
            for bloc in iter(lambda: fichier.read(65536), b""):
                digest.update(bloc)
        return digest.hexdigest()
    except OSError:
        return None


def motif_exclusion(relatif, maison):
    """(motif d'exclusion, ou "") pour un chemin RELATIF a la Matrice.

    L'ordre des regles suit la lecture : dossier technique, point de
    restauration, forme d'etat, etat de routine, zone jetable, archive.
    """
    morceaux = relatif.split("/")
    for morceau in morceaux:
        if morceau in DOSSIERS_EXCLUS:
            return "dossier technique (" + morceau + ")"
    # LA PASSERELLE USER : ecrite par le user lui-meme, hors de toute porte. Le
    # jugement se CONSOMME a son domicile -- le PREDICAT et le MOTIF (M-076) : c'est
    # ce qui fait dire la MEME chose a ce controle et au garde ascii. Elle reste
    # COMPTE par `perimetre()`, jamais filtree en silence (L-104).
    if est_passerelle_user(relatif):
        return MOTIF_PASSERELLE_USER
    # LA ZONE DES SOURCES DU CREATEUR (MO-543, decision createur 2026-10-02) :
    # `docs/` porte la VISION, les transcriptions et les notes du createur. La
    # Matrice n y ecrit JAMAIS (la porte `ecrire` y REFUSE deja, code 2), donc
    # AUCUNE ecriture de cette zone ne peut porter de note qui l atteste : la
    # juger accusait une porte a chaque passe, pour un fichier que personne
    # n ecrit par une porte. Meme grammaire que la passerelle user -- le
    # PREDICAT et le MOTIF sont CONSOMMES a leur domicile (M-076), jamais
    # recopies ici, et la zone reste COMPTEE par `perimetre()` (L-104).
    if est_zone_sources(relatif):
        return MOTIF_ZONE_SOURCES
    # LE RUNTIME PYTHON EMBARQUE (2026-10-04, decision createur) : c est un
    # ARTEFACT PRODUIT par une porte -- `runtime/installer.py` le telecharge,
    # verifie son empreinte, l extrait et le PROUVE par l usage. Ce n est donc
    # ni une source, ni un fichier pose a la main, ni un artefact d un outil
    # etranger : le juger accusation 37 fichiers a chaque passe (un garde qu on
    # apprend a ignorer, R-008). Meme grammaire que les zones voisines -- le
    # PREDICAT et le MOTIF sont CONSOMMES a leur domicile (M-076), et la zone
    # reste COMPTE par `perimetre()`, jamais filtree en silence (L-104).
    if est_zone_runtime(relatif):
        return MOTIF_ZONE_RUNTIME
    # UN ETAT DE CONTROLE est un fichier de reference qui se repose a chaque
    # passe (l'espion d'integrite pose son registre, EO-191). Il n'est pas une
    # SOURCE : il DECRIT les sources. Le dossier `registre/` est la convention
    # deja utilisee par l'espion, et elle est DITE avec son compte.
    if "registre" in morceaux[:-1]:
        return "etat d'un controle (dossier registre)"
    nom = morceaux[-1]
    if maison["motif_bak"] is not None and maison["motif_bak"].search(nom):
        return "point de restauration (forme du domicile ecrire)"
    for forme in FORMES_ETAT:
        if nom.endswith(forme):
            return "forme d'etat (" + forme + " : ecrite par sa propre porte)"
    # LE TEMPORAIRE D'ECRITURE ATOMIQUE : toute porte qui ecrit un etat le pose
    # d'abord A COTE (`.tmp`) puis REMPLACE -- la forme est DECLAREE par le domicile
    # `ecrire` (SUFFIXE_TMP) et CONSOMMEE ici, comme sa forme de point de
    # restauration. Il ne vit que le temps d'un remplacement : le juger reviendrait
    # a accuser une porte pour les microsecondes ou elle est nue (mesure du
    # 2026-09-23 : aucun `.tmp` sur le disque, seulement cette fenetre).
    suffixe_tmp = maison.get("suffixe_tmp", "")
    if suffixe_tmp and nom.endswith(suffixe_tmp):
        return "temporaire d'ecriture atomique (forme declaree par le domicile ecrire)"
    if MOTIF_ETAT.search(nom):
        return "etat de routine (reecrit a chaque passe)"
    if nom.endswith(FORME_REGISTRE):
        return "registre d'un controle (reference posee par sa propre porte)"
    # LES JOURNAUX DE ROUTINE : la rotation partagee les BORNE (moteur
    # data/commun/rotation_journal.py), et ils portent tous le prefixe `journal-`
    # -- mesure du 2026-09-22 : `veille-flux/journal-veille.txt` a ete accuse en
    # changeant de FORME (.txt la ou j'attendais .jsonl). Le prefixe est la forme
    # declaree, et il est DIT avec son compte.
    if nom.startswith("journal-"):
        return "journal d'une routine (borne par la rotation partagee)"
    zone = maison["zone_cameleon"]
    if zone is not None:
        try:
            if zone(BASE / relatif):
                return "zone jetable du voisin (domicile zone_tmp)"
        except (OSError, ValueError, TypeError):
            pass
    # LA ZONE JETABLE D'OPTIMUS est PURGEE a chaque cloture (EO-357) : elle ne
    # porte aucun source, et son contenu change a chaque round -- la juger ferait
    # crier le controle a chaque passe. Le domicile est CONSOMME (zone_tmp).
    if maison["zone_optimus"] and (relatif == maison["zone_optimus"]
                                   or relatif.startswith(maison["zone_optimus"] + "/")):
        return "zone jetable d'Optimus (purgee a chaque cloture)"
    archives = maison["archives"]
    if archives and relatif.startswith(archives.strip("/") + "/"):
        return "archive de rotation (domicile bdd-conservation)"
    # UNE PRODUCTION DECLAREE PAR SA ROUTINE : elle se REEcrit a chaque passe, sa
    # porte est la routine qui la declare -- la juger ferait crier le controle a
    # chaque passe (mesure du 2026-09-23). Le motif NOMME la routine : une exclusion
    # doit dire QUI l'autorise, jamais seulement qu'elle existe.
    for production, routine in maison.get("productions", ()):
        if relatif == production:
            return "production declaree par sa routine (" + routine + ")"
    # UN DRAPEAU D'ARRET : son nom REEL est declare par la table unique du serveur.
    # Huit familles de noms et TROIS extensions (`.arret`, `-arret.txt`, `-arret.flag`)
    # -- une FORME de nom n'aurait rien dit de vrai ; une table le dit.
    for drapeau, motif in maison.get("drapeaux", ()):
        if relatif == drapeau:
            return motif
    for vue, motif in maison.get("vues", ()):
        if relatif == vue:
            return motif
    if relatif in maison.get("etats_pilote", ()):
        return "etat du pilote (declare par son propre domicile)"
    # LES ARCHIVES DU PILOTE : la sortie d'une file (elle-meme ecrite par sa
    # porte). La forme `-archive` est celle que le domicile du pilote declare.
    if "-archive" in nom:
        return "archive d'une file (sortie de son propre domicile)"
    return ""


def perimetre():
    """[(cle canonique, chemin absolu)] des SOURCES, + le releve des exclusions.

    Le perimetre est la MATRICE, moins ce qui est declare hors du jugement. Un
    changement dans un dossier non declare ne peut pas etre attribue : il est donc
    COMPTE et DIT, jamais filtre en silence.
    """
    racine = racine_matrice_stricte(BASE)
    maison = domiciles()
    if racine is None:
        return [], {}, maison
    sources = []
    exclus = {}
    for chemin in Path(racine).rglob("*"):
        if not chemin.is_file():
            continue
        # LE REGISTRE DU CONTROLE EST HORS DE SON PROPRE JUGEMENT : il change A
        # CHAQUE POSE (c'est sa fonction), donc l'inclure ferait accuser le
        # controle par lui-meme a chaque passe. Meme regle que l'archive exclue
        # nommement par le balayage : un consommateur qui doit s'exclure l'exclut
        # EN LE DISANT. Il est COMPTE (jamais filtre en silence).
        if chemin.resolve() == REGISTRE.resolve():
            motif = "registre du controle (ecrit par sa propre pose)"
            exclus[motif] = exclus.get(motif, 0) + 1
            continue
        # LE DOMICILE DES NOTES EST HORS DE SON PROPRE JUGEMENT : c'est la porte
        # `noter` qui l'ecrit, et une note NE PEUT PAS se noter elle-meme (le
        # fichier changerait en s'ecrivant -- mesure du 2026-09-22 : accuse des la
        # premiere note posee). Il est COMPTE et DIT, jamais filtre en silence.
        if maison["bdd"] and chemin.resolve() == Path(maison["bdd"]).resolve():
            motif = "domicile des notes (ecrit par sa propre porte)"
            exclus[motif] = exclus.get(motif, 0) + 1
            continue
        # UNE BDD DE LA MATRICE : son EMPREINTE ETALON est posee A COTE d'elle
        # (convention declaree par les portes de BDD : `nom + .sha256`). Le
        # critere est DERIVE du disque, jamais d'une liste : le jour ou une BDD
        # nait, son etalon nait avec elle et le controle la connait.
        if chemin.with_name(chemin.name + ".sha256").is_file():
            motif = "BDD de la Matrice (empreinte etalon posee a cote)"
            exclus[motif] = exclus.get(motif, 0) + 1
            continue
        relatif = forme_canonique(chemin, BASE)
        if not relatif or relatif.startswith(".."):
            continue
        motif = motif_exclusion(relatif, maison)
        if motif:
            exclus[motif] = exclus.get(motif, 0) + 1
            continue
        sources.append((relatif, chemin))
    return sorted(sources), exclus, maison


def notes_du_domicile(maison):
    """{cle canonique: [(date, empreinte)]} lu au DOMICILE des modifications.

    Le controle ne note rien lui-meme : il lit ce que la porte a laisse. Une cle
    non canonique du domicile est ramenee par `forme_canonique` -- meme regle,
    meme domicile (EO-363).

    L'EMPREINTE est lue AVEC la date (friction du 2026-09-23) : une note est
    ecrite pour UNE ecriture, et c'est son empreinte qui le prouve. Une note qui
    n'en porte pas (anterieure a la mesure) rend une empreinte VIDE -- elle n'est
    jamais devinee, et le verdict DIT alors ce qui manque.
    """
    if not maison["bdd"] or not Path(maison["bdd"]).is_file():
        return {}
    try:
        donnees = json.loads(Path(maison["bdd"]).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    champ = maison.get("champ_empreinte") or ""
    notes = {}
    for cle, entree in (donnees.get("fichiers") or {}).items():
        canonique = forme_canonique(cle, BASE)
        if not canonique:
            continue
        for item in (entree or {}).get("modifications", []):
            empreinte = str(item.get(champ, "") or "") if champ else ""
            notes.setdefault(canonique, []).append((str(item.get("date", "")), empreinte))
    return notes


def notes_sans_empreinte(notes):
    """[cle] des fiches dont AUCUNE note ne porte d'empreinte (anterieure a la mesure).

    La dette est MESUREE et DITE, a la pose comme a la verification (L-286) : une
    note qui ne porte pas l'empreinte de son contenu ne peut plus rien attester --
    le controle ne doit pas le decouvrir au premier refus. Ce n'est pas un silence :
    c'est un compte.
    """
    return sorted(cle for cle, entrees in notes.items()
                  if entrees and not any(empreinte for _, empreinte in entrees))


def verdict_attribution(entrees, empreinte_mesuree, date_pose):
    """(attribuee, motif) : une note atteste-t-elle VRAIMENT ce contenu ?

    DEUX conditions, et la seconde est la correction du 2026-09-23 :
      - la note est POSTERIEURE a la pose (c'est l'ecriture de CE tour -- une note
        anterieure raconte un autre tour) ;
      - la note PORTE l'empreinte du contenu mesure (elle parle de CE contenu).
    Avant, seule la date etait lue : une note ecrite pour une AUTRE ecriture
    blanchissait n'importe quel changement posterieur, et le controle, qui
    imprimait les deux empreintes sans les comparer, ne pouvait pas s'en apercevoir.
    Le motif est rendu dans TOUS les cas de refus : une accusation qui ne dit pas ce
    qui manque coute un tour de plus.
    """
    posterieures = [(date, empreinte) for date, empreinte in entrees if date > date_pose]
    if not posterieures:
        return False, ("aucune note posterieure a la pose au domicile bdd-modifications"
                       if entrees else
                       "aucune note au domicile bdd-modifications")
    for _, empreinte in posterieures:
        if empreinte and empreinte == empreinte_mesuree:
            return True, ""
    # L'ORDRE DES MOTIFS COMPTE (mesure du 2026-09-23, prouvee en direct) : une fiche
    # porte souvent PLUSIEURS notes posterieures (une ancienne sans empreinte, une
    # recente avec). Accuser "SANS empreinte" quand une note en porte une et qu'elle
    # ne correspond pas enverrait chercher la mauvaise cause : ici, c'est la note
    # qui est PERIMEE, et le motif doit le dire en premier.
    avec_empreinte = [empreinte for _, empreinte in posterieures if empreinte]
    if avec_empreinte:
        return False, (str(len(avec_empreinte)) + " note(s) posterieure(s) d une AUTRE"
                       " empreinte : la note est PERIMEE (ecrite pour un autre contenu)")
    return False, (str(len(posterieures)) + " note(s) posterieure(s) SANS empreinte : ecrite(s)"
                   " avant que la note ne mesure le contenu -- aucune ne peut attester")


def ecritures_non_attribuees(reference, actuelles, notes, date_pose):
    """[(cle, attendue, mesuree, motif)] : change SANS note qui l'atteste.

    TROIS populations, et une seule est accusee :
      - inchangee : hors du controle (l'empreinte est le fait mesure) ;
      - DISPARUE : un fichier efface n'est pas juge ici (une suppression se
        declare par sa porte, et le controle ne voit qu'une absence) ;
      - changee : une note POSTERIEURE a la pose doit porter l'empreinte MESUREE.
    Une note ANTERIEURE a la pose ne blanchit rien, et une note perimee non plus :
    c'est precisement l'erreur que le controle existe pour attraper.
    """
    accusees = []
    for cle in sorted(reference):
        attendue = reference[cle]
        mesuree = actuelles.get(cle)
        if mesuree is None or mesuree == attendue:
            continue
        attribuee, motif = verdict_attribution(notes.get(cle) or [], mesuree, date_pose)
        if attribuee:
            continue
        accusees.append((cle, attendue, mesuree, motif))
    return accusees


def creations_non_attribuees(reference, actuelles, notes, date_pose):
    """[(cle, motif)] des sources NEUVES (absentes de la pose) sans note qui les atteste.

    Une CREATION hors porte est le cas le plus probable d'une ecriture par un
    outil natif : le fichier n'existe pas a la pose, donc aucun changement
    d'empreinte ne peut le trahir. Sans cette population, le controle ne verrait
    que les ecritures DANS un fichier deja connu -- et laisserait passer tout le
    reste en silence. La note doit y porter l'empreinte du contenu CREE.
    """
    neuves = []
    for cle in sorted(actuelles):
        if cle in reference:
            continue
        attribuee, motif = verdict_attribution(notes.get(cle) or [], actuelles[cle], date_pose)
        if attribuee:
            continue
        neuves.append((cle, motif))
    return neuves


def lire_reference():
    """(reference, date de pose) du registre, ou (None, "") s'il est absent."""
    if not REGISTRE.is_file():
        return None, ""
    try:
        donnees = json.loads(REGISTRE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, ""
    return donnees.get("empreintes") or {}, str(donnees.get("date_pose") or "")


def declarer_familles(maison):
    """Les familles DECLAREES, leurs fichiers PRESENTS, et ce qui n'a PAS ete LU (L-104).

    Un drapeau d'arret ne vit que le temps d'un arret : ne compter que les
    fichiers EXCLUS dirait `0` presque toujours, et une exclusion qu'on ne compte
    jamais est un angle mort. On dit donc ce qui est DECLARE, puis ce qui est la.
    Et ce qui n'a pas pu etre LU se dit aussi : une routine dont les constantes ne
    se chargent pas est une routine dont aucune production ne peut etre connue --
    un silence, si le controle ne le nommait pas.
    """
    drapeaux = maison.get("drapeaux", ())
    presents = sum(1 for drapeau, _ in drapeaux if (MATRICE / drapeau).is_file())
    print("  hors jugement DECLARE : " + str(len(drapeaux))
          + " drapeau(x) d'arret (table unique du serveur ; presents sur disque : "
          + str(presents) + ")")
    print("  hors jugement DECLARE : " + str(len(maison.get("productions", ())))
          + " production(s) de routine declaree(s)")
    muettes = maison.get("declarations_muettes", ())
    print("  declarations de routine NON LUES : "
          + (", ".join(muettes) if muettes else "aucune"))


def poser():
    """Pose les empreintes de reference ET la date : tout ce qui precede est pardonne."""
    sources, exclus, maison = perimetre()
    if not sources:
        print("REFUS : aucun source dans le perimetre -- rien a poser (Matrice introuvable ?)")
        return 2
    empreintes = {}
    illisibles = 0
    for cle, chemin in sources:
        valeur = empreinte(chemin)
        if valeur is None:
            illisibles += 1
            continue
        empreintes[cle] = valeur
    date_pose = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registre = {
        "date_pose": date_pose,
        "perimetre": "les sources de la Matrice, moins les exclusions DECLAREES",
        "empreintes": empreintes,
    }
    REGISTRE.write_text(json.dumps(registre, ensure_ascii=False, indent=2), encoding="utf-8")

    # LA PORTEE MESUREE AVANT DE REFUSER (L-286) : combien de sources n'ont AUCUNE
    # note au domicile ? Elles sont dans le perimetre, mais le controle ne pourra
    # rien leur attribuer -- la dette est DITE a la pose, pas decouverte au refus.
    notes = notes_du_domicile(maison)
    sans_note = [cle for cle in empreintes if not notes.get(cle)]
    print("REFERENCE POSEE : " + str(len(empreintes)) + " sources"
          + (" (" + str(illisibles) + " illisible(s), non posees)" if illisibles else ""))
    print("  date de pose : " + date_pose)
    print("  sans note au domicile des modifications : " + str(len(sans_note))
          + " source(s) -- le controle ne pourra leur attribuer aucun changement")
    print("  notes SANS empreinte (anterieures a la mesure du contenu) : "
          + str(len(notes_sans_empreinte(notes))) + " fiche(s)"
          + " -- elles ne peuvent PLUS attester un changement")
    declarer_familles(maison)
    for motif in sorted(exclus):
        print("  hors jugement : " + motif + " -- " + str(exclus[motif]) + " fichier(s)")
    print("  registre : " + str(REGISTRE.relative_to(MATRICE)))
    return 0


def verifier():
    """Chaque changement posterieur a la pose doit porter une note posterieure."""
    reference, date_pose = lire_reference()
    if reference is None:
        print("REFUS : aucune reference posee -- lancer `poser` d'abord.")
        return 2
    sources, exclus, maison = perimetre()
    actuelles = {}
    for cle, chemin in sources:
        valeur = empreinte(chemin)
        if valeur is not None:
            actuelles[cle] = valeur
    notes = notes_du_domicile(maison)
    accusees = ecritures_non_attribuees(reference, actuelles, notes, date_pose)
    neuves = creations_non_attribuees(reference, actuelles, notes, date_pose)

    changees = [cle for cle in reference
                if cle in actuelles and actuelles[cle] != reference[cle]]
    disparues = [cle for cle in reference if cle not in actuelles]
    attribuees = len(changees) - len(accusees)
    print("ATTRIBUTION : pose du " + date_pose + " | " + str(len(reference)) + " source(s) posee(s)")
    print("  changees depuis la pose : " + str(len(changees))
          + " (attribuees a une porte : " + str(attribuees) + ")")
    print("  sources NEUVES depuis la pose : " + str(len(actuelles) - len(reference) + len(disparues))
          + " dont NON attribuees : " + str(len(neuves)))
    print("  disparues : " + str(len(disparues)) + " (non jugees ici)")
    print("  notes SANS empreinte (anterieures a la mesure du contenu) : "
          + str(len(notes_sans_empreinte(notes))) + " fiche(s)"
          + " -- elles ne peuvent PLUS attester un changement")
    declarer_familles(maison)
    for motif in sorted(exclus):
        print("  hors jugement : " + motif + " -- " + str(exclus[motif]) + " fichier(s)")
    if not accusees and not neuves:
        print("VERDICT OK : toute ecriture posterieure a la pose est attribuee a une porte.")
        return 0
    print("ECRITURE HORS DE SA PORTE (" + str(len(accusees) + len(neuves)) + ") :")
    for cle, attendue, mesuree_vue, motif in accusees:
        print("  - " + cle)
        print("      empreinte attendue : " + attendue)
        print("      empreinte mesuree  : " + mesuree_vue)
        print("      " + motif)
    for cle, motif in neuves:
        print("  - " + cle + " (source NEUVE, absente de la pose)")
        print("      " + motif)
    return 1


def auto_test():
    """Le cobaye MORD, le contre-temoin EPARGNE (L-032) -- sur des faits FABRIQUES.

    Aucune epreuve ne touche le disque : tout est joue sur des dictionnaires en
    memoire. Rejouable telle quelle : c'est la preuve, pas un recit de preuve.
    """
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)

    pose = "2026-09-22 10:00:00"
    cle = "matrice/data/commun/cible.py"
    reference = {cle: "A" * 64}
    changee = {cle: "B" * 64}
    # L'EMPREINTE DU CONTENU CHANGE : c'est ELLE que la note doit porter pour
    # attester CETTE ecriture (friction du 2026-09-23). `autre` est l'empreinte
    # d'une AUTRE ecriture -- celle d'une note PERIMEE.
    mesuree = "B" * 64
    autre = "C" * 64

    # 1. COBAYE POSITIF : l'ecriture PASSE PAR LA PORTE -- une note posterieure a la
    #    pose ET qui porte l'empreinte du contenu mesure.
    apres = {cle: [(pose, "A" * 64), ("2026-09-22 10:05:00", mesuree)]}
    accusees = ecritures_non_attribuees(reference, changee, apres, pose)
    controler("le cobaye EPARGNE une note posterieure qui PORTE l'empreinte mesuree",
              not accusees, str(len(accusees)) + " accusation(s)")

    # 2. COBAYE NEGATIF : la MEME ecriture, sans note -- elle est ACCUSEE.
    accusees = ecritures_non_attribuees(reference, changee, {}, pose)
    controler("le cobaye MORD une ecriture SANS note", len(accusees) == 1, str(len(accusees)))
    if accusees:
        nom, attendue, empreinte_vue, _ = accusees[0]
        controler("l'accusation NOMME le fichier", nom == cle, nom)
        controler("l'accusation porte les DEUX empreintes",
                  attendue == "A" * 64 and empreinte_vue == mesuree,
                  attendue[:8] + " / " + empreinte_vue[:8])

    # 3. LE COBAYE QUI IMPORTE : une note ANTERIEURE a la pose ne blanchit RIEN.
    #    C'est l'erreur que le controle existe pour attraper : un fichier a deja
    #    une histoire, donc il a TOUJOURS une note -- seulement pas celle de CETTE
    #    ecriture. Un controle qui se contente d'une note quelconque ne voit rien.
    anterieure = {cle: [("2026-09-01 08:00:00", mesuree), ("2026-09-02 09:00:00", mesuree)]}
    accusees = ecritures_non_attribuees(reference, changee, anterieure, pose)
    controler("le cobaye MORD une note ANTERIEURE a la pose", len(accusees) == 1, str(len(accusees)))

    # 4. LA NOTE PERIMEE (friction du 2026-09-23) : posterieure a la pose, donc
    #    l'ANCIENNE regle -- la date seule -- la croyait ; mais elle a ete ecrite
    #    pour un AUTRE contenu. C'est le cobaye qui manquait : une note ne dit pas
    #    QUAND on a note, elle dit CE QU on a note.
    perimee = {cle: [("2026-09-22 10:05:00", autre)]}
    accusees = ecritures_non_attribuees(reference, changee, perimee, pose)
    controler("le cobaye MORD une note posterieure d une AUTRE empreinte (perimee)",
              len(accusees) == 1, str(len(accusees)))
    if accusees:
        controler("l'accusation DIT que la note est PERIMEE",
                  "PERIMEE" in accusees[0][3], accusees[0][3][:80])
    controler("le contre-temoin est AVEUGLE : la DATE SEULE blanchissait la note perimee",
              any(date > pose for date, _ in perimee[cle]),
              "il fallait comparer, pas dater -- d ou l'empreinte dans la note")

    # 5. LA NOTE ANTERIEURE A LA MESURE : ecrite avant que la note ne mesure le
    #    contenu, elle ne porte pas d'empreinte. Elle ne peut donc RIEN attester --
    #    et le verdict le DIT, au lieu de laisser croire a une note manquante.
    ancienne = {cle: [("2026-09-22 10:05:00", "")]}
    accusees = ecritures_non_attribuees(reference, changee, ancienne, pose)
    controler("le cobaye MORD une note posterieure SANS empreinte", len(accusees) == 1,
              str(len(accusees)))
    if accusees:
        controler("l'accusation DIT que la note ne porte pas d'empreinte",
                  "SANS empreinte" in accusees[0][3], accusees[0][3][:80])

    # 6. LE CONTRE-TEMOIN DU CONTROLE ENTIER : sans lui, la MEME ecriture passe EN
    #    SILENCE. Le temoin brut -- l'empreinte seule, ce que le projet savait faire
    #    -- voit le changement et ne sait RIEN de la porte : l'ecriture legitime et
    #    l'ecriture hors porte y sont INDISTINGUABLES. C'est mesure, pas affirme.

    def temoin_brut(reference_vue, actuelles_vues):
        """Le controle NAIF : toute empreinte qui change est un changement."""
        return sorted(k for k in reference_vue if reference_vue[k] != actuelles_vues.get(k))

    legitime = ecritures_non_attribuees(reference, changee, apres, pose)
    hors_porte = ecritures_non_attribuees(reference, changee, {}, pose)
    controler("le contre-temoin est AVEUGLE : le temoin brut voit les DEUX cas de la meme facon",
              temoin_brut(reference, changee) == [cle], str(len(temoin_brut(reference, changee))))
    controler("le controle les SEPARE : 0 accusation pour la porte, 1 pour le hors-porte",
              len(legitime) == 0 and len(hors_porte) == 1,
              "legitime=" + str(len(legitime)) + " hors-porte=" + str(len(hors_porte)))

    # 7. LE TEMOIN QUI NE DOIT PAS MENTIR : inchangee = hors du controle, et une
    #    source DISPARUE n'est pas accusee d'ecriture (elle n'est plus la).
    controler("une source INCHANGEE est hors du controle",
              not ecritures_non_attribuees(reference, {cle: "A" * 64}, {}, pose))
    controler("une source DISPARUE n'est pas accusee d'ecriture",
              not ecritures_non_attribuees(reference, {}, {}, pose))

    # 8. LA CREATION HORS PORTE : le fichier n'existe pas a la pose, donc aucun
    #    changement d'empreinte ne peut le trahir -- c'est la population qu'un
    #    controle par empreintes laisserait passer ENTIEREMENT. Elle aussi doit
    #    porter l'empreinte du contenu CREE : la memoire n'a pas de version de la
    #    porte qui se contenterait d'une date sur les fichiers neufs.
    neuve = "_operateur/optimus-prime/outil-fantome.py"
    avec = dict(changee)
    avec[neuve] = autre
    controler("le cobaye MORD une source NEUVE sans note",
              [nom for nom, _ in creations_non_attribuees(reference, avec, {}, pose)] == [neuve],
              neuve)
    controler("le contre-temoin EPARGNE une source neuve NOTEE avec l'empreinte du contenu",
              not creations_non_attribuees(
                  reference, avec, {neuve: [("2026-09-22 10:01:00", autre)]}, pose))
    controler("le cobaye MORD une source neuve notee d une empreinte PERIMEE",
              len(creations_non_attribuees(
                  reference, avec, {neuve: [("2026-09-22 10:01:00", mesuree)]}, pose)) == 1)
    controler("une source deja posee n'est jamais comptee comme neuve",
              not creations_non_attribuees(reference, reference, {}, pose))

    # 9. LES EXCLUSIONS SONT DECLAREES, ET ELLES MORDENT LA OU ELLES DOIVENT.
    maison = {"motif_bak": re.compile(r"\.bak\.[0-9]{8}_[0-9]{6}$"), "zone_cameleon": None,
              "zone_optimus": "_operateur/optimus-prime/tmp-optimus",
              "vues": (("_operateur/optimus-prime/suivi-pilote/suivi-pilote.md",
                        "vue recalculee par sa propre porte (domicile suivi-pilote)"),),
              "archives": "_operateur/optimus-prime/purification/archives",
              "suffixe_tmp": ".tmp",
              "productions": (("matrice/routines/verifier-liens-cartes/rapport-liens.json",
                               "verifier-liens-cartes"),
                              ("matrice/routines/veille-flux/alertes-emises.json",
                               "veille-flux")),
              "drapeaux": (("matrice/routines/veille-flux/veille-flux.arret",
                            "drapeau d'arret (nom declare par la table unique du serveur)"),)}
    controler("un journal est EXCLU (forme d'etat)",
              motif_exclusion("matrice/data/historiques-missions.jsonl", maison) != "",
              motif_exclusion("matrice/data/historiques-missions.jsonl", maison))
    controler("un etat de routine est EXCLU",
              motif_exclusion("matrice/routines/routeur-maintenance/routeur-etat.json", maison) != "",
              motif_exclusion("matrice/routines/routeur-maintenance/routeur-etat.json", maison))
    controler("un etat QUALIFIE est EXCLU (le faux positif attrape le 2026-09-22)",
              motif_exclusion("matrice/routines/espion-integrite/espion-etat-bdds.json", maison) != "",
              motif_exclusion("matrice/routines/espion-integrite/espion-etat-bdds.json", maison))
    controler("un etat de CADENCE est EXCLU (le faux positif attrape le 2026-09-23)",
              motif_exclusion("matrice/routines/vigie-portes/vigie-portes-cadence.json", maison) != "",
              motif_exclusion("matrice/routines/vigie-portes/vigie-portes-cadence.json", maison))
    controler("une VUE recalculee est EXCLUE (elle se reecrit a chaque passe)",
              motif_exclusion("_operateur/optimus-prime/suivi-pilote/suivi-pilote.md", maison) != "",
              motif_exclusion("_operateur/optimus-prime/suivi-pilote/suivi-pilote.md", maison))
    controler("une PRODUCTION declaree par sa routine est EXCLUE (friction du 2026-09-23)",
              motif_exclusion("matrice/routines/verifier-liens-cartes/rapport-liens.json",
                              maison) != "",
              motif_exclusion("matrice/routines/verifier-liens-cartes/rapport-liens.json", maison))
    controler("une SOURCE de la MEME routine n'est PAS exclue (contre-temoin de la production)",
              motif_exclusion("matrice/routines/verifier-liens-cartes/passe/fonctions.py",
                              maison) == "", "aucun motif")
    controler("une SOURCE n'est PAS exclue (contre-temoin des exclusions)",
              motif_exclusion("matrice/data/commun/cible.py", maison) == "",
              "aucun motif")
    controler("le CANAL DE DEMANDES DE L'OPERATEUR est DECLARE hors jugement",
              motif_exclusion("user-demandes/user-demandes.md", maison) != "",
              motif_exclusion("user-demandes/user-demandes.md", maison))

    # 10. L'AUDIT DES ECRITURES DE ROUTINE (2026-09-23) : trois familles etaient
    #     JUGEES faute d'etre declarees. Chacune a son cobaye -- et chacune a son
    #     CONTRE-TEMOIN, parce qu'une exclusion qui mord trop large est un silence
    #     de plus.
    controler("un TEMPORAIRE d'ecriture atomique est EXCLU (forme declaree par `ecrire`)",
              motif_exclusion("matrice/routines/veille-flux/veille-flux-cadence.json.tmp",
                              maison) != "",
              motif_exclusion("matrice/routines/veille-flux/veille-flux-cadence.json.tmp",
                              maison))
    controler("un DRAPEAU d'arret est EXCLU (nom declare par la table unique)",
              motif_exclusion("matrice/routines/veille-flux/veille-flux.arret", maison) != "",
              motif_exclusion("matrice/routines/veille-flux/veille-flux.arret", maison))
    controler("l'ETAT ANTI-SPAM de veille-flux est EXCLU (production declaree)",
              motif_exclusion("matrice/routines/veille-flux/alertes-emises.json", maison) != "",
              motif_exclusion("matrice/routines/veille-flux/alertes-emises.json", maison))
    controler("une SOURCE de veille-flux n'est PAS exclue (contre-temoin : la base acceptee)",
              motif_exclusion("matrice/routines/veille-flux/base-acceptee.json", maison) == "",
              "aucun motif")
    controler("un fichier d'une routine SANS drapeau declare n'est PAS exclu (contre-temoin)",
              motif_exclusion("matrice/routines/selecteur-flux/provenance.json", maison) == "",
              "aucun motif")

    # 11. LA DECLARATION EST-ELLE SEULEMENT ATTEIGNABLE ? Un domicile qui importe
    #     ses VOISINS par leur nom n'est pas chargeable par chemin : sans le
    #     drapeau `dossier_local`, la table des drapeaux serait un SILENCE -- le
    #     controle ne saurait meme pas qu'il ne la lit pas.
    for nom_voisin in ("constants_suivi_sync", "constants_verifier_liens_cartes",
                       "constants_vigie_portes"):
        sys.modules.pop(nom_voisin, None)
    sans_dossier = charger_module(DOMICILE_TABLE_DRAPEAUX, "cobaye_sans_dossier")
    controler("la table des drapeaux est INATTEINTE sans son dossier (le drapeau du"
              " chargeur est donc necessaire)", sans_dossier is None,
              "module charge : " + str(sans_dossier is not None))
    table = charger_module(DOMICILE_TABLE_DRAPEAUX, "cobaye_avec_dossier", dossier_local=True)
    declares = getattr(table, NOM_TABLE_DRAPEAUX, None) if table is not None else None
    controler("la table des drapeaux est ATTEINTE avec son dossier",
              bool(declares) and getattr(table, NOM_DRAPEAU_SERVEUR, None) is not None,
              str(len(declares or {})) + " drapeau(x) de routine + le drapeau du serveur")
    controler("le dossier du module n'est PAS laisse sur sys.path (un `constants` ne"
              " doit pas rester atteignable)",
              str(DOMICILE_TABLE_DRAPEAUX.resolve().parent) not in sys.path,
              "sys.path intact")
    # 12. LE SILENCE DES DECLARATIONS : une routine dont les constantes importent
    #     leurs VOISINS n'etait pas lue du tout (mesure du 2026-09-23 : `vie` etait
    #     la seule muette des neuf) -- ses productions auraient ete invisibles. Le
    #     controle ne devine pas ; il LIT, et il DIT ce qu'il n'a pas pu lire.
    muettes = domiciles()["declarations_muettes"]
    controler("une routine qui importe ses voisins par leur nom N'EST PLUS muette"
              " (dossier local du chargeur)", "vie" not in muettes,
              ", ".join(muettes) if muettes else "aucune muette")
    controler("une routine SANS declaration lisible reste DITE, jamais silencieuse",
              all(dossier.is_dir() for dossier in
                  (DOSSIER_ROUTINES / nom for nom in muettes)),
              ", ".join(muettes) if muettes else "aucune")

    print()
    print("AUTO-TEST " + str(sum(resultats)) + "/" + str(len(resultats))
          + " -- " + ("VERDICT OK" if all(resultats) else "VERDICT KO"))
    return 0 if all(resultats) else 1


def main():
    parser = argparse.ArgumentParser(description="Controle d'attribution des ecritures (ORDRE 3.2)")
    parser.add_argument("verbe", nargs="?", choices=("poser", "verifier"), help="poser | verifier")
    parser.add_argument("--auto-test", action="store_true", help="les cobayes, sur des faits fabriques")
    args = parser.parse_args()
    if args.auto_test:
        return auto_test()
    if args.verbe == "poser":
        return poser()
    if args.verbe == "verifier":
        return verifier()
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
