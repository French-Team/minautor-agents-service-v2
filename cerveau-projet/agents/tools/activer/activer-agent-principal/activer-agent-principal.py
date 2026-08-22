#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
activer-agent-principal.py

Outil pour modifier AGENTS.md de maniere fiable lors des activations
et reactivations d'agents, en supportant plusieurs sessions LLM en
parallele (chacune avec son bloc dedie et son agent principal).

Actions:
  sidentifier [session]          - Creer/choisir sa session (agent principal = Cerberus)
  activer <session> <agent> <raison> [mission]  - Activer un agent dans sa session
  reactiver <session> <raison> <agent_precedent> - Reactiver Cerberus dans sa session
  sessions                       - Lister les sessions et leur agent principal
  aide                           - Afficher cette aide

Variable d'environnement:
  AGENTS_FILE         - surcharger le chemin de AGENTS.md (tests sur copie)
  AGENTS_HISTORIQUE   - surcharger le chemin du fichier historique
  CLASSEUR_STOCKAGE   - surcharger le chemin du classeur-variables (tests sur copie)

Proprietaire : Vulcain
Version : 0.5.29
Statut : prepare
"""

import io
import json
import os
import re
import subprocess
import sys
from datetime import datetime

VERSION = "0.5.29"
STATUT = "prepare"
REGEX_RESIDU = re.compile(r"^v?\d+\.\d+\.\d+$")

AGENTS_FILE = os.environ.get("AGENTS_FILE", "AGENTS.md")
AGENTS_HISTORIQUE = os.environ.get("AGENTS_HISTORIQUE", "AGENTS-historique.md")
CLASSEUR_STOCKAGE = os.environ.get("CLASSEUR_STOCKAGE", "cerveau-projet/agents/classeur-variables/stockage/variables-actuelles.md")
CERBERUS_FICHE = "cerveau-projet/agents/cerberus/cerberus.md"
MAX_ENTREES_HISTORIQUE = 150

# v0.5.14 : couleur HTML fixe PAR AGENT dans l historique (rendu markdown).
# NB : nom SINGULIER - un nom pluriel terminc par 'AGENTS' casserait les
# regex permissives qui extraient le dictionnaire des agents (ex: test-092).
# Les couleurs ne sont appliquees QUE sur la ligne '###' (repere humain),
# JAMAIS sur la ligne de table (format machine exige par lire-activite-recente
# et evaluer-processus). Valeurs ASCII (#rrggbb), lisibles sur fond clair.
COULEURS_PAR_AGENT = {
    "cerberus": "#dc2626",  # gardien - rouge
    "vulcain": "#ea580c",   # forge - orange
    "morpheus": "#7c3aed",  # reves - violet
    "janus": "#0d9488",     # deux visages - teal
    "buffy": "#2563eb",     # developpeur principal - bleu
    "atlas": "#ca8a04",     # cartographe - ocre
    "themis": "#be185d",    # justice - rose
    "clio": "#65a30d",      # histoire - vert olive
    "hygie": "#16a34a",     # sante/nettoyage - vert
    "hermes": "#0284c7",    # langue - bleu ciel
    "gardien": "#475569",   # securite - ardoise
    "argus": "#9333ea",     # detection - violet vif
    "chiron": "#0891b2",    # education - cyan
    "athena": "#c026d3",    # pense-betes - fuchsia
    "promethee": "#d97706",  # specs - ambre
    "minerve": "#059669",   # todos - emeraude
    "socrate": "#a855f7",   # revision strategique - violet clair
    "redacteur-v2": "#7c3aed",
    "hades": "#4b5563",  # redaction docs v2 - violet profond
}
COULEUR_DEFAUT = "#334155"

# v0.5.15 : une entree d historique commence par une ligne de table
# ('| <span ...>agent</span> | HH:MM | AAAA-MM-JJ | session | ...') OU par
# son repere humain ('### <span ...>' colore). Les lignes '#>', '###>' et
# les continuations sont attachees a l entree precedente. NB : le repere se
# reconnait par son prefixe '### ' (aucun autre '### ' dans l historique).
# v0.5.24 : ajout de l agent redacteur-v2 (redaction des docs v2, round
# solo dedie) : couleur + triplet (role, fiche, corrections) dans AGENTS et
# COULEURS_PAR_AGENT (py + sh).
# v0.5.20 : le corps et l encart affichent l ID LLM (ex: freebuff) au lieu
# de la session (demande utilisateur : heure | agent | id | raison).
ENTREE_HISTORIQUE_RE = re.compile(r"^- \d{2}:\d{2} \|")


def couleur_agent(agent):
    """Couleur ANSI de l agent (pour affichage terminal)."""
    return COULEURS_PAR_AGENT.get((agent or "").lower(), COULEUR_DEFAUT)


def composer_bloc_historique(timestamp, identifiant, agent, raison, type_round="R"):
    """Compose une ligne d entree (format v0.6.1 timeline).

    Format sous un bloc ### Agent :
      - HH:MM | id | TYPE | raison   (TYPE = R round ou IR inter-round)
    (id = id LLM, ex: freebuff ; repli sur la session si inconnue)
    """
    heure = (timestamp or "").split(" ")[-1] if " " in (timestamp or "") else ""
    raison_nettoyee = " ".join((raison or "").split())
    # JAMAIS tronquer - l historique doit etre complet pour audit/retour
    return "- %s | %s | %s | %s\n" % (heure, identifiant or "", type_round, raison_nettoyee)
PREFIXE_SESSION = "session-llm-"

# agent : (role, fiche, corrections)
AGENTS = {
    "cerberus": ("Gardien de l'entree -- analyse et active les agents",
                 "cerveau-projet/agents/cerberus/cerberus.md",
                 "cerveau-projet/agents/cerberus/corrections.md"),
    "buffy": ("Developpeur principal -- contenu et structures",
              "cerveau-projet/agents/buffy/buffy.md",
              "cerveau-projet/agents/buffy/corrections.md"),
    "atlas": ("Explorateur -- recherche et decouverte",
              "cerveau-projet/agents/atlas/atlas.md",
              "cerveau-projet/agents/atlas/corrections.md"),
    "janus": ("Controleur des statuts -- validation et verification",
              "cerveau-projet/agents/janus/janus.md",
              "cerveau-projet/agents/janus/corrections.md"),
    "vulcain": ("Constructeur d'outils -- creation et developpement",
                "cerveau-projet/agents/vulcain/vulcain.md",
                "cerveau-projet/agents/vulcain/corrections.md"),
    "athena": ("Redactrice de pense-betes -- transformation des demandes",
               "cerveau-projet/agents/athena/athena.md",
               "cerveau-projet/agents/athena/corrections.md"),
    "morpheus": ("Testeur -- validation des outils et des tests",
                 "cerveau-projet/agents/morpheus/morpheus.md",
                 "cerveau-projet/agents/morpheus/corrections.md"),
    "promethee": ("Redacteur de specs -- specification technique",
                  "cerveau-projet/agents/promethee/promethee.md",
                  "cerveau-projet/agents/promethee/corrections.md"),
    "minerve": ("Redactrice de todos -- organisation des taches",
                "cerveau-projet/agents/minerve/minerve.md",
                "cerveau-projet/agents/minerve/corrections.md"),
    "clio": ("Muse de l'histoire -- mise a jour du README",
             "cerveau-projet/agents/clio/clio.md",
             "cerveau-projet/agents/clio/corrections.md"),
    "themis": ("Evaluatrice croisee -- evaluation et audit",
               "cerveau-projet/agents/themis/themis.md",
               "cerveau-projet/agents/themis/corrections.md"),
    "hygie": ("Agent de nettoyage -- seul agent habilite a acceder a tout le workspace et a supprimer sans demande prealable",
              "cerveau-projet/agents/hygie/hygie.md",
              "cerveau-projet/agents/hygie/corrections.md"),
    "hermes": ("Agent de la langue -- orthographe, vocabulaire et fautes de francais commises par les agents",
               "cerveau-projet/agents/hermes/hermes.md",
               "cerveau-projet/agents/hermes/corrections.md"),
    "gardien": ("Gardien du marbre -- propose la modification des zones protegees (l utilisateur valide), verifie l integrite du noyau",
                 "cerveau-projet/agents/gardien/gardien.md",
                 "cerveau-projet/agents/gardien/corrections.md"),
    "argus": ("Detecteur de contradictions -- trouve et compare les incoherences (cases, regles, protocoles, git)",
               "cerveau-projet/agents/argus/argus.md",
               "cerveau-projet/agents/argus/corrections.md"),
    "chiron": ("Educateur des agents -- formation continue",
                "cerveau-projet/agents/chiron/chiron.md",
                "cerveau-projet/agents/chiron/corrections.md"),
    "socrate": ("Conversateur de revision strategique -- discute et priorise les problemes",
                "cerveau-projet/agents/socrate/socrate.md",
                "cerveau-projet/agents/socrate/corrections.md"),
    "hades": ("Gardien des archives git -- SEUL habilite aux commandes git",
              "cerveau-projet/agents/hades/hades.md",
              "cerveau-projet/agents/hades/corrections.md"),
    "redacteur-v2": ("Redacteur des docs de la v2 (proposition, regles, conventions) -- mode conversation (reactive Cerberus sur fin de cycle)",
                "cerveau-projet/agents/redacteur-v2/redacteur-v2.md",
                "cerveau-projet/agents/redacteur-v2/corrections.md"),
}

def get_agent_info(agent):
    """Retourner (role, fiche, corrections) d'un agent (casse insensible)."""
    return AGENTS.get(agent.lower(), None)


