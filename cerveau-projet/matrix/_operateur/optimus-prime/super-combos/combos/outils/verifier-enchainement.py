#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-enchainement.py -- Garde : une mission CHARGEE garde son verdict, donc la chaine ne s'arrete plus APRES CHAQUE mission.

POURQUOI (demande createur EO-264, 2026-09-19) : < pourquoi le pilote ne charge-t-il
pas PLUSIEURS missions pour les executer a la suite ? Chaque mission close rend STOP
ENCHAINEMENT et l operateur doit relancer a la main >.

MESURE DU 2026-09-21 (avant le correctif) : `decision_enchainement` jugeait une mission
par (1) son CHAMP `auto_validation` et (2) `mission["id"] in index_auto`. Or l index
des auto-validees vit dans l ETAT DE L ENTONNOIR et ne porte que des ids d ITEM
(EO-N) -- jamais des ids de MISSION (MO-N). Une mission CHARGEe perdait donc son
verdict au PONT entonnoir -> pilote : mesure du jour, 45 missions sur 83 ne portaient
aucun champ, dont MO-318 (ne de EO-271) alors qu EO-271 EST dans l index (55 ids).
Le verdict n etait pas perdu -- il etait INTROUVABLE, faute d une identite relisible.

CE QU'IL EXIGE (6 controles) :
  1. UN SEUL DOMICILE DU FORMAT : le prefixe de provenance (`entonnoir:`) n est
     compose QUE chez son domicile (pilote/commun.py). Une composition residuelle
     ailleurs est un ecart : elle compile et change le sens sans un bruit (L-029).
  2. LE LECTEUR EST CELUI DU DOMICILE : `item_deja_servi` et le refus nomme de
     l injection PASSENT par `item_id_de_la_source` -- trois lectures du meme format
     vivaient dispersees, une quatrieme allait naitre (M-076).
  3. LA DECISION LIT LA PROVENANCE : `est_auto_validee` resout l id d item, sans
     jamais faire de repli muet (une provenance illisible reste NON auto-validee).
  4. FONCTIONNEL (import reel, cobayes en memoire, AUCUNE ecriture) : les TROIS voies
     repondent -- le champ, l index nommant la mission, la provenance de l item -- et
     le COBAYE QUI MORD : index VIDE ou provenance d un item NON auto-valide rendent
     NON (un garde qui ne rougit pas ne prouve rien).
  5. LA DECISION ELLE-MEME : une mission auto ne s arrete pas ; une mission NON auto
     s arrete AVEC un motif qui NOMME l id (le createur sait qui reprend la main).
  6. LA MESURE REELLE QU EXIGE EO-264 : la tete SERVIE (celle du brin, ou celle du
     lot quand le brin a ete verse), son verdict d auto-validation, l etat du lot et
     les missions en attente -- AFFICHES, jamais supposes.
  7. LA PORTE DU LOT (MO-380) : le verbe `lot etat` dit VRAI -- rang k/n, item, type,
     urgence lus chez leur domicile, ACCUSE par son nom un maillon qui a perdu sa
     memoire, et n accuse pas l etat legitime < aucun lot arme > (L-159).

CE QU'IL NE FAIT PAS : aucune ecriture, aucun etat modifie, aucun flag pose. Il lit
l etat reel du pilote et de l entonnoir pour le controle 6, en LECTURE SEULE.

