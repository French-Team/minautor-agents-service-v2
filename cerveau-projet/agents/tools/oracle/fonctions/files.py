# -*- coding: ascii -*-
"""fonctions/files.py - Files de missions pour Oracle (v1).

Une mission en attente est stockee dans files/<file>.jsonl.
Files : asap (prioritaire), normale, plus-tard, attente (missions
interrompues, transposition de la file-attente v2 - decision utilisateur
2026-08-29 : mise en attente de la mission en cours lors d un inter-round).

Chaque mission : {id, date, mission, statut, agent, priorite, type}
Statuts : EN_ATTENTE -> PRISE -> TERMINEE

ORDRE D IMPORTANCE (decision utilisateur 2026-09-02) : la file asap n est
PLUS consommee en FIFO strict. Le relais prend la mission EN_ATTENTE la plus
importante : priorite la plus basse d abord (1 avant 2), puis a priorite
egale la DATE la plus RECENTE d abord (un message recent peut etre plus
important qu un ancien). La priorite et le type sont deduits a l ajout par
classifier() (mots-cles), stockes dans l entree, et re-deduits pour les
anciennes entrees sans champ.
"""

import json
import os
import re
import uuid
from datetime import datetime
from pathlib import Path

FILES_DIR = Path(__file__).parent.parent / "files"
FILES_DIR.mkdir(exist_ok=True)

FILES_VALIDES = ["asap", "normale", "plus-tard", "attente"]


def _file_path(nom):
    """Chemin vers le fichier de file."""
    if nom not in FILES_VALIDES:
        return None
    return FILES_DIR / f"{nom}.jsonl"


# ============================================================
# INJECTION OUTIL (P2, decision utilisateur 2026-09-02) :
# quand la mission mentionne un outil du catalogue generateurs-commande,
# on injecte un bloc [OUTIL] avec la MINI-DESCRIPTION et la LISTE DES FLAGS
# (pas d exemple en dur : les flags ne dependent pas de la syntaxe bash).
# L agent sait quoi utiliser et pourquoi sans lire le code (Pattern 9).
# ============================================================

_CATALOGUE_PATH = (Path(__file__).parent.parent.parent.parent.parent /
                   "agents" / "tools" / "generateurs" /
                   "generateurs-commande" / "catalogue-commandes.json")

_NOMS_OUTILS = None


def _charger_outils():
    """Charger le catalogue une seule fois : {nom: commande}."""
    global _NOMS_OUTILS
    if _NOMS_OUTILS is not None:
        return _NOMS_OUTILS
    _NOMS_OUTILS = {}
    try:
        if not os.path.isfile(_CATALOGUE_PATH):
            return _NOMS_OUTILS
        data = json.loads(Path(_CATALOGUE_PATH).read_text(encoding="utf-8"))
        for c in data.get("commandes", []):
            nom = c.get("nom")
            if nom:
                _NOMS_OUTILS[nom] = c
    except (OSError, ValueError):
        pass
    return _NOMS_OUTILS


def _flags_outil(cmd):
    """Liste lisible des flags/parametres d un outil du catalogue."""
    morceaux = []
    for p in cmd.get("parametres", []):
        cle = p.get("cle", "")
        flag = p.get("flag", "")
        type_p = p.get("type", "texte")
        obligatoire = "REQUIS" if p.get("obligatoire") else "optionnel"
        if type_p == "flag" and flag:
            morceaux.append("%s (%s, %s)" % (flag, type_p, obligatoire))
        else:
            morceaux.append("%s (%s, %s)" % (cle, type_p, obligatoire))
    return "; ".join(morceaux) if morceaux else "(aucun flag)"


def injecter_bloc_outil(mission):
    """Retourner la mission enrichie d un bloc [OUTIL] pour chaque outil du
    catalogue mentionne (max 3, pour ne pas gonfler la mission)."""
    outils = _charger_outils()
    if not outils:
        return mission
    trouves = []
    for nom in sorted(outils.keys(), key=len, reverse=True):
        if len(trouves) >= 3:
            break
        # Nom complet entoure de non-lettres (pas de faux positif: le nom
        # d un outil est une sous-chaine de son propre nom uniquement).
        if re.search(r"(?<![a-z0-9-])%s(?![a-z0-9-])" % re.escape(nom),
                     mission.casefold()):
            trouves.append(nom)
    if not trouves:
        return mission
    bloc = ["", "=== OUTILS A UTILISER (injectes par le pilote) ==="]
    for nom in trouves:
        cmd = outils[nom]
        bloc.append("[OUTIL] %s -- %s" % (nom, cmd.get("description", "")))
        bloc.append("  Flags : %s" % _flags_outil(cmd))
        bloc.append("  Pour etre guide : python3 cerveau-projet/agents/tools/executer/"
                    "executer-formulaire/executer-formulaire.py --outil %s --schema" % nom)
    return mission + "\n".join(bloc)

