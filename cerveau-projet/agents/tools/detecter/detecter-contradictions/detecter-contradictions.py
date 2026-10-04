#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-contradictions.py
#
# Outil specialise d Argus (detecteur de contradictions) : croise les sources
# du cerveau-projet pour trouver et comparer les incoherences.
#
#   1. --cases  : audit des parcours JSON (cases orphelines, fins non
#                 joignables, boucles indirectes, references mortes) - base
#                 detecter-cablages-manquants
#   2. --regles : audit regles/protocoles : contradictions entre les fichiers
#                 regles-immuables/general/ (references cassees, doublons de
#                 regles exclusives)
#   3. --git    : lecture du depot git en LECTURE SEULE (git log --all) :
#                 evolutions vraies et fausses, fichiers modifies hors
#                 protocole, residus de versions
#   4. --coherence : coherence regle gravee <-> protocole associe : chaque
#                 section ### X (IMMUABLE) de regles-groupes-agents.md doit
#                 decrire le meme mecanisme que son protocole (mots
#                 c0/c0b/OUI/NON, flux OUI -> cible, reference croisee)
#   5. Rapport markdown classe par gravite (critique/majeur/mineur) avec
#      preuves (fichier + ligne + 2 sources)
#
# Usage :
#   python3 detecter-contradictions.py --tous
#   python3 detecter-contradictions.py --cases
#   python3 detecter-contradictions.py --regles
#   python3 detecter-contradictions.py --git
#   python3 detecter-contradictions.py --tous --rapport rapport.md --verbose
#   python3 detecter-contradictions.py --fichier <parcours.json>
#
# Options :
#   --tous              : lance les 4 audits (cases, regles, coherence, git)
#   --coherence         : audit regle gravee <-> protocole associe uniquement
#   --cases             : audit des parcours JSON uniquement
#   --regles            : audit des regles/protocoles uniquement
#   --git               : lecture git (lecture seule) uniquement
#   --fichier <chemin>  : auditer UN parcours JSON arbitraire (copie, preuve)
#   --rapport <fichier> : ecrit le rapport markdown classe par gravite
#   --verbose           : detail des verifications
#   --version
#
# Version : 0.1.3
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: argus
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (detecter-).
# =============================================================================
"""
detecter-contradictions.py
detecter-contradictions

Usage:
  detecter-contradictions.py [OPTIONS]
"""

import argparse
import glob
import io
import json
import os
import re
import subprocess
import sys
from datetime import datetime

VERSION = "0.1.3"
STATUT = "ebauche"

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
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def charger_parcours(chemin):
    """Charge un parcours JSON et retourne (data, nom, erreur)."""
    try:
        with io.open(chemin, encoding="utf-8", newline="") as fh:
            data = json.load(fh)
    except Exception as e:
        return None, os.path.basename(chemin), "JSON invalide : %s" % e
    nom = data.get("parcours", {}).get("nom", os.path.basename(chemin))
    return data, nom, None


# ---------------------------------------------------------------------------
# AUDIT 1 : CASES (parcours JSON)
# ---------------------------------------------------------------------------

def cases_atteignables(cases, depart):
    if not depart or depart not in cases:
        return set()
    atteintes = set()
    file = [depart]
    while file:
        cid = file.pop(0)
        if cid in atteintes:
            continue
        atteintes.add(cid)
        case = cases[cid]
        suivant = case.get("suivant")
        if suivant and suivant in cases:
            file.append(suivant)
        for b in case.get("branches", []):
            vers = b.get("vers")
            if vers and vers in cases:
                file.append(vers)
    return atteintes


def successeurs(cases, cid):
    c = cases.get(cid, {})
    res = []
    if c.get("suivant") and c["suivant"] in cases:
        res.append(c["suivant"])
    for b in c.get("branches", []):
        if b.get("vers") and b["vers"] in cases:
            res.append(b["vers"])
    return res


def trouver_cycles(cases, depart):
    cycles = []

    def dfs(noeud, pile, vu):
        if noeud not in cases:
            return
        if noeud in pile:
            idx = pile.index(noeud)
            cycle = pile[idx:]
            if len(set(cycle)) >= 2:
                sig = tuple(sorted(set(cycle)))
                if sig not in vu:
                    vu.add(sig)
                    cycles.append(cycle[:])
            return
        pile.append(noeud)
        for s in successeurs(cases, noeud):
            dfs(s, pile, vu)
        pile.pop()

    vu = set()
    if depart and depart in cases:
        dfs(depart, [], vu)
    return cycles