def verifier_ascii(chaine):
    """Retourner True si la chaine est 100% ASCII."""
    return all(ord(c) < 128 for c in chaine)


def verrouiller_constitution():
    """Verrou du marbre : refuser l ecriture si la zone constitution diverge.

    Active uniquement en mode reel (AGENTS_FILE non surcharge par les tests).
    Le verrou-marbre est la source unique du calcul d empreinte.
    """
    if os.environ.get("AGENTS_FILE"):
        return True  # mode test : copies temporaires, marbre non applicable
    outil = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                         "proteger", "proteger-verrou-marbre", "proteger-verrou-marbre.py")
    try:
        rc = subprocess.call([sys.executable, outil, "--zone", "constitution"])
    except OSError as e:
        print("[AVERTISSEMENT] verrou-marbre injoignable : %s" % e)
        return True
    if rc != 0:
        print("")
        print("[BLOQUE] MARBRE : la zone constitution a ete modifiee sans protocole.")
        print("  Refus d ecrire dans AGENTS.md : le marbre protege la Constitution.")
        print("  Protocole : cerveau-projet/agents/regles-immuables/general/protocole-securite-marbre.md")
        return False
    return True


def verifier_fichier_ascii(fichier):
    """Verifier qu'un fichier entier est ASCII. Afficher les lignes concernees."""
    nb = 0
    try:
        with io.open(fichier, "r", encoding="utf-8", errors="replace") as fh:
            for i, ligne in enumerate(fh, 1):
                for ch in ligne:
                    if ord(ch) > 127:
                        nb += 1
                        print("  Ligne %d: caractere non-ASCII U+%04X" % (i, ord(ch)))
                        break
    except IOError:
        pass
    return nb == 0


def verifier_residus_racine():
    """GARDE-FOU (v0.5.2) : detecter dans le repertoire courant les fichiers
    nommes comme des versions semver pures (ex: 0.2.1, v0.2.6). Ces fichiers
    sont des residus probables de redirections accidentelles de sortie (une
    commande precedente a redirige sa sortie, souvent celle de cet outil, vers
    un fichier nomme comme une version). Anti-residu : les supprimer - les
    sources de verite de version vivent dans cerveau-projet/agents/clio/."""
    try:
        residus = sorted(n for n in os.listdir(".")
                         if os.path.isfile(n) and REGEX_RESIDU.match(n))
    except OSError:
        return
    if not residus:
        return
    print("=" * 60)
    print("!!! WARNING GARDE-FOU (activer-agent-principal v%s) !!!" % VERSION)
    print("Des fichiers nommes comme des versions semver sont presents dans le")
    print("repertoire courant (residus probables de redirections accidentelles")
    print("de sortie) :")
    for n in residus[:10]:
        print("    - %s" % n)
    print("ANTI-RESIDU : supprimez-les. Les sources de verite de version vivent")
    print("dans cerveau-projet/agents/clio/ (version-readme.txt,")
    print("statut-projet.txt), JAMAIS a la racine.")
    print("=" * 60)


def instruction_demarrage(agent):
    """Bloc DEMARRAGE OBLIGATOIRE pour un agent active (sauf Cerberus).
    v0.5.4 : corrige le bug d arret a c0 - l agent sait comment lancer son
    parcours depuis la case de depart."""
    return (
        "DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :\n"
        "python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \\\n"
        "  cerveau-projet/agents/%s/parcours/parcours-%s.json --case c0\n"
        "(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds\n"
        "a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis\n"
        "ensuite les branches case par case ; si tu reprends apres une interruption,\n"
        "reprends a la case courante avec --case <cid> --reponses '<reponse>')."
    ) % (agent, agent)


