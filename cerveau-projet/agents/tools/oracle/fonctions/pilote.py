#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
pilote.py -- PILOTE ORACLE (maitre d hotel de la carte/arbre des agents v1).

Vision utilisateur 2026-08-27 : Oracle prend le CONTROLE de la carte
(parcours.json) ou de l arbre (arbre-*.json) de l agent actif.
L agent est un invite servi sur un plateau : Oracle lit la case courante
ou le besoin courant, repond aux questions verrouillees a sa place,
sert la commande outil a executer, historise DEBUT/FIN automatiquement,
et avance seul jusqu a une vraie decision libre.

v0.2.0 : support du format arbre v2-like (racine -> theme -> redirects
-> fins centralisees). Detection auto du format depuis identite.type.

Principe (pilotage auto fiable) :
  - case type action/indice : servir la commande outil de la case a
    l agent (via son inbox), passer a la suivante.
  - case type question verrouillable : resoudre LA reponse depuis l etat
    de carte (mission_type, etape, contexte) et suivre la branche.
  - case type question libre (decision indeterminee) : s arreter et
    laisser la main (Oracle ne devine pas les decisions humaines/de fin).
  - case type fin : historiser la fin et terminer.

L etat de carte est persiste dans oracle/etat-cartes/<agent>.json :
  {
    "agent": "vulcain",
    "parcours": "cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json",
    "case_courante": "c1h",
    "mission_type": "construire",
    "mission": "texte de la mission",
    "historise_debut": true,
    "etape": "travail" | "fin" | "autre"
  }