def cycle_a_sortie(cases, cycle):
    ensemble = set(cycle)
    for cid in ensemble:
        for s in successeurs(cases, cid):
            if s not in ensemble:
                return True
    return False


def auditer_parcours(chemin):
    """Audit d un parcours : retourne une liste de contradictions (gravite, type, message)."""
    data, _, err = charger_parcours(chemin)
    # Libelle = nom reel du fichier audite (evite la confusion si le champ
    # `nom` du JSON est celui d une copie) - limite 4 du test de comportement.
    nom = os.path.basename(chemin)
    resultats = []
    if err:
        resultats.append(("critique", "CHARGEMENT", "%s : %s" % (nom, err)))
        return resultats
    cases = data.get("cases", {})
    depart = data.get("parcours", {}).get("case_depart")

    if not depart:
        resultats.append(("critique", "CASE_DEPART", "%s : case_depart manquante" % nom))
    elif depart not in cases:
        resultats.append(("critique", "CASE_DEPART", "%s : case_depart '%s' inexistante" % (nom, depart)))

    atteignables = cases_atteignables(cases, depart)

    for cid, case in cases.items():
        if case.get("type") == "fin" and cid not in atteignables:
            resultats.append(("critique", "FIN_NON_JOIGNABLE",
                              "%s : fin '%s' non joignable depuis la case de depart" % (nom, cid)))
    for cid in sorted(cases):
        if cid not in atteignables:
            resultats.append(("majeur", "CAS_ORPHELINE",
                              "%s : case '%s' jamais atteignable depuis la case de depart" % (nom, cid)))
    for cycle in trouver_cycles(cases, depart):
        if not cycle_a_sortie(cases, cycle):
            resultats.append(("majeur", "BOUCLE_BLOQUANTE",
                              "%s : cycle SANS sortie : %s" % (nom, " -> ".join(cycle))))
    for cid, case in cases.items():
        if case.get("suivant") == cid:
            resultats.append(("majeur", "BOUCLE_BLOQUANTE",
                              "%s : case '%s' : suivant pointe vers elle-meme" % (nom, cid)))
    for cid, case in cases.items():
        suivant = case.get("suivant")
        if suivant and suivant not in cases:
            resultats.append(("majeur", "REF_MORTE",
                              "%s : case '%s' : suivant '%s' inexistant" % (nom, cid, suivant)))
        for b in case.get("branches", []):
            vers = b.get("vers")
            if vers and vers not in cases:
                resultats.append(("majeur", "REF_MORTE",
                                  "%s : case '%s' : branche '%s' -> '%s' inexistant" % (nom, cid, b.get("reponse", "?"), vers)))
    return resultats


def auditer_arbre_v2(chemin):
    """Audit d un arbre v2 (arbre-<agent>.json) : retourne une liste de
    contradictions (gravite, type, message). Le format v2 (migration
    v1->v2 2026-09-05) remplace les cases v1 par racine/branches ->
    themes -> fins centralisees : on verifie les references cassees."""
    resultats = []
    nom = os.path.basename(os.path.dirname(chemin))
    try:
        with io.open(chemin, encoding="utf-8") as fh:
            data = json.load(fh)
    except ValueError as e:
        return [("critique", "JSON_INVALIDE", "%s : %s" % (nom, e))]
    dossier = os.path.dirname(chemin)
    racine = data.get("racine") or {}
    # Branches de la racine -> fichiers theme existants
    for b in racine.get("branches", []) or []:
        vers = b.get("vers")
        if vers and not os.path.isfile(os.path.join(dossier, vers)):
            resultats.append(("majeur", "REF_MORTE",
                              "%s : branche '%s' -> theme '%s' inexistant"
                              % (nom, b.get("reponse", "?"), vers)))
        if vers and os.path.isfile(os.path.join(dossier, vers)):
            try:
                t = json.load(io.open(os.path.join(dossier, vers), encoding="utf-8"))
                if (t.get("identite") or {}).get("type") != "theme":
                    resultats.append(("majeur", "THEME_TYPE",
                                      "%s : %s identite.type != theme" % (nom, vers)))
            except ValueError:
                resultats.append(("majeur", "JSON_INVALIDE",
                                  "%s : theme '%s' JSON invalide" % (nom, vers)))
    # Fins centralisees
    fins_ref = (data.get("fins") or {}).get("fichier")
    if fins_ref and not os.path.isfile(os.path.join(dossier, fins_ref)):
        resultats.append(("majeur", "FINS_MANQUANTES",
                          "%s : fins.fichier '%s' inexistant" % (nom, fins_ref)))
    return resultats


