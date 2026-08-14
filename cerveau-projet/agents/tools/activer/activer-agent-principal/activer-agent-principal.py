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
Version : 0.5.5
Statut : prepare
"""

import io
import os
import re
import sys
from datetime import datetime

VERSION = "0.5.5"
STATUT = "prepare"
REGEX_RESIDU = re.compile(r"^v?\d+\.\d+\.\d+$")

AGENTS_FILE = os.environ.get("AGENTS_FILE", "AGENTS.md")
AGENTS_HISTORIQUE = os.environ.get("AGENTS_HISTORIQUE", "AGENTS-historique.md")
CLASSEUR_STOCKAGE = os.environ.get("CLASSEUR_STOCKAGE", "cerveau-projet/agents/classeur-variables/stockage/variables-actuelles.md")
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
    "hygie": ("Agent de nettoyage -- seul agent habilite a acceder a tout le workspace et a supprimer sans demande prealable",
              "cerveau-projet/agents/hygie/hygie.md",
              "cerveau-projet/agents/hygie/corrections.md"),
    "hermes": ("Agent de la langue -- orthographe, vocabulaire et fautes de francais commises par les agents",
               "cerveau-projet/agents/hermes/hermes.md",
               "cerveau-projet/agents/hermes/corrections.md"),
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
        "DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :\n"
        "python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \\n"
        "  cerveau-projet/agents/%s/parcours/parcours-%s.json --case c0 --reponses OUI\n"
        "(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance\n"
        "avec --reponses NON pour relire d abord ; suis ensuite les branches case\n"
        "par case ; si tu reprends apres une interruption, reprends a la case courante\n"
        "avec --case <cid> --reponses '<reponse>')."
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
        if re.match(r"^\| 20[0-9][0-9]-", ligne):
            if not insere:
                sortie.append(nouvelle_ligne + "\n")
                insere = True
                compteur += 1
            if compteur < MAX_ENTREES_HISTORIQUE:
                sortie.append(ligne)
                compteur += 1
            continue
        sortie.append(ligne)
    if not insere:
        sortie.append(nouvelle_ligne + "\n")

    with io.open(AGENTS_HISTORIQUE, "w", encoding="utf-8", newline="\n") as fh:
        fh.writelines(sortie)

    if not verifier_fichier_ascii(AGENTS_HISTORIQUE):
        print("WARNING: Caracteres non-ASCII presents dans %s (voir lignes ci-dessus)" % AGENTS_HISTORIQUE)

    print("Historique mis a jour dans %s" % AGENTS_HISTORIQUE)
    return 0


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

    # Retirer une section existante (jusqu'a la prochaine section ##)
    ls = contenu.split("\n")
    sortie = []
    i = 0
    while i < len(ls):
        if ls[i].strip() == "## Sessions connues":
            i += 1
            while i < len(ls) and not ls[i].startswith("## "):
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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    ajouter_historique(timestamp, session, agent_actif, "Identification LLM - demarrage de session")
    mettre_a_jour_profil_session(session, agent_actif, llm_id)
    actualiser_sessions_connues()
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
    contenu = editer_champs_session(contenu, session, champs)
    ecrire_agents(contenu)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    ajouter_historique(timestamp, session, agent, raison_finale)
    mettre_a_jour_profil_session(session, agent)
    actualiser_sessions_connues()
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
        "Nom Agent": "Cerberus",
        "Role Agent": role,
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
    actualiser_sessions_connues()
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

    action = argv[0]

    if action not in ("aide", "--help", "-h", "--version"):
        verifier_residus_racine()

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