def classifier(mission):
    """Classer une mission : retourne (priorite, type).

    Decision utilisateur 2026-09-02 : la file de relais doit etre ORDONNEE
    par importance puis CLASSIFIEE par type. La priorite est deduite des
    mots-cles du texte (defaut 2) : urgence/alarme/anomalie et declencheurs
    utilisateur ([urgent]/[attention]) passent en priorite 1. Le type
    identifie la nature de la mission (surveillance/purge/revision/
    coordination/test/creation) pour affichage et pilotage.
    """
    texte = (mission or "").casefold()
    if any(m in texte for m in (
            "[urgent]", "[attention]", "etat urgent", "p1 non-acquitte",
            "p1 non acquitte", "purge p1", "anomalie", "serveur mort",
            "processus fantome", "defcon", "alerte", "urgent")):
        priorite = 1
    else:
        priorite = 2
    if any(m in texte for m in ("[urgent]", "[attention]", "etat urgent",
                                "anomalie", "defcon", "alerte", "urgent")):
        typ = "urgent"
    elif "purge" in texte or "acquitter" in texte:
        typ = "purge"
    elif "revision" in texte or "questionner" in texte or "prioriser" in texte:
        typ = "revision"
    elif any(m in texte for m in ("test", "non-regression", "non regression")):
        typ = "test"
    elif any(m in texte for m in ("creer", "construire", "outil", "modifier")):
        typ = "creation"
    else:
        typ = "coordination"
    return priorite, typ


def ajouter(mission, file="asap", agent=""):
    """Ajouter une mission dans la file, sans duplicata en attente.
    P2 (2026-09-02) : la mission est enrichie du bloc [OUTIL] (mini-
    description + flags du catalogue) quand elle mentionne un outil.
    L entree est CLASSIFIEE a l ajout : champs priorite (1 = importante,
    2 = normale) et type (urgent/purge/revision/test/creation/coordination)."""
    chemin = _file_path(file)
    if chemin is None:
        return None, f"file invalide '{file}' (valides: {', '.join(FILES_VALIDES)})"
    mission = injecter_bloc_outil(mission)
    mission_norm = " ".join((mission or "").split()).casefold()
    for ligne in chemin.read_text(encoding="utf-8").splitlines() if chemin.exists() else []:
        try:
            ancien = json.loads(ligne)
        except ValueError:
            continue
        if (ancien.get("statut") == "EN_ATTENTE"
                and ancien.get("agent", "").strip().casefold() == (agent or "").strip().casefold()
                and " ".join((ancien.get("mission", "")).split()).casefold() == mission_norm):
            return ancien, "doublon: mission deja en attente"
    priorite, typ = classifier(mission)
    entree = {
        "id": uuid.uuid4().hex[:8],
        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "mission": mission,
        "statut": "EN_ATTENTE",
        "agent": agent,
        "priorite": priorite,
        "type": typ,
    }
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    return entree, None


def _priorite_entree(e):
    """Priorite d une entree : champ stocke sinon deduction (anciennes
    entrees sans champ priorite)."""
    p = e.get("priorite")
    if isinstance(p, int):
        return p
    priorite, _ = classifier(e.get("mission", ""))
    return priorite


