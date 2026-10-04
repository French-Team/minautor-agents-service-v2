#!/usr/bin/env python3
# -*- coding: ascii -*-
# classeur.py -- routine centrale du classeur de variables v1
# identite:
#   type: routine
#   appartient_a: commun
#   commun: true

"""Routine centrale de lecture/ecriture du classeur-variables v1.

Contrat :
  - toute lecture est tracee comme CLASSEUR ENTREE ;
  - toute ecriture est tracee comme CLASSEUR SORTIE ;
  - toute erreur est tracee avec resultat=ERREUR ;
  - les fichiers restent ASCII + LF ;
  - l historique passe par Oracle, jamais par une copie concurrente.

Cette routine est appelee par les points centraux qui manipulent le classeur.
Elle ne lance aucun daemon et ne modifie aucune mission.
"""

import importlib.util
import io
import os
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"


def _racine_projet():
    """Trouver la racine en cherchant AGENTS.md."""
    courant = Path(__file__).resolve()
    for parent in [courant.parent] + list(courant.parents):
        if (parent / "AGENTS.md").is_file():
            return parent
    return Path.cwd()


RACINE = _racine_projet()
CLASSEUR_DEFAUT = Path(os.environ.get("CLASSEUR_STOCKAGE", str(RACINE / "cerveau-projet" / "agents" / "classeur-variables" / "stockage" / "variables-actuelles.md")))


def _chemin_env(nom, defaut):
    """Lire un chemin surchargeable par les tests sur copie."""
    return Path(os.environ.get(nom, str(defaut)))


def _chemin_historique(fichier):
    """Resoudre l historique sans ecrire dans le projet depuis une copie."""
    env = os.environ.get("CLASSEUR_HISTORIQUE")
    if env:
        return Path(env)
    chemin = Path(fichier)
    if chemin.name == "variables-actuelles.md" and chemin.parent.name == "stockage":
        return chemin.parent.parent / "historique" / "historique-modifications.md"
    return chemin.with_name("historique-modifications.md")


def _historiser(agent, session, raison, classeur_path=None):
    """Tracer dans Oracle et dans AGENTS-activite-recente.md."""
    if os.environ.get("CLASSEUR_TRACE_EN_COURS") == "1":
        return True
    oracle = RACINE / "cerveau-projet" / "agents" / "tools" / "activer" / "activer-agent-principal" / "activer-agent-principal.py"
    if not oracle.is_file():
        return False
    env = {
        "AGENTS_FILE": _chemin_env("AGENTS_FILE", RACINE / "AGENTS.md"),
        "AGENTS_HISTORIQUE": _chemin_env("AGENTS_HISTORIQUE", RACINE / "AGENTS-historique.md"),
        "AGENTS_ACTIVITE_RECENTE": _chemin_env("AGENTS_ACTIVITE_RECENTE", RACINE / "AGENTS-activite-recente.md"),
        "CLASSEUR_STOCKAGE": Path(classeur_path or CLASSEUR_DEFAUT),
        "CLASSEUR_HISTORIQUE": _chemin_historique(classeur_path or CLASSEUR_DEFAUT),
        "GRADES_V1": _chemin_env("GRADES_V1", RACINE / "cerveau-projet" / "agents" / "tools" / "oracle" / "grades-v1.json"),
    }
    anciens = {nom: os.environ.get(nom) for nom in env}
    ancien_trace = os.environ.get("CLASSEUR_TRACE_EN_COURS")
    os.environ["CLASSEUR_TRACE_EN_COURS"] = "1"
    try:
        os.environ.update({nom: str(valeur) for nom, valeur in env.items()})
        spec = importlib.util.spec_from_file_location("aap_classeur", str(oracle))
        if spec is None or spec.loader is None:
            return False
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return module.ajouter_historique(
            timestamp,
            session or "session-admin",
            agent or "inconnu",
            raison,
            "R",
            executeur="Oracle",
        ) == 0
    except Exception:
        return False
    finally:
        if ancien_trace is None:
            os.environ.pop("CLASSEUR_TRACE_EN_COURS", None)
        else:
            os.environ["CLASSEUR_TRACE_EN_COURS"] = ancien_trace
        for nom, valeur in anciens.items():
            if valeur is None:
                os.environ.pop(nom, None)
            else:
                os.environ[nom] = valeur


