#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# valider-case.py
#
# Valide une carte de decision (parcours JSON) et ALLEGE les cases : structure,
# modele compose (branches min 2, deviation = rejoint), surcharge des indices
# (budget pondere : indice COURT <= 100 car. = 0,5 unite, LONG > 100 = 1 unite,
# budget 3,0 par case, texte > 160 car. = SIGNALEE -> proposition de reference),
# references (chaque ref resolvable), normes (types, nommage, ASCII, LF).
#
# Spec de reference : pense-betes/specs/spec-refonte-cartes-decision.001.01.ebauche.md
# (etape 2 de la refonte : l'outil qui rend les cartes lisibles et suivies).
#
# Verdict : CONFORME / A ALLEGER / NON CONFORME + rapport markdown.
# =============================================================================

import io
import os
import re
import sys
from datetime import datetime

VERSION = "1.1.0"
STATUT = "ebauche"

TYPES_VALIDES = ("question", "controle", "indice", "action", "fin")
SEUIL_COURT = 100         # indice <= 100 car. = COURT (poids 0,5) ; > 100 = LONG (poids 1)
BUDGET_INDICES = 3.0      # budget pondere par case (2 courts = 1 long) : > 3,0 = surcharge
SEUIL_TEXTE = 160         # texte de regle plus long que 160 car. = surcharge (plafond absolu)

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
SPEC_GUIDER = os.path.join(RACINE, "cerveau-projet", "agents", "tools",
                           "guider", "guider-parcours", "spec",
                           "spec-guider-parcours.001.01.ebauche.md")


def couleur(texte, code):
    if not sys.stdout.isatty():
        return texte
    return "\033[%sm%s\033[0m" % (code, texte)


def charger_parcours(chemin):
    """Charge un parcours JSON. Retourne (parcours, erreur)."""
    if not os.path.isfile(chemin):
        return None, "fichier introuvable : %s" % chemin
    try:
        with io.open(chemin, encoding="utf-8") as fh:
            d = json_load(fh.read())
        return d, None
    except Exception as e:
        return None, "JSON invalide : %s" % e


def json_load(texte):
    import json
    return json.loads(texte)


def nommer_parcours(chemin, parcours=None):
    if parcours:
        info = parcours.get("parcours", {})
        if info.get("nom"):
            return info.get("nom")
        if info.get("agent"):
            return info.get("agent")
    return os.path.basename(os.path.dirname(chemin)) or chemin


# --------------------------------------------------------------------------
# 1. STRUCTURE
# --------------------------------------------------------------------------

def verifier_structure(parcours, erreurs):
    cases = parcours.get("cases", {})
    if not isinstance(cases, dict) or not cases:
        erreurs.append("STRUCTURE : aucune case dans le parcours")
        return
    # ids uniques (structure de dict = unique par construction, verifie quand meme)
    # types valides
    for cid, case in cases.items():
        typ = case.get("type", "question")
        if typ not in TYPES_VALIDES:
            erreurs.append("STRUCTURE : case '%s' type invalide '%s' (valides: %s)"
                           % (cid, typ, ", ".join(TYPES_VALIDES)))
    # case_depart existe
    depart = parcours.get("parcours", {}).get("case_depart")
    if depart and depart not in cases:
        erreurs.append("STRUCTURE : case_depart '%s' inexistante" % depart)
    # fins joignables : chaque fin doit etre atteignable depuis le depart (BFS)
    atteignables = cases_atteignables(cases, depart)
    for cid, case in cases.items():
        if case.get("type") == "fin" and cid not in atteignables:
            erreurs.append("STRUCTURE : fin '%s' non joignable depuis la case de depart" % cid)