def auditer_cases(racine, verbose=False):
    """Audit de tous les arbres v2 (les parcours v1 sont des vestiges retires)."""
    pattern = os.path.join(racine, "cerveau-projet", "agents", "*", "parcours", "arbre-*.json")
    chemins = sorted(glob.glob(pattern))
    resultats = []
    for chemin in chemins:
        resultats.extend(auditer_arbre_v2(chemin))
    if verbose:
        print(_couleur("  [AUDIT ARBRES V2] %d arbres scannes" % len(chemins), "bleu"))
    return resultats


# ---------------------------------------------------------------------------
# AUDIT 2 : REGLES / PROTOCOLES
# ---------------------------------------------------------------------------

def lister_regles(racine):
    """Liste les fichiers .md des regles-immuables/general/."""
    dossier = os.path.join(racine, "cerveau-projet", "agents", "regles-immuables", "general")
    fichiers = []
    if os.path.isdir(dossier):
        for f in sorted(os.listdir(dossier)):
            if f.endswith(".md"):
                fichiers.append(os.path.join(dossier, f))
    return fichiers


def auditer_regles(racine, verbose=False):
    """Audit des regles/protocoles : references cassees, doublons de titres,
    fichiers .001.XX.* hors convention."""
    resultats = []
    fichiers = lister_regles(racine)

    # 1. references cassees : liens markdown [texte](chemin) pointant vers un
    #    fichier inexistant (chemin relatif au fichier source)
    for chemin in fichiers:
        try:
            with io.open(chemin, encoding="utf-8", newline="") as fh:
                contenu = fh.read()
        except Exception:
            continue
        base = os.path.dirname(os.path.abspath(chemin))
        for m in re.finditer(r"\]\(([^)#]+?)(?:#[^)]*)?\)", contenu):
            cible = m.group(1)
            if cible.startswith("http") or cible.startswith("mailto"):
                continue
            cible_resolue = os.path.normpath(os.path.join(base, cible))
            if not os.path.exists(cible_resolue):
                ligne = contenu.count("\n", 0, m.start()) + 1
                resultats.append(("majeur", "REF_CASSEE",
                                  "%s:%d : lien '%s' -> '%s' inexistant" % (
                                      os.path.basename(chemin), ligne, cible, cible_resolue)))

    # 2. doublons de titres de sections (deux regles exclusives qui se contredisent)
    # Les titres GENERIQUES communs a tous les fichiers de regles (structure
    # du template de regle) ne sont PAS des contradictions : ils sont ignores.
    TITRES_GENERIQUES = set([
        "## Principe Fondamental",
        "## Pourquoi ?",
        "## Regles detaillees",
        "## Application",
        "## Validation",
        "## Liens",
        "## Navigation",
        "## Pieges courants",
        "## Lien avec les autres regles",
        "## Objectif",
        "## Portee",
        "## Contexte",
        "## Verdict",
        "## Conclusion",
        "## Exemples",
        "## Verification",
        "## Controle",
        "## Checklist",
        "## Synopse",
        "## Synthese",
    ])
    titres = {}
    for chemin in fichiers:
        try:
            with io.open(chemin, encoding="utf-8", newline="") as fh:
                lignes = fh.read().split("\n")
        except Exception:
            continue
        for i, ligne in enumerate(lignes, 1):
            if ligne.startswith("### ") or ligne.startswith("## "):
                titre = ligne.strip()
                if titre in TITRES_GENERIQUES:
                    continue
                if titre in titres:
                    resultats.append(("mineur", "TITRE_DOUBLON",
                                      "%s:%d : '%s' duplicate de %s" % (
                                          os.path.basename(chemin), i, titre, titres[titre])))
                else:
                    titres[titre] = "%s:%d" % (os.path.basename(chemin), i)

    if verbose:
        print(_couleur("  [AUDIT REGLES] %d fichiers regles scannes" % len(fichiers), "bleu"))
    return resultats


