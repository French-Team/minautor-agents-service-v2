"""Fonctions partagees de la porte des fichiers de travail du cameleon (MO-378).

Un seul domicile pour les ATOMES de cette porte (M-076) : chaque categorie les
CONSOMME, aucune ne les recopie. Les DOMICILES (zone, journal) viennent de
constants.py, qui les tient du moteur PARTAGE data/commun/zone_tmp.py.
"""

import json
from datetime import datetime
from pathlib import Path

from constants import (
    ACTION_CREE,
    ACTION_PURGE,
    EXTENSIONS,
    JOURNAL,
    MOTIF_CANONIQUE,
    MOTIF_LIBELLE,
    MOTIF_MISSION,
    RACINE,
)
from zone_tmp import contenu as contenu_zone


def maintenant():
    """L horodatage des traces du projet, a la seconde."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def chemin_relatif(chemin):
    """Le chemin RELATIF a la RACINE du workspace, en barres obliques."""
    try:
        return Path(chemin).resolve().relative_to(RACINE.resolve()).as_posix()
    except (ValueError, OSError):
        return str(chemin).replace(chr(92), "/")


def nom_canonique(mission, libelle, extension):
    """Le NOM CANONIQUE du cameleon (m-<numero>-<libelle>.<ext>), ou (None, refus).

    Trois champs, trois refus DISTINCTS et nommes. La mission est rendue en
    minuscules : le nom porte la mission, donc la purge ciblee s y relit.
    """
    mission = (mission or "").strip().lower()
    libelle = (libelle or "").strip().lower()
    extension = (extension or "").strip().lower().lstrip(".")
    if not MOTIF_MISSION.match(mission):
        return None, ("REFUS : identifiant de mission invalide (< " + str(mission)
                      + " >) -- forme attendue M-<numero>, par exemple M-378.")
    if not MOTIF_LIBELLE.match(libelle):
        return None, ("REFUS : libelle invalide (< " + str(libelle)
                      + " >) -- minuscules, chiffres et tirets : par exemple bilan.")
    if extension not in EXTENSIONS:
        return None, ("REFUS : extension < " + str(extension) + " > hors liste -- "
                      + ", ".join(EXTENSIONS) + ".")
    return mission + "-" + libelle + "." + extension, None


def mission_du_nom(nom):
    """L identifiant de mission PORTE par un nom canonique, ou None."""
    trouve = MOTIF_CANONIQUE.match(nom or "")
    if not trouve:
        return None
    return "m-" + trouve.group(1)


def est_canonique(nom):
    """Vrai si le nom porte la forme canonique du cameleon."""
    return MOTIF_CANONIQUE.match(nom or "") is not None


def journal_lire(chemin_journal=None):
    """Les entrees du journal, dans l ORDRE, ligne par ligne.

    Une ligne ILLISIBLE n est pas avalee : elle est rendue sous l action
    `illisible` avec son texte brut -- un journal qui cache une ligne qu il ne
    comprend pas se lirait comme un journal complet.
    """
    chemin = Path(chemin_journal or JOURNAL)
    entrees = []
    if not chemin.is_file():
        return entrees
    try:
        lignes = chemin.read_text(encoding="utf-8").splitlines()
    except OSError:
        return entrees
    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            entrees.append(json.loads(ligne))
        except ValueError:
            entrees.append({"action": "illisible", "brut": ligne})
    return entrees


def journal_noter(entree, chemin_journal=None):
    """Ajoute UNE entree horodatee au journal (ajout seul, jamais de reecriture)."""
    chemin = Path(chemin_journal or JOURNAL)
    entree = dict(entree)
    entree["date"] = maintenant()
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(str(chemin), "a", encoding="utf-8", newline="\n") as flux:
        flux.write(json.dumps(entree, ensure_ascii=True) + "\n")
    return entree


def noms_journalises(chemin_journal=None):
    """{nom: entree} des noms POSES par la porte (au moins une ligne cree)."""
    poses = {}
    for entree in journal_lire(chemin_journal):
        if entree.get("action") == ACTION_CREE and entree.get("nom"):
            poses[entree["nom"]] = entree
    return poses


def elements_zone(zone, chemin_journal=None):
    """La zone, element par element, avec sa CLASSE -- aucun element tu.

    Trois classes, DITES :
      - `canonique` : le nom porte <mission>-<libelle>.<ext> ET la porte l a pose ;
      - `canonique-non-journalise` : la forme est canonique, mais la porte ne l a
        jamais pose -- un fichier ne hors de la porte, ce qui se DIT ;
      - `residu` : le nom ne porte AUCUNE forme canonique -- le cas d un fichier
        pose a la main, que cette porte REND VISIBLE.
    """
    journalises = noms_journalises(chemin_journal)
    elements = []
    for element in contenu_zone(zone):
        nom = element.name
        try:
            stat = element.stat()
            taille = stat.st_size if element.is_file() else -1
            modifie = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        except OSError:
            taille, modifie = -1, ""
        canonique = est_canonique(nom)
        if canonique and nom in journalises:
            classe = "canonique"
        elif canonique:
            classe = "canonique-non-journalise"
        else:
            classe = "residu"
        elements.append({"nom": nom, "dossier": element.is_dir(), "taille": taille,
                         "modifie": modifie, "canonique": canonique,
                         "mission": mission_du_nom(nom) or "", "classe": classe})
    return elements


def _options(arguments, connues, drapeaux=()):
    """Rend (options, positionnels, refus) -- une option INCONNUE est un REFUS NOMME."""
    options = {}
    positionnels = []
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument.startswith("--"):
            nom = argument[2:]
            if nom not in connues:
                return None, None, ("REFUS : option inconnue < " + argument + " > -- connues : "
                                    + ", ".join("--" + connu for connu in connues) + ".")
            if nom in drapeaux:
                options[nom] = True
                index += 1
                continue
            if index + 1 >= len(arguments):
                return None, None, "REFUS : option sans valeur < " + argument + " >."
            options[nom] = arguments[index + 1]
            index += 2
            continue
        positionnels.append(argument)
        index += 1
    return options, positionnels, None