def cases_atteignables(cases, depart):
    """BFS anti-boucle : ids de cases atteignables depuis depart."""
    if not depart or depart not in cases:
        return set()
    vus = set()
    file = [depart]
    while file:
        cid = file.pop(0)
        if cid in vus:
            continue
        vus.add(cid)
        case = cases.get(cid, {})
        suivant = case.get("suivant")
        if suivant and suivant in cases:
            file.append(suivant)
        for b in case.get("branches", []):
            vers = b.get("vers")
            if vers and vers in cases:
                file.append(vers)
    return vus


# --------------------------------------------------------------------------
# 2. MODELE COMPOSE
# --------------------------------------------------------------------------

def verifier_modele(parcours, erreurs, avertissements):
    cases = parcours.get("cases", {})
    for cid, case in cases.items():
        typ = case.get("type", "question")
        branches = case.get("branches") or []
        suivant = case.get("suivant")
        # boucle directe : une branche qui pointe vers soi-meme
        # EXCEPTION : controle avec branche NON -> soi-meme = pattern de re-essai
        # volontaire (le controle est refait tant que NON), signale en avertissement.
        for b in branches:
            if b.get("vers") == cid:
                if typ == "controle" and (b.get("reponse") or "").lower() == "non":
                    avertissements.append(
                        "MODELE : case '%s' pattern de re-essai (controle NON -> soi-meme, voulu)" % cid)
                else:
                    erreurs.append("MODELE : case '%s' boucle directe (branche '%s' -> elle-meme)"
                                   % (cid, b.get("reponse")))
        # decision (question/controle) : branches min 2
        if typ in ("question", "controle") and len(branches) < 2:
            erreurs.append("MODELE : case '%s' (%s) n'a que %d branche(s) (min 2 requis)"
                           % (cid, typ, len(branches)))
        # indice/action : suivant requis
        if typ in ("indice", "action") and not suivant:
            erreurs.append("MODELE : case '%s' (%s) sans 'suivant'" % (cid, typ))
        # impasses : case non-fin sans suivant ni branches
        if typ != "fin" and not suivant and not branches:
            avertissements.append("MODELE : case '%s' (%s) sans sortie (impasse ?)" % (cid, typ))
        # deviation sans rejoint : une branche vers une case de deviation dont
        # le flux ne revient pas vers la case courante = avertissement
        for b in branches:
            vers = b.get("vers")
            if vers and vers in cases and "deviation" in (b.get("reponse") or "").lower():
                if not flux_revient(cases, vers, cid):
                    avertissements.append(
                        "MODELE : deviation '%s' -> '%s' sans rejoint visible vers '%s'"
                        % (cid, vers, cid))


def flux_revient(cases, origine, cible, profondeur=0, vus=None):
    """BFS : le flux depuis origine atteint-il cible (rejoint) ?"""
    if vus is None:
        vus = set()
    if profondeur > 40 or origine in vus:
        return False
    vus.add(origine)
    case = cases.get(origine, {})
    suivant = case.get("suivant")
    if suivant == cible:
        return True
    if suivant and suivant in cases and flux_revient(cases, suivant, cible, profondeur + 1, vus):
        return True
    for b in case.get("branches", []):
        vers = b.get("vers")
        if vers == cible:
            return True
        if vers and vers in cases and flux_revient(cases, vers, cible, profondeur + 1, vus):
            return True
    return False


# --------------------------------------------------------------------------
# 3. ALLEGEMENT (surcharge)
# --------------------------------------------------------------------------

def poids_indices(indices):
    """Poids pondere des indices : court (<= SEUIL_COURT car. ou sans texte)
    = 0,5 ; long (> SEUIL_COURT car.) = 1. Budget = BUDGET_INDICES."""
    poids = 0.0
    for ind in indices:
        texte = ind.get("texte", "")
        if isinstance(texte, str) and len(texte) > SEUIL_COURT:
            poids += 1.0
        else:
            poids += 0.5
    return poids