# ---------------------------------------------------------------------------
# AUDIT 2bis : REGLES CROISEES (contenu) -- v0.1.1
# Deux regles qui se contredisent sur le fond : memes marqueurs opposes
# (SEUL/JAMAIS/TOUJOURS/OBLIGATOIRE/INTERDIT) sur un contenu similaire.
# ---------------------------------------------------------------------------

def _normaliser(texte):
    """Normaliser une affirmation : minuscules, sans accents, sans ponctuation."""
    import unicodedata
    t = unicodedata.normalize("NFD", texte)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.lower()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def _marqueurs(texte_normalise):
    """Retourner (exclusif, permissif, negatif) pour une affirmation normalisee.

    - exclusif : SEUL / EST LE SEUL (monopole declare)
    - permissif : PEUT / AUTORISE / HABILITE / A LE DROIT (partage possible)
    - negatif : JAMAIS / INTERDIT / NE DOIT / N EST PAS / N A PAS
    Un marqueur exclusif (ex: "seul") est retire des permissifs pour eviter
    le double comptage.
    """
    t = texte_normalise
    exclusif = [m for m in ["seul", "est le seul"] if m in t]
    permissif = [m for m in ["peut", "autorise", "habilite", "a le droit",
                             "toujours", "obligatoire"] if m in t]
    negatif = [m for m in ["jamais", "interdit", "ne doit", "n est pas",
                           "n a pas", "ne peut"] if m in t]
    return exclusif, permissif, negatif


def _similarite(a, b):
    """Ratio de tokens communs entre deux affirmations normalisees."""
    ta = set(a.split())
    tb = set(b.split())
    if not ta or not tb:
        return 0.0
    communs = ta & tb
    return len(communs) / float(min(len(ta), len(tb)))


def _extraire_affirmations(chemin):
    """Extraire les affirmations reglementaires (lignes avec marqueurs)."""
    affirmations = []
    try:
        with io.open(chemin, encoding="utf-8", newline="") as fh:
            lignes = fh.read().split("\n")
    except Exception:
        return affirmations
    for i, ligne in enumerate(lignes, 1):
        brute = ligne.strip()
        # Anti-bruit : sauter les tableaux markdown (lignes de referencement) et
        # les liens [texte](chemin) (references de fichiers, pas des affirmations)
        if brute.startswith("|") or "](" in brute:
            continue
        norm = _normaliser(ligne)
        if len(norm) < 15:
            continue
        excl, perm, neg = _marqueurs(norm)
        if not (excl or perm or neg):
            continue
        # Anti-bruit : une ligne MIXTE (permissif ET negatif, ou exclusif ET
        # negatif) est une affirmation nuancee, pas une regle pure : on la saute.
        if (perm and neg) or (excl and neg):
            continue
        affirmations.append((os.path.basename(chemin), i, norm, excl, perm, neg))
    return affirmations