def prendre(file="asap"):
    """Prendre la mission EN_ATTENTE la PLUS IMPORTANTE, de facon atomique.

    Decision utilisateur 2026-09-02 : PAS de FIFO strict. Tri par importance :
    (1) priorite la plus basse d abord (1 avant 2) ; (2) a priorite egale, la
    date la plus RECENTE d abord (un message recent peut etre plus important
    qu un ancien). La priorite vient du champ stocke (deduit sinon)."""
    chemin = _file_path(file)
    if chemin is None:
        return None, f"file invalide '{file}'"
    if not chemin.exists():
        return None, None
    lignes = [l.strip() for l in chemin.read_text(encoding="utf-8").splitlines() if l.strip()]
    candidats = []
    for i, l in enumerate(lignes):
        try:
            e = json.loads(l)
            if e.get("statut") == "EN_ATTENTE":
                candidats.append((i, e))
        except ValueError:
            continue
    if not candidats:
        return None, None
    # Tri par importance (decision utilisateur 2026-09-02) : priorite la
    # plus basse d abord (1 avant 2), puis DATE la plus RECENTE d abord a
    # priorite egale. Le tri est stable : les entrees sans date restent en
    # fin de classement dans leur ordre initial.
    candidats.sort(key=lambda pair: _cle_importance(pair[1]))
    i, e = candidats[0]
    # L entree relayee porte TOUJOURS la classification (decision utilisateur
    # 2026-09-02) : les anciennes entrees sans champ priorite/type sont
    # enrichies a la prise pour que mission-relais et l affichage disposent
    # de la priorite/du type deduits (retro-compatibilite).
    if not isinstance(e.get("priorite"), int):
        priorite, typ = classifier(e.get("mission", ""))
        e["priorite"] = priorite
        e["type"] = typ
    e["statut"] = "PRISE"
    e["prise_date"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    lignes[i] = json.dumps(e, ensure_ascii=False)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    return e, None


def terminer(id_mission, file="asap"):
    """Marquer une mission comme terminee."""
    chemin = _file_path(file)
    if chemin is None:
        return None, f"file invalide '{file}'"
    if not chemin.exists():
        return None, "mission introuvable"
    lignes = [l.strip() for l in chemin.read_text(encoding="utf-8").splitlines() if l.strip()]
    for i, l in enumerate(lignes):
        try:
            e = json.loads(l)
            if e.get("id") == id_mission:
                e["statut"] = "TERMINEE"
                lignes[i] = json.dumps(e, ensure_ascii=False)
                with open(chemin, "w", encoding="utf-8") as f:
                    f.write("\n".join(lignes) + "\n")
                return e, None
        except ValueError:
            continue
    return None, "mission introuvable"


def lister(file=None):
    """Lister les missions (toutes les files si file=None)."""
    resultats = []
    files = FILES_VALIDES if file is None else [file]
    for nom in files:
        chemin = _file_path(nom)
        if chemin is None or not chemin.exists():
            continue
        for l in chemin.read_text(encoding="utf-8").splitlines():
            if not l.strip():
                continue
            try:
                e = json.loads(l)
                e["_file"] = nom
                resultats.append(e)
            except ValueError:
                continue
    return resultats


def en_attente_count(file=None):
    """Nombre de missions en attente."""
    return sum(1 for m in lister(file) if m.get("statut") == "EN_ATTENTE")


def _cle_importance(e):
    """Cle de tri par importance : (priorite ASC, date DESC). Utilisee par
    les fonctions de classement de la file (prendre, lister par ordre
    d importance). Une entree sans date passe en fin de classement."""
    date = e.get("date", "") or ""
    if not date:
        return (_priorite_entree(e), 1, "")
    return (_priorite_entree(e), 0, tuple(-ord(c) for c in date))


def cmd_mission_ajouter(args):
    """Ajouter une mission dans une file."""
    entree, erreur = ajouter(args.mission, file=args.file, agent=getattr(args, "agent", ""))
    if erreur:
        if erreur.startswith("doublon:"):
            print(f"[ORACLE] Mission deja en attente: {entree['id']} ({args.file})")
        else:
            print(f"[ORACLE] ERREUR: {erreur}")
        return
    print(f"[ORACLE] Mission ajoutee: {entree['id']} ({args.file})")


def cmd_mission_prendre(args):
    """Prendre la premiere mission en attente."""
    entree, erreur = prendre(args.file)
    if erreur:
        print(f"[ORACLE] ERREUR: {erreur}")
        return
    if entree is None:
        print(f"[ORACLE] Aucune mission en attente dans '{args.file}'")
        return
    print(f"[ORACLE] Mission {entree['id']} prise:")
    print(f"  Date: {entree['date']}")
    print(f"  Mission: {entree['mission']}")


# Cartes de deduction de l agent cible depuis le TEXTE de la mission,
# quand la mission est deposee sans champ `agent` explicite. Decision
# utilisateur 2026-08-29 : Oracle choisit l agent habilite puis historise
# son DEBUT a sa place et lance le pilote.
_CARTE_AGENT = [
    # Alerte de coordination (v1) : un ETAT URGENT / P1 non-acquittes doit
    # revenir a ORACLE (coordinateur de la coordination) qui declenche le
    # super-combo purge-p1 pour distribuer les P1 a chaque destinataire,
    # au lieu du fallback vague cerberus (lecon 2026-08-30). Placee en
    # TETE : prioritaire sur toute autre carte.
    (["etat urgent", "p1 non-acquitte", "p1 non acquitte",
      "purge p1", "alerts de coordination", "coordination v1"],
     "oracle"),
    (["test", "non-regression", "non regression", "ecrire/executer",
      "lancer les tests"], "morpheus"),
    (["outil", "creer/modifier un outil", "optimiser un outil", "construire"],
     "vulcain"),
    (["inventaire", "audit", "verification", "evaluation", "evaluer"],
     "themis"),
    (["pense-bete", "pense bete"], "athena"),
    (["spec"], "promethee"),
    (["todo"], "minerve"),
    (["readme", "muse de l histoire"], "clio"),
    (["orthographe", "vocabulaire", "fautes"], "hermes"),
    (["workspace", "nettoyer", "residus"], "hygie"),
    (["contradiction", "incoherence"], "argus"),
    (["gardien", "marbre", "zone protegee"], "gardien"),
    (["git"], "hades"),
    (["revision strategique", "prioriser"], "socrate"),
    (["documentation v2", "freelance"], "ferrari"),
]


def deduire_agent(mission, agent_explicite=""):
    """Deviner l agent cible d une mission : champ agent explicite sinon
    deduction par mots-cles sur le texte. Retourne (agent, source)."""
    agent = (agent_explicite or "").strip().lower()
    if agent:
        return agent, "champ-agent"
    texte = (mission or "").lower()
    for mots, cible in _CARTE_AGENT:
        if any(m in texte for m in mots):
            return cible, "deduction"
    return "cerberus", "inconnu"


def relais(file="asap"):
    """Prendre (PRISE) la mission la PLUS IMPORTANTE pour la relayer a
    l agent cible. Retourne (entree, erreur). La mission garde son champ
    `agent` (deduit si absent) pour que Oracle sache a qui l envoyer.
    Ordonnancement par importance (decision utilisateur 2026-09-02,
    voir prendre()).
    """
    entree, erreur = prendre(file)
    if erreur or entree is None:
        return entree, erreur
    agent, source = deduire_agent(entree.get("mission",
                                              ""), entree.get("agent", ""))
    entree["agent"] = agent
    entree["agent_source"] = source
    if "priorite" not in entree:
        priorite, typ = classifier(entree.get("mission", ""))
        entree["priorite"] = priorite
        entree["type"] = typ
    return entree, None


def cmd_mission_terminer(args):
    """Terminer une mission."""
    entree, erreur = terminer(args.id, file=args.file)
    if erreur:
        print(f"[ORACLE] ERREUR: {erreur}")
        return
    print(f"[ORACLE] Mission {args.id} terminee")


def cmd_mission_lister(args):
    """Lister les missions.
    v0.6.0 (Verrou bleu) : filtres optionnels --statut et --agent. Par
    defaut comportement inchange (liste toutes les missions de la file).
    Un --statut en MAJUSCULE insensible a la casse, l agent filtre aussi
    en minuscules (l agent peut porter la casse du nom)."""
    file = getattr(args, "file", None)
    filtre_statut = getattr(args, "statut", None)
    filtre_agent = getattr(args, "filtre_agent", None)
    missions = lister(file)
    if missions and filtre_statut:
        missions = [m for m in missions
                    if m.get("statut", "").upper() == filtre_statut.upper()]
    if missions and filtre_agent:
        missions = [m for m in missions
                    if m.get("agent", "").lower() == filtre_agent.lower()]
    if not missions:
        print("[ORACLE] Aucune mission")
        return
    en_attente = sum(1 for m in missions if m.get("statut") == "EN_ATTENTE")
    print(f"[ORACLE] {len(missions)} mission(s), {en_attente} en attente:")
    # Ordre d affichage par importance (decision utilisateur 2026-09-02) :
    # priorite puis date recente d abord, comme le relais consomme la file.
    for m in sorted(missions, key=_cle_importance):
        statut = m.get("statut", "?")
        marqueur = " *" if statut == "EN_ATTENTE" else ""
        p = "P%d" % m.get("priorite", 2)
        typ = m.get("type", "?")
        print(f"  [{m['_file']:10s}] {m['id']} {statut}{marqueur} {p}/{typ} : "
              f"{m['mission'][:50]}")
