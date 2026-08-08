#!/usr/bin/env python3
# -*- coding: ascii -*-
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
Version : 0.4.0
Statut : prepare
"""

import io
import os
import re
import sys
from datetime import datetime

VERSION = "0.4.0"
STATUT = "prepare"

AGENTS_FILE = os.environ.get("AGENTS_FILE", "AGENTS.md")
AGENTS_HISTORIQUE = os.environ.get("AGENTS_HISTORIQUE", "AGENTS-historique.md")
CLASSEUR_STOCKAGE = os.environ.get("CLASSEUR_STOCKAGE", "cerveau-projet/classeur-variables/stockage/variables-actuelles.md")
CERBERUS_FICHE = "cerveau-projet/agents/cerberus/cerberus.md"
MAX_ENTREES_HISTORIQUE = 150
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
}


def get_agent_info(agent):
    """Retourner (role, fiche, corrections) d'un agent (casse insensible)."""
    return AGENTS.get(agent.lower(), None)


def verifier_ascii(chaine):
    """Retourner True si la chaine est 100% ASCII."""
    return all(ord(c) < 128 for c in chaine)


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
    SOURCE DOUBLE (v0.4.0) : 1) AGENTS.md -- bloc avec le champ '**Id LLM** | <id>' ;
    2) classeur -- ligne profil-session avec 'id: <llm-id>'. Permet au LLM de se
    reconnaitre directement en lisant AGENTS.md."""
    # 1. AGENTS.md : champ Id LLM dans les blocs de session
    if os.path.isfile(AGENTS_FILE):
        with io.open(AGENTS_FILE, "r", encoding="utf-8", errors="replace") as fh:
            contenu = fh.read()
        for session, bloc in extraire_blocs_session(contenu):
            m = re.search(r"\*\*Id LLM\*\* \| ([^|]+)", bloc)
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
    """Retourner l'id LLM lie a une session (AGENTS.md champ Id LLM, puis classeur),
    ou None si la session n'est liee a aucun id. Utile pour detecter un CONFLIT
    d'alignement (v0.4.0) : session-llm-N deja liee a un autre id."""
    # 1. AGENTS.md
    if os.path.isfile(AGENTS_FILE):
        with io.open(AGENTS_FILE, "r", encoding="utf-8", errors="replace") as fh:
            contenu = fh.read()
        for session, bloc in extraire_blocs_session(contenu):
            if session == session_id:
                m = re.search(r"\*\*Id LLM\*\* \| ([^|]+)", bloc)
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


def poser_id_llm_bloc(contenu, session_id, llm_id):
    """Ajouter ou mettre a jour le champ '**Id LLM** | <id>' dans le bloc de session.
    Si la ligne existe -> remplacee ; sinon inseree juste apres le champ **Nom**.
    Retourne le contenu modifie."""
    lignes = contenu.split("\n")
    sortie = []
    dans_bloc = False
    for ligne in lignes:
        if dans_bloc and (re.match(r"^### Session : ", ligne) or ligne.startswith("## ")):
            dans_bloc = False
        if re.match(r"^### Session : " + re.escape(session_id) + r"\s*$", ligne):
            dans_bloc = True
        if dans_bloc:
            if re.match(r"^\| \*\*Id LLM\*\* \| ", ligne):
                sortie.append("| **Id LLM** | %s |" % llm_id)
                continue
            if re.match(r"^\| \*\*Nom\*\* \| ", ligne):
                sortie.append(ligne)
                sortie.append("| **Id LLM** | %s |" % llm_id)
                continue
        sortie.append(ligne)
    return "\n".join(sortie)