def lire_agents():
    """Lire AGENTS.md (erreur si absent)."""
    if not os.path.isfile(AGENTS_FILE):
        print("ERREUR: Le fichier %s n'existe pas" % AGENTS_FILE)
        return None
    with io.open(AGENTS_FILE, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def ecrire_agents(contenu):
    """Ecrire AGENTS.md (LF)."""
    with io.open(AGENTS_FILE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)


def migrer_si_necessaire(contenu):
    """Convertir l'ancienne structure mono-session en multi-session.
    Retourne (contenu, migre) ou migre indique si la conversion a eu lieu."""
    if "## Sessions LLM" in contenu:
        return contenu, False
    if "## Agent Principal Actuel" not in contenu:
        return contenu, False
    m = re.search(r"## Agent Principal Actuel\n(.*?)(?=\n## |\Z)", contenu, re.DOTALL)
    if not m:
        return contenu, False
    ancien = m.group(0)
    bloc = m.group(1)
    nouveau = "## Sessions LLM\n\n### Session : session-llm-1\n" + bloc + "\n"
    return contenu.replace(ancien, nouveau, 1), True


def extraire_blocs_session(contenu):
    """Retourner la liste des (session_id, texte_du_bloc) presents."""
    blocs = []
    lignes = contenu.split("\n")
    i = 0
    while i < len(lignes):
        m = re.match(r"^### Session : (.+?)\s*$", lignes[i])
        if m:
            session_id = m.group(1)
            j = i + 1
            bloc = []
            while j < len(lignes):
                if re.match(r"^### Session : ", lignes[j]) or lignes[j].startswith("## "):
                    break
                bloc.append(lignes[j])
                j += 1
            blocs.append((session_id, "\n".join(bloc)))
            i = j
        else:
            i += 1
    return blocs


def trouver_prochaine_session(contenu):
    """Trouver le prochain session-llm-N libre."""
    existantes = set(s for s, _ in extraire_blocs_session(contenu))
    n = 1
    while (PREFIXE_SESSION + str(n)) in existantes:
        n += 1
    return PREFIXE_SESSION + str(n)


def trouver_session_par_id(llm_id):
    """Retrouver la session liee a un llm-id (ou None).
    SOURCE DOUBLE (v0.4.0) : 1) AGENTS.md -- bloc avec le champ '**Nom LLM** | <id>'
    (ancien nom **Id LLM** accepte) ; 2) classeur -- ligne profil-session avec
    'id: <llm-id>'. Permet au LLM de se reconnaitre directement en lisant AGENTS.md."""
    # 1. AGENTS.md : champ Nom LLM dans les blocs de session
    if os.path.isfile(AGENTS_FILE):
        with io.open(AGENTS_FILE, "r", encoding="utf-8", errors="replace") as fh:
            contenu = fh.read()
        for session, bloc in extraire_blocs_session(contenu):
            m = re.search(r"\*\*(?:Id LLM|Nom LLM)\*\* \| ([^|]+)", bloc)
            if m and m.group(1).strip() == llm_id:
                return session
    # 2. Classeur : liaison id dans les lignes profil-session
    fichier = CLASSEUR_STOCKAGE
    if os.path.isfile(fichier):
        with io.open(fichier, "r", encoding="utf-8", errors="replace") as fh:
            contenu = fh.read()
        for ligne in contenu.split(chr(10)):
            if "id: " + llm_id in ligne:
                m = re.search(r"session: (session-llm-\d+)", ligne)
                if m:
                    return m.group(1)
    return None


def id_lie_a_session(session_id):
    """Retourner l'id LLM lie a une session (AGENTS.md champ Nom LLM, puis classeur),
    ou None si la session n'est liee a aucun id. Utile pour detecter un CONFLIT
    d'alignement (v0.4.0) : session-llm-N deja liee a un autre id."""
    # 1. AGENTS.md
    if os.path.isfile(AGENTS_FILE):
        with io.open(AGENTS_FILE, "r", encoding="utf-8", errors="replace") as fh:
            contenu = fh.read()
        for session, bloc in extraire_blocs_session(contenu):
            if session == session_id:
                m = re.search(r"\*\*(?:Id LLM|Nom LLM)\*\* \| ([^|]+)", bloc)
                if m and m.group(1).strip():
                    return m.group(1).strip()
    # 2. Classeur
    fichier = CLASSEUR_STOCKAGE
    if os.path.isfile(fichier):
        with io.open(fichier, "r", encoding="utf-8", errors="replace") as fh:
            contenu = fh.read()
        for ligne in contenu.split(chr(10)):
            if "session: " + session_id in ligne:
                m = re.search(r"id: (\S+)", ligne)
                if m:
                    return m.group(1)
    return None


def session_cible_pour_id(llm_id):
    """REGLE ALIGNEMENT (v0.4.0) : id llm-N -> session-llm-N (le numero de session
    porte le numero de l'id). Retourne la session cible, ou None si l'id n'est pas
    de la forme llm-N (ex: llm-atlas -> pas d'alignement, prochaine libre)."""
    m = re.match(r"^llm-(\d+)$", llm_id)
    if m:
        return PREFIXE_SESSION + m.group(1)
    return None


def poser_nom_llm_bloc(contenu, session_id, llm_id):
    """Ajouter ou mettre a jour le champ '**Nom LLM** | <id>' EN TETE du bloc de
    session (convention v0.5.0 : nom-llm avant nom-agent). L'ancien champ
    **Id LLM** est migre automatiquement vers **Nom LLM**. Retourne le contenu."""
    return editer_champs_session(contenu, session_id, {"Nom LLM": llm_id})


def creer_session(contenu, session_id, llm_id=None):
    """Ajouter un bloc de session (Cerberus par defaut) apres ## Sessions LLM.
    Si llm_id fourni (v0.4.0), le champ **Nom LLM** est ecrit en tete du bloc."""
    if any(s == session_id for s, _ in extraire_blocs_session(contenu)):
        return contenu
    info = get_agent_info("cerberus")
    role, fiche, corrections = info
    date = datetime.now().strftime("%Y-%m-%d")
    champ_id = ""
    if llm_id:
        champ_id = "| **Nom LLM** | %s |\n" % llm_id
    bloc = (
        "\n### Session : %s\n\n"
        "| Champ | Valeur |\n"
        "|---|---|\n"
    ) % session_id
    bloc += champ_id
    bloc += (
        "| **Nom Agent** | Cerberus |\n"
        "| **Role Agent** | %s |\n"
        "| **Derniere mise a jour** | %s |\n"
        "| **Fiche** | [%s](%s) |\n"
        "| **Corrections** | [%s](%s) |\n"
        "| **Active par** | Identification |\n"
        "| **Raison** | Identification LLM - demarrage de session |\n"
    ) % (role, date, fiche, fiche, corrections, corrections)
    lignes = contenu.split("\n")
    sortie = []
    insere = False
    for ligne in lignes:
        sortie.append(ligne)
        if re.match(r"^## Sessions LLM\s*$", ligne) and not insere:
            sortie.append(bloc)
            insere = True
    if not insere:
        print("ERREUR: Section ## Sessions LLM introuvable dans %s" % AGENTS_FILE)
        return None
    return "\n".join(sortie)


def editer_champs_session(contenu, session_id, champs):
    """Remplacer les champs (dict nom -> valeur) du bloc de session_id uniquement.
    Convention v0.5.0 : reconstruction complete du bloc dans l'ordre canonique --
    les anciens noms de champs (Nom, Role, Id LLM) sont migres automatiquement vers
    les nouveaux (Nom Agent, Role Agent, Nom LLM), les champs manquants sont inseres
    a leur position, Nom LLM est place EN TETE."""
    ORDRE = ["Nom LLM", "Nom Agent", "Role Agent", "Derniere mise a jour",
             "Fiche", "Corrections", "Active par", "Raison"]

    def reconstruire_bloc(bloc, champs):
        """Analyser les lignes d'un bloc, appliquer les champs, reemettre dans l'ordre.
        v0.5.4 : la Raison peut etre MULTILIGNE (les lignes suivantes sans '| **')
        sont des continuations de la Raison - elles sont conservees et recollees."""
        valeurs = {}
        continuations = {}
        i = 0
        while i < len(bloc):
            ligne = bloc[i]
            m = re.match(r"^\| \*\*([^*]+)\*\* \| (.*) \|$", ligne)
            if not m:
                i += 1
                continue
            champ = m.group(1).strip()
            valeur = m.group(2).strip()
            # capturer les lignes de continuation de ce champ (Raison multiligne)
            suivantes = []
            j = i + 1
            while j < len(bloc) and not re.match(r"^\| \*\*([^*]+)\*\* \|", bloc[j]):
                suivantes.append(bloc[j])
                j += 1
            if suivantes:
                continuations[champ] = suivantes
            # Migration anciens noms
            if champ == "Nom":
                champ = "Nom Agent"
            elif champ == "Role":
                champ = "Role Agent"
            elif champ == "Id LLM":
                champ = "Nom LLM"
            # Fiche/Corrections : extraire le chemin depuis [x](x)
            if champ in ("Fiche", "Corrections"):
                mm = re.match(r"^\[(.*)\]\((.*)\)$", valeur)
                if mm:
                    valeur = mm.group(2)
            valeurs[champ] = valeur
            i = j
        valeurs.update(champs)
        # Recollement des continuations (Raison multiligne) sur le champ mis a jour.
        # v0.5.5 : si le champ a ETE REMPLACE (present dans champs), l'ancienne
        # suite est IGNOREE (y compris la Raison) - le bug v0.5.4 faisait une
        # exception pour la Raison et recolait les anciennes continuations
        # (blocs DEMARRAGE) a chaque nouvelle raison -> accumulation infinie.
        for champ_c, suite in continuations.items():
            if champ_c in champs:
                # champ remplace par un nouveau : ignorer l'ancienne suite
                continue
            if champ_c in valeurs:
                valeurs[champ_c] = valeurs[champ_c] + "\n" + "\n".join(suite)
        nouvelles = ["", "| Champ | Valeur |", "|---|---|"]
        for champ in ORDRE:
            if champ in valeurs:
                v = valeurs[champ]
                if champ in ("Fiche", "Corrections"):
                    nouvelles.append("| **%s** | [%s](%s) |" % (champ, v, v))
                elif champ == "Raison" and "\n" in v:
                    # Raison multiligne : premiere ligne dans la cellule, les
                    # suivantes en lignes brutes (format historique de AGENTS.md)
                    lignes_raison = v.split("\n")
                    nouvelles.append("| **%s** | %s |" % (champ, lignes_raison[0]))
                    for suite in lignes_raison[1:]:
                        nouvelles.append(suite)
                else:
                    nouvelles.append("| **%s** | %s |" % (champ, v))
        # Champs inconnus conserves (s'ils existaient dans le bloc)
        for champ, v in valeurs.items():
            if champ not in ORDRE:
                nouvelles.append("| **%s** | %s |" % (champ, v))
        return nouvelles

    lignes = contenu.split("\n")
    sortie = []
    i = 0
    while i < len(lignes):
        ligne = lignes[i]
        if re.match(r"^### Session : " + re.escape(session_id) + r"\s*$", ligne):
            sortie.append(ligne)
            i += 1
            bloc = []
            while i < len(lignes) and not (re.match(r"^### Session : ", lignes[i]) or lignes[i].startswith("## ")):
                bloc.append(lignes[i])
                i += 1
            sortie.extend(reconstruire_bloc(bloc, champs))
            continue
        sortie.append(ligne)
        i += 1
    return "\n".join(sortie)


def ajouter_historique(timestamp, session, agent, raison, type_round="R"):
    """Ajouter une entree dans le fichier historique, max 150.

    Format v0.6.2 timeline :
      ## YYYY-MM-DD
      ### Agent
      - HH:MM | id | TYPE | raison   (TYPE = R round ou IR inter-round)

    La colonne porte l ID LLM (resolu depuis la session via id_lie_a_session,
    repli sur la session si aucun id lie). Aussi met a jour l encart
    'Activites recentes' en haut du fichier (header : id).
    """
    if not os.path.isfile(AGENTS_HISTORIQUE):
        print("ERREUR: Le fichier %s n'existe pas" % AGENTS_HISTORIQUE)
        return 1

    identifiant = id_lie_a_session(session) or session
    nouvelle_ligne = composer_bloc_historique(timestamp, identifiant, agent, raison, type_round)

    if not verifier_ascii(nouvelle_ligne):
        print("ERREUR: Caractere non-ASCII detecte dans la raison - ecriture historique REFUSEE")
        return 1

    with io.open(AGENTS_HISTORIQUE, "r", encoding="utf-8", errors="replace") as fh:
        contenu = fh.read()

    # Extraire la date et convertir en JJ/MM/AAAA
    date_raw = (timestamp or "").split(" ")[0] if " " in (timestamp or "") else ""
    if len(date_raw) == 10 and date_raw[4] == "-":
        parts = date_raw.split("-")
        date = "%s/%s/%s" % (parts[2], parts[1], parts[0])
    else:
        date = date_raw
    heure = (timestamp or "").split(" ")[-1] if " " in (timestamp or "") else ""
    agent_titre = (agent or "Inconnu")

    # 1. Inserer dans le bloc jour/agent (format timeline)
    marqueur_jour = "## %s" % date
    marqueur_agent = "### %s" % agent_titre
   
    if marqueur_jour in contenu:
        # v0.5.21 : borner la recherche du bloc agent A LA SECTION DU JOUR.
        # Avant, contenu.index(marqueur_agent) trouvait le PREMIER '### <agent>'
        # du fichier (souvent dans un jour anterieur) et y inserait l entree
        # (les entrees Cerberus du jour courant tombaient dans le bloc du jour
        # precedent).
        idx_jour = contenu.index(marqueur_jour)
        fin_jour = contenu.find("\n## ", idx_jour + len(marqueur_jour))
        if fin_jour == -1:
            fin_jour = len(contenu)
        section_jour = contenu[idx_jour:fin_jour]
        if marqueur_agent in section_jour:
            idx_agent = idx_jour + section_jour.index(marqueur_agent)
            pos_inser = idx_agent + len(marqueur_agent)
            if pos_inser < len(contenu) and contenu[pos_inser] == "\n":
                pos_inser += 1
            contenu = contenu[:pos_inser] + nouvelle_ligne + contenu[pos_inser:]
        else:
            contenu = contenu[:idx_jour + len(marqueur_jour)] + "\n\n" + marqueur_agent + "\n" + nouvelle_ligne + contenu[idx_jour + len(marqueur_jour):]
    else:
        # v0.5.21 : inserer APRES l encart 'Activites recentes' (jamais entre
        # l en-tete et l encart). Cible : la premiere section jour existante
        # (## JJ/MM/AAAA) ; repli : apres l encart, puis fin de l en-tete.
        m_section = re.search(r"^## \d{2}/\d{2}/\d{4}", contenu, re.MULTILINE)
        if m_section:
            idx_inser = m_section.start()
        else:
            idx_encart = contenu.find("## Activites recentes")
            if idx_encart != -1:
                idx_apres = contenu.find("\n---\n", idx_encart)
                idx_inser = idx_apres + len("\n---\n") if idx_apres != -1 else len(contenu)
            else:
                idx_entete = contenu.find("\n---\n")
                idx_inser = idx_entete + len("\n---\n") if idx_entete != -1 else 0
        nouveau_bloc = "\n" + marqueur_jour + "\n\n" + marqueur_agent + "\n" + nouvelle_ligne
        contenu = contenu[:idx_inser] + nouveau_bloc + contenu[idx_inser:]

    # 2. Mettre a jour l encart 'Activites recentes' (10 dernieres)
    contenu = maj_encart_activites(contenu, date, heure, agent_titre, identifiant, raison)

    with io.open(AGENTS_HISTORIQUE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(contenu)

    if not verifier_fichier_ascii(AGENTS_HISTORIQUE):
        print("WARNING: Caracteres non-ASCII presents dans %s" % AGENTS_HISTORIQUE)

    print("Historique mis a jour dans %s" % AGENTS_HISTORIQUE)
    return 0


def maj_encart_activites(contenu, date, heure, agent, identifiant, raison):
    """Mettre a jour l encart 'Activites recentes' en haut du fichier.

    Extrait les 10 dernieres entrees du fichier et les place dans un
    tableau visible en haut, entre l en-tete et l historique par jour.
    Colonne : id (id LLM, ex: freebuff).
    """
    # Extraire toutes les entrees du format timeline avec l agent et la date
    entrees = []
    agent_courant = "?"
    date_courante = ""
    for ligne in contenu.split("\n"):
        l = ligne.strip()
        if l.startswith("## ") and not l.startswith("## Activites"):
            date_courante = l[3:].strip()
        elif l.startswith("### "):
            agent_courant = l[4:].strip()
        elif l.startswith("- ") and " | " in l:
            parties = l[2:].split(" | ", 3)
            if len(parties) >= 3:
                h = parties[0].strip()
                s = parties[1].strip()
                if len(parties) == 4:
                    t = parties[2].strip()
                    r = parties[3].strip()
                else:
                    t = ""
                    r = parties[2].strip()
                # Cle de tri : date + heure (JJ/MM/AAAA HH:MM)
                cle_tri = "%s %s" % (date_courante, h)
                entrees.append((cle_tri, h, agent_courant, s, r, t))

    # Trier par date/heure decroissante et prendre les 10 plus recentes
    entrees.sort(key=lambda x: x[0], reverse=True)
    recentes = [(h, a, s, r, t) for _, h, a, s, r, t in entrees[:10]]

    # Construire l encart
    encart = "---\n\n## Activites recentes (10)\n\n"
    encart += "| Heure | Agent | id | Type | Raison |\n"
    encart += "|-------|-------|----|------|--------|\n"
    for h, a, s, r, t in recentes:
        r_aff = r if len(r) <= 80 else r[:77] + "..."
        encart += "| %s | %s | %s | %s | %s |\n" % (h, a, s, t, r_aff)
    encart += "\n---\n"

    # Remplacer l ancien encart (s il existe) ou l inserer
    marqueur_debut = "## Activites recentes"
    marqueur_fin = "---\n\n## "
   
    if marqueur_debut in contenu:
        idx_debut = contenu.index(marqueur_debut)
        # Remonter au debut de la section (lignes precedentes)
        while idx_debut > 0 and contenu[idx_debut - 1] in "\n\r":
            idx_debut -= 1
        # Trouver la fin (prochain ## apres le debut)
        idx_fin = contenu.find("\n## ", idx_debut + len(marqueur_debut))
        if idx_fin == -1:
            idx_fin = contenu.find("\n---\n\n## ", idx_debut)
        if idx_fin != -1:
            contenu = contenu[:idx_debut] + encart + contenu[idx_fin:]
        else:
            contenu = contenu[:idx_debut] + encart
    else:
        # Inserer apres le premier ---
        idx = contenu.find("\n---\n")
        if idx != -1:
            contenu = contenu[:idx + 5] + "\n" + encart + contenu[idx + 5:]
        else:
            contenu = encart + contenu

    return contenu


def mettre_a_jour_sessions_connues(contenu):
    """Reconstruire la section '## Sessions connues' d'AGENTS.md a partir du
    classeur-variables (lignes profil-session-*). La section liste toutes les
    sessions existantes (session, id LLM, agent actif, derniere activite) pour
    que chaque LLM sache que les autres existent et voie leur activite en temps
    reel. Retourne le contenu modifie (section remplacee ou inseree)."""
    if not os.path.isfile(CLASSEUR_STOCKAGE):
        return contenu
    lignes = []
    with io.open(CLASSEUR_STOCKAGE, "r", encoding="utf-8", errors="replace") as fh:
        for ligne in fh:
            if "profil-session-" not in ligne:
                continue
            m = re.search(r"session: (session-llm-\d+)", ligne)
            if not m:
                continue
            session = m.group(1)
            mid = re.search(r"id: (\S+)", ligne)
            llm_id = mid.group(1) if mid else "-"
            mage = re.search(r"agent: (\S+)", ligne)
            agent = mage.group(1) if mage else "?"
            mdate = re.search(r"date: (\S+ \S+)", ligne)
            date = mdate.group(1) if mdate else "-"
            lignes.append((session, llm_id, agent, date))
    if not lignes:
        return contenu

    def cle_session(entree):
        m = re.search(r"session-llm-(\d+)", entree[0])
        return int(m.group(1)) if m else 0

    lignes.sort(key=cle_session)
    table = ("## Sessions connues\n\n"
             "| Session | Nom LLM | Agent actif | Derniere activite |\n"
             "|---|---|---|---|\n")
    for session, llm_id, agent, date in lignes:
        table += "| %s | %s | %s | %s |\n" % (session, llm_id, agent, date)

    # Retirer une section existante (jusqu'a la prochaine section ## OU un
    # marqueur du marbre <!-- MARBRE: --> : les outils ne doivent JAMAIS
    # avaler les bornes des zones protegees - bug detecte par le marbre
    # 2026-08-15 (le DEBUT de la zone constitution a ete mange par cette boucle)
    ls = contenu.split("\n")
    sortie = []
    i = 0
    while i < len(ls):
        if ls[i].strip() == "## Sessions connues":
            i += 1
            while i < len(ls) and not ls[i].startswith("## ") \
                    and not ls[i].startswith("<!-- MARBRE:"):
                i += 1
            continue
        sortie.append(ls[i])
        i += 1
    contenu = "\n".join(sortie)

    # Inserer avant '## Configuration Active' (ou en fin si absente)
    if "## Configuration Active" in contenu:
        contenu = contenu.replace("## Configuration Active",
                                  table + "## Configuration Active", 1)
    else:
        contenu = contenu.rstrip("\n") + "\n\n" + table
    return contenu


def actualiser_sessions_connues():
    """Relire AGENTS.md, reconstruire la section '## Sessions connues' (a partir
    du classeur a jour) et reecrire. A appeler APRES la mise a jour du profil
    session pour que la section reflete l'etat courant."""
    contenu = lire_agents()
    if contenu is None:
        return
    contenu = mettre_a_jour_sessions_connues(contenu)
    ecrire_agents(contenu)


def mettre_a_jour_profil_session(session, agent, llm_id=None):
    """Ecrire ou mettre a jour profil-session-<session> dans le classeur-variables.
    Format : | `profil-session-<session>` | session: <session> [/ id: <llm-id>] / agent: <agent> / date: <AAAA-MM-JJ HH:MM> | activer-agent-principal | <AAAA-MM-JJ> | [OK] |
    REGLE LIAISON ID (v0.3.5) : quand llm_id n'est pas fourni (activer/reactiver),
    PRESERVER l'id deja lie a la session dans la ligne existante -- sinon la liaison
    id<->session posee par sidentifier serait ECRASEE et le prochain sidentifier
    creerait une nouvelle session (sessions fantomes)."""
    fichier = CLASSEUR_STOCKAGE
    if not os.path.isfile(fichier):
        print("WARNING: Fichier classeur %s introuvable - profil session non ecrit" % fichier)
        return 1

    maintenant = datetime.now()
    ts = maintenant.strftime("%Y-%m-%d %H:%M:%S.%f")
    jour = maintenant.strftime("%Y-%m-%d")
    # REGLE DE DERIVATION (IMMUABLE): id = profil-session- + partie apres le prefixe session-
    id_session = session[len("session-"):] if session.startswith("session-") else session
    prefixe_ligne = "| `profil-session-" + id_session + "`"

    with io.open(fichier, "r", encoding="utf-8", errors="replace") as fh:
        lignes = fh.read().split(chr(10))

    # REGLE LIAISON ID (v0.3.5): preserver l'id existant si non fourni
    if llm_id is None:
        for l in lignes:
            if l.startswith(prefixe_ligne):
                m = re.search(r"id: (\S+)", l)
                if m:
                    llm_id = m.group(1)
                break

    if llm_id:
        nouvelle_ligne = ("| `profil-session-%s` | session: %s / id: %s / agent: %s / date: %s | "
                          "activer-agent-principal | %s | [OK] |") % (id_session, session, llm_id, agent, ts, jour)
    else:
        nouvelle_ligne = ("| `profil-session-%s` | session: %s / agent: %s / date: %s | "
                          "activer-agent-principal | %s | [OK] |") % (id_session, session, agent, ts, jour)

    if not verifier_ascii(nouvelle_ligne):
        print("ERREUR: Caractere non-ASCII dans le profil session - ecriture classeur REFUSEE")
        return 1

    trouve = False
    for i, l in enumerate(lignes):
        if l.startswith(prefixe_ligne):
            lignes[i] = nouvelle_ligne
            trouve = True
            break
    if not trouve:
        idx = -1
        for i, l in enumerate(lignes):
            if l.startswith("| `"):
                idx = i
        if idx >= 0:
            lignes.insert(idx + 1, nouvelle_ligne)
        else:
            lignes.append(nouvelle_ligne)

    with io.open(fichier, "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(chr(10).join(lignes))

    print("Profil session mis a jour dans %s : %s (%s)" % (fichier, session, agent))
    return 0


def agent_actif_bloc(contenu, session_id):
    """Retourner l'agent REEL du bloc de session (champ Nom Agent), ou Cerberus
    si le champ est absent. CORRECTION v0.5.1 : sidentifier ecrivait Cerberus
    en dur, ce qui falsifiait le profil classeur quand un AUTRE agent (ex:
    morpheus) etait actif -> double source contradictoire -> l agent s arretait
    au demarrage."""
    for sid, bloc in extraire_blocs_session(contenu):
        if sid == session_id:
            m = re.search(r"\*\*(?:Nom Agent|Nom)\*\* \| ([^|]+)", bloc)
            if m and m.group(1).strip():
                return m.group(1).strip()
            return "Cerberus"
    return "Cerberus"


def sidentifier(llm_id=None):
    """Creer/choisir la session du LLM (agent principal = Cerberus).
    REGLE UTILISATEUR (mode ID) : chaque LLM possede SON id (donne par
    l'utilisateur au lancement).
    REGLE ALIGNEMENT (v0.4.0) : id llm-N -> session-llm-N. Le numero de session
    porte le numero de l'id. Conflit gere : si session-llm-N est deja liee a un
    AUTRE id, message clair + attribution de la prochaine session libre.
    SOURCE DOUBLE : l'outil cherche la liaison dans AGENTS.md (champ **Nom LLM**)
    puis dans le classeur (id: <llm-id>). Le LLM peut donc se reconnaitre en
    lisant AGENTS.md.
    - id deja lie -> c'est SA session (retrouvee)
    - id inconnu llm-N -> session-llm-N si libre (ou orpheline), sinon prochaine libre
    - id inconnu non numerique (llm-atlas) -> prochaine session libre + liaison
    - sans argument -> compatibilite heritage : prochaine session libre"""
    contenu = lire_agents()
    if contenu is None:
        return 1
    contenu, migre = migrer_si_necessaire(contenu)

    if llm_id is not None:
        llm_id = llm_id.strip()
        session_liee = trouver_session_par_id(llm_id)
        if session_liee:
            session = session_liee
            agent_actif = agent_actif_bloc(contenu, session)
            print("Session retrouvee pour id %s : %s (agent principal : %s)"
                  % (llm_id, session, agent_actif))
        else:
            # REGLE ALIGNEMENT (v0.4.0) : id llm-N -> session-llm-N
            cible = session_cible_pour_id(llm_id)
            if cible:
                id_deja_lie = id_lie_a_session(cible)
                if id_deja_lie is not None and id_deja_lie != llm_id:
                    # CONFLIT : session-llm-N deja liee a un autre LLM
                    session = "session-llm-1" if migre else trouver_prochaine_session(contenu)
                    print("ATTENTION: %s deja liee a l'id %s - attribution %s (agent principal : Cerberus)"
                          % (cible, id_deja_lie, session))
                else:
                    # Libre ou orpheline (aucun id) -> absorption
                    session = cible
                    print("Nouvelle session pour id %s : %s (alignee sur l'id, agent principal : Cerberus)"
                          % (llm_id, session))
            else:
                session = "session-llm-1" if migre else trouver_prochaine_session(contenu)
                print("Nouvelle session pour id %s : %s (agent principal : Cerberus)"
                      % (llm_id, session))
    else:
        # Sans argument : premier LLM -> llm-1 (via migration), sinon prochaine libre
        session = "session-llm-1" if migre else trouver_prochaine_session(contenu)
        print("Session attribuee : %s (agent principal : Cerberus)" % session)

    if not any(s == session for s, _ in extraire_blocs_session(contenu)):
        contenu = creer_session(contenu, session, llm_id)
        if contenu is None:
            return 1
        ecrire_agents(contenu)
    elif llm_id is not None:
        # Bloc existant : poser/mettre a jour le champ Nom LLM (reconnaissance par lecture)
        contenu = poser_nom_llm_bloc(contenu, session, llm_id)
        ecrire_agents(contenu)

    agent_actif = agent_actif_bloc(contenu, session)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    ajouter_historique(timestamp, session, agent_actif, "Identification LLM - demarrage de session", "R")
    mettre_a_jour_profil_session(session, agent_actif, llm_id)
    actualiser_sessions_connues()
    return 0


CHRONO_OUTIL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                            "..", "chronometrer", "chronometrer-duree",
                            "chronometrer-duree.py")


def appeler_chrono(args):
    """Appelle chronometrer-duree en subprocess (pattern proteger-verrou-marbre).
    Retourne (rc, sortie). En mode test (AGENTS_FILE surcharge), le chrono est
    neutralise : le fichier CHRONOS_FICHIER est surcharge dans un dossier temp."""
    cmd = [sys.executable, CHRONO_OUTIL] + args + ["--confirme-doc"]
    env = dict(os.environ)
    if os.environ.get("AGENTS_FILE"):
        # mode test : chrono isole dans un fichier temporaire par session
        env["CHRONOS_FICHIER"] = os.path.join(
            os.path.dirname(os.environ.get("AGENTS_FILE", "")),
            "chronos-test.jsonl")
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=10,
                           env=env)
        return p.returncode, (p.stdout or "").strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        print("[AVERTISSEMENT] chronometrer-duree injoignable : %s" % e)
        return 1, ""


ANALYSEUR_TOKENS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "..", "analyser", "analyser-tokens",
                                 "analyser-tokens.py")