def _detecter_conflits(affirmations):
    """Croiser les affirmations : contradictions (exclusif/permissif/negatif
    opposes sur un contenu similaire) + doublons de formulation."""
    resultats = []
    n = len(affirmations)
    for i in range(n):
        fi, li, ti, exi, peri, negi = affirmations[i]
        for j in range(i + 1, n):
            fj, lj, tj, exj, perj, negj = affirmations[j]
            # Contradiction UNIQUEMENT entre 2 sources DIFFERENTES (regle
            # DOUBLE SOURCE d Argus : une redite dans le meme fichier n est
            # pas une contradiction, c est la meme source qui se repete).
            if fi == fj:
                continue
            # Exiger au moins 4 tokens communs (les phrases trop courtes
            # matchent tout : anti-bruit)
            if len(set(ti.split()) & set(tj.split())) < 4:
                continue
            sim = _similarite(ti, tj)
            if sim < 0.55:
                continue
            # Combinaisons contradictoires sur le meme sujet :
            #  - exclusif vs permissif : SEUL X fait Y vs X PEUT faire Y
            #  - exclusif vs negatif   : SEUL X fait Y vs JAMAIS X ne fait Y
            #  - permissif vs negatif  : X PEUT faire Y vs X NE DOIT PAS faire Y
            # Seuil durci (0.7) pour exclusif-vs-negatif : le SUJET doit etre
            # quasi identique (anti-faux-positif : SEUL janus vs JAMAIS morpheus
            # sont deux affirmations compatibles, pas une contradiction).
            conflit = ((exi and (perj or negj)) or (exj and (peri or negi)) or
                       ((peri and negj) or (perj and negi)))
            if conflit and ((exi and negj) or (exj and negi)) and sim < 0.7:
                continue
            if conflit:
                if exi and (perj or negj):
                    label = "exclusif contredit par %s" % ("permissif" if perj else "negatif")
                elif exj and (peri or negi):
                    label = "exclusif contredit par %s" % ("permissif" if peri else "negatif")
                else:
                    label = "permissif contredit par negatif"
                resultats.append(("majeur", "CONTRADICTION_REGLE",
                                  "%s:%d vs %s:%d : '%s' [%s]" % (
                                      fi, li, fj, lj, ti[:100], label)))
            # Doublon : meme formulation quasi identique dans 2 fichiers
            elif sim >= 0.85 and fi != fj:
                resultats.append(("mineur", "REGLE_DOUBLON",
                                  "%s:%d duplique dans %s:%d : '%s'" % (
                                      fi, li, fj, lj, ti[:100])))
    return resultats


def croiser_regles(racine, verbose=False):
    """Audit du CONTENU des regles : deux sources qui se contredisent."""
    resultats = []
    affirmations = []
    for chemin in lister_regles(racine):
        affirmations.extend(_extraire_affirmations(chemin))
    resultats.extend(_detecter_conflits(affirmations))
    if verbose:
        print(_couleur("  [AUDIT REGLES CROISEES] %d affirmations reglementaires comparees" % len(affirmations), "bleu"))
    return resultats


# ---------------------------------------------------------------------------
# AUDIT 2ter : COHERENCE REGLE GRAVEE <-> PROTOCOLE ASSOCIE -- v0.1.2
# Chaque section ### X (IMMUABLE) de regles-groupes-agents.md decrit un
# mecanisme (branches OUI/INCERTAIN/NON, ordre corrections-puis-fiche,
# cibles c0/c0b/c0c...). Le protocole associe (protocole-activation, etc.)
# doit decrire le MEME mecanisme : si la regle omet une etape du protocole
# (ou la contredit), c est une contradiction REGLE_PROTOCOLE.
# ---------------------------------------------------------------------------

# Table de correspondance : nom de section IMMUABLE -> protocole(s) associe(s)
# (fichier .md dans regles-immuables/general/, sans le suffixe .001.XX.*)
REGLE_PROTOCOLE = {
    "RELIRE SA FICHE AVANT MISSION": "protocole-activation",
    "RELEVE MEME ROUND": "protocole-activation",
    "SEUL HYGIE SUPPRIME": "protocole-nettoyage",
    "SEUL JANUS LANCE LA NON-REGRESSION": "protocole-tests",
    "SEUL MORPHEUS ECRIT ET EXECUTE LES TESTS": "protocole-tests",
    "SEUL CLIO MET A JOUR LE README": "protocole-verification-coherence",
    "SEUL BUFFY CORRIGE LES FICHIERS DES AGENTS": "protocole-controle-buffy",
    "LE MODELE DE CONFIANCE": "protocole-controle-statuts",
}

# Mots-mecanisme OBLIGATOIRES PAR REGLE : seules les regles de type
# MECANISME (relecture, releve) portent des mots de parcours (c0/c0b/OUI/
# INCERTAIN/NON). Les regles d EXCLUSIVITE (SEUL X) n ont pas de mecanisme
# de parcours : pour elles on ne verifie que la reference au protocole et
# l absence de contradiction de flux.
MOTS_PAR_REGLE = {
    "RELIRE SA FICHE AVANT MISSION": ["c0", "c0b", "OUI", "INCERTAIN", "NON"],
    "RELEVE MEME ROUND": ["activation", "execution", "round"],
}