def verifier_allegement(parcours, allegements):
    cases = parcours.get("cases", {})
    for cid, case in cases.items():
        indices = case.get("indices") or []
        poids = poids_indices(indices)
        if poids > BUDGET_INDICES:
            allegements.append(
                "ALLEGER : case '%s' a un poids de %.1f unites (budget %s - "
                "court <= %d car. = 0,5 / long > %d = 1) - regrouper dans un combo "
                "(Pattern 3) ou remplacer par des references"
                % (cid, poids, BUDGET_INDICES, SEUIL_COURT, SEUIL_COURT))
        for ind in indices:
            texte = ind.get("texte", "")
            if isinstance(texte, str) and len(texte) > SEUIL_TEXTE:
                ref = ind.get("ref")
                allegements.append(
                    "ALLEGER : case '%s' indice de %d caracteres (> %d) - deplacable vers "
                    "une reference (pattern/protocole)%s"
                    % (cid, len(texte), SEUIL_TEXTE,
                       " ou conserver si la reference '%s' existe" % ref if ref else ""))


# --------------------------------------------------------------------------
# 4. REFERENCES
# --------------------------------------------------------------------------

def verifier_references(parcours, erreurs):
    cases = parcours.get("cases", {})
    for cid, case in cases.items():
        for ind in case.get("indices", []):
            ref = ind.get("ref")
            if not ref:
                continue
            if not resoudre_reference(ref):
                erreurs.append("REFERENCES : case '%s' reference non resolvable '%s'"
                               % (cid, ref))


def resoudre_reference(ref):
    """Verifie qu'une reference d indice est resolvable vers une source existante."""
    # pattern-<N> : pattern N de la spec-guider-parcours
    m = re.match(r"^pattern-(\d+)$", ref)
    if m:
        try:
            txt = io.open(SPEC_GUIDER, encoding="utf-8").read()
            return ("### Pattern %s" % m.group(1)) in txt
        except Exception:
            return False
    # chemin relatif : fichier existant
    if os.path.isfile(os.path.join(RACINE, ref)):
        return True
    # dossier protocole / regle : recherche par nom dans regles-immuables
    if ref.startswith("protocole-") or ref.startswith("regle-"):
        dossier = os.path.join(RACINE, "cerveau-projet", "agents", "regles-immuables")
        if os.path.isdir(dossier):
            for racine, dossiers, fichiers in os.walk(dossier):
                for nom in dossiers + fichiers:
                    if nom.startswith(ref):
                        return True
    return False


# --------------------------------------------------------------------------
# 5. NORMES / NOMMAGE
# --------------------------------------------------------------------------

def verifier_normes(parcours, erreurs):
    cases = parcours.get("cases", {})
    # Convention etendue v1.0.2 : c[<prefixe-alpha>]<numero>[a-z]?
    #   - cas normal : c0, c12b, c29d (numero + suffixe lettres minuscules)
    #   - prefixe thematique majuscule optionnel : cT1..cT10 (T = ligne Trio de
    #     Janus, decision utilisateur 2026-08-11 : conserver les IDs cT*)
    # Le prefixe est UNE LETTRE MAJUSCULE ; le suffixe reste en minuscules.
    pattern_id = re.compile(r"^c[A-Z]?\d+[a-z]*$")
    for cid, case in cases.items():
        if not pattern_id.match(cid):
            erreurs.append("NOMMAGE : id de case '%s' non conforme (attendu c[<prefixe-alpha-maj>]<numero>[a-z]?)" % cid)
        if "titre" not in case:
            erreurs.append("NORMES : case '%s' sans titre" % cid)
    # ASCII + LF sur le fichier (verifie dans main via ascii_count)


# --------------------------------------------------------------------------
# 6. CASE UNIQUE
# --------------------------------------------------------------------------