Usage: python verifier-enchainement.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = racine introuvable.
"""

import argparse
import io
import json
import sys
from pathlib import Path

# Les domiciles : declares UNE fois ici, jamais recopies dans la logique.
# Ces chemins sont RELATIFS au dossier du pilote (jamais un prefixe `pilote/` en
# plus) : mesure du 2026-09-21, la premiere version les composait avec `pilote/`
# alors que l appelant lui passait DEJA le dossier du pilote -- `pilote/pilote/...`
# et le garde plantait au deuxieme controle (un chemin qui se double se DIT au
# lancement, jamais a la lecture).
DOSSIER_PILOTE = Path("_operateur") / "optimus-prime" / "pilote"
FICHIER_COMMUN = Path("commun.py")
FICHIER_DECISION = Path("injection") / "fonctions.py"
FICHIER_STATE_ENTONNOIR = Path("entonnoir-files-optimus.json")
FICHIER_FILE_MISSIONS = Path("file-missions-optimus.json")
# LE TEMOIN PEUT QUITTER LA FILE VIVANTE (L-139) : MO-318 a ete archive le
# 2026-09-22 pendant un round -- le controle tombait alors ROUGE sur un etat
# SAIN. Un temoin vit donc sur un porteur qui SURVIT : la file ET son archive.
FICHIER_FILE_MISSIONS_ARCHIVE = Path("file-missions-optimus-archive.json")

# Le prefixe du format, tel que la logique l ECRIT (controle 1).
LITTERAL_INTERDIT = '"entonnoir:"'
PREFIXE_DOMAINE = "PREFIXE_SOURCE_ENTONNOIR"
COMPOSITIONS_RESIDUELLES_ATTENDUES = 0
MARQUEUR_LECTEUR = "def item_id_de_la_source("
DOMICILES_LECTEUR_ATTENDUS = 1
MARQUEUR_CONSOMMEURS = "item_id_de_la_source("
CONSOMMATEURS_ATTENDUS = 2  # la decision + le refus nomme de l injection
MARQUEUR_CLES = "FAMILLE_SOURCE_ENTONNOIR"

# LE CONTRAT DE CONTINUITE (MO-318) : il n etait servi que pour une mission de LOT, or
# le lot n est pas toujours arme -- le contrat n atteignait donc jamais l agent dans le
# cas le plus frequent (la suite vient du brin ou de la file). Controles : un seul
# domicile, servi des qu une suite EXISTE, MUET sinon (le contre-temoin exige), un texte
# qui DIT vrai, et la suite calculee au moment ou le contrat voyage.
FICHIER_CONSTANTES = Path("constants.py")
MARQUEUR_CONTRAT = "RAPPEL_CHAINE = ("
MARQUEUR_ANCIEN_NOM = "RAPPEL_CHAINE_ARMEE"
MARQUEUR_DECLENCHEUR = 'mission.get("lot") or suite'
MARQUEUR_SUITE_CALCULEE = "suite_auto_a_conduire(file_missions, index_auto"
MOTS_DU_CONTRAT = ("lot", "brin", "file")  # les DEUX sources, nommees

# FORCER (MO-341) : la continuite ne tient pas a un rappel, elle tient a un REFUS.
# La meme regle vivait en TROIS formes et MANQUAIT au chargement d une mission
# simple -- l agent pouvait ouvrir un travail neuf pendant qu une mission attendait.
FICHIER_FILE_FONCTIONS = Path("file") / "fonctions.py"
MARQUEUR_REFUS_STRICT = "def refus_serie_stricte("
ANCIEN_REFUS = "REFUS : une mission est deja en cours"
# Mesure du 2026-09-21 : la regle vivait en SEPT endroits (deux sans garde du tout --
# `charger` une mission n en avait AUCUNE) et le texte etait ecrit de quatre facons.
# Une seule forme doit rester : celle du domicile.
MARQUEUR_APPEL_REFUS = "refus_serie_stricte(file_missions)"
PORTES_CONSOMMATRICES_ATTENDUES = 7
FORMES_ANCIENNES_ATTENDUES = 1  # la seule occurrence restante : le message du domicile
MOTS_DU_REFUS = ("fin", "reporter", "serie stricte")

# L identifiant d un ITEM (le seul que porte l index des auto-validees).
ID_ITEM_AUTO = "EO-345"
ID_ITEM_NON_AUTO = "EO-272"
ID_MISSION = "MO-318"

DOSSIERS_IGNORES = ("__pycache__",)
PREFIXE_ZONE_JETABLE = "tmp-"

RESULTATS = []


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def trouver_racine(depart):
    """Le dossier qui porte `_operateur/optimus-prime/pilote/commun.py`, ou None."""
    for candidat in [depart, depart / "cerveau-projet" / "matrix", depart / "matrix"]:
        if (candidat / DOSSIER_PILOTE / FICHIER_COMMUN).is_file():
            return candidat
    return None


def fichiers_du_pilote(pilote):
    """Les .py du pilote en CHAMP (hors zones jetables, caches et sauvegardes)."""
    trouves = []
    for chemin in sorted(pilote.rglob("*.py")):
        parties = chemin.relative_to(pilote).parts
        if any(p in DOSSIERS_IGNORES or p.startswith(PREFIXE_ZONE_JETABLE)
               for p in parties[:-1]):
            continue
        if ".bak." in chemin.name:
            continue
        trouves.append(chemin)
    return trouves


def controler_un_seul_domicile(pilote):
    """CONTROLE 1 : le format de provenance n est compose QUE chez son domicile."""
    residuels = []
    for chemin in fichiers_du_pilote(pilote):
        texte = chemin.read_text(encoding="utf-8", errors="replace")
        for numero, ligne in enumerate(texte.splitlines(), 1):
            if LITTERAL_INTERDIT in ligne:
                residuels.append(chemin.name + ":" + str(numero))
    controler("un seul domicile du format de provenance",
              len(residuels) == COMPOSITIONS_RESIDUELLES_ATTENDUES,
              (str(len(residuels)) + " composition(s) residuelle(s) : "
               + ", ".join(residuels)) if residuels
              else ("aucune composition de " + LITTERAL_INTERDIT + " hors du domicile"))
    commun = (pilote / FICHIER_COMMUN).read_text(encoding="utf-8", errors="replace")
    controler("le lecteur vit chez le domicile",
              commun.count(MARQUEUR_LECTEUR) == DOMICILES_LECTEUR_ATTENDUS
              and MARQUEUR_CLES in commun,
              "1 lecteur (" + MARQUEUR_LECTEUR.strip() + ") + " + PREFIXE_DOMAINE)
    return not residuels


def controler_consommateurs(pilote, racine):
    """CONTROLE 2 : les consommateurs PASSENT par le lecteur (aucune 3e copie)."""
    decision = (pilote / FICHIER_DECISION).read_text(encoding="utf-8", errors="replace")
    appels = decision.count(MARQUEUR_CONSOMMEURS)
    controler("les consommateurs passent par le lecteur du domicile",
              appels >= CONSOMMATEURS_ATTENDUS,
              str(appels) + " appel(s) dans injection/fonctions.py (decision + refus nomme)")
    return appels >= CONSOMMATEURS_ATTENDUS


def charger_decision(pilote):
    """Importe les fonctions de decision du pilote (lecture seule)."""
    if str(pilote) not in sys.path:
        sys.path.insert(0, str(pilote))
    from commun import memoire_de_la_source, refus_serie_stricte  # noqa: E402
    from file.fonctions import afficher_lot, charger_mission  # noqa: E402
    from injection.fonctions import (  # noqa: E402
        charger_rappel_route,
        decision_enchainement,
        est_auto_validee,
        suite_auto_a_conduire,
    )
    fonctions = {"charger_rappel_route": charger_rappel_route,
                 "suite_auto_a_conduire": suite_auto_a_conduire,
                 "refus_serie_stricte": refus_serie_stricte,
                 "memoire_de_la_source": memoire_de_la_source,
                 "afficher_lot": afficher_lot,
                 "charger_mission": charger_mission}
    return est_auto_validee, decision_enchainement, fonctions


def controler_fonctionnel(est_auto_validee, decision_enchainement, index_reel):
    """CONTROLES 3 a 5 : les trois voies, le cobaye qui mord, et la decision."""
    index_auto = [ID_ITEM_AUTO]
    mission_auto = {"id": ID_MISSION, "source": "entonnoir:" + ID_ITEM_AUTO + ":dev/outil:haute"}
    mission_non_auto = {"id": "MO-900", "source": "entonnoir:" + ID_ITEM_NON_AUTO + ":dev/outil:haute"}
    sans_provenance = {"id": "MO-901", "source": ""}
    par_champ = {"id": "MO-902", "auto_validation": "auto"}
    par_index = {"id": ID_ITEM_AUTO}
    controler("voie 3 : la PROVENANCE resout le verdict",
              est_auto_validee(mission_auto, index_auto) is True,
              "source " + mission_auto["source"] + " + index [" + ID_ITEM_AUTO + "] -> True")
    controler("voies 1 et 2 intactes (champ, index nommant la mission)",
              est_auto_validee(par_champ, index_auto) and est_auto_validee(par_index, index_auto),
              "champ `auto_validation` et index nommant la mission -> True")
    cobaye = {
        "provenance d un item NON auto-valide": est_auto_validee(mission_non_auto, index_auto),
        "mission sans provenance lisible": est_auto_validee(sans_provenance, index_auto),
        "index VIDE (le cobaye doit MORDRE)": est_auto_validee(mission_auto, []),
    }
    mordu = [nom for nom, verdict in cobaye.items() if verdict is not False]
    controler("cobaye : les trois cas NON auto-valides rendent bien NON",
              not mordu,
              "aucun repli muet -- " + str(len(cobaye)) + " cas juges NON")
    arret_auto, _ = decision_enchainement(mission_auto, False, True, index_auto)
    arret_non, motif = decision_enchainement(mission_non_auto, False, True, index_auto)
    nomme = ID_MISSION not in motif or "MO-900" in motif
    controler("la DECISION suit le verdict (et nomme qui reprend la main)",
              arret_auto is False and arret_non is True and nomme,
              ("auto -> la chaine CONTINUE ; non auto -> STOP : " + motif[:70])
              if (arret_auto is False and arret_non is True)
              else "decision inattendue")
    # La MEME decision, jouee sur l INDEX REEL : le cas qui arretait la chaine.
    if index_reel:
        reel = next((m for m in charger_missions() if m.get("id") == ID_MISSION), None)
        if reel is not None:
            arret, _ = decision_enchainement(reel, False, True, index_reel)
            controler("la mission reelle " + ID_MISSION + " ne bloque plus la chaine",
                      arret is False,
                      "source " + str(reel.get("source")) + " resolue dans l index reel ("
                      + str(len(index_reel)) + " ids)")
        else:
            # LE TEMOIN INTERROGE AUSSI L ARCHIVE : la file TOURNE, donc un
            # temoin choisi dans la file vivante finit par en sortir et le garde
            # accuse alors un etat SAIN. Le controle DIT ou il a lu le temoin --
            # une mesure qui ne nomme pas sa source se lit comme un echec.
            archive = next((m for m in charger_missions(archive=True)
                            if m.get("id") == ID_MISSION), None)
            if archive is not None:
                arret_archive, _ = decision_enchainement(archive, False, True, index_reel)
                controler("la mission reelle " + ID_MISSION + " ne bloque plus la chaine",
                          arret_archive is False,
                          "temoin lu dans l ARCHIVE (la file a tourne depuis sa pose) -- source "
                          + str(archive.get("source")))
            else:
                controler("la mission reelle " + ID_MISSION + " est presente",
                          False, "absente de la file ET de l archive : le cas temoin ne peut pas etre rejoue")
    return True


def charger_missions(archive=False):
    """Les missions de la file du pilote (lecture seule), ou [] si illisible."""
    chemin = Path(__file__).resolve()
    for parent in chemin.parents:
        nom_fichier = FICHIER_FILE_MISSIONS_ARCHIVE if archive else FICHIER_FILE_MISSIONS
        candidat = parent / DOSSIER_PILOTE / nom_fichier
        if candidat.is_file():
            try:
                return json.loads(candidat.read_text(encoding="utf-8")).get("missions", [])
            except Exception:
                return []
    return []


def controler_rappel_chaine(pilote, fonctions):
    """CONTROLES 7 a 10 (MO-318) : le contrat de continuite atteint enfin l agent."""
    constantes = (pilote / FICHIER_CONSTANTES).read_text(encoding="utf-8", errors="replace")
    source = (pilote / FICHIER_DECISION).read_text(encoding="utf-8", errors="replace")
    controler("le contrat de continuite a UN seul domicile",
              constantes.count(MARQUEUR_CONTRAT) == 1
              and MARQUEUR_ANCIEN_NOM not in constantes
              and MARQUEUR_ANCIEN_NOM not in source,
              "1 declaration (" + MARQUEUR_CONTRAT.strip() + "), aucun ancien nom")
    debut = constantes.find(MARQUEUR_CONTRAT)
    texte = constantes[debut:debut + 700] if debut >= 0 else ""
    manquants = [mot for mot in MOTS_DU_CONTRAT if mot not in texte]
    controler("le contrat DIT vrai (il nomme ses deux sources)",
              not manquants,
              "nomme lot + brin + file" if not manquants
              else "source non nommee : " + ", ".join(manquants))
    controler("le declencheur n est plus le LOT SEUL",
              MARQUEUR_DECLENCHEUR in source
              and MARQUEUR_SUITE_CALCULEE in source,
              "la suite est calculee au moment ou le contrat voyage")
    if fonctions is None:
        return False
    charger_rappel_route = fonctions.get("charger_rappel_route")
    if charger_rappel_route is None:
        return controler("le contrat est SERVI des qu une suite existe", False,
                         "charger_rappel_route absente")
    # LE COBAYE QUI MORD : servi avec une suite, MUET sans (le contre-temoin que l item
    # exige -- une fin hors chaine ne reveille rien).
    avec = charger_rappel_route({"id": "MO-900"}, "EO-345")
    sans = charger_rappel_route({"id": "MO-901"}, "")
    lot = charger_rappel_route({"id": "MO-902", "lot": "L-1"}, "")
    controler("le contrat est SERVI avec une suite, MUET sans",
              bool(avec) and not sans and bool(lot),
              "suite -> servi | mission seule -> MUET (contre-temoin) | lot -> servi")
    return True


def controler_forcer(pilote, fonctions):
    """CONTROLES 11 a 14 (MO-341) : le refus qui FORCE la chaine.

    Demande createur : < on doit forcer >. Un rappel dit la suite, il ne la garantit
    pas -- mais un REFUS, lui, s applique. Ce garde exige : un seul domicile du refus,
    les QUATRE portes qui le consomment, son texte qui NOMME la mission ET ses deux
    remedes, et -- le controle qui compte -- la porte qui MANQUAIT qui refuse pour de
    vrai (cobaye en memoire : aucune ecriture, aucune creation).
    """
    commun = (pilote / FICHIER_COMMUN).read_text(encoding="utf-8", errors="replace")
    fichier = (pilote / FICHIER_FILE_FONCTIONS).read_text(encoding="utf-8", errors="replace")
    injection = (pilote / FICHIER_DECISION).read_text(encoding="utf-8", errors="replace")
    anciennes = (commun + fichier + injection).count(ANCIEN_REFUS)
    controle_domicile = controler(
        "le refus de la serie stricte a UN seul domicile",
        commun.count(MARQUEUR_REFUS_STRICT) == 1
        and anciennes == FORMES_ANCIENNES_ATTENDUES,
        "1 declaration (" + MARQUEUR_REFUS_STRICT.strip() + ") ; formes anciennes restantes : "
        + str(anciennes) + " (le message du domicile, et rien d autre)")
    occurrences = sum(texte.count(MARQUEUR_APPEL_REFUS)
                      for texte in (commun, fichier, injection))
    portes = occurrences - sum(texte.count(MARQUEUR_REFUS_STRICT)
                               for texte in (commun, fichier, injection))
    controler("les portes CONSOMMENT le refus du domicile",
              portes == PORTES_CONSOMMATRICES_ATTENDUES,
              str(portes) + " portes (charger, charger un lot, injecter, enchainer, conduire,"
              " verser le brin, consommer la tete)")
    if fonctions is None:
        return controle_domicile
    refus_serie_stricte = fonctions.get("refus_serie_stricte")
    charger_mission = fonctions.get("charger_mission")
    if refus_serie_stricte is None or charger_mission is None:
        return controler("le refus est joignable", False, "fonction absente")
    libre = refus_serie_stricte({"missions": [{"id": "MO-1", "statut": "en-attente"}]})
    message = refus_serie_stricte({"missions": [{"id": "MO-900", "statut": "en-cours",
                                                 "theme": "ROUTINE"}]})
    manquants = [mot for mot in MOTS_DU_REFUS if mot not in message]
    controler("le refus NOMME la mission et ses deux remedes (fin / reporter)",
              libre == "" and not manquants,
              "file libre -> aucun refus | file occupee -> " + "MO-900 + fin + reporter"
              if not manquants else "manque : " + ", ".join(manquants))
    # LE CONTROLE QUI COMPTE : la porte qui MANQUAIT (charger une mission) refuse.
    cobaye = {"missions": [{"id": "MO-900", "statut": "en-cours", "theme": "ROUTINE"}]}
    avant = len(cobaye["missions"])
    tampon, sauvegarde = io.StringIO(), sys.stdout
    try:
        sys.stdout = tampon
        code = charger_mission(["--theme", "PILOTE", "--type", "dev",
                                "--objectif", "travail neuf interdit pendant la chaine"],
                               lambda: cobaye, None)
    finally:
        sys.stdout = sauvegarde
    sortie = tampon.getvalue()
    return controler("la porte qui MANQUAIT refuse pour de vrai (travail neuf interdit)",
                     code == 1 and len(cobaye["missions"]) == avant
                     and "REFUS" in sortie,
                     "code 1, aucune creation, la mission en cours est NOMMEE")


def controler_lot_visible(pilote, fonctions=None):
    """CONTROLE 7 : la reprise du retard se LIT, et sa memoire perdue s ACCUSE (MO-380).

    EO-380 (demande du createur) : un lot de 37 missions versees d un seul geste ne se
    lisait qu en ouvrant le JSON. Le cockpit appelle le verbe du pilote (`lot etat`) :
    ce controle verifie que ce verbe dit VRAI -- il nomme le rang, l item, le type et
    l urgence quand ils existent, il ACCUSE (code 1, maillon NOMME) quand la memoire
    de naissance manque, et il n accuse jamais l etat legitime < aucun lot arme >.
    """
    afficher_lot = (fonctions or {}).get("afficher_lot")
    memoire = (fonctions or {}).get("memoire_de_la_source")
    if afficher_lot is None or memoire is None:
        controler("la porte du lot est importable (lot etat)", False,
                  "import manquant : le cockpit ne pourrait pas appeler le verbe")
        return False
    longue = memoire("entonnoir:EO-272:dev/autre:haute")
    controler("le domicile lit la memoire de naissance, et n invente jamais",
              longue.get("type") == "dev" and longue.get("urgence") == "haute"
              and memoire("entonnoir:EO-121") == {}
              and memoire("descriptif:x:y:z") == {},
              "forme longue -> type/categorie/urgence | forme COURTE -> {} (rien d invente)")
    # LE COBAYE QUI MORD : un maillon sans memoire doit etre NOMME, la file non touchee.
    cobaye = {"lot": {"ids": ["MO-901", "MO-902"]}, "missions": [
        {"id": "MO-901", "statut": "en-attente", "lot": "COBAYE",
         "source": "entonnoir:EO-272:dev/autre:haute", "titre": "avec memoire"},
        {"id": "MO-902", "statut": "en-attente", "lot": "COBAYE",
         "source": "entonnoir:EO-121", "titre": "sans memoire"}]}
    avant = json.dumps(cobaye, sort_keys=True)
    tampon, sauvegarde = io.StringIO(), sys.stdout
    try:
        sys.stdout = tampon
        code_lot = afficher_lot(cobaye)
    finally:
        sys.stdout = sauvegarde
    sortie = tampon.getvalue()
    controler("un maillon du lot sans memoire est ACCUSE, par son nom",
              code_lot == 1 and "MO-902" in sortie and "MO-901" not in sortie.split("ACCUSE")[-1]
              and json.dumps(cobaye, sort_keys=True) == avant,
              "code 1, le maillon fautif est nomme, la file cobaye n est pas touchee")
    # LE CONTRE-TEMOIN : pas de lot arme -> code 0 (aucun etat legitime accuse, L-159).
    tampon = io.StringIO()
    try:
        sys.stdout = tampon
        code_sans_lot = afficher_lot({"missions": [{"id": "MO-903", "statut": "en-attente"}]})
    finally:
        sys.stdout = sauvegarde
    controler("sans lot arme, la porte ne condamne rien (contre-temoin)",
              code_sans_lot == 0 and "Aucun lot arme" in tampon.getvalue(),
              "code 0 + la raison est DITE au lieu de laisser croire a un lot vide")
    return code_lot == 1


def controler_mesure_reelle(pilote, fonctions=None, index_reel=None):
    """CONTROLE 6 : la mesure REELLE qu exige EO-264 (tete, verdict, lot)."""
    entonnoir = pilote / FICHIER_STATE_ENTONNOIR
    file_missions = pilote / FICHIER_FILE_MISSIONS
    if not (entonnoir.is_file() and file_missions.is_file()):
        controler("la mesure reelle (tete du brin, verdict, lot)", False,
                  "etat introuvable")
        return False
    etat = json.loads(entonnoir.read_text(encoding="utf-8"))
    index_auto = list(etat.get("auto_validees") or [])
    brin = etat.get("brin") or []
    tete = brin[0] if brin else None
    tete_id = tete.get("id") if isinstance(tete, dict) else None
    verdict_tete = bool(tete_id) and tete_id in index_auto
    file_d = json.loads(file_missions.read_text(encoding="utf-8"))
    en_attente = [m.get("id") for m in file_d.get("missions", [])
                  if m.get("statut") == "en-attente"]
    # LE BRIN PEUT ETRE VIDE A BON DROIT : quand il vient d etre verse en LOT
    # (file verser -- mesure du 2026-09-21, la reprise du retard). Exiger une tete
    # de brin accusait alors un etat LEGITIME. La mesure nomme donc la tete
    # SERVIE, quelle que soit sa source : le brin, sinon la file du lot.
    ids_lot = list((file_d.get("lot") or {}).get("ids") or [])
    tete_servie = tete_id or (ids_lot[0] if ids_lot else None)
    print("  MESURE REELLE (EO-264) : tete SERVIE = " + str(tete_servie)
          + " (brin " + ("vide -- verse en lot" if not tete_id else "non vide")
          + "); tete du brin = " + str(tete_id)
          + " (auto-validee : " + ("oui" if verdict_tete else "NON")
          + ") | lot = " + str(len(ids_lot)) + " id(s) " + str(file_d.get("lot"))
          + " | en attente = " + ", ".join(en_attente[:6])
          + (" (+ %d)" % (len(en_attente) - 6) if len(en_attente) > 6 else ""))
    premier = controler(
        "les TROIS faits de la mesure sont nommes (tete SERVIE, verdict, lot)",
        bool(tete_servie) and isinstance(index_auto, list),
        str(len(index_auto)) + " id(s) auto-valide(s) a l index de l entonnoir")
    # MO-318 : LA SUITE que le contrat annoncera a l agent -- affichee, et coherente
    # (soit un item du brin, soit une mission de la file : jamais une valeur inventee).
    suite_auto = (fonctions or {}).get("suite_auto_a_conduire")
    if suite_auto is None:
        return premier
    mission_courante = next((m.get("id") for m in file_d.get("missions", [])
                             if m.get("statut") == "en-cours"), "")
    suite = suite_auto(file_d, index_auto, mission_courante or "")
    connus = {m.get("id") for m in file_d.get("missions", [])}
    print("  SUITE AUTO (le contrat l annoncera) : " + (suite if suite else
          "AUCUNE -- le contrat restera MUET (contre-temoin)"))
    return controler("la suite annoncee vient du brin ou de la file (jamais inventee)",
                     suite == "" or suite in index_auto or suite in connus,
                     "suite = " + (suite if suite else "aucune"))


def main():
    parseur = argparse.ArgumentParser(description="Garde de l enchainement du pilote.")
    parseur.add_argument("--racine", default=".", help="racine du depot")
    options = parseur.parse_args()
    racine = trouver_racine(Path(options.racine).resolve())
    if racine is None:
        print("REFUS : racine introuvable (aucun _operateur/optimus-prime/pilote/commun.py).")
        return 2
    pilote = racine / DOSSIER_PILOTE
    print("GARDE DE L ENCHAINEMENT -- le verdict d une mission chargee se RESOUT chez son domicile")
    controler_un_seul_domicile(pilote)
    controler_consommateurs(pilote, racine)
    etat = None
    chemin_etat = pilote / FICHIER_STATE_ENTONNOIR
    if chemin_etat.is_file():
        try:
            etat = json.loads(chemin_etat.read_text(encoding="utf-8"))
        except Exception:
            etat = None
    index_reel = list((etat or {}).get("auto_validees") or [])
    fonctions = None
    try:
        est_auto_validee, decision_enchainement, fonctions = charger_decision(pilote)
    except Exception as erreur:
        controler("import des decisions du pilote", False,
                  type(erreur).__name__ + " : " + str(erreur)[:80])
        est_auto_validee = decision_enchainement = None
    if est_auto_validee is not None:
        controler_fonctionnel(est_auto_validee, decision_enchainement, index_reel)
    controler_rappel_chaine(pilote, fonctions)
    controler_forcer(pilote, fonctions)
    controler_lot_visible(pilote, fonctions)
    controler_mesure_reelle(pilote, fonctions, index_reel)
    echecs = [nom for nom, ok, _ in RESULTATS if not ok]
    if echecs:
        print("")
        print("VERDICT KO : " + str(len(echecs)) + " echec(s) -- " + "; ".join(echecs))
        return 1
    print("")
    print("VERDICT OK : enchainement -- le verdict se resout par la provenance, la chaine ne")
    print("  s arrete plus APRES CHAQUE mission (elle s arrete sur une mission VRAIMENT non")
    print("  auto-validee, en la NOMMANT).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