# Regles pour lesquelles le protocole decrit un flux OUI -> cible : la regle
# ne doit pas contredire cette cible (et ne doit pas omettre c0c si le
# protocole l inclut dans le flux de relecture).
FLUX_CROISES = {
    "RELIRE SA FICHE AVANT MISSION": True,
}


def _texte_section_immuable(contenu_regles, titre):
    """Extraire le texte d une section ### <titre> (IMMUABLE)."""
    m = re.search(r"### %s \(IMMUABLE\)(.*?)(?=### |## |\Z)" % re.escape(titre),
                  contenu_regles, re.S)
    return m.group(1) if m else ""


def _texte_protocole(racine, nom_protocole):
    """Charger le texte du protocole associe (premiere version .md trouvee)."""
    dossier = os.path.join(racine, "cerveau-projet", "agents", "regles-immuables", "general")
    cible = os.path.join(dossier, nom_protocole)
    if not os.path.isdir(cible):
        return ""
    for f in sorted(os.listdir(cible)):
        if f.endswith(".md"):
            try:
                with io.open(os.path.join(cible, f), encoding="utf-8", newline="") as fh:
                    return fh.read()
            except Exception:
                continue
    return ""


def auditer_coherence_regles(racine, verbose=False):
    """Audit de coherence regle gravee <-> protocole associe.

    Pour chaque section ### X (IMMUABLE) de regles-groupes-agents.md avec un
    protocole associe : verifier que la regle mentionne les mots-mecanisme
    essentiels (c0/c0b/OUI/NON) et que les etapes du protocole (ex: c0c
    contexte, INCERTAIN) ne sont pas contredites par la regle. La regle peut
    legitiment omettre un detail (c0c) si elle ne le contredit pas -- mais
    une omission qui change le FLUX (ex: OUI -> mission au lieu de
    OUI -> c0c -> mission) est signalee en mineur (regle plus courte que le
    protocole) et un vrai conflit (JAMAIS vs TOUJOURS) en majeur.
    """
    resultats = []
    chemin_regles = os.path.join(racine, "cerveau-projet", "agents",
                                 "regles-immuables", "general",
                                 "regles-groupes-agents.md")
    try:
        with io.open(chemin_regles, encoding="utf-8", newline="") as fh:
            contenu_regles = fh.read()
    except Exception as e:
        resultats.append(("majeur", "REGLE_PROTOCOLE",
                          "regles-groupes-agents.md illisible : %s" % e))
        return resultats

    for titre, nom_protocole in REGLE_PROTOCOLE.items():
        if not nom_protocole:
            continue
        texte_regle = _texte_section_immuable(contenu_regles, titre)
        if not texte_regle:
            resultats.append(("majeur", "REGLE_ABSENTE",
                              "section IMMUABLE '%s' absente de regles-groupes-agents.md" % titre))
            continue
        texte_proto = _texte_protocole(racine, nom_protocole)
        if not texte_proto:
            resultats.append(("mineur", "PROTOCOLE_ABSENT",
                              "protocole %s associe a la regle '%s' introuvable" % (nom_protocole, titre)))
            continue

        # 1. Reference croisee : la regle doit citer son protocole (mineur)
        if nom_protocole.replace("-", " ") not in texte_regle and \
           nom_protocole not in texte_regle:
            resultats.append(("mineur", "REGLE_SANS_REFERENCE",
                              "regle '%s' ne reference pas son protocole %s" % (titre, nom_protocole)))

        # 2. Mots-mecanisme obligatoires (uniquement pour les regles de type
        #    MECANISME : la table MOTS_PAR_REGLE liste qui doit porter quoi)
        mots_obligatoires = MOTS_PAR_REGLE.get(titre, [])
        for mot in mots_obligatoires:
            if mot not in texte_regle:
                resultats.append(("majeur", "REGLE_PROTOCOLE",
                                  "regle '%s' : mot-mecanisme obligatoire '%s' absent (present dans le protocole %s)" % (
                                      titre, mot, nom_protocole)))

        # 3. Cible c0c : uniquement pour les regles dont le protocole decrit
        #    le flux de relecture complet (RELIRE SA FICHE AVANT MISSION).
        #    Si le protocole dit OUI -> c0c -> mission et que la regle dit
        #    OUI -> mission, la regle omet une etape obligatoire du flux.
        if FLUX_CROISES.get(titre) and "c0c" in texte_proto and "c0c" not in texte_regle:
            resultats.append(("majeur", "REGLE_PROTOCOLE",
                              "regle '%s' omet l etape c0c decrite par le protocole %s (flux tronque : OUI doit passer par c0c avant la mission)" % (
                                  titre, nom_protocole)))

        # 4. Contradiction de flux : OUI -> X dans la regle vs OUI -> Y dans
        #    le protocole (le flux apres OUI differe). Verifie uniquement si
        #    le protocole exprime un flux OUI explicite.
        if FLUX_CROISES.get(titre):
            flux_regle = re.findall(r"OUI[^;\n]*?->\s*(\w+)", texte_regle)
            flux_proto = re.findall(r"OUI[^;\n]*?->\s*(\w+)", texte_proto)
            if flux_regle and flux_proto and flux_regle[0] != flux_proto[0]:
                resultats.append(("majeur", "REGLE_PROTOCOLE",
                                  "regle '%s' : flux OUI -> %s contredit le protocole %s (OUI -> %s)" % (
                                      titre, flux_regle[0], nom_protocole, flux_proto[0])))

    if verbose:
        print(_couleur("  [AUDIT COHERENCE REGLE/PROTOCOLE] %d regles IMMUABLE croisees avec leur protocole" %
                       len([t for t in REGLE_PROTOCOLE if REGLE_PROTOCOLE[t]]), "bleu"))
    return resultats