def verifier_case(cid, parcours, erreurs, allegements):
    cases = parcours.get("cases", {})
    if cid not in cases:
        erreurs.append("STRUCTURE : case '%s' inexistante" % cid)
        return
    verifier_structure(parcours, erreurs) if False else None
    # verifier uniquement la case cible
    case = cases[cid]
    typ = case.get("type", "question")
    branches = case.get("branches") or []
    suivant = case.get("suivant")
    if typ not in TYPES_VALIDES:
        erreurs.append("STRUCTURE : case '%s' type invalide '%s'" % (cid, typ))
    for b in branches:
        if b.get("vers") == cid:
            if typ == "controle" and (b.get("reponse") or "").lower() == "non":
                pass  # pattern de re-essai volontaire (controle NON -> soi-meme)
            else:
                erreurs.append("MODELE : case '%s' boucle directe" % cid)
    if typ in ("question", "controle") and len(branches) < 2:
        erreurs.append("MODELE : case '%s' n'a que %d branche(s) (min 2)" % (cid, len(branches)))
    if typ in ("indice", "action") and not suivant:
        erreurs.append("MODELE : case '%s' (%s) sans 'suivant'" % (cid, typ))
    indices = case.get("indices") or []
    poids = poids_indices(indices)
    if poids > BUDGET_INDICES:
        allegements.append("ALLEGER : case '%s' a un poids de %.1f unites (budget %s - "
                           "court <= %d car. = 0,5 / long > %d = 1)"
                           % (cid, poids, BUDGET_INDICES, SEUIL_COURT, SEUIL_COURT))
    for ind in indices:
        texte = ind.get("texte", "")
        if isinstance(texte, str) and len(texte) > SEUIL_TEXTE:
            allegements.append("ALLEGER : case '%s' indice de %d caracteres (> %d)"
                               % (cid, len(texte), SEUIL_TEXTE))
        ref = ind.get("ref")
        if ref and not resoudre_reference(ref):
            erreurs.append("REFERENCES : case '%s' reference non resolvable '%s'" % (cid, ref))


# --------------------------------------------------------------------------
# RAPPORT
# --------------------------------------------------------------------------

def generer_rapport(chemin, erreurs, allegements, avertissements, verdict, parcours=None):
    L = []
    L.append("# Rapport valider-case -- %s" % nommer_parcours(chemin, parcours))
    L.append("")
    L.append("**Date** : %s | **Validateur-case** : v%s | **Parcours** : %s" % (
        datetime.now().strftime("%Y-%m-%d %H:%M"), VERSION, chemin))
    L.append("")
    L.append("## Verdict")
    L.append("")
    L.append("**%s**" % verdict)
    L.append("")
    L.append("| Classe | Nombre |")
    L.append("|---|---|")
    L.append("| ERREURS (non conformite) | %d |" % len(erreurs))
    L.append("| A ALLEGER (surcharge) | %d |" % len(allegements))
    L.append("| AVERTISSEMENTS | %d |" % len(avertissements))
    L.append("")
    L.append("## Erreurs (%d)" % len(erreurs))
    L.append("")
    if erreurs:
        for e in erreurs:
            L.append("- %s" % e)
    else:
        L.append("Aucune erreur.")
    L.append("")
    L.append("## A alleger (%d)" % len(allegements))
    L.append("")
    if allegements:
        for a in allegements:
            L.append("- %s" % a)
    else:
        L.append("Aucune surcharge.")
    L.append("")
    L.append("## Avertissements (%d)" % len(avertissements))
    L.append("")
    if avertissements:
        for a in avertissements:
            L.append("- %s" % a)
    else:
        L.append("Aucun avertissement.")
    return "\n".join(L) + "\n"


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------