def appeler_analyser_tokens(args):
    """Appelle analyser-tokens en subprocess (mode machine --snapshot).
    Retourne (rc, sortie). En mode test, TOKENS_SESSION est surcharge pour
    un comportement deterministe (option --tokens-mock)."""
    cmd = [sys.executable, ANALYSEUR_TOKENS] + args
    env = dict(os.environ)
    mock = os.environ.get("TOKENS_MOCK")
    if mock:
        env["TOKENS_SESSION"] = mock
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=10,
                           env=env)
        return p.returncode, (p.stdout or "").strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        print("[AVERTISSEMENT] analyser-tokens injoignable : %s" % e)
        return 1, ""


def snapshot_tokens():
    """Snapshot cumulatif courant des tokens (JSON machine). Retourne dict
    ou None si injoignable. Mode hybride : API (TOKENS_SESSION) si fournie,
    sinon estimation locale par taille des traces."""
    rc, sortie = appeler_analyser_tokens(["--snapshot"])
    if rc != 0 or not sortie:
        return None
    try:
        m = json.loads(sortie.split("\n")[0])
        if isinstance(m, dict):
            return m
    except ValueError:
        pass
    return None


def arreter_chrono_session(session):
    """Arrete le chrono ouvert de la session. Retourne (agent, duree,
    tokens_debut) ou (None, None, None) si aucun chrono actif."""
    rc, sortie = appeler_chrono(["arreter", session])
    if rc != 0 or not sortie or sortie == "AUCUN_CHRONO":
        return None, None, None
    parties = sortie.split("|")
    if len(parties) >= 2:
        # la sortie est 'agent | duree' suivie des MESSAGES POUR L AGENT
        # sur les lignes suivantes : ne garder que la 1re ligne de la duree
        # (sinon les messages parasites sont inseres dans le repere ### de
        # AGENTS-historique -- bug detecte par test-098 via la non-regression
        # Janus 2026-08-19, mission chronometre).
        duree = parties[1].strip().split("\n")[0].strip()
        tokens_debut = None
        if len(parties) >= 3:
            # le 3e champ est le JSON tokens_debut SUIVI des MESSAGES POUR
            # L AGENT : ne garder que la 1re ligne (meme piege que la duree).
            try:
                tokens_debut = json.loads(
                    parties[2].strip().split("\n")[0])
            except ValueError:
                tokens_debut = None
        return parties[0].strip(), duree, tokens_debut
    return None, None, None