Proprietaire : Vulcain (outils v1). Version : 0.1.0.
"""

import io
import json
import os
import sys
from datetime import datetime
from pathlib import Path

VERSION = "0.2.0"

# Racine du projet : oracle/fonctions -> outils -> agents -> cerveau-projet -> racine
_RACINE = Path(__file__).resolve().parents[4]
_ETAT_DIR = Path(__file__).resolve().parents[1] / "etat-cartes"


def _chemin_etat(agent):
    return _ETAT_DIR / ("%s.json" % agent)


def _charger_etat(agent):
    """Charger l etat de carte d un agent (dict vide si absent)."""
    chemin = _chemin_etat(agent)
    if chemin.is_file():
        try:
            return json.loads(chemin.read_text(encoding="utf-8"))
        except ValueError:
            return {}
    return {}


def _sauver_etat(etat):
    """Sauvegarder l etat de carte d un agent (creation du dossier si besoin)."""
    _ETAT_DIR.mkdir(parents=True, exist_ok=True)
    with io.open(_chemin_etat(etat.get("agent", "")), "w",
                 encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(etat, ensure_ascii=True, indent=1))


def init_etat(agent, parcours, mission_type, mission, precedent=None):
    """Initialiser (ou reinitialiser) l etat de carte d un agent.

    Appelee a l activation (oracle.py cmd_activer) : ORACLE se souvient
    de la mission confiee pour piloter la carte sans que l agent ait a
    rappeler le type de mission.

    precedent : le maillon qui A ACTIVE cet agent (celui qui le rappellera
    en fin de mission). Oracle l enregistre pour piloter la reactivation
    du maillon precedent avec pose du FIN (vision 2026-08-27).
    """
    chemin_parcours = os.path.relpath(str(parcours), str(_RACINE)).replace("\\", "/")
    etat = {
        "agent": agent,
        "parcours": chemin_parcours,
        "case_courante": None,
        "mission_type": mission_type,
        "mission": mission,
        "historise_debut": False,
        "precedent": precedent,
        "etape": "debut",
    }
    _sauver_etat(etat)
    return etat


def _charger_parcours(chemin):
    """Charger un parcours JSON (reutilise la logique de guider-parcours)."""
    p = Path(chemin)
    if not p.is_file():
        # chemin relatif a la racine du projet
        p = _RACINE / chemin
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError:
        return None


def _type_mission_auto(raison):
    """Deduire le type de mission depuis la raison d activation.

    Repli robuste : mots-cles de la mission. Valeurs possibles selon les
    cartes : construire / modifier / creer / tester / verifier / audit /
    autre (fallback). La carte branche dessus.
    """
    r = (raison or "").lower()
    # Ordre de priorite : les plus specifiques d abord. Ex : "audit" avant
    # "verifier" (une mission d audit peut contenir le mot verifier), "creer"
    # avant "construire" (? non - construire est generique mais prioritaire),
    # et les verifications de prefixe ('verifier ', 'tester ') avant les mots
    # contenus pour ne pas confondre audit/verification.
    mape = [
        ("audit", ["audit", "evalue", "evaluation", "evaluer ", "auditer"]),
        ("veracite", ["veracite", "verite", "verifier le readme", "verifier les readme"]),
        ("tester", ["tester ", "ecrire/executer les tests", "verifier les tests", "ecrire et executer les tests", "lancer les tests"]),
        ("inter-round", ["inter-round", "rapport ko"]),
        ("creer", ["creer ", "creation ", "cree le", "migrer ", "migration "]),
        ("construire", ["construire", "nouvel outil ", "nouvel outil"]),
        ("modifier", ["modifier", "corriger", "mise a jour", "bump "]),
        ("maj", ["maj ", "mettre a jour", "mettre a jour", "synchroniser"]),
        ("verifier", ["verifier ", "validation", "controle ", "verifie "]),
        ("controle", ["controle ", "controler", "verifier le travail", "verifier le work"]),
        ("non-regression", ["non-regression", "non regression", "lancer les tests", "suite de tests"]),        ("detecter", ["detecter ", "contradictions", "incoherence", "incoherences"]),
        ("explorer", ["explorer ", "cartographier", "analyser la structure"]),
        ("rechercher", ["rechercher ", "recherche web", "documentation technique"]),
        ("corriger", ["corriger les fautes", "orthographe", "vocabulaire", "detecter-fautes"]),
        ("nettoyer", ["nettoyer", "nettoyage", "residus", "supprimer les"]),
        ("verifier-marbre", ["verifier le marbre", "integrite du marbre", "marbre"]),
        ("modifier-marbre", ["modifier le marbre", "proposer une modification"]),
        ("proposer", ["proposer ", "proposer une modification", "modifier une zone"]),
        ("signaler", ["signaler ", "signaler une violation", "violation"]),
        ("eduer", ["eduer", "re-eduer", "educer", "formation", "education"]),
        ("educer", ["educer", "re-eduer", "eduer", "formation", "education"]),
        ("eduquer", ["eduquer", "education", "re-eduer"]),
        ("agent", ["agent ", "agent habilite", "activer l agent"]),
        ("auto-correction", ["auto-correction", "auto correction", "corriger ma carte"]),
        ("revision", ["revision strategique", "questionner", "prioriser"]),
        ("synthese", ["synthese", "synthetiser", "missions-revision"]),
        ("honnetete", ["honnetete", "preuve d honnetete", "residu suspect"]),
        ("snapshots", ["snapshot", "snapshots", "rotation 7 jours"]),
        ("purifier", ["purifier", "purification", "rvav", "fichiers surcharges"]),
        ("veille", ["veille", "orthographe globale", "scan --tous"]),
        ("cartographier", ["cartographier", "dependances", "appels"]),
        ("documenter", ["documenter", "documentation technique", "rvav"]),
        ("completer", ["completer", "enrichir", "ajouter des sections"]),
        ("controler", ["controler ", "verifier le travail", "verifier le work"]),
        ("outils", ["outil bloque", "probleme outil", "outil qui ne marche"]),
        ("sauvegarder", ["sauvegarder", "commit", "push", "git status", "git log", "git diff"]),
        ("restaurer", ["restaurer", "checkout", "restore", "revenir en arriere", "anciennete"]),
        ("fiche-agent", ["fiche agent", "corriger une fiche", "proto 1"]),
        ("arbre-decision", ["arbre de decision", "corriger un arbre", "proto 4"]),
        ("jarvis", ["corriger jarvis", "proto 2", "jarvis.py"]),
        ("outils-combos", ["outils combos", "corriger un outil", "proto 5"]),
        ("routines", ["corriger les routines", "proto 3", "routines v2"]),
        ("protocoles", ["corriger un protocole", "proto 6", "protocoles v2"]),
        ("regles", ["corriger les regles", "proto 7", "regles-immuables v2"]),
        ("protocole", ["protocole", "convention", "regle"]),
        ("lire", ["lire ", "lire les ", "consulter ", "relire"]),
        # Themes Cerberus
        ("accueil", ["accueil", "accueillir", "demande"]),
        ("activation", ["activation ", "activer un"]),
        ("retour", ["retour ", "retour d"]),
        ("ameliorer", ["ameliorer", "amelioration"]),
    ]
    for typ, mots in mape:
        if any(m in r for m in mots):
            return typ
    return "autre"


def _resoudre_question(case, etat):
    """Resoudre une question verrouillable du parcours.

    Retourne la reponse a donner, ou None si c est une decision libre que
    l agent/Oracle ne doit pas deviner.

    Regles de pilotage (parcours v1, vues sur cerberus/buffy/vulcain/
    morpheus/janus/themis) :
      - c0b "Confirmation as-tu lu ta fiche" : OUI (Oracle a servi la
        fiche + corrections, l agent est pret).
      - cU1 "Probleme avec un outil" : NON (Oracle gere, pas l agent).
      - c1 "Mission" : la branche = mission_type de l etat de carte.
      - "Ameliorations possibles de mon fonctionnement" : NON par defaut.
      - "COMBO ou CATALOGUE" : NON (sauf si la mission porte un combo).
      - "Choisir la technologie" : OUI (Python dispo, profil-systeme).
      - "Besoin d outil" : TEMPORAIRE par defaut (script jetable).
      - "Probleme avec un outil en cours de mission" (cU1) : NON.
      - Autres questions connues : deduction par titre/mots-cles.
    """
    titre = (case.get("titre", "") or "").lower().replace("'", " ").replace("-", " ")
    question = (case.get("question", "") or "").lower().replace("'", " ").replace("-", " ")
    branches = [b.get("reponse", "") for b in case.get("branches", [])]

    # --- Confirmation lecture (tres frequente, debut de parcours) ---
    if titre.startswith("confirmation") and "lu ta fiche" in titre:
        return _s("OUI", branches)

    # --- Mission / demande / situation (type deduit de l activation) ---
    if titre == "mission" and ("quelle est la mission" in question
                               or "quelle est la demande" in question
                               or "quelle est la situation" in question
                               or "quelle est ta mission" in question):
        mt = etat.get("mission_type", "autre")
        ret = _s(mt, branches)
        if ret is None:
            ret = _s("autre", branches)
        return ret

    # --- Probleme avec un outil en cours de mission (cU1) ---
    if "probleme avec un outil" in titre:
        return _s("NON", branches)

    # --- Ameliorations possibles de mon fonctionnement ---
    if "ameliorations possibles" in titre:
        return _s("NON", branches)

    # --- COMBO ou CATALOGUE ---
    if "combo" in titre and "catalogue" in titre:
        raison = (etat.get("mission", "") or "").lower()
        if "combo" in raison.split():
            return _s("OUI", branches)
        return _s("NON", branches)

    # --- Choisir la technologie (Python dispo, profil-systeme) ---
    if "choisir la technologie" in titre:
        return _s("OUI", branches)

    # --- Lire l outil a construire : NON si construction (pas de doc a
    #     lire), OUI si modification (doc existante a lire) ---
    if "lire l outil" in titre:
        if etat.get("mission_type") in ("construire", "creer", "creer "):
            return _s("NON", branches)
        return _s("OUI", branches)

    # --- Besoin d outil : TEMPORAIRE par defaut ---
    if "besoin d outil" in titre:
        if "TEMPORAIRE" in branches:
            return "TEMPORAIRE"
        return None

    # --- Inventaire / audit (cerberus) ---
    if "inventaire" in titre and "audit" in titre:
        return _s("NON", branches)

    # --- Erreurs hors mission (buffy/cerberus) ---
    if "erreurs hors mission" in titre or "erreur hors mission" in titre:
        return _s("NON", branches)

    # --- Defaut signale dans un rapport (janus/themis) ---
    if "defaut signale" in titre:
        return _s("NON", branches)

    # --- DELEGATION (mise sous tutelle des maillons de chaine) : case
    #     qui demande si l agent a active un maillon (Morpheus/Themis pour
    #     les tests / l audit). Vision 2026-08-27 : Oracle est le maitre
    #     d hotel, il NE BRISE PAS le round - il repond OUI a la delegation
    #     et active lui-meme le maillon. Indice : la case porte un outil
    #     activer-agent-principal et la question contient "AS-TU ACTIVE".
    if (("as-tu active" in question or "as-tu acti" in question)
            and "maillon" in etat.get("etape", "")
            and any(i.get("type") == "outil"
                    and "activer" in (i.get("nom") or "").lower()
                    for i in case.get("indices", []))):
        return _s("OUI", branches)

    # --- Decision libre (non pilotable) : Oracle ne devine JAMAIS ---
    #     Ex : verdict de test / audit (le testeur juge), choix de l agent
    #     habilite, retour de Themis effectivement recu. Ici la chaine passe
    #     la main proprement (jamais de boucle ni de blocage).
    return None


def _s(rep, branches):
    """Resoudre une reponse exacte parmi les branches (reaplique reponse_exacte)."""
    rep = rep.strip()
    for b in branches:
        if b.strip().lower() == rep.lower():
            return b
    # si la reponse n est pas une branche exacte, rechercher le prefixe
    for b in branches:
        if b.strip().lower().startswith(rep.lower()):
            return b
    return None


def _extraire_commande(case):
    """Extraire la commande outil a servir depuis les indices d une case.

    Retourne (message, commande) : message = plateau sert a l agent,
    commande = texte exact de l outil a executer (ou None).
    """
    indices = case.get("indices", [])
    commandes = []
    for ind in indices:
        typ = ind.get("type", "")
        if typ == "outil":
            if ind.get("commande"):
                commandes.append(ind.get("commande"))
            elif ind.get("chemin"):
                commandes.append(ind.get("chemin"))
        elif typ == "fichier" and ind.get("chemin"):
            commandes.append(ind.get("chemin"))
    if not commandes:
        return "", None
    return "SERVE POUR VOUS :\n" + "\n".join("  > " + c for c in commandes), "\n".join(commandes)


# Cache des modules charges une seule fois
_mod_aap = None  # activer-agent-principal
_mod_vfs = None  # verifier-flux-securite

def _charger_mod_aap():
    """Charger activer-agent-principal en cache (une seule fois)."""
    global _mod_aap
    if _mod_aap is not None:
        return _mod_aap
    try:
        import importlib.util
        aap_path = str(_RACINE / "agents" / "tools" / "activer" /
                       "activer-agent-principal" / "activer-agent-principal.py")
        if not os.path.isfile(aap_path):
            return None
        spec = importlib.util.spec_from_file_location("aap", aap_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _mod_aap = mod
        return mod
    except Exception:
        return None


def _verifier_flux():
    """Verifier le flux apres chaque historisation. Retourne True si OK."""
    global _mod_vfs
    try:
        if _mod_vfs is None:
            import importlib.util
            vfs = str(_RACINE / "agents" / "tools" / "verifier" /
                      "verifier-flux-securite" / "verifier-flux-securite.py")
            if not os.path.isfile(vfs):
                return True
            spec = importlib.util.spec_from_file_location("vfs", vfs)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _mod_vfs = mod
        ok, erreurs = _mod_vfs.verifier_flux()
        if not ok:
            print("[ORACLE] FLUX KO : %d anomalie(s)" % len(erreurs))
            for e in erreurs[:3]:
                print("  - %s" % e)
        return ok
    except Exception:
        return True


def _historiser(agent, raison, agent_effectif=None):
    """Historiser une action (marquage DEBUT/FIN) via activer-agent-principal.

    agent_effectif : agent affiche dans la colonne Agent du tableau.
    Si None, utilise le nom de l agent (cerberus, buffy...).
    Oracle n apparait que quand c est LUI l agent (ex: historiser DEBUT
    pour son propre compte).
    Apres chaque historisation, verifie le flux (routine de securite).
    """
    aap = _charger_mod_aap()
    if aap is None:
        return False
    try:
        aap.ajouter_historique(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S.000"),
            "session-admin", agent, raison, "R",
            agent_effectif=agent_effectif,
            executeur="Oracle")
        # Verifier le flux apres chaque historisation
        _verifier_flux()
        return True
    except Exception:
        return False


def _fin_auto(etat, bilan):
    """Poser le marqueur FIN sur l agent qui quitte la chaine (colonne
    Debut/Fin) de facon fiable, sans dependre de l agent.

    Vision 2026-08-27 : Oracle maitre d hotel pose FIN a la fin de la
    carte de l agent, symetriquement au DEBUT qu il a pose a l activation.
    """
    agent = etat.get("agent")
    bilan = bilan or (etat.get("mission", "") or "")
    texte = "FIN: %s" % bilan
    ok = _historiser(agent, texte)
    etat["historise_fin"] = True
    etat["etape"] = "fin"
    _sauver_etat(etat)
    return ok and texte


def _maillon_precedent(etat):
    """Deduire le maillon precedent a reactiver en fin de mission.

    C est l agent qui avait active celui-ci (champ 'precedent' de l etat de
    carte), pose par cmd_activer / _activer_maillon. Repli : Cerberus
    (fin de chaine - Pattern 8).
    """
    prec = (etat.get("precedent") or "").strip()
    if prec and prec.lower() != "cerberus":
        return prec
    return "cerberus"


def _reactiver_maillon(agent_qui_finit, bilan):
    """Piloter la reintegration du maillon precedent avec pose du FIN.

    Appelee quand la carte de l agent est TERMINEE. Oracle :
      1. pose FIN:<bilan> sur l agent qui sort (colonne Debut/Fin),
      2. reactiver le maillon precedent (celui qui l avait active) OU
         Cerberus pour la fin de chaine -- en accord avec la carte
         (Pattern 8). L activation se fait via activer-agent-principal.
    Retourne un message de trace.
    """
    etat = _charger_etat(agent_qui_finit)
    messages = []
    # 1. Poser le FIN (toujours faire, meme si deja pose) et le signaler.
    fin = _fin_auto(etat, bilan)
    messages.append(fin)
    # 2. Determiner la cible a reactiver.
    cible = _maillon_precedent(etat)
    messages.append("[PILOTE] Fin de %s : reactivation %s" % (agent_qui_finit, cible))
    import importlib.util
    aap_path = str(_RACINE / "agents" / "tools" / "activer" /
                   "activer-agent-principal" / "activer-agent-principal.py")
    if not os.path.isfile(aap_path):
        return "\n".join(messages) + "\n[PILOTE] reactiver-agent-principal introuvable"
    try:
        spec = importlib.util.spec_from_file_location("aap", aap_path)
        aap = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(aap)
        if cible.lower() == "cerberus":
            # Retour a Cerberus : le message doit indiquer un RETOUR
            # (pas un debut de mission). Format : RETOUR <agent> : <bilan>
            raison_retour = "RETOUR %s : %s" % (agent_qui_finit.upper(), bilan or "")
            rc = aap.activer_cerberus(
                "session-admin", raison_retour, agent_qui_finit)
        else:
            # Reprise du maillon precedent : on le reactiver pour qu il
            # reprenne son round (retour d inter-round / reprise de chaine).
            rc = aap.activer_agent("session-admin", cible, bilan,
                                   historiser=False)
            _historiser(cible, "DEBUT: " + (bilan or ""))
        if rc == 0:
            messages.append("[PILOTE] Maillon precedent '%s' reactive par Oracle" % cible)
        else:
            messages.append("[PILOTE] Echec reactivation %s (rc=%s)" % (cible, rc))
    except Exception as exc:
        messages.append("[PILOTE] Erreur reactivation %s: %s" % (cible, exc))
    return "\n".join(messages)

def _activer_maillon(agent_pilote, case, mission_agent, cible_forcee=None):
    """Oracle (maitre d hotel) active le maillon suivant de la chaine.

    Appelee quand une case de DELEGATION est resolue a OUI : Oracle active
    lui-meme le maillon (Morpheus pour les tests, Themis pour l audit, le
    maillon de sa carte) au lieu de demander a l agent de le faire - le
    round ne se brise jamais.

    Le maillon cible est deduit de la commande outil de la case (qui porte
    le nom de l agent? pour activer-agente-principal) ou de la mission.
    Repli : on n active rien si la cible est indeterminee (Oracle ne devine
    pas un nom d agent).
    """
    import importlib.util
    import os
    aap_path = str(_RACINE / "agents" / "tools" / "activer" /
                   "activer-agent-principal" / "activer-agent-principal.py")
    if not os.path.isfile(aap_path):
        return "[PILOTE] activer-agent-principal introuvable (%s)" % aap_path
    # Determiner le maillon cible depuis la commande de la case ou la mission
    cible = cible_forcee
    if not cible:
        for ind in case.get("indices", []):
            cmd = ind.get("commande", "") or ""
            import re
            m = re.search(r"activer\s+\S+\s+(\S+)", cmd)
            if m and not m.group(1).startswith("<"):
                cible = m.group(1)
    if not cible:
        return "[PILOTE] maillon cible indetermine (delegation non activee automatiquement)"
    spec = importlib.util.spec_from_file_location("aap", aap_path)
    aap = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aap)
    try:
        rc = aap.activer_agent("session-admin", cible, mission_agent,
                               historiser=False)
        if rc == 0:
            # Poser le marqueur DEBUT a l entre dans la chaine (colonne
            # Debut/Fin). Vision 2026-08-27 : Oracle maitre d hotel pose
            # DEBUT pour chaque maillon qu il active, comme cmd_activer.
            try:
                aap.ajouter_historique(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S.000"),
                    "session-admin", cible, "DEBUT: " + mission_agent, "R",
                    executeur="Oracle")
            except Exception:
                pass
            # Marquer DEBUT deja historise pour eviter le double
            _etat_cible = _charger_etat(cible)
            _etat_cible["historise_debut"] = True
            _sauver_etat(_etat_cible)
            # Enregistrer le precedent du maillon cible (l agent pilote qui
            # vient de l activer) pour que la fin de mission puisse le
            # reactiver proprement.
            _etat_cible = _charger_etat(cible)
            if _etat_cible.get("agent"):
                _etat_cible["precedent"] = agent_pilote
            else:
                _etat_cible = {
                    "agent": cible,
                    "case_courante": None,
                    "precedent": agent_pilote,
                }
            _sauver_etat(_etat_cible)
            return "[PILOTE] Maillon '%s' active par Oracle (chainage automatique)" % cible
        return "[PILOTE] Echec activation maillon %s (rc=%s)" % (cible, rc)
    except Exception as exc:
        return "[PILOTE] Erreur activation maillon %s: %s" % (cible, exc)


def _est_case_delegation(case):
    """Vrai si une case est une DELEGATION de maillon (Oracle active le
    suivant) : question 'AS-TU ACTIVE ...' et un outil activer-agent dans
    les indices."""
    q = (case.get("question", "") or "").lower()
    q = q.replace("'", " ").replace("-", " ")
    return (("as tu active" in q or "as tu activer" in q)
            and any(i.get("type") == "outil"
                    and i.get("nom", "") == "activer-agent-principal"
                    for i in case.get("indices", [])))


def _charger_fichier(arbre_dir, nom_fichier):
    """Charger un fichier JSON (theme, fins) depuis le dossier de l arbre."""
    p = arbre_dir / nom_fichier
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError:
        return None


def _resoudre_racine(racine, etat):
    """Resoudre la racine de l arbre : deduire la branche (theme) depuis
    la mission_type de l etat de carte.

    Retourne le fichier theme cible (vers) ou None si decision libre.
    """
    mt = (etat.get("mission_type", "") or "").upper()
    agent = etat.get("agent", "")
    branches = racine.get("branches", [])
    # Enumerer les reponses valides (branches reelles de la racine)
    reponses_valides = set(br.get("reponse", "").upper() for br in branches)
    # Cerberus : ROUTEUR PUR (hub a 4 directions, decision 2026-08-29).
    # Toujours DE-USER (une demande arrive de l utilisateur) : il route,
    # il ne travaille jamais. Repli sur ACCUEIL si la racine l a encore.
    if agent == "cerberus":
        for cle in ("DE-USER", "ACCUEIL"):
            for br in branches:
                if br.get("reponse", "").upper() == cle:
                    return br.get("vers")
    # Correspondance directe par reponse exacte (CONSTRUIRE, MODIFIER, etc.)
    for br in branches:
        if br.get("reponse", "").upper() == mt:
            return br.get("vers")
    # Fallback : recherche par mots-cles dans la description
    mapping = {
        "CONSTRUIRE": ["construire", "nouvel outil"],
        "CREER": ["creer ", "creation ", "pense-bete", "nouveau "],
        "COMPLETER": ["completer", "completer", "enrichir", "ajouter des sections"],
        "MODIFIER": ["modifier", "corriger", "ameliorer", "mise a jour"],
        "MAJ": ["maj", "mettre a jour", "synchroniser", "readme"],
        "CONTROLE": ["controle", "controler", "verifier le travail", "verifier"],
        "NON-REGRESSION": ["non-regression", "non regression", "lancer les tests", "suite de tests"],
        "DETECTER": ["detecter", "contradictions", "incoherence", "incoherences"],
        "EXPLORER": ["explorer", "cartographier", "analyser la structure"],
        "RECHERCHER": ["rechercher", "recherche web", "documentation"],
        "CORRIGER": ["corriger les fautes", "orthographe", "vocabulaire"],
        "NETTOYER": ["nettoyer", "nettoyage", "residus"],
        "VERIFIER": ["verifier le marbre", "integrite", "verifier l integrite"],
        "PROPOSER": ["proposer ", "proposer une modification", "modifier une zone", "proposer la modification"],
        "SIGNALER": ["signaler ", "signaler une violation", "violation detectee", "signaler la violation"],
        "EDUCER": ["eduer", "re-eduer", "educer", "formation", "education"],
        "AUTO-CORRECTION": ["auto-correction", "auto correction", "corriger ma carte", "ma carte"],
        "REVISION": ["revision strategique", "questionner", "prioriser"],
        "SYNTHESE": ["synthese", "synthetiser", "missions-revision", "creer le fichier"],
        "AUDIT": ["audit", "auditer", "evalue", "evaluation", "evaluer"],
        "VERACITE": ["veracite", "verite", "verifier le readme"],
        "AUTRE": ["autre", "documentation", "delegation", "audit"],
        "INTER-ROUND": ["inter-round", "rapport ko"],
        "LIRE": ["lire", "consulter", "fiche", "lecon"],
        "ACTIVATION": ["activation ", "activer un", "activer l agent"],
        "AGENT": ["agent ", "agent habilite", "activer l agent"],
        "AMELIORER": ["ameliorer", "amelioration", "optimiser"],
        "CARTOGRAPHIER": ["cartographier", "dependances", "appels", "analyser les dependances"],
        "CONTROLER": ["controler ", "verifier le travail", "verifier le work", "controle de"],
        "DOCUMENTER": ["documenter", "documentation technique", "rapport technique"],
        "EDUQUER": ["eduquer", "education", "re-eduer"],
        "HONNETETE": ["honnetete", "preuve d honnetete", "residu suspect"],
        "OUTILS": ["outil bloque", "probleme outil", "outil qui ne marche", "comprendre l outil"],
        "PROTOCOLE": ["protocole", "convention", "regle", "convention"],
        "PURIFIER": ["purifier", "purification", "rvav", "fichiers surcharges"],
        "RETOUR": ["retour ", "retour d", "verifier le rapport"],
        "SNAPSHOTS": ["snapshot", "snapshots", "rotation 7 jours"],
        "TESTER": ["tester ", "ecrire/executer les tests", "lancer les tests", "ecrire et executer les tests"],
        "SAUVEGARDER": ["sauvegarder", "commit", "push", "git status", "git log"],
        "RESTAURER": ["restaurer", "checkout", "restore", "revenir en arriere", "anciennete"],
        "FICHE-AGENT": ["fiche agent", "corriger une fiche", "proto 1", "fiche d agent"],
        "ARBRE-DECISION": ["arbre de decision", "corriger un arbre", "proto 4", "arbre v2"],
        "JARVIS": ["corriger jarvis", "proto 2", "jarvis.py", "jarvis-server"],
        "OUTILS-COMBOS": ["outils combos", "corriger un outil", "proto 5", "outil v2"],
        "ROUTINES": ["corriger les routines", "proto 3", "routines v2", "etat-executions"],
        "PROTOCOLES": ["corriger un protocole", "proto 6", "protocoles v2"],
        "REGLES": ["corriger les regles", "proto 7", "regles-immuables v2"],
        "VEILLE": ["veille", "orthographe globale", "scan --tous"],
        "ACCUEIL": ["accueil", "demande", "utilisateur"],
    }
    raison = (etat.get("mission", "") or "").lower()
    for reponse, mots in mapping.items():
        if reponse not in reponses_valides:
            continue
        if any(m in raison for m in mots):
            for br in branches:
                if br.get("reponse", "").upper() == reponse:
                    return br.get("vers")
    # Dernier repli : ACCUEIL si present (route generique)
    if "ACCUEIL" in reponses_valides:
        for br in branches:
            if br.get("reponse", "").upper() == "ACCUEIL":
                return br.get("vers")
    # Aucune correspondance : decision libre
    return None


def _substituer_placeholders(cmd, agent, mission=""):
    """Substituer les placeholders connus dans une commande arbre.

    Substitutions automatiques :
      <session>    -> "session-admin" (session v1)
      <MOI>        -> nom de l agent (ex: "vulcain")
      <ma mission> -> texte reel de la mission
    """
    cmd = cmd.replace("<session>", "session-admin")
    cmd = cmd.replace("<MOI>", agent)
    if mission:
        cmd = cmd.replace("<ma mission>", mission)
    return cmd


# Racine reel du projet (hors cerveau-projet/)
_RACINE_PROJET = Path(__file__).resolve().parents[5]


def _resoudre_chemins(cmd):
    """Resoudre les chemins relatifs dans une commande.

    tmp-buffy/script.py -> [racine]/tmp-buffy/script.py
    cerveau-projet/... -> [racine]/cerveau-projet/...
    """
    import shlex
    try:
        mots = shlex.split(cmd)
    except ValueError:
        mots = cmd.split()
    resultats = []
    for mot in mots:
        if ("/" in mot or "\\" in mot or
            mot.endswith((".py", ".sh", ".json", ".md"))):
            p = Path(mot)
            if not p.is_absolute():
                # tmp-<agent>/ -> racine du projet
                if mot.startswith("tmp-"):
                    mot = str(_RACINE_PROJET / mot)
                # cerveau-projet/ -> racine / cerveau-projet/
                elif mot.startswith("cerveau-projet/"):
                    mot = str(_RACINE_PROJET / mot)
        resultats.append(mot)
    return " ".join(resultats)


def _extraire_commandes_arbre(etape_texte, agent="", mission=""):
    """Extraire les commandes executables depuis le texte libre d une etape
    de l arbre (format v2-like).

    Detecte les lignes contenant python3 ... et extrait la commande.
    Substitue les placeholders connus (<session>, <MOI>).
    Filtre : placeholders non resolus (<agent>, <chemin>, etc.),
    lignes pures instructionnelles (sans python3).

    Retourne une liste de commandes extraites (peut etre vide).
    """
    commandes = []
    # Decouper en lignes (certains etapes ont plusieurs commandes)
    lignes = etape_texte.split("\n")
    for ligne in lignes:
        ligne = ligne.strip()
        # Detecter python3 n importe ou dans la ligne
        # (apres "Si OUI : ", "Mesurer la duree : ", etc.)
        idx = ligne.find("python3")
        if idx < 0:
            continue
        # Extraire la commande depuis python3 jusqu a la fin
        cmd = ligne[idx:]
        # Couper les notes finales entre parentheses : "cmd (note)" -> "cmd"
        paren_depth = 0
        cut = len(cmd)
        for i in range(len(cmd) - 1, -1, -1):
            if cmd[i] == ")":
                paren_depth += 1
            elif cmd[i] == "(":
                paren_depth -= 1
                if paren_depth == 0:
                    cut = i
                    break
        if cut < len(cmd):
            cmd = cmd[:cut].rstrip()
        # Substituer les placeholders connus AVANT le filtre bloquant
        cmd = _substituer_placeholders(cmd, agent, mission)
        # Placeholders non-resolubles sans contexte humain : rejeter
        # SAUF commandes d activation (Oracle resout <agent> et <raison>)
        bloquants = ["<agent-habilite>", "<motif>", "<nom>",
                     "<domaine>", "<chemin>", "<chemin-outil>",
                     "<lecon>", "<mon bilan>",
                     "<agent_appelant>"]
        est_activation = "activer-agent-principal" in cmd and " activer " in cmd
        if not est_activation and any(b in cmd for b in bloquants):
            continue
        # Pour les activations, garder la commande meme avec <agent> <raison>
        # Resoudre les chemins relatifs (tmp-buffy/ -> racine/tmp-buffy/)
        cmd = _resoudre_chemins(cmd)
        commandes.append(cmd)
    return commandes


def _executer_commande_oracle(cmd, agent, etat):
    """Detecter et executer les commandes que Oracle fait lui-meme.

    Oracle fait TOUT : historise DEBUT/FIN, active les agents, reactive.
    L agent n execute que le travail.

    Retourne (message, execute) : execute=True si Oracle a fait l action.
    """
    if "oracle.py historiser" in cmd and "DEBUT:" in cmd:
        # Eviter le double DEBUT (cmd_activer deja fait)
        if etat.get("historise_debut"):
            return "[ORACLE] DEBUT deja historise pour %s" % agent, True
        raison = etat.get("mission", "")
        _historiser(agent, "DEBUT: " + raison)
        etat["historise_debut"] = True
        _sauver_etat(etat)
        return "[ORACLE] DEBUT historise pour %s" % agent, True
    if "oracle.py historiser" in cmd and "FIN:" in cmd:
        bilan = etat.get("mission", "")
        _historiser(agent, "FIN: " + bilan)
        return "[ORACLE] FIN historisee pour %s" % agent, True
    if "activer-agent-principal" in cmd and " activer " in cmd:
        # BUG CORRIGE 2026-08-28 : Oracle n active PLUS les maillons
        # automatiquement. La delegation est une decision libre : l agent
        # active le maillon lui-meme apres son travail reel. Avant, le
        # pilote deroulait tout l arbre en un appel et activait
        # morpheus/janus/themis sans aucun travail fait, cassant le round.
        return "[PILOTE] Activation laissee a l agent decision libre", False
    return None, False


def _executer_fin_oracle(redir, agent, etat, fins_data):
    """Executer une fin d arbre via Oracle (pas via l agent).

    Oracle historise la FIN et execute l action (reactiver/activer).
    Retourne les messages de trace.
    """
    messages = []
    action_fin = redir.get("action", "")
    cible = redir.get("cible", "")
    bilan = etat.get("mission", "")

    # 1. Marquer FIN dans l etat (pas d historisation ici :
    #    _reactiver_maillon appelera _fin_auto qui historise FIN)
    etat["historise_fin"] = True
    etat["etape"] = "fin"
    _sauver_etat(etat)

    # 2. Bug corrige 2026-08-28 : Oracle n execute PLUS l action de fin
    #    automatiquement reactiver ou activer. La fin suit SA carte : c est
    #    l agent qui active le suivant ou reactive Cerberus (Pattern 13).
    if action_fin == "reactiver" and cible == "cerberus":
        messages.append("[PILOTE] Fin de parcours : l agent doit reactiver "
                        "Cerberus selon SA carte, Pattern 13")
    elif action_fin == "activer" and cible and not cible.startswith("<"):
        messages.append("[PILOTE] Fin de parcours : l agent doit activer "
                        "'%s' selon SA carte, Pattern 13" % cible)
    elif action_fin == "redirection":
        vers = redir.get("vers", "")
        messages.append("[ORACLE] Redirection -> %s" % vers)
    else:
        # procedure ou fin-theme : historiser FIN ici
        _historiser(agent, "FIN: " + bilan)
        messages.append("[ORACLE] FIN historisee pour %s" % agent)

    return messages


def _piloter_theme(theme, fins_data, etat, agent, limite):
    """Piloter un theme de l arbre : naviguer dans les redirects (besoins).

    Oracle fait TOUT :
      - historise DEBUT/FIN (pas l agent)
      - active les agents (pas Cerberus)
      - reactive Cerberus (pas l agent)
      - sert les commandes de TRAVAIL dans l inbox de l agent

    Retourne (messages, etape_finale) ou (messages, "decision-libre")
    """
    # Les redirects sont dans theme["theme"]["redirects"] (format v2-like)
    redirects = theme.get("theme", {}).get("redirects", [])
    if not redirects:
        redirects = theme.get("redirects", [])
    if not redirects:
        nom = theme.get("theme", {}).get("nom") or theme.get("identite", {}).get("nom", "?")
        return ["[PILOTE] Theme '%s' sans redirects" % nom], "fin"

    redirect_idx = etat.get("redirect_idx", 0)
    etape_idx = etat.get("etape_idx", 0)
    messages = []
    pas = 0

    while pas < limite and redirect_idx < len(redirects):
        pas += 1
        redir = redirects[redirect_idx]
        besoin = redir.get("besoin", "")
        action = redir.get("action", "procedure")
        etapes = redir.get("etapes", [])
        regle = redir.get("regle", "")

        messages.append("--- BESOIN %d/%d : %s ---" % (
            redirect_idx + 1, len(redirects), besoin))
        if regle:
            messages.append("[REGLE] %s" % regle)

        # --- REDIRECTION : suivre le lien ---
        if action == "redirection":
            vers = redir.get("vers", "")
            messages.append("[PILOTE] Redirection -> %s" % vers)
            break

        # --- FIN D ARBRE : Oracle historise FIN + execute l action ---
        if action in ("activer", "reactiver") and not etapes:
            fin_msgs = _executer_fin_oracle(redir, agent, etat, fins_data)
            messages.extend(fin_msgs)
            break

        # --- PROCEDURE : parcourir les etapes ---
        while etape_idx < len(etapes):
            etape = etapes[etape_idx]
            commandes = _extraire_commandes_arbre(etape, agent, etat.get("mission", ""))

            if commandes:
                for cmd in commandes:
                    # Oracle execute ses propres actions
                    msg, execute = _executer_commande_oracle(cmd, agent, etat)
                    if execute:
                        messages.append(msg)
                    else:
                        # Commande de travail : servir dans l inbox
                        messages.append("SERVE POUR VOUS :\n  > %s" % cmd)
                etape_idx += 1
            else:
                messages.append("  [INFO] %s" % etape)
                etape_idx += 1
                # Verifier si des commandes restent dans les etapes suivantes
                a_commande = False
                for i in range(etape_idx, len(etapes)):
                    if _extraire_commandes_arbre(etapes[i], agent, etat.get("mission", "")):
                        a_commande = True
                        break
                if not a_commande:
                    # INFO-only redirect : on sort pour avancer au suivant
                    break

        # Avancer au redirect suivant
        redirect_idx += 1
        etape_idx = 0
        etat["redirect_idx"] = redirect_idx
        etat["etape_idx"] = 0
        _sauver_etat(etat)

    # Theme termine
    if redirect_idx >= len(redirects):
        nom = theme.get("theme", {}).get("nom") or theme.get("identite", {}).get("nom", "?")
        messages.append("[PILOTE] Theme '%s' termine." % nom)
        # Oracle execute la fin du theme (depuis l objet fin du theme -> fins.json)
        fin_ref = theme.get("fin", {})
        if fin_ref.get("type") == "lien" and fins_data:
            fin_case = fins_data.get("fins", {}).get(fin_ref.get("case", ""), {})
            if fin_case:
                fin_msgs = _executer_fin_oracle(fin_case, agent, etat, fins_data)
                messages.extend(fin_msgs)
        else:
            messages.append("  Retour a la racine.")
        return messages, "fin-theme"

    # Sauvegarder la position courante
    etat["redirect_idx"] = redirect_idx
    etat["etape_idx"] = etape_idx
    _sauver_etat(etat)
    return messages, "en-cours"


def _piloter_arbre(arbre, arbre_dir, etat, agent, limite):
    """Piloter un arbre de decisions v2-like.

    Charge la racine, resout la branche (theme), puis navigue dans le
    theme via _piloter_theme(). Gere les fins centralisees (fins.json).

    Retourne un dict {etat, messages}.
    """
    racine = arbre.get("racine", {})
    fins_ref = arbre.get("fins", {})
    fins_fichier = fins_ref.get("fichier", "fins.json")
    fins_data = _charger_fichier(arbre_dir, fins_fichier)

    messages = []
    theme_courant = etat.get("theme_courant")

    # Premiere execution : resoudre la racine
    if not theme_courant:
        # Verification que la mission_type est definie
        if not etat.get("mission_type"):
            return {"erreur": "mission_type non defini pour %s" % agent, "etat": etat}
        vers = _resoudre_racine(racine, etat)
        if not vers:
            etat["etape"] = "decision-libre"
            _sauver_etat(etat)
            return {
                "etat": etat,
                "messages": ["DECISION LIBRE : theme '%s" % etat.get("mission_type", "?") +
                             "' non reconnu dans la racine. Laisser la main a l agent."]
            }
        theme_courant = vers
        etat["theme_courant"] = theme_courant
        etat["redirect_idx"] = 0
        etat["etape_idx"] = 0
        _sauver_etat(etat)
        messages.append("[PILOTE] Racine resolue : theme = %s" % theme_courant)

    # Charger le theme
    theme = _charger_fichier(arbre_dir, theme_courant)
    if not theme:
        return {"erreur": "theme introuvable: %s" % theme_courant, "etat": etat}

    # Naviguer dans le theme
    theme_messages, etape_finale = _piloter_theme(theme, fins_data, etat, agent, limite)
    messages.extend(theme_messages)

    # Gerer la fin du theme
    if etape_finale == "fin-theme":
        # Retour a la racine : reinitialiser le theme courant
        etat["theme_courant"] = None
        etat.pop("redirect_idx", None)
        etat.pop("etape_idx", None)
        _sauver_etat(etat)
        # Relancer le pilotage (re-resolution de la racine)
        # Si le theme est termine, c est que la mission est terminee
        if not etat.get("historise_fin"):
            _fin_auto(etat, etat.get("mission", ""))
        messages.append("PARCOURS TERMINE (arbre %s)" % agent)
    elif etape_finale == "decision-libre":
        # DECISION LIBRE : l agent LLM decide. Etat deja sauvegarde.
        # Ne PAS executer la fin du theme ici.
        messages.append("[PILOTE] En attente de la decision de l agent.")
    elif etape_finale == "en-cours":
        # Position sauvegardee dans le theme, on continue au prochain appel
        pass

    return {"etat": etat, "messages": messages}


def pilote(agent, parcours_perso=None, limite=float("inf")):
    """Piloter la carte/arbre de l agent : avancer case par case (carte)
    ou redirect par redirect (arbre) jusqu a une decision libre ou la fin.

    Retourne un dict etat final + messages.
    Retourne {"erreur": msg} en cas d impossibilite.
    """
    etat = _charger_etat(agent)
    if not etat.get("parcours"):
        return {"erreur": "aucun etat de carte pour %s (oracle pilote init_etat?)" % agent}
    chemin = parcours_perso or etat["parcours"]
    parcours = _charger_parcours(chemin)
    if not parcours:
        return {"erreur": "parcours introuvable: %s" % chemin}

    # Detection du format : arbre (v2-like) ou carte (v1 cases)
    identite = parcours.get("identite", {})
    if identite.get("type") == "arbre":
        # Format arbre v2-like : navigation multi-fichiers
        arbre_dir = Path(chemin).parent
        if not arbre_dir.is_absolute():
            arbre_dir = _RACINE / arbre_dir
        return _piloter_arbre(parcours, arbre_dir, etat, agent, limite)

    # Format carte v1 : navigation cases
    cases = parcours.get("cases", {})
    meta = parcours.get("parcours", {})

    # Case de depart : premiere execution -> c0 (relecture) ; sinon reprise
    cid = etat.get("case_courante") or meta.get("case_depart") or "c0"
    if cid not in cases:
        cid = meta.get("case_depart") or "c0"

    messages = []
    pas = 0

    while pas < limite:
        pas += 1
        case = cases.get(cid)
        if not case:
            return {"erreur": "case %s introuvable" % cid, "etat": etat}
        typ = case.get("type", "question")

        if typ == "fin":
            if not etat.get("historise_fin"):
                _fin_auto(etat, etat.get("mission", ""))
            messages.append("PARCOURS TERMINE (case %s)" % cid)
            break

        if typ in ("action", "indice"):
            if "historiser la fin" in (case.get("titre") or "").lower():
                fin = _fin_auto(etat, etat.get("mission", ""))
                messages.append(fin or "[PILOTE] FIN pose automatiquement")
                suivant_fin = case.get("suivant")
                if suivant_fin:
                    etat["case_courante"] = suivant_fin
                    _sauver_etat(etat)
                    cid = suivant_fin
                    continue
                break
            plateau, cmd = _extraire_commande(case)
            if plateau:
                messages.append(plateau)
            suivant = case.get("suivant")
            if not suivant:
                etat["historise_fin"] = True
                etat["etape"] = "fin"
                _sauver_etat(etat)
                break
            etat["case_courante"] = suivant
            _sauver_etat(etat)
            cid = suivant
            continue

        # Question : resoudre automatiquement
        reponse = _resoudre_question(case, etat)

        # DELEGATION - bug corrige 2026-08-28 : plus d activation
        # automatique des maillons. La delegation est une decision libre :
        # l agent active le maillon apres son travail reel (Pattern 13).
        if _est_case_delegation(case):
            etat["case_courante"] = cid
            etat["etape"] = "decision-libre"
            _sauver_etat(etat)
            messages.append("DELEGATION a la case %s : decision libre, "
                            "l agent active le maillon apres son travail" % cid)
            break

        if reponse is None:
            etat["case_courante"] = cid
            etat["etape"] = "decision-libre"
            _sauver_etat(etat)
            messages.append("DECISION LIBRE a la case %s (%s) : laisser la main" % (
                cid, case.get("titre", "")))
            break
        b = _s(reponse, [br.get("reponse", "") for br in case.get("branches", [])])
        vers = None
        if b is not None:
            for br in case.get("branches", []):
                if br.get("reponse", "").strip().lower() == b.lower():
                    vers = br.get("vers")
                    break
        if not vers:
            messages.append("REPONSE '%s' sans branche a la case %s : arret" % (reponse, cid))
            etat["case_courante"] = cid
            _sauver_etat(etat)
            break
        etat["case_courante"] = vers
        _sauver_etat(etat)
        cid = vers

    etat["case_courante"] = cid
    _sauver_etat(etat)
    return {"etat": etat, "messages": messages}


def cmd_pilote(args):
    """CLI : oracle pilote <agent> [--apres CASE] [--limite N]."""
    agent = args.agent
    parcours_perso = getattr(args, "parcours", None)
    limite = getattr(args, "limite", 1)
    res = pilote(agent, parcours_perso, limite)
    if "erreur" in res:
        print("[PILOTE] ERREUR: %s" % res["erreur"])
        return 1
    etat = res.get("etat", {})
    print("=== ORACLE PILOTE -- %s ===" % agent)
    print("Parcours : %s" % etat.get("parcours", "?"))
    print("Case courante : %s" % (etat.get("case_courante", "?")))
    print("Mission type : %s" % etat.get("mission_type", "?"))
    print("Etape : %s" % etat.get("etape", "?"))
    print()
    if etat.get("mission"):
        print("TA MISSION : %s" % etat.get("mission"))
    print("ORDRE : DEMARRE MAINTENANT, execute la mission, puis suis ta carte.")
    print()
    for m in res.get("messages", []):
        print(m)
    return 0


def main():
    import argparse
    parser = argparse.ArgumentParser(prog="oracle-pilote", description="Pilote de carte v1")
    parser.add_argument("agent", help="Agent a piloter")
    parser.add_argument("--parcours", help="Parcours perso (defaut: etat de carte)")
    parser.add_argument("--limite", type=int, default=1, help="Nb max de pas (defaut 1 : servir UNE etape de travail a la fois)")
    parser.add_argument("--init", action="store_true",
                        help="(re)initialiser l etat : agent + --mission-type")
    parser.add_argument("--mission-type", default="construire")
    parser.add_argument("--mission", default="")
    parser.add_argument("--version", action="version", version="pilote v%s" % VERSION)
    args = parser.parse_args()
    if args.init:
        init_etat(args.agent, args.parcours, args.mission_type, args.mission)
        print("[PILOTE] Etat de carte initialise pour %s (%s)" % (args.agent, args.mission_type))
        return 0
    return cmd_pilote(args)


if __name__ == "__main__":
    sys.exit(main())