def _trace(operation, variable, source, resultat, agent, session, detail="", classeur_path=None):
    """Emettre une trace lisible dans les activites recentes."""
    operation = (operation or "").upper()
    variable = variable or "*"
    source = source or "inconnu"
    resultat = resultat or "ERREUR"
    raison = "CLASSEUR %s: variable=%s source=%s resultat=%s" % (
        operation, variable, source, resultat)
    if detail:
        raison += " detail=%s" % detail
    return _historiser(agent, session, raison, classeur_path)


def lire_fichier(fichier=None, variable="*", source="classeur", agent="oracle", session="session-admin", tracer=True):
    """Lire le stockage et tracer une entree.

    Retourne (lignes, ligne_variable). En cas d erreur fichier, retourne
    (None, None). Une variable absente est signalee dans le detail mais la
    lecture du classeur reste une entree valide.
    """
    chemin = Path(fichier or CLASSEUR_DEFAUT)
    try:
        contenu = chemin.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        if tracer:
            _trace("ENTREE", variable, source, "ERREUR", agent, session, "lecture=%s" % type(exc).__name__, str(chemin))
        return None, None
    lignes = contenu.split("\n")
    trouvee = None
    if variable and variable != "*":
        prefixe = "| `" + variable + "` |"
        for ligne in lignes:
            if ligne.startswith(prefixe):
                trouvee = ligne
                break
    resultat = "OK"
    detail = "fichier=%s" % chemin.name
    if variable and variable != "*" and trouvee is None:
        resultat = "ERREUR"
        detail += " variable_absente"
    if tracer:
        try:
            _trace("ENTREE", variable, source, resultat, agent, session, detail, str(chemin))
        except Exception:
            pass
    return lignes, trouvee


def valeur_depuis_ligne(ligne):
    """Extraire la valeur de la deuxieme cellule d une ligne markdown."""
    if not ligne:
        return None
    cellules = ligne.split("|")
    if len(cellules) < 3:
        return None
    return cellules[2].strip()


def _ecrire_historique(fichier, variable, source, ancienne_valeur, nouvelle_valeur, raison):
    """Conserver une trace immuable de l ecriture du classeur."""
    chemin = _chemin_historique(fichier)
    try:
        contenu = chemin.read_text(encoding="utf-8") if chemin.is_file() else ""
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        entree = (
            "## %s -- Ecriture\n\n"
            "- **Variable** : %s\n"
            "- **Ancienne valeur** : %s\n"
            "- **Nouvelle valeur** : %s\n"
            "- **Source** : %s\n"
            "- **Raison** : %s\n\n"
        ) % (date, variable or "*", ancienne_valeur or "(non fournie)",
             nouvelle_valeur or "(non fournie)", source or "inconnu",
             raison or "Ecriture centralisee du classeur")
        entree.encode("ascii")
        marqueur = "## Entrees recentes"
        if marqueur in contenu:
            pos = contenu.index(marqueur) + len(marqueur)
            contenu = contenu[:pos] + "\n" + entree + contenu[pos:]
        else:
            contenu += "\n" + entree
        with io.open(chemin, "w", encoding="ascii", newline="\n") as fh:
            fh.write(contenu)
        return True
    except (OSError, UnicodeError):
        return False


def ecrire_lignes(fichier, lignes, variable="*", source="classeur", agent="oracle", session="session-admin", ancienne_valeur=None, nouvelle_valeur=None, raison=None):

    """Ecrire le stockage en ASCII + LF et tracer une sortie."""
    chemin = Path(fichier or CLASSEUR_DEFAUT)
    texte = "\n".join(lignes)
    try:
        texte.encode("ascii")
    except UnicodeEncodeError:
        _trace("SORTIE", variable, source, "ERREUR", agent, session, "non-ascii", str(chemin))
        return False
    try:
        with io.open(chemin, "w", encoding="ascii", newline="\n") as fh:
            fh.write(texte)
    except OSError as exc:
        _trace("SORTIE", variable, source, "ERREUR", agent, session, "ecriture=%s" % type(exc).__name__, str(chemin))
        return False
    if not _ecrire_historique(chemin, variable, source, ancienne_valeur,
                              nouvelle_valeur, raison):
        _trace("SORTIE", variable, source, "ERREUR", agent, session,
               "historique-modifications", str(chemin))
        return False
    _trace("SORTIE", variable, source, "OK", agent, session,
           "fichier=%s" % chemin.name, str(chemin))
    return True


def lire_variable(fichier=None, variable="*", source="classeur", agent="oracle", session="session-admin"):
    """Lire une variable et retourner sa valeur, ou None si absente."""
    _, ligne = lire_fichier(fichier, variable, source, agent, session)
    return valeur_depuis_ligne(ligne)