def demarrer_chrono_session(session, agent):
    """Demarre le chrono de l agent nouvellement active, avec le snapshot
    tokens de debut (pour la difference par intervention)."""
    snap = snapshot_tokens()
    args = ["demarrer", session, agent]
    if snap:
        args += ["--tokens", json.dumps(snap, ensure_ascii=True)]
    appeler_chrono(args)


def ajouter_duree_repere(agent, duree, conso=None):
    """Ajoute '(duree, tokens: Xk env / Yk recus)' au repere '###' de la
    DERNIERE entree de l agent dans AGENTS-historique. Ne fait rien si
    l agent est inconnu ou si le repere porte deja une duree."""
    if not duree or not os.path.isfile(AGENTS_HISTORIQUE):
        return
    texte_conso = formater_conso_tokens(conso)
    suffixe = " (%s)" % duree
    if texte_conso:
        suffixe = " (%s, %s)" % (duree, texte_conso)
    with io.open(AGENTS_HISTORIQUE, "r", encoding="utf-8",
                 errors="replace") as fh:
        lignes = fh.readlines()
    cible = None
    motif_repere = re.compile(
        r"- <span style=\"color:#[0-9a-f]{6}\">%s</span>" % re.escape(agent))
    for idx, ligne in enumerate(lignes):
        if not ligne.startswith("### <span"):
            continue
        if not motif_repere.search(ligne):
            continue
        cible = idx
        break  # la 1re occurrence = la plus recente (ordre decroissant)
    if cible is None:
        return
    ligne = lignes[cible].rstrip("\n")
    if "(" in ligne and "min" in ligne:
        return  # deja une duree
    lignes[cible] = ligne + suffixe + "\n"
    with io.open(AGENTS_HISTORIQUE, "w", encoding="utf-8", newline="\n") as fh:
        fh.writelines(lignes)