def creer_session(contenu, session_id, llm_id=None):
    """Ajouter un bloc de session (Cerberus par defaut) apres ## Sessions LLM.
    Si llm_id fourni (v0.4.0), le champ **Id LLM** est ecrit dans le bloc."""
    if any(s == session_id for s, _ in extraire_blocs_session(contenu)):
        return contenu
    info = get_agent_info("cerberus")
    role, fiche, corrections = info
    date = datetime.now().strftime("%Y-%m-%d")
    champ_id = ""
    if llm_id:
        champ_id = "| **Id LLM** | %s |\n" % llm_id
    bloc = (
        "\n### Session : %s\n\n"
        "| Champ | Valeur |\n"
        "|---|---|\n"
        "| **Nom** | Cerberus |\n"
    ) % session_id
    bloc += champ_id
    bloc += (
        "| **Role** | %s |\n"
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
    """Remplacer les champs (dict nom -> valeur) du bloc de session_id uniquement."""
    lignes = contenu.split("\n")
    sortie = []
    dans_bloc = False
    for ligne in lignes:
        if dans_bloc and (re.match(r"^### Session : ", ligne) or ligne.startswith("## ")):
            dans_bloc = False
        if re.match(r"^### Session : " + re.escape(session_id) + r"\s*$", ligne):
            dans_bloc = True
        if dans_bloc:
            for champ, valeur in champs.items():
                motif = r"^\| \*\*%s\*\* \| " % re.escape(champ)
                if re.match(motif, ligne):
                    if champ in ("Fiche", "Corrections"):
                        sortie.append("| **%s** | [%s](%s) |" % (champ, valeur, valeur))
                    else:
                        sortie.append("| **%s** | %s |" % (champ, valeur))
                    break
            else:
                sortie.append(ligne)
            continue
        sortie.append(ligne)
    return "\n".join(sortie)


def ajouter_historique(timestamp, session, agent, raison):
    """Ajouter une entree (4 colonnes) en haut du tableau, max 150."""
    if not os.path.isfile(AGENTS_HISTORIQUE):
        print("ERREUR: Le fichier %s n'existe pas" % AGENTS_HISTORIQUE)
        return 1

    nouvelle_ligne = "| %s | %s | %s | %s |" % (timestamp, session, agent, raison)

    if not verifier_ascii(nouvelle_ligne):
        print("ERREUR: Caractere non-ASCII detecte dans la raison - ecriture historique REFUSEE")
        return 1

    with io.open(AGENTS_HISTORIQUE, "r", encoding="utf-8", errors="replace") as fh:
        lignes = fh.readlines()

    sortie = []
    insere = False
    compteur = 0
    for ligne in lignes:
        if re.match(r"^\s*\|?---", ligne) and not insere:
            sortie.append(ligne)
            sortie.append(nouvelle_ligne + "\n")
            insere = True
            compteur += 1
            continue
        if re.match(r"^\| 20[0-9][0-9]-", ligne):
            if compteur < MAX_ENTREES_HISTORIQUE:
                sortie.append(ligne)
                compteur += 1
            continue
        sortie.append(ligne)

    with io.open(AGENTS_HISTORIQUE, "w", encoding="utf-8", newline="\n") as fh:
        fh.writelines(sortie)

    if not verifier_fichier_ascii(AGENTS_HISTORIQUE):
        print("WARNING: Caracteres non-ASCII presents dans %s (voir lignes ci-dessus)" % AGENTS_HISTORIQUE)

    print("Historique mis a jour dans %s" % AGENTS_HISTORIQUE)
    return 0


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
    ts = maintenant.strftime("%Y-%m-%d %H:%M")
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


def sidentifier(llm_id=None):
    """Creer/choisir la session du LLM (agent principal = Cerberus).
    REGLE UTILISATEUR (mode ID) : chaque LLM possede SON id (donne par
    l'utilisateur au lancement).
    REGLE ALIGNEMENT (v0.4.0) : id llm-N -> session-llm-N. Le numero de session
    porte le numero de l'id. Conflit gere : si session-llm-N est deja liee a un
    AUTRE id, message clair + attribution de la prochaine session libre.
    SOURCE DOUBLE : l'outil cherche la liaison dans AGENTS.md (champ **Id LLM**)
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
            print("Session retrouvee pour id %s : %s (agent principal : Cerberus)"
                  % (llm_id, session))
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
        # Bloc existant : poser/mettre a jour le champ Id LLM (reconnaissance par lecture)
        contenu = poser_id_llm_bloc(contenu, session, llm_id)
        ecrire_agents(contenu)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    ajouter_historique(timestamp, session, "Cerberus", "Identification LLM - demarrage de session")
    mettre_a_jour_profil_session(session, "Cerberus", llm_id)
    return 0


def activer_agent(session, agent, raison, mission=None):
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

    if not any(s == session for s, _ in extraire_blocs_session(contenu)):
        contenu = creer_session(contenu, session)
        if contenu is None:
            return 1

    role, fiche, corrections = info
    date = datetime.now().strftime("%Y-%m-%d")
    champs = {
        "Nom": agent,
        "Role": role,
        "Derniere mise a jour": date,
        "Fiche": fiche,
        "Corrections": corrections,
        "Active par": "Cerberus (automatique)",
        "Raison": raison,
    }
    contenu = editer_champs_session(contenu, session, champs)
    ecrire_agents(contenu)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    ajouter_historique(timestamp, session, agent, raison)
    mettre_a_jour_profil_session(session, agent)
    print("Session %s : agent %s active avec succes" % (session, agent))
    return 0


def reactiver_cerberus(session, raison, agent_precedent):
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
        "Nom": "Cerberus",
        "Role": role,
        "Derniere mise a jour": date,
        "Fiche": fiche,
        "Corrections": corrections,
        "Active par": "%s (retour de mission)" % agent_precedent,
        "Raison": raison,
    }
    contenu = editer_champs_session(contenu, session, champs)
    ecrire_agents(contenu)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    ajouter_historique(timestamp, session, "Cerberus", raison)
    mettre_a_jour_profil_session(session, "Cerberus")
    print("Session %s : Cerberus reactive avec succes" % session)
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
        m = re.search(r"\*\*Nom\*\* \| ([^|]+)", bloc)
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

    action = argv[0]

    if action in ("aide", "--help", "-h"):
        afficher_aide()
        return 0

    if action == "--version":
        print("activer-agent-principal v%s (%s)" % (VERSION, STATUT))
        return 0

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
        return activer_agent(session, agent, raison, mission)

    if action == "reactiver":
        if len(argv) < 4:
            print("ERREUR: Parametres manquants pour l'action 'reactiver' (session, raison, agent_precedent)")
            afficher_aide()
            return 1
        session = argv[1]
        raison = argv[2]
        agent_precedent = argv[3]
        return reactiver_cerberus(session, raison, agent_precedent)

    print("ERREUR: Action inconnue '%s'" % action)
    afficher_aide()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
