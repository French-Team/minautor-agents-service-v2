#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
valider-cartes-decision.py

Verifie que les agents respectent leur CARTE DE DECISION. Depuis la v0.2.0
(allegement des fiches), la carte de decision d'un agent est son PARCOURS JSON
(agents/<agent>/parcours/parcours-<agent>.json) : c'est la SOURCE DE VERITE du
guidage. Cet outil valide la structure et les references d'un parcours.

Validations d'un parcours :
  1. Le fichier parcours-<agent>.json existe
  2. Le JSON est valide (json.load)
  3. Structure : cles top-level identite + parcours + cases presentes
  4. parcours.case_depart existe et designe une case reelle
  5. Chaque case a un type valide (question/indice/controle/fin/action)
  6. References valides : suivant et vers des branches pointent vers des cases
  7. La case c0 est une question de relecture honnete (Pattern 4, spec v0.5.0)
  8. AUCUN SUIVANT MORT (garde-fou v0.3.2) :
     - case type 'fin' avec champ suivant -> la navigation s'arrete a la fin,
       le suivant est ignore (mort)
     - case avec branches non vides ET champ suivant -> les branches priment,
       le suivant n'est jamais lu (mort)
     Le suivant n'est legitime que sur une case SANS branches et NON-fin
       (question/indice/action/controle qui enchaine).
  9. COMMANDE ACTIVER EXACTE (garde-fou v0.4.0, P8) :
     - toute case type 'fin' dont le titre commence par 'FIN - Activer <agent>'
       doit contenir dans son message la commande exacte
       'activer-agent-principal.py activer session-llm-1 <agent>' ET la
       mention 'PAS reactiver' (sinon l'agent retombe sur reactiver qui
       ramene toujours a Cerberus).
  10. FORMAT DE VERSION (garde-fou v0.4.0, P9) :
      - parcours.version ne doit PAS commencer par le prefixe 'v'
        (format canonique sans v, ex: 0.3.3).
  11. COHERENCE FICHE/PARCOURS (garde-fou v0.4.0, P10) :
      - si la fiche agents/<agent>/<agent>.md contient le Pattern 14
        'PARCOURS (vX.Y.Z)', la version doit correspondre a parcours.version.
      - signale KO si la ligne PARCOURS (v manque ou differe.

Utilisation:
  valider-cartes-decision.py --agent <nom>
  valider-cartes-decision.py --tous
  valider-cartes-decision.py --fichier <chemin.json>

Proprietaire : Vulcain (outil partage)
Version : 0.4.7
Statut : prepare
"""

import io
import json
import os
import re
import subprocess
import sys

VERSION = "0.4.7"
REGEX_RESIDU = re.compile(r"^v?\d+\.\d+\.\d+$")
STATUT = "prepare"

AGENTS_DIR = "cerveau-projet/agents"
TYPES_VALIDES = ("question", "indice", "controle", "fin", "action")


def racine_projet():
    """Remonte jusqu au dossier racine (contenant AGENTS.md)."""
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def agent_actif_session():
    """Agent ACTIF de la session : table '## Sessions connues' d AGENTS.md,
    agent de la session la plus recente. C est l APPELLANT reel de l outil -
    distinct du parametre --agent (CIBLE de la verification)."""
    racine = racine_projet()
    chemin = os.path.join(racine, "AGENTS.md")
    try:
        contenu = io.open(chemin, encoding="utf-8", errors="replace").read()
    except (IOError, OSError):
        return ""
    m = re.search(r"## Sessions connues\n(.*?)(?=\n## |\Z)", contenu, re.S)
    if not m:
        return ""
    lignes = []
    for ligne in m.group(1).splitlines():
        ligne = ligne.strip()
        if not ligne.startswith("| session-llm-"):
            continue
        cellules = [c.strip() for c in ligne.strip("|").split("|")]
        if len(cellules) >= 4:
            lignes.append(cellules)
    if not lignes:
        return ""
    lignes.sort(key=lambda c: c[3], reverse=True)
    actif = lignes[0][2].strip()
    return actif if actif and actif != "-" else ""


def verrouiller_habilitation(agent, outil):
    """Verrou d habilitation + auto-journalisation : appele
    proteger-verrou-habilitation et retourne (code, message).
    Code 0 = habilite (usage journalise en mode verrou-auto), 1 = bloque,
    2 = erreur. L outil signale LUI-MEME son usage (espionnage)."""
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


def afficher_aide():
    print("=== valider-cartes-decision v%s ===" % VERSION)
    print("")
    print("Verifie la carte de decision d'un agent = son PARCOURS JSON (source de verite).")
    print("")
    print("Usage: valider-cartes-decision.py [options]")
    print("")
    print("Options:")
    print("  --agent <nom>          Verifier le parcours d'un agent specifique")
    print("  --tous                 Verifier les parcours de tous les agents")
    print("  --fichier <chemin>     Verifier un fichier parcours JSON specifique")
    print("  --aide                 Afficher cette aide")
    print("")
    print("Exemples:")
    print("  valider-cartes-decision.py --agent buffy")
    print("  valider-cartes-decision.py --tous")
    print("  valider-cartes-decision.py --fichier cerveau-projet/agents/buffy/parcours/parcours-buffy.json")


def lister_agents():
    """Tous les dossiers agents qui ont un dossier parcours/."""
    agents = []
    if not os.path.isdir(AGENTS_DIR):
        return agents
    for nom in sorted(os.listdir(AGENTS_DIR)):
        dossier = os.path.join(AGENTS_DIR, nom)
        if os.path.isdir(dossier) and os.path.isdir(os.path.join(dossier, "parcours")):
            agents.append(nom)
    return agents


def chemin_parcours_agent(agent):
    return os.path.join(AGENTS_DIR, agent, "parcours", "parcours-" + agent + ".json")


def valider_parcours(contenu, nom_display, agent=None):
    """Valide un parcours JSON. Retourne 0 si conforme, 1 sinon."""
    print("=== Verification %s ===" % nom_display)
    print("")

    try:
        donnees = json.loads(contenu)
    except ValueError as e:
        print("1. JSON valide")
        print("   [ERREUR] JSON invalide : %s" % e)
        print("")
        print("=== Resultat : NON CONFORME ===")
        return 1

    erreurs = []
    controles_ok = []

    # 1. JSON valide
    controles_ok.append("1. JSON valide")
    print("1. JSON valide")
    print("   [OK] JSON parse sans erreur")

    # 2. Structure : identite + parcours + cases
    manquantes = [c for c in ("identite", "parcours", "cases") if c not in donnees]
    print("2. Structure (identite + parcours + cases)")
    if manquantes:
        print("   [ERREUR] Cles manquantes : %s" % ", ".join(manquantes))
        erreurs.append("structure")
    else:
        controles_ok.append("2. Structure (identite + parcours + cases)")
        print("   [OK] Cles top-level presentes")
        identite = donnees["identite"]
        if identite.get("type") != "parcours":
            print("   [ERREUR] identite.type doit etre 'parcours' (trouve: %s)"
                  % identite.get("type"))
            erreurs.append("identite.type")
        else:
            print("   [OK] identite.type = parcours")

    # 3. case_depart
    print("3. Case de depart (case_depart)")
    parcours = donnees.get("parcours", {})
    cases = donnees.get("cases", {})
    case_depart = parcours.get("case_depart")
    if not case_depart:
        print("   [ERREUR] parcours.case_depart manquante")
        erreurs.append("case_depart")
    elif case_depart not in cases:
        print("   [ERREUR] case_depart '%s' introuvable dans cases" % case_depart)
        erreurs.append("case_depart")
    else:
        controles_ok.append("3. Case de depart (case_depart)")
        print("   [OK] case_depart '%s' existe" % case_depart)

    # 4. Types de cases valides
    print("4. Types de cases (question/indice/controle/fin/action)")
    types_invalides = []
    for cid, case in cases.items():
        typ = case.get("type")
        if typ not in TYPES_VALIDES:
            types_invalides.append("%s:%s" % (cid, typ))
    if types_invalides:
        print("   [ERREUR] Types invalides : %s" % ", ".join(types_invalides[:5]))
        erreurs.append("types")
    else:
        controles_ok.append("4. Types de cases")
        print("   [OK] %d cases, tous types valides" % len(cases))

    # 5. References valides (suivant + vers des branches)
    print("5. References (suivant + branches.vers)")
    refs_cassees = []
    for cid, case in cases.items():
        suivant = case.get("suivant")
        if suivant and suivant not in cases:
            refs_cassees.append("%s.suivant->%s" % (cid, suivant))
        # Reference morte TOP-LEVEL : le champ 'vers' d une case (hors branches)
        # doit pointer vers une case existante. Une case fin avec 'vers' vers une
        # case absente (ex: c7 'vers': 'conversation' de redacteur-v2) etait
        # silencieusement ignoree par la navigation - detectee ici (2026-08-22).
        vers_top = case.get("vers")
        if vers_top and vers_top not in cases:
            refs_cassees.append("%s.vers->%s" % (cid, vers_top))
        for b in case.get("branches") or []:
            vers = b.get("vers")
            if vers and vers not in cases:
                refs_cassees.append("%s.branche->%s" % (cid, vers))
    if refs_cassees:
        print("   [ERREUR] References cassees : %s" % ", ".join(refs_cassees[:5]))
        erreurs.append("references")
    else:
        controles_ok.append("5. References")
        print("   [OK] Toutes les references pointent vers des cases existantes")

    # 6. Relecture obligatoire (Pattern 4 v2, migration 2026-08-16) :
    #    c0 = action RELIRE OBLIGATOIRE (corrections puis fiche) -> c0b ;
    #    c0b = question confirmation (OUI -> c0c, NON -> c0).
    print("6. Relecture obligatoire (c0 action RELIRE + c0b confirmation)")
    c0 = cases.get("c0")
    c0b = cases.get("c0b")
    if not isinstance(c0, dict):
        print("   [ERREUR] Case c0 absente")
        erreurs.append("c0")
    elif c0.get("type") != "action":
        print("   [ERREUR] c0 doit etre de type action (RELIRE OBLIGATOIRE)")
        erreurs.append("c0")
    elif "RELIRE" not in (c0.get("titre") or "").upper():
        print("   [ERREUR] le titre de c0 doit contenir RELIRE")
        erreurs.append("c0")
    else:
        lecteurs = [i for i in c0.get("indices", [])
                    if i.get("type") == "outil" and i.get("nom") == "lire-fichier"]
        if len(lecteurs) < 2:
            print("   [ATTENTION] c0 doit porter au moins 2 outils lire-fichier (corrections + fiche)")
        controles_ok.append("6. Relecture c0")
        print("   [OK] c0 est une action RELIRE OBLIGATOIRE")
    if not isinstance(c0b, dict):
        print("   [ERREUR] Case c0b (confirmation) absente")
        erreurs.append("c0b")
    elif c0b.get("type") != "question":
        print("   [ERREUR] c0b doit etre de type question (confirmation de lecture)")
        erreurs.append("c0b")
    else:
        vers_oui = [b.get("vers") for b in c0b.get("branches", [])
                    if b.get("reponse") == "OUI"]
        vers_non = [b.get("vers") for b in c0b.get("branches", [])
                    if b.get("reponse") == "NON"]
        # Chemin legitime de la confirmation : OUI -> c0c directement, ou
        # OUI -> c0e (consultation pre-mission) -> c0c ; NON -> c0.
        oui_ok = vers_oui == ["c0c"] or (
            vers_oui == ["c0e"] and isinstance(cases.get("c0e"), dict)
            and cases["c0e"].get("suivant") == "c0c")
        if not oui_ok or vers_non != ["c0"]:
            print("   [ERREUR] c0b doit avoir OUI -> c0c (ou OUI -> c0e -> c0c) et NON -> c0")
            erreurs.append("c0b")
        else:
            controles_ok.append("6. Confirmation c0b")
            print("   [OK] c0b est une question de confirmation (OUI -> c0c/c0e, NON -> c0)")

    # 7. Garde-fou v0.3.2 : AUCUN SUIVANT MORT
    #    Mecanique guider-parcours : (a) une case 'fin' arrete la navigation
    #    (son 'suivant' est ignore) ; (b) les branches d'une case priment sur
    #    son 'suivant' (jamais lu). Le 'suivant' n'est legitime que sur une
    #    case SANS branches et NON-fin.
    print("7. Garde-fou suivant mort (fin avec suivant / branches + suivant)")
    suivants_morts = []
    for cid, case in sorted(cases.items()):
        suivant = case.get("suivant")
        if not suivant:
            continue
        typ = case.get("type")
        branches = case.get("branches") or []
        if typ == "fin":
            suivants_morts.append("%s (fin avec suivant -> la navigation s'arrete a la fin)" % cid)
        elif branches:
            suivants_morts.append("%s (branches + suivant -> les branches priment, le suivant n'est jamais lu)" % cid)
    if suivants_morts:
        print("   [ERREUR] Suivants morts detectes : %s" % "; ".join(suivants_morts[:5]))
        if len(suivants_morts) > 5:
            print("   [ERREUR] ... et %d autre(s)" % (len(suivants_morts) - 5))
        erreurs.append("suivant_mort")
    else:
        controles_ok.append("7. Garde-fou suivant mort")
        print("   [OK] Aucun suivant mort (0 fin avec suivant, 0 branches + suivant)")

    # 8. Garde-fou v0.4.0 (P8) : COMMANDE ACTIVER EXACTE dans les fins
    #    'FIN - Activer <agent>'. Sans la commande exacte, l'agent retombe
    #    sur reactiver (qui ramene toujours a Cerberus).
    #    MULTI-SESSIONS (v0.4.6) : la commande accepte le placeholder <session>
    #    (chaque session le remplace par SON id a l execution) OU une session
    #    concrete session-llm-N -- le format figee 'session-llm-1' interdisait
    #    aux autres sessions de suivre leur carte (D6).
    print("8. Commande activer exacte dans les fins 'Activer X' (P8)")
    fins_activer = []
    for cid, case in sorted(cases.items()):
        if case.get("type") != "fin":
            continue
        titre = (case.get("titre") or "").strip()
        m = re.match(r"^FIN\s*-\s*Activer\s+([A-Za-z0-9_-]+)\s*$", titre)
        if not m:
            continue
        cible = m.group(1)
        msg = case.get("message") or ""
        # Comparaison insensible a la casse : le titre porte l'agent avec une
        # majuscule (Janus) tandis que la commande reelle est en minuscule.
        motif = (r"activer-agent-principal\.py activer (?:<session>|session-llm-\d+) %s"
                 % re.escape(cible.lower()))
        if not re.search(motif, msg.lower()) or "PAS reactiver" not in msg:
            fins_activer.append("%s (FIN - Activer %s sans commande exacte)" % (cid, cible))
    if fins_activer:
        print("   [ERREUR] Fins Activer X sans commande exacte : %s" % "; ".join(fins_activer[:5]))
        if len(fins_activer) > 5:
            print("   [ERREUR] ... et %d autre(s)" % (len(fins_activer) - 5))
        erreurs.append("commande_activer")
    else:
        controles_ok.append("8. Commande activer exacte (P8)")
        print("   [OK] Toutes les fins 'FIN - Activer X' contiennent la commande exacte + 'PAS reactiver'")

    # 9. Garde-fou v0.4.0 (P9) : FORMAT DE VERSION sans prefixe 'v'
    print("9. Format de version sans prefixe 'v' (P9)")
    version = parcours.get("version")
    if not version:
        print("   [ERREUR] parcours.version absente")
        erreurs.append("version")
    elif version.startswith("v"):
        print("   [ERREUR] parcours.version '%s' commence par 'v' (format canonique sans v)" % version)
        erreurs.append("version")
    else:
        controles_ok.append("9. Format de version (P9)")
        print("   [OK] parcours.version '%s' sans prefixe v" % version)

    # 10. Garde-fou v0.4.0 (P10) : COHERENCE FICHE/PARCOURS (Pattern 14)
    print("10. Coherence fiche/parcours (Pattern 14, P10)")
    if not agent:
        controles_ok.append("10. Coherence fiche/parcours (P10) - non applicable (fichier direct)")
        print("   [NOTE] Pas de nom d'agent : verifie uniquement via --agent/--tous")
    else:
        fiche = os.path.join(AGENTS_DIR, agent, "%s.md" % agent)
        if not os.path.isfile(fiche):
            print("   [ATTENTION] Fiche %s absente : coherence non verifiee" % fiche)
        else:
            try:
                with io.open(fiche, encoding="utf-8") as fh:
                    texte_fiche = fh.read()
            except Exception:
                texte_fiche = ""
            m = re.search(r"PARCOURS\s*\(v([0-9]+\.[0-9]+\.[0-9]+)\)", texte_fiche)
            if not m:
                print("   [ATTENTION] Pattern 14 (PARCOURS (vX.Y.Z)) absent de la fiche")
            elif m.group(1) != version:
                print("   [ERREUR] Incoherence fiche/parcours : fiche v%s != parcours %s" % (m.group(1), version))
                erreurs.append("coherence_fiche")
            else:
                controles_ok.append("10. Coherence fiche/parcours (P10)")
                print("   [OK] Fiche PARCOURS (v%s) == parcours %s" % (m.group(1), version))

    print("")
    if erreurs:
        print("=== Resultat : NON CONFORME (%d erreur(s)) ===" % len(erreurs))
        return 1
    print("=== Resultat : CONFORME ===")
    return 0


def verifier_parcours_fichier(chemin, nom_display, agent=None):
    """Verifie un fichier parcours JSON (ou signale qu'une fiche .md n'est plus la cible)."""
    if not os.path.isfile(chemin):
        print("=== Verification %s : %s ===" % (nom_display, chemin))
        print("")
        print("ERREUR : Le fichier %s n'existe pas" % chemin)
        return 1

    if chemin.endswith(".md"):
        print("=== Verification %s : %s ===" % (nom_display, chemin))
        print("")
        print("NOTE : la carte de decision ne vit plus dans la fiche .md")
        print("(allegement v0.2.0). La SOURCE DE VERITE est le parcours JSON :")
        print("  agents/<agent>/parcours/parcours-<agent>.json")
        print("Utiliser --agent <nom> ou --fichier <parcours.json>.")
        print("")
        print("=== Resultat : NON CONFORME (mauvaise cible) ===")
        return 1

    try:
        with io.open(chemin, encoding="utf-8") as fh:
            contenu = fh.read()
    except Exception:
        print("=== Verification %s : %s ===" % (nom_display, chemin))
        print("")
        print("ERREUR : Impossible de lire le fichier %s" % chemin)
        return 1

    return valider_parcours(contenu, nom_display, agent=agent)


def verifier_agent(agent):
    chemin = chemin_parcours_agent(agent)
    return verifier_parcours_fichier(chemin, "de l'agent %s" % agent, agent=agent)


def verifier_tous():
    print("=== Verification de tous les agents ===")
    print("")

    agents = lister_agents()
    conformes = 0
    total = 0

    for agent in agents:
        total += 1
        if verifier_agent(agent) == 0:
            conformes += 1
        print("")

    print("=== Resume ===")
    print("Agents verifies : %d" % total)
    print("Agents conformes : %d" % conformes)
    print("Agents non conformes : %d" % (total - conformes))
    return 0


def verifier_residus_racine():
    """GARDE-FOU ANTI-RESIDUS : detecter dans le repertoire courant les fichiers
    nommes comme des versions semver pures (ex: 0.2.1, v0.2.6). Ces fichiers
    sont des residus probables de redirections accidentelles de sortie d une
    commande precedente (souvent la sortie d un outil du cerveau). Anti-residu :
    les supprimer - les sources de verite de version vivent dans
    cerveau-projet/agents/clio/ (version-readme.txt, statut-projet.txt),
    JAMAIS a la racine."""
    try:
        residus = sorted(n for n in os.listdir(".")
                         if os.path.isfile(n) and REGEX_RESIDU.match(n))
    except OSError:
        return
    if not residus:
        return
    print("=" * 60)
    print("!!! WARNING GARDE-FOU (v%s) !!!" % VERSION)
    print("Des fichiers nommes comme des versions semver sont presents dans le")
    print("repertoire courant (residus probables de redirections accidentelles")
    print("de sortie) :")
    for n in residus[:10]:
        print("    - %s" % n)
    print("ANTI-RESIDU : supprimez-les. Les sources de verite de version vivent")
    print("dans cerveau-projet/agents/clio/ (version-readme.txt,")
    print("statut-projet.txt), JAMAIS a la racine.")
    print("=" * 60)


def main(argv):
    if not argv:
        afficher_aide()
        return 1

    if argv[0] in ("--aide", "--help", "-h"):
        afficher_aide()
        return 0

    if argv[0] == "--version":
        print("valider-cartes-decision v%s (%s)" % (VERSION, STATUT))
        return 0

    verifier_residus_racine()

    if argv[0] == "--agent":
        if len(argv) < 2:
            print("ERREUR : Nom de l'agent manquant")
            afficher_aide()
            return 1
        # VERROU AUTO-JOURNALISATION (v0.4.5) : l outil signale LUI-MEME son
        # usage (autorise -> registre mode verrou-auto ; non autorise -> bloque).
        code_verrou, msg_verrou = verrouiller_habilitation(
            agent_actif_session() or argv[1], "valider-cartes-decision")
        if code_verrou != 0:
            print(msg_verrou)
            return code_verrou
        return verifier_agent(argv[1])

    if argv[0] == "--tous":
        return verifier_tous()

    if argv[0] == "--fichier":
        if len(argv) < 2:
            print("ERREUR : Chemin du fichier manquant")
            afficher_aide()
            return 1
        return verifier_parcours_fichier(argv[1], "du fichier")

    print("ERREUR : Option inconnue '%s'" % argv[0])
    afficher_aide()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