# ---------------------------------------------------------------------------
# AUDIT 3 : GIT (lecture seule)
# ---------------------------------------------------------------------------

def auditer_git(racine, verbose=False):
    """Lecture du depot git en LECTURE SEULE + croisement avec le working tree."""
    resultats = []
    # 1. git log --all : entrees du passe (evolutions vraies et fausses)
    try:
        p = subprocess.run(
            ["git", "log", "--all", "--oneline", "-n", "200"],
            cwd=racine, capture_output=True, text=True, timeout=30)
    except Exception as e:
        resultats.append(("mineur", "GIT_INDISPONIBLE", "git log --all : %s" % e))
        return resultats
    if p.returncode != 0:
        resultats.append(("mineur", "GIT_INDISPONIBLE", "git log --all a echoue"))
        return resultats
    entrees = [l for l in p.stdout.split("\n") if l.strip()]
    if verbose:
        print(_couleur("  [AUDIT GIT] %d entrees git log --all (lecture seule)" % len(entrees), "bleu"))
    # Signaler les fichiers temporaires commites (residus de versions passes)
    for ligne in entrees:
        if re.search(r"\.tmp-|\.zz-|tmp-[a-z]+|rapport-impact|erreur", ligne, re.I):
            resultats.append(("mineur", "GIT_RESIDU_TEMP",
                              "commit avec residu temporaire : %s" % ligne[:90]))

    # 2. Croisement avec le working tree : residus PRESENTS a la racine
    #    (dossiers tmp-*, scripts .tmp-/.zz-, rapports egare s, fichiers de version)
    motifs_residus = re.compile(r"^(\.tmp-|\.zz-|tmp-[a-z]+$|erreur$|ERREUR$|adapter$|\d+\.\d+\.\d+$)")
    try:
        entrees_racine = sorted(os.listdir(racine))
    except Exception:
        entrees_racine = []
    for nom in entrees_racine:
        chemin = os.path.join(racine, nom)
        if motifs_residus.match(nom):
            typ = "dossier temporaire" if os.path.isdir(chemin) else "fichier residu"
            resultats.append(("majeur", "GIT_RESIDU_ACTUEL",
                              "residu present a la racine : %s (%s)" % (nom, typ)))
    return resultats


# ---------------------------------------------------------------------------
# RAPPORT
# ---------------------------------------------------------------------------