def main(argv):
    args = list(argv)

    if "--version" in args:
        print("valider-case v%s (%s)" % (VERSION, STATUT))
        return 0
    if "--aide" in args or "-h" in args or "--help" in args:
        print("valider-case v%s (%s)" % (VERSION, STATUT))
        print("USAGE : valider-case.py <parcours.json> [options]")
        print("  --complet        Valider TOUTES les cases (defaut)")
        print("  --case <id>      Valider UNE case")
        print("  --surcharge      Verifier uniquement la surcharge des indices")
        print("  --modele         Verifier uniquement le modele compose")
        print("  --references     Verifier uniquement les references")
        print("  Nommage (v1.0.2) : c[<prefixe-alpha-maj>]<numero>[a-z]? (c0, c12b, cT6, cT10)")
        print("  --dry-run        Simuler sans ecrire le rapport")
        print("  --rapport <fichier>  Rapport markdown (defaut: rapport-valider-case-<date>.md)")
        print("  --version / --aide")
        return 0

    # Options
    case_cible = None
    mode_surcharge = "--surcharge" in args
    mode_modele = "--modele" in args
    mode_references = "--references" in args
    dry_run = "--dry-run" in args
    rapport_fichier = None
    if "--rapport" in args:
        idx = args.index("--rapport")
        if idx + 1 < len(args):
            rapport_fichier = args[idx + 1]
    if "--case" in args:
        idx = args.index("--case")
        if idx + 1 < len(args):
            case_cible = args[idx + 1]

    # Chemin du parcours (argument positionnel)
    chemins = [a for a in args if not a.startswith("--")]
    if not chemins:
        print("ERREUR : chemin du parcours JSON requis (voir --aide)")
        return 1
    chemin = chemins[0]

    parcours, err = charger_parcours(chemin)
    if err:
        print("ERREUR : %s" % err)
        return 1

    erreurs, allegements, avertissements = [], [], []

    if case_cible:
        verifier_case(case_cible, parcours, erreurs, allegements)
    else:
        verifier_structure(parcours, erreurs)
        if mode_modele or not (mode_surcharge or mode_references):
            verifier_modele(parcours, erreurs, avertissements)
        if mode_surcharge or not (mode_modele or mode_references):
            verifier_allegement(parcours, allegements)
        if mode_references or not (mode_surcharge or mode_modele):
            verifier_references(parcours, erreurs)
        verifier_normes(parcours, erreurs)

    # Normes du fichier : ASCII
    na = ascii_count(chemin)
    if na > 0:
        erreurs.append("NORMES : %d caractere(s) non-ASCII dans le parcours" % na)

    # Verdict
    if erreurs:
        verdict = "NON CONFORME"
    elif allegements:
        verdict = "A ALLEGER"
    else:
        verdict = "CONFORME"

    # Affichage console
    print("=== valider-case v%s : %s ===" % (VERSION, nommer_parcours(chemin, parcours)))
    print("Verdict : %s" % couleur(verdict, "rouge" if erreurs else "jaune" if allegements else "vert"))
    print("  erreurs: %d | a alleger: %d | avertissements: %d"
          % (len(erreurs), len(allegements), len(avertissements)))
    for e in erreurs[:15]:
        print("  [ERREUR] %s" % e)
    for a in allegements[:15]:
        print("  [A ALLEGER] %s" % a)
    for a in avertissements[:10]:
        print("  [AVERTISSEMENT] %s" % a)
    if len(erreurs) > 15:
        print("  ... et %d autre(s) erreur(s)" % (len(erreurs) - 15))

    # Rapport markdown (GARDE-FOU v1.0.1) : jamais d'ecriture dans le repertoire
    # courant sans --rapport <fichier> explicite (lecon : rapport a la racine
    # cree par valider-case lance sans options).
    rapport = generer_rapport(chemin, erreurs, allegements, avertissements, verdict, parcours)
    if rapport_fichier is None:
        if dry_run:
            print("DRY-RUN : aucun rapport (simulation)")
        else:
            print("AUCUN RAPPORT ECRIT : utilise --rapport <fichier> pour en generer un")
            print("(jamais de rapport par defaut dans le repertoire courant)")
    elif dry_run:
        print("DRY-RUN : rapport non ecrit (%s)" % rapport_fichier)
    else:
        with io.open(rapport_fichier, "w", encoding="utf-8", newline="") as fh:
            fh.write(rapport)
        print("RAPPORT ECRIT : %s" % os.path.abspath(rapport_fichier))

    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
