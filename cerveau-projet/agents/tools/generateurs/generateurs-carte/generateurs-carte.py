#!/usr/bin/env python3
# -*- coding: ascii -*-
# generateurs-carte.py
# Agit sur une CARTE DE DECISION COMPLETE (parcours JSON) : creer un squelette
# conforme aux patterns 4-5-6-7, analyser les chemins de case_depart aux fins,
# detecter les anomalies (boucles, cases inatteignables, references cassees),
# dupliquer un chemin (groupe de cases) avec recablage et prefixe.
# Version : 0.2.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

# ============================================================
# REGLE IMMUABLE DE NOMMAGE : le nom DOIT commencer par le
# prefixe du dossier de categorie (generateurs-) : controle au demarrage.
# REGLE IMMUABLE : 100% stdlib Python.
# REGLE IMMUABLE : ASCII strict (aucun accent, emoji ou Unicode).
# ============================================================

import argparse
import json
import subprocess
import sys
from collections import deque
from pathlib import Path

VERSION = "0.2.0"
STATUT = "ebauche"

# Racine du projet : 5 remontees depuis ce fichier
# (generateurs-carte -> generateurs -> tools -> agents -> cerveau-projet -> racine)
RACINE = Path(__file__).resolve().parents[5]
GUIDER_PY = RACINE / "cerveau-projet" / "agents" / "tools" / "guider" / "guider-parcours" / "guider-parcours.py"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def verifier_nommage(script_path):
    chemin = Path(script_path)
    nom_fichier = chemin.stem
    if nom_fichier == "outil-template":
        return
    dossier = chemin.parent.name
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


# ------------------------------------------------------------
# Chargement / sauvegarde
# ------------------------------------------------------------

def charger_parcours(chemin):
    """Charge le parcours JSON et valide sa structure de base."""
    chemin = Path(chemin)
    if not chemin.exists():
        print(_couleur("ERREUR: Parcours introuvable: %s" % chemin, "rouge"), file=sys.stderr)
        sys.exit(1)
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            donnees = json.load(f)
    except json.JSONDecodeError as e:
        print(_couleur("ERREUR: JSON invalide: %s" % e, "rouge"), file=sys.stderr)
        sys.exit(1)
    if "parcours" not in donnees or "cases" not in donnees:
        print(_couleur("ERREUR: Structure invalide (attendu: parcours + cases)", "rouge"), file=sys.stderr)
        sys.exit(1)
    return donnees


def sauvegarder_parcours(chemin, donnees):
    """Ecrit le parcours JSON en ASCII strict avec indentation 2."""
    chemin = Path(chemin)
    try:
        contenu = json.dumps(donnees, ensure_ascii=True, indent=2)
        contenu.encode("ascii")
    except UnicodeEncodeError:
        print(_couleur("ERREUR: Contenu non-ASCII refuse (regle immuable)", "rouge"), file=sys.stderr)
        sys.exit(1)
    with open(chemin, "w", encoding="ascii", newline="\n") as f:
        f.write(contenu)
        f.write("\n")


def valider_references(donnees, verbose=False):
    """Valide que toutes les references (suivant, vers, case_depart) existent."""
    cases = donnees["cases"]
    depart = donnees["parcours"].get("case_depart")
    erreurs = []
    if depart not in cases:
        erreurs.append("case_depart '%s' inexistante" % depart)
    for case_id, case in cases.items():
        suivant = case.get("suivant")
        if suivant is not None and suivant not in cases:
            erreurs.append("case %s: suivant '%s' inexistant" % (case_id, suivant))
        for i, branche in enumerate(case.get("branches", [])):
            vers = branche.get("vers")
            if vers is not None and vers not in cases:
                erreurs.append("case %s: branche[%d] vers '%s' inexistant" % (case_id, i, vers))
    if erreurs:
        for e in erreurs:
            print(_couleur("  [ERREUR] %s" % e, "rouge"), file=sys.stderr)
        return False
    if verbose:
        print(_couleur("  [OK] References validees (%d cases)" % len(cases), "vert"))
    return True