def ecrire_rapport(chemin_rapport, resultats, audits_lances):
    gravite_ordre = {"critique": 0, "majeur": 1, "mineur": 2}
    tri = sorted(resultats, key=lambda r: gravite_ordre.get(r[0], 3))
    with io.open(chemin_rapport, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Rapport : contradictions detectees (Argus)\n\n")
        fh.write("Date : %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        fh.write("Audits lances : %s\n" % ", ".join(audits_lances))
        fh.write("Contradictions : %d (critique %d, majeur %d, mineur %d)\n\n" % (
            len(resultats),
            sum(1 for r in resultats if r[0] == "critique"),
            sum(1 for r in resultats if r[0] == "majeur"),
            sum(1 for r in resultats if r[0] == "mineur")))
        if not resultats:
            fh.write("Aucune contradiction detectee.\n")
        for gravite, typ, msg in tri:
            fh.write("- **[%s]** [%s] %s\n" % (gravite.upper(), typ, msg))
    print(_couleur("[OK] Rapport ecrit : %s" % chemin_rapport, "vert"))


def main():
    parser = argparse.ArgumentParser(
        description="Croise les sources du cerveau-projet pour detecter les contradictions (cases, regles, protocoles, git)")
    parser.add_argument("--tous", action="store_true", help="Lance les 3 audits (arbres v2, regles, git)")
    parser.add_argument("--cases", action="store_true", help="Audit des arbres v2 uniquement (les parcours v1 sont retires)")
    parser.add_argument("--regles", action="store_true", help="Audit des regles/protocoles uniquement")
    parser.add_argument("--coherence", action="store_true", help="Audit de coherence regle gravee <-> protocole associe (IMMUABLE)")
    parser.add_argument("--git", action="store_true", help="Lecture git (lecture seule) uniquement")
    parser.add_argument("--fichier", type=str, default="", help="Auditer UN arbre v2 arbitraire (copie, preuve negative)")
    parser.add_argument("--rapport", type=str, default="", help="Chemin du rapport markdown (optionnel)")
    parser.add_argument("--verbose", action="store_true", help="Detail des verifications")
    parser.add_argument("--version", action="version",
                        version="detecter-contradictions v%s" % VERSION)
    parser.add_argument("--aide", action="help",
                        help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    if not (args.tous or args.cases or args.regles or args.git or args.fichier or args.coherence):
        parser.print_help()
        return 2

    racine = racine_projet()
    resultats = []
    audits_lances = []
    if args.fichier:
        audits_lances.append("fichier:%s" % os.path.basename(args.fichier))
        resultats.extend(auditer_arbre_v2(args.fichier))
    elif args.tous or args.cases:
        audits_lances.append("cases")
        resultats.extend(auditer_cases(racine, args.verbose))
    if args.tous or args.regles:
        audits_lances.append("regles")
        resultats.extend(auditer_regles(racine, args.verbose))
        resultats.extend(croiser_regles(racine, args.verbose))
    if args.tous or args.coherence:
        audits_lances.append("coherence-regle-protocole")
        resultats.extend(auditer_coherence_regles(racine, args.verbose))
    if args.tous or args.git:
        audits_lances.append("git")
        resultats.extend(auditer_git(racine, args.verbose))

    print(_couleur("=== Detecter les contradictions (Argus) ===", "bleu"))
    print("  Audits : %s" % ", ".join(audits_lances))
    print("")
    gravite_ordre = {"critique": 0, "majeur": 1, "mineur": 2}
    tri = sorted(resultats, key=lambda r: gravite_ordre.get(r[0], 3))
    for gravite, typ, msg in tri:
        nom_couleur = {"critique": "rouge", "majeur": "jaune", "mineur": "neutre"}.get(gravite, "neutre")
        print("  [%s] [%s] %s" % (_couleur(gravite.upper(), nom_couleur), typ, msg))
    if not resultats:
        print(_couleur("  Aucune contradiction detectee", "vert"))

    total = len(resultats)
    print("")
    if total == 0:
        verdict = "PROPRE"
        print(_couleur("  Verdict : %s (0 contradiction)" % verdict, "vert"))
    else:
        verdict = "%d CONTRADICTION(S) DETECTEE(S)" % total
        print(_couleur("  Verdict : %s" % verdict, "rouge"))

    if args.rapport:
        ecrire_rapport(args.rapport, resultats, audits_lances)

    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