def formater_conso_tokens(conso):
    """Formate la conso tokens pour le repere : '12.4k env / 8.2k recus'.
    Retourne '' si nulle ou absente (parite avec analyser-tokens)."""
    if not conso:
        return ""
    env = int(conso.get("envoyes", 0) or 0)
    rec = int(conso.get("recus", 0) or 0)
    if env == 0 and rec == 0:
        return ""
    def _k(n):
        if n >= 1000:
            return "%.1fk" % (n / 1000.0)
        return str(n)
    return "tokens: %s env / %s recus" % (_k(env), _k(rec))


def conso_tokens_intervention(tokens_debut):
    """Conso de l intervention = snapshot fin - snapshot debut (compteurs
    cumulatifs). Retourne dict {envoyes, recus, fiable} ou None."""
    if not tokens_debut:
        return None
    snap_fin = snapshot_tokens()
    if not snap_fin:
        return None
    try:
        env = max(0, int(snap_fin.get("envoyes", 0))
                  - int(tokens_debut.get("envoyes", 0)))
        rec = max(0, int(snap_fin.get("recus", 0))
                  - int(tokens_debut.get("recus", 0)))
    except (TypeError, ValueError):
        return None
    return {"envoyes": env, "recus": rec,
            "fiable": bool(tokens_debut.get("fiable"))
                       and bool(snap_fin.get("fiable"))}