def valider_auto(chemin, donnees):
    """Validation auto complete : json (recharge), references, guider-parcours --liste."""
    print(_couleur("  [VALIDATION AUTO]", "bleu"))
    ok_refs = valider_references(donnees, verbose=True)
    if not ok_refs:
        print(_couleur("  [ERREUR] References invalides : corriger avant usage", "rouge"), file=sys.stderr)
        return False
    try:
        resultat = subprocess.run(
            [sys.executable, str(GUIDER_PY), str(chemin), "--liste"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if resultat.returncode != 0:
            print(_couleur("  [ERREUR] guider-parcours --liste a echoue", "rouge"), file=sys.stderr)
            print(resultat.stderr, file=sys.stderr)
            return False
        lignes = [l for l in resultat.stdout.splitlines() if l.strip()]
        print(_couleur("  [OK] guider-parcours --liste : %d lignes" % len(lignes), "vert"))
    except (OSError, subprocess.TimeoutExpired) as e:
        print(_couleur("  [ATTENTION] guider-parcours non lance: %s" % e, "jaune"), file=sys.stderr)
    return True


# ------------------------------------------------------------
# Squelette de carte (action creer)
# ------------------------------------------------------------

def squelette_carte(agent, nom, version, description):
    """Construit le squelette d'une carte conforme aux patterns 4-5-6-7-8-10-3."""
    cases = {
        "c0": {
            "titre": "Relecture : ta fiche et tes corrections en memoire ?",
            "type": "question",
            "question": "As-tu EN MEMOIRE ta fiche et tes corrections, capables de les appliquer SANS relire ? Reponds la VERITE (regles-veracite).",
            "indices": [
                {
                    "type": "regle",
                    "texte": "REGLE ABSOLUE -- RELECTURE : a chaque activation ou reactivation, je me pose la question de la relecture. Seul OUI prouve la memorisation : relire sans retenir = inutile.",
                }
            ],
            "branches": [
                {"reponse": "OUI", "vers": "c0c"},
                {"reponse": "INCERTAIN", "vers": "c0b"},
                {"reponse": "NON", "vers": "c0b"},
            ],
        },
        "c0b": {
            "titre": "RELIRE OBLIGATOIRE : corrections puis fiche",
            "type": "indice",
            "indices": [
                {
                    "type": "regle",
                    "texte": "ACTION OBLIGATOIRE : je relis MES corrections EN PREMIER puis MA fiche avant de continuer. Je ne lis jamais les fichiers des autres agents : chacun lit les siens en prenant le relais.",
                },
                {
                    "type": "outil",
                    "nom": "lire-fichier",
                    "chemin": "cerveau-projet/agents/tools/lire/lire-fichier/",
                    "commande": "python3 cerveau-projet/agents/tools/lire/lire-fichier/lire-fichier.py cerveau-projet/agents/%s/corrections.md" % agent,
                },
                {
                    "type": "outil",
                    "nom": "lire-fichier",
                    "chemin": "cerveau-projet/agents/tools/lire/lire-fichier/",
                    "commande": "python3 cerveau-projet/agents/tools/lire/lire-fichier/lire-fichier.py cerveau-projet/agents/%s/%s.md" % (agent, agent),
                },
            ],
            "suivant": "c0c",
        },
        "c0c": {
            "titre": "CONTEXTE OBLIGATOIRE : activite recente des agents",
            "type": "indice",
            "indices": [
                {
                    "type": "regle",
                    "texte": "REGLE ABSOLUE -- CONTEXTE TEMPS REEL (Pattern 6) : meme si je viens de lire l historique, je le RELIS TOUJOURS : c est le fil temps reel du cerveau (il change a chaque activation des autres LLM), le dynamique ne se memorise pas. Je lis aussi la section Sessions connues d AGENTS.md pour savoir que les autres LLM existent et voir leur derniere activite (evite les collisions).",
                },
                {
                    "type": "outil",
                    "nom": "lire-activite-recente",
                    "chemin": "cerveau-projet/agents/tools/lire/lire-activite-recente/",
                    "commande": "python3 cerveau-projet/agents/tools/lire/lire-activite-recente/lire-activite-recente.py",
                },
                {
                    "type": "fichier",
                    "chemin": "AGENTS.md",
                    "raison": "Section ## Sessions connues : la table des sessions existantes (session | id LLM | agent actif | derniere activite) -- savoir que les autres LLM existent et leur activite en temps reel",
                },
            ],
            "suivant": "c1",
        },
        "c1": {
            "titre": "Mission",
            "type": "question",
            "question": "Quelle est la mission ?",
            "indices": [
                {
                    "type": "regle",
                    "texte": "REGLE PATTERN 10 (spec-guider-parcours v0.2.18) : UNE CARTE = UN ROLE - cette carte ne contient QUE des actions propres au role de %s : activation, verification, decision. JAMAIS d outils d ANALYSE ou d EXECUTION appartenant au role d un autre agent (lister-outils, detecter-impacts, generateurs-carte hors edition de SES cases...). PIEGE DU GLISSEMENT : lire pour DECIDER est du role ; lire pour EXECUTER est de la derive." % agent,
                },
            ],
            "branches": [
                {"reponse": "a-definir", "vers": "c2"},
                {"reponse": "autre", "vers": "c9"},
            ],
        },
        "c2": {
            "titre": "Exemple d'action (a completer)",
            "type": "indice",
            "indices": [
                {
                    "type": "regle",
                    "texte": "REGLE PATTERN 3 (spec-guider-parcours v0.2.4) : RAPPEL DES COMBOS - une SUITE LINEAIRE d outils repetee (>= 2 occurrences) ou longue (>= 3 outils) doit etre encapsulee dans un COMBO : case unique Lancer le combo X qui reference combos-moteur + definition-combo.json (protocole-creation-combos), au lieu d enchainer les outils dans la carte. La carte reste allegee : 1 case = 1 combo.",
                },
                {
                    "type": "regle",
                    "texte": "REGLE PATTERN 7 (spec-guider-parcours v0.2.13) : toute case de DECISION porte AU MINIMUM 2 branches (sauf action directe). Completez cette carte avec generateurs-case (ajouter/editer/supprimer) ou generateurs-carte (dupliquer-chemin).",
                },
                {
                    "type": "regle",
                    "texte": "REGLE IMMUABLE ASCII (Pattern 2) : avant d'ecrire dans un fichier, verifier que le contenu est 100%% ASCII - aucun accent, emoji ou caractere Unicode. Guillemets ASCII uniquement, jamais de guillemets francais.",
                },
            ],
            "suivant": "c2b",
        },
        "c2b": {
            "titre": "RVAV avant activation (chaine bout-en-bout)",
            "type": "indice",
            "indices": [
                {
                    "type": "regle",
                    "texte": "REGLE IMMUABLE RVAV : je ne valide JAMAIS sans avoir passe la boucle RVAV complete (Rechercher, Verifier, Analyser, Valider) sur mon travail AVANT d activer le maillon suivant de la chaine.",
                },
                {
                    "type": "fichier",
                    "chemin": "cerveau-projet/agents/regles-immuables/general/rvav-workflow.md",
                    "raison": "Boucle RVAV obligatoire : Rechercher, Verifier, Analyser, Valider",
                },
            ],
            "suivant": "c9",
        },
        "c9": {
            "titre": "FIN - Mission terminee",
            "type": "fin",
            "message": "CHAINE BOUT-EN-BOUT (spec-guider-parcours v0.2.15) : mission terminee et validee (RVAV). J ACTIVE le maillon suivant de la chaine a MA fin (tests -> Morpheus, controle -> Janus) ; le dernier maillon REACTIVE Cerberus avec le bilan consolide. Une activation directe par Cerberus : fin = reactiver Cerberus.",
        },
    }
    return {
        "parcours": {
            "nom": nom,
            "agent": agent,
            "version": version,
            "case_depart": "c0",
            "description": description,
        },
        "cases": cases,
    }


def action_creer(args):
    """Cree une carte squelette complete conforme aux patterns."""
    chemin = Path(args.parcours)
    if chemin.exists() and not args.force:
        print(_couleur("ERREUR: Le fichier '%s' existe deja (utiliser --force pour ecraser)" % chemin, "rouge"), file=sys.stderr)
        sys.exit(1)
    agent = args.agent or chemin.parent.name or "agent"
    if agent == "parcours":
        agent = "agent"
    nom = args.nom or ("parcours-%s" % agent)
    donnees = squelette_carte(agent, nom, args.version, args.description or ("Parcours (jeu de piste) de %s. A completer avec generateurs-case." % agent))
    if args.dry_run:
        print(_couleur("[DRY-RUN] Carte '%s' (agent %s, %d cases) creee a %s" % (nom, agent, len(donnees["cases"]), chemin), "jaune"))
        return 0
    sauvegarder_parcours(chemin, donnees)
    print(_couleur("[OK] Carte '%s' creee (agent %s, %d cases) : %s" % (nom, agent, len(donnees["cases"]), chemin), "vert"))
    valider_auto(chemin, donnees)
    return 0


# ------------------------------------------------------------
# Analyse des chemins (action analyser)
# ------------------------------------------------------------

def analyser_chemins(donnees):
    """Retourne tous les chemins de case_depart vers les fins (BFS, limite anti-boucle)."""
    cases = donnees["cases"]
    depart = donnees["parcours"].get("case_depart")
    chemins = []
    file = deque([[depart]])
    visites = set()
    limite = 10000
    while file and len(chemins) < limite:
        chemin = file.popleft()
        derniere = chemin[-1]
        case = cases.get(derniere)
        if case is None:
            continue
        if case.get("type") == "fin":
            chemins.append(chemin)
            continue
        suivants = []
        if case.get("suivant"):
            suivants.append(case["suivant"])
        for branche in case.get("branches", []):
            if branche.get("vers"):
                suivants.append(branche["vers"])
        if not suivants:
            chemins.append(chemin + [None])  # impasse
            continue
        for nxt in suivants:
            if nxt in chemin:
                continue  # evite les boucles
            file.append(chemin + [nxt])
    return chemins


def action_analyser(args):
    """Liste tous les chemins de case_depart vers les fins."""
    donnees = charger_parcours(args.parcours)
    cases = donnees["cases"]
    depart = donnees["parcours"].get("case_depart")
    chemins = analyser_chemins(donnees)
    print("=== Analyse des chemins : %s (depart %s, %d cases) ===" % (args.parcours, depart, len(cases)))
    print("Chemins trouves : %d" % len(chemins))
    print("")
    for i, chemin in enumerate(chemins, 1):
        fin = chemin[-1]
        fin_label = cases.get(fin, {}).get("titre", "IMPASSE") if fin else "IMPASSE"
        etapes = []
        for c in chemin:
            if c is None:
                etapes.append("[impasse]")
            else:
                etapes.append("%s(%s)" % (c, cases[c].get("type", "?")))
        print("  Chemin %d -> %s : %s" % (i, fin_label, " -> ".join(etapes)))
    return 0


# ------------------------------------------------------------
# Detection d'anomalies (action detecter)
# ------------------------------------------------------------

def detecter_anomalies(donnees):
    """Detecte les anomalies : boucles, cases inatteignables, impasses, references cassees."""
    cases = donnees["cases"]
    depart = donnees["parcours"].get("case_depart")
    anomalies = []

    # 1. References cassees
    if depart not in cases:
        anomalies.append("case_depart '%s' inexistante" % depart)
    for case_id, case in cases.items():
        suivant = case.get("suivant")
        if suivant is not None and suivant not in cases:
            anomalies.append("case %s: suivant '%s' inexistant" % (case_id, suivant))
        for i, branche in enumerate(case.get("branches", [])):
            vers = branche.get("vers")
            if vers is not None and vers not in cases:
                anomalies.append("case %s: branche[%d] vers '%s' inexistant" % (case_id, i, vers))

    # 2. Boucles d'attente (branche vers sa propre case, titre/question avec attente)
    for case_id, case in cases.items():
        titre_q = ((case.get("titre", "") or "") + " " + (case.get("question", "") or "")).lower()
        attend = any(m in titre_q for m in ("attendre", "attente", "en attente"))
        for branche in case.get("branches", []):
            if branche.get("vers") == case_id and attend:
                anomalies.append("BOUCLE D'ATTENTE: case %s se branche vers elle-meme avec 'attente' (regle 10)" % case_id)
        if case.get("suivant") == case_id and attend:
            anomalies.append("BOUCLE D'ATTENTE: case %s pointe sur elle-meme avec 'attente' (regle 10)" % case_id)

    # 3. Cases inatteignables depuis case_depart
    atteintes = set()
    file = deque([depart]) if depart in cases else deque()
    while file:
        cid = file.popleft()
        if cid in atteintes:
            continue
        atteintes.add(cid)
        case = cases.get(cid)
        if not case:
            continue
        if case.get("suivant"):
            file.append(case["suivant"])
        for branche in case.get("branches", []):
            if branche.get("vers"):
                file.append(branche["vers"])
    for case_id in cases:
        if case_id not in atteintes:
            anomalies.append("case '%s' INATTEIGNABLE depuis case_depart" % case_id)

    # 4. Cases sans sortie (ni suivant, ni branches, ni fin)
    for case_id, case in cases.items():
        if case.get("type") != "fin" and not case.get("suivant") and not case.get("branches"):
            anomalies.append("case '%s' SANS SORTIE (ni suivant ni branches, type %s)" % (case_id, case.get("type")))

    # 5. Pattern 7 : decision a branche unique (question/controle avec 1 seule branche)
    for case_id, case in cases.items():
        if case.get("type") in ("question", "controle") and len(case.get("branches", [])) == 1:
            anomalies.append("Pattern 7: decision '%s' a UNE SEULE branche (min 2 sauf action directe)" % case_id)

    return anomalies


def action_detecter(args):
    """Detecte les anomalies de la carte."""
    donnees = charger_parcours(args.parcours)
    cases = donnees["cases"]
    anomalies = detecter_anomalies(donnees)
    print("=== Detection d'anomalies : %s (%d cases) ===" % (args.parcours, len(cases)))
    if not anomalies:
        print(_couleur("[OK] Aucune anomalie detectee", "vert"))
    else:
        for a in anomalies:
            print(_couleur("  [ANOMALIE] %s" % a, "jaune" if "ATTENTE" in a or "INATTEIGNABLE" in a or "SANS SORTIE" in a else "rouge"))
        print(_couleur("Total : %d anomalie(s)" % len(anomalies), "rouge"))
    return 0


# ------------------------------------------------------------
# Duplication d'un chemin (action dupliquer-chemin)
# ------------------------------------------------------------

def action_dupliquer(args):
    """Duplique un groupe de cases (chemin de --debut a --fin) avec recablage et prefixe."""
    donnees = charger_parcours(args.parcours)
    cases = donnees["cases"]
    debut = args.debut
    fin = args.fin
    prefixe = args.prefixe or "d"
    if debut not in cases:
        print(_couleur("ERREUR: case de debut '%s' inexistante" % debut, "rouge"), file=sys.stderr)
        sys.exit(1)
    if fin not in cases:
        print(_couleur("ERREUR: case de fin '%s' inexistante" % fin, "rouge"), file=sys.stderr)
        sys.exit(1)

    # Parcours en largeur pour trouver les cases du chemin debut -> fin
    parents = {}
    file = deque([debut])
    visitees = set()
    while file:
        cid = file.popleft()
        if cid in visitees:
            continue
        visitees.add(cid)
        if cid == fin:
            break
        case = cases.get(cid, {})
        suivants = []
        if case.get("suivant"):
            suivants.append(case["suivant"])
        for branche in case.get("branches", []):
            if branche.get("vers"):
                suivants.append(branche["vers"])
        for nxt in suivants:
            if nxt not in visitees:
                parents[nxt] = cid
                file.append(nxt)

    if fin not in parents and fin != debut:
        print(_couleur("ERREUR: aucun chemin de '%s' vers '%s'" % (debut, fin), "rouge"), file=sys.stderr)
        sys.exit(1)

    # Reconstruction du chemin
    chemin_ids = []
    courant = fin
    while courant != debut:
        chemin_ids.append(courant)
        courant = parents.get(courant)
        if courant is None:
            print(_couleur("ERREUR: chemin incomplet vers '%s'" % fin, "rouge"), file=sys.stderr)
            sys.exit(1)
    chemin_ids.append(debut)
    chemin_ids.reverse()

    # Construire les nouveaux ids (prefixe + numero)
    def nouveau_id(ancien):
        return "%s%s" % (prefixe, ancien)

    nouvelles = {}
    mapping = {cid: nouveau_id(cid) for cid in chemin_ids}
    for cid in chemin_ids:
        case = cases[cid]
        copie = json.loads(json.dumps(case, ensure_ascii=True))
        if copie.get("suivant") and copie["suivant"] in mapping:
            copie["suivant"] = mapping[copie["suivant"]]
        for branche in copie.get("branches", []):
            if branche.get("vers") in mapping:
                branche["vers"] = mapping[branche["vers"]]
        nouvelles[mapping[cid]] = copie

    # Recablage : les references EXTERNES vers les cases dupliquees restent sur les
    # originales (les copies ne sont pas branchees automatiquement, sauf --brancher-debut)

    if args.dry_run:
        print(_couleur("[DRY-RUN] Chemin '%s'->'%s' duplique (%d cases) avec prefixe '%s' : %s" % (debut, fin, len(chemin_ids), prefixe, ", ".join(sorted(nouvelles))), "jaune"))
        return 0

    for nid, ncase in nouvelles.items():
        cases[nid] = ncase

    # L'original du debut pointe vers la copie du debut (a moins d'un --apres)
    if args.brancher_debut:
        cases[debut]["suivant"] = mapping[debut]

    sauvegarder_parcours(args.parcours, donnees)
    print(_couleur("[OK] Chemin '%s'->'%s' duplique : %d case(s) ajoutee(s) avec prefixe '%s'" % (debut, fin, len(chemin_ids), prefixe), "vert"))
    valider_auto(args.parcours, donnees)
    return 0


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def construire_parser():
    parser = argparse.ArgumentParser(
        prog="generateurs-carte",
        description="Agit sur une carte de decision COMPLETE (parcours JSON) : creer un squelette, analyser les chemins, detecter les anomalies, dupliquer un chemin.",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    # creer
    p_creer = subparsers.add_parser("creer", help="Creer une carte squelette complete (patterns 4-5-6-7)")
    p_creer.add_argument("parcours", type=str, help="Chemin du fichier JSON a creer")
    p_creer.add_argument("--agent", type=str, help="Nom de l'agent (defaut: dossier parent)")
    p_creer.add_argument("--nom", type=str, help="Nom du parcours (defaut: parcours-<agent>)")
    p_creer.add_argument("--ver", dest="version", type=str, default="0.1.0", help="Version du parcours (defaut: 0.1.0)")
    p_creer.add_argument("--description", type=str, help="Description du parcours")
    p_creer.add_argument("--force", action="store_true", help="Ecraser si le fichier existe")

    # analyser
    p_analyser = subparsers.add_parser("analyser", help="Lister tous les chemins de case_depart aux fins")
    p_analyser.add_argument("parcours", type=str, help="Chemin du parcours JSON")

    # detecter
    p_detecter = subparsers.add_parser("detecter", help="Detecter les anomalies (boucles, inatteignables, impasses)")
    p_detecter.add_argument("parcours", type=str, help="Chemin du parcours JSON")

    # dupliquer-chemin
    p_dup = subparsers.add_parser("dupliquer-chemin", help="Dupliquer un chemin (groupe de cases) avec recablage")
    p_dup.add_argument("parcours", type=str, help="Chemin du parcours JSON")
    p_dup.add_argument("--debut", dest="debut", type=str, required=True, help="Case de debut du chemin")
    p_dup.add_argument("--fin", dest="fin", type=str, required=True, help="Case de fin du chemin")
    p_dup.add_argument("--prefixe", type=str, default="d", help="Prefixe des nouveaux ids (defaut: d)")
    p_dup.add_argument("--brancher-debut", action="store_true", dest="brancher_debut", help="Faire pointer le debut d'origine vers la copie")

    # options globales
    for sub in (p_creer, p_analyser, p_detecter, p_dup):
        sub.add_argument("--dry-run", action="store_true", help="Simuler sans rien modifier")
        sub.add_argument("--verbose", action="store_true", help="Afficher les details")
        sub.add_argument("--version", action="version", version="generateurs-carte v%s" % VERSION)
    return parser


def main():
    verifier_nommage(sys.argv[0])
    parser = construire_parser()
    args = parser.parse_args()

    if args.action == "creer":
        return action_creer(args)
    elif args.action == "analyser":
        return action_analyser(args)
    elif args.action == "detecter":
        return action_detecter(args)
    elif args.action == "dupliquer-chemin":
        return action_dupliquer(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