def activer_agent(session, agent, raison, mission=None, type_round="R"):
    """Activer un agent dans la session (ne touche que son bloc)."""
    if not verifier_ascii(raison):
        print("ERREUR: Caractere non-ASCII detecte dans la raison - activation REFUSEE")
        return 1

    info = get_agent_info(agent)
    if info is None:
        print("ERREUR: Agent inconnu '%s'" % agent)
        return 1

    contenu = lire_agents()
    if contenu is None:
        return 1
    contenu, _ = migrer_si_necessaire(contenu)

    # GARDE-FOU (v0.5.22) : relais de chaine autorise (Pattern 8, decision
    # utilisateur Option A 2026-08-21 : l agent suivant active l agent suivant
    # pour continuer la boucle). Si un agent autre que Cerberus est encore
    # actif dans la session :
    #   - Agent cible = Cerberus (reactivation) : toujours autorise
    #   - Meme agent cible (auto-reactivation) : AVERTISSEMENT, autorise
    #   - Agent different (relais de chaine) : AVERTISSEMENT, AUTORISE
    #     (chaque maillon active le suivant a sa fin de carte - Pattern 8)
    #   - --forcer : option conservee (avertissement forcee, compatibilite)
    agent_actuel = agent_actif_bloc(contenu, session)
    if agent_actuel and agent_actuel.lower() != "cerberus":
        forcer = "--forcer" in sys.argv
        if agent.lower() == "cerberus":
            # Reactivation de Cerberus : toujours autorise
            pass
        elif agent.lower() == agent_actuel.lower():
            # Auto-reactivation : avertissement uniquement
            print("")
            print("=== AVERTISSEMENT GARDE-FOU (agent oublie) ===")
            print("L agent '%s' est encore actif dans %s." % (agent_actuel, session))
            print("Il a probablement oublie de reactiver Cerberus.")
            print("Auto-reactivation de '%s' autorisee." % agent)
            print("==============================================")
            print("")
        elif forcer:
            # Activation forcee : avertissement + continuation
            print("")
            print("=== AVERTISSEMENT GARDE-FOU (activation forcee) ===")
            print("L agent '%s' est encore actif dans %s." % (agent_actuel, session))
            print("Activation de '%s' FORCEE (--forcer)." % agent)
            print("Le travail de '%s' risque d etre perdu." % agent_actuel)
            print("===========================================================")
            print("")
        else:
            # RELAIS DE CHAINE : autorise sans avertissement (Pattern 8, v0.5.29).
            # Chaque maillon active le suivant a sa fin de carte : c'est le
            # comportement normal, plus besoin d'avertir.
            pass

    if not any(s == session for s, _ in extraire_blocs_session(contenu)):
        contenu = creer_session(contenu, session)
        if contenu is None:
            return 1

    role, fiche, corrections = info
    date = datetime.now().strftime("%Y-%m-%d")
    # v0.5.4 : ajouter l'instruction de demarrage a la Raison quand un agent
    # (autre que Cerberus) est active - anti-bug d arret a la case c0.
    raison_finale = raison
    if agent.lower() != "cerberus" and "DEMARRAGE OBLIGATOIRE" not in raison:
        raison_finale = raison + "\n\n" + instruction_demarrage(agent)
    champs = {
        "Nom Agent": agent,
        "Role Agent": role,
        "Derniere mise a jour": date,
        "Fiche": fiche,
        "Corrections": corrections,
        "Active par": "Cerberus (automatique)",
        "Raison": raison_finale,
    }
    # v0.5.16+ : chronometrage + tokens de l intervention - on ferme le
    # chrono de l agent precedent (passage de relais) et on ajoute sa duree
    # ET sa conso tokens (difference debut/fin) au repere de son entree dans
    # l historique, PUIS on ouvre le chrono du nouvel agent (sa propre duree
    # et sa conso seront connues au prochain passage de relais).
    agent_prec, duree_prec, tokens_prec = arreter_chrono_session(session)
    if agent_prec and duree_prec:
        conso_prec = conso_tokens_intervention(tokens_prec)
        ajouter_duree_repere(agent_prec, duree_prec, conso_prec)
    demarrer_chrono_session(session, agent)

    contenu = editer_champs_session(contenu, session, champs)
    ecrire_agents(contenu)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    ajouter_historique(timestamp, session, agent, raison_finale, type_round)
    mettre_a_jour_profil_session(session, agent)
    actualiser_sessions_connues()
    print("Session %s : agent %s active avec succes" % (session, agent))
    # MESSAGES INFORMATIONNELS (regle immuable v0.3.0) : rappels contextuels
    print("")
    print("=== MESSAGES POUR L AGENT ===")
    print("  > RELEVE MEME ROUND : l agent active (%s) doit enchainer IMMEDIATEMENT (relire SA fiche + SES corrections puis executer sa mission) - ne jamais s arreter apres une activation" % agent)
    print("  > la fin de mission suit SA carte (Pattern 13) : activer le maillon suivant selon SA carte ; seul le DERNIER maillon reactive Cerberus avec le bilan consolide (jamais de reactivation directe a Cerberus en milieu de chaine)")
    return 0


def reactiver_cerberus(session, raison, agent_precedent, type_round="R"):
    """Reactiver Cerberus dans la session (ne touche que son bloc)."""
    if not verifier_ascii(raison):
        print("ERREUR: Caractere non-ASCII detecte dans la raison - reactivation REFUSEE")
        return 1

    if not os.path.isfile(CERBERUS_FICHE):
        print("ERREUR: Le fichier %s n'existe pas" % CERBERUS_FICHE)
        return 1

    print("Lecture de %s..." % CERBERUS_FICHE)
    with io.open(CERBERUS_FICHE, "r", encoding="utf-8", errors="replace") as fh:
        fh.read()

    contenu = lire_agents()
    if contenu is None:
        return 1
    contenu, _ = migrer_si_necessaire(contenu)

    if not any(s == session for s, _ in extraire_blocs_session(contenu)):
        contenu = creer_session(contenu, session)
        if contenu is None:
            return 1

    role, fiche, corrections = get_agent_info("cerberus")
    date = datetime.now().strftime("%Y-%m-%d")
    champs = {
        "Nom Agent": "Cerberus",
        "Role Agent": role,
        "Derniere mise a jour": date,
        "Fiche": fiche,
        "Corrections": corrections,
        "Active par": "%s (retour de mission)" % agent_precedent,
        "Raison": raison,
    }
    # v0.5.16+ : fin de mission - fermer le chrono de l agent precedent et
    # ajouter sa duree ET sa conso tokens au repere de son entree dans
    # l historique.
    agent_prec, duree_prec, tokens_prec = arreter_chrono_session(session)
    if agent_prec and duree_prec:
        conso_prec = conso_tokens_intervention(tokens_prec)
        ajouter_duree_repere(agent_prec, duree_prec, conso_prec)

    contenu = editer_champs_session(contenu, session, champs)
    ecrire_agents(contenu)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    ajouter_historique(timestamp, session, "Cerberus", raison, type_round)
    mettre_a_jour_profil_session(session, "Cerberus")
    actualiser_sessions_connues()
    print("Session %s : Cerberus reactive avec succes" % session)
    # MESSAGES OBLIGATOIRES (v0.6.2) : forcer Cerberus a suivre sa carte
    print("")
    print("=== INSTRUCTION OBLIGATOIRE ===")
    print("CERBERUS REACTIVE : tu DOIS suivre ta carte de decision.")
    print("")
    # Lancer guider-parcours pour Cerberus
    parcours = "cerveau-projet/agents/cerberus/parcours/parcours-cerberus.json"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tools_dir = os.path.dirname(os.path.dirname(script_dir))
    guider = os.path.join(tools_dir, "guider", "guider-parcours", "guider-parcours.py")
    if os.path.isfile(guider):
        print("LANCE CETTE COMMANDE MAINTENANT :")
        print("")
        print("python3 %s %s --case c0" % (guider, parcours))
        print("")
        print("Puis relis ta fiche et tes corrections avant de continuer.")
    else:
        print("Lance guider-parcours pour ton parcours :")
        print("python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py %s --case c0" % parcours)
    print("")
    print("=== MESSAGES POUR L AGENT ===")
    print("  > RELEVE MEME ROUND : Cerberus doit suivre sa carte IMMEDIATEMENT")
    print("  > le cycle est termine : Cerberus accueille la demande suivante ou relance une mission")
    return 0


def lister_sessions():
    """Lister les sessions et leur agent principal."""
    contenu = lire_agents()
    if contenu is None:
        return 1
    blocs = extraire_blocs_session(contenu)
    if not blocs:
        print("Aucune session LLM enregistree")
        return 0
    for session, bloc in blocs:
        m = re.search(r"\*\*(?:Nom Agent|Nom)\*\* \| ([^|]+)", bloc)
        nom = m.group(1).strip() if m else "?"
        print("%s : %s" % (session, nom))
    return 0


def afficher_aide():
    print("Usage: activer-agent-principal.py <action> [parametres]")
    print("")
    print("Actions disponibles:")
    print("  sidentifier [session]              - Creer/choisir sa session (agent principal = Cerberus)")
    print("  activer <session> <agent> <raison> [mission]  - Activer un agent dans sa session")
    print("  reactiver <session> <raison> <agent_precedent> - Reactiver Cerberus dans sa session")
    print("  sessions                           - Lister les sessions et leur agent principal")
    print("  aide                               - Afficher cette aide")
    print("")
    print("Exemples:")
    print("  activer-agent-principal.py sidentifier")
    print("  activer-agent-principal.py sidentifier session-llm-1")
    print("  activer-agent-principal.py activer session-llm-1 Buffy \"Mission correction\"")
    print("  activer-agent-principal.py reactiver session-llm-1 \"Mission terminee\" Buffy")


def main(argv):
    if not argv:
        afficher_aide()
        return 0

    # v0.5.24 : extraire --type r|ir (indicateur ROUND/INTER-ROUND, regle R5
    # protocole-fin-mission v0.2.0). Defaut R si absent.
    type_round = "R"
    if "--type" in argv:
        i_type = argv.index("--type")
        if i_type + 1 < len(argv):
            type_round = argv[i_type + 1].upper()
            del argv[i_type:i_type + 2]
        else:
            print("ERREUR: --type attend r ou ir")
            return 1
    if type_round not in ("R", "IR"):
        print("ERREUR: --type attend r ou ir")
        return 1

    action = argv[0]

    if action not in ("aide", "--help", "-h", "--version"):
        verifier_residus_racine()

    if action in ("aide", "--aide", "--help", "-h"):
        afficher_aide()
        return 0

    if action == "--version":
        print("activer-agent-principal v%s (%s)" % (VERSION, STATUT))
        return 0

    if action in ("sidentifier", "identifier", "activer", "reactiver"):
        if not verrouiller_constitution():
            return 1

    if action in ("sidentifier", "identifier"):
        session = argv[1] if len(argv) > 1 else None
        return sidentifier(session)

    if action == "sessions":
        return lister_sessions()

    if action == "activer":
        if len(argv) < 4:
            print("ERREUR: Parametres manquants pour l'action 'activer' (session, agent, raison)")
            afficher_aide()
            return 1
        session = argv[1]
        agent = argv[2]
        raison = argv[3]
        mission = argv[4] if len(argv) > 4 else None
        return activer_agent(session, agent, raison, mission, type_round)

    if action == "reactiver":
        if len(argv) < 4:
            print("ERREUR: Parametres manquants pour l'action 'reactiver' (session, raison, agent_precedent)")
            afficher_aide()
            return 1
        session = argv[1]
        raison = argv[2]
        agent_precedent = argv[3]
        return reactiver_cerberus(session, raison, agent_precedent, type_round)

    print("ERREUR: Action inconnue '%s'" % action)
    afficher_aide()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
