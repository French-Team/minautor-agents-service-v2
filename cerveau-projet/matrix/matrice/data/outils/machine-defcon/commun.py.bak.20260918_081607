"""Fonctions communes de machine-defcon : etat courant, transition, journal.

Le niveau courant vit dans le classeur-variables (cle defcon) : UNE source
de verite, maintenue avec le motif de la porte bdd-variables (atomique +
empreinte SHA-256). Le journal defcon-historique.jsonl trace chaque transition.
"""
import hashlib
import json
import os
from datetime import datetime

from constants import (
    CHEMIN_CLASSEUR,
    CHEMIN_EMPREINTE_CLASSEUR,
    CHEMIN_JOURNAL,
    CLE_DEFCON,
    ENCODAGE,
    INDENTATION_JSON,
    NOM_CLASSEUR_TMP,
    TAILLE_BLOC_LECTURE,
)


def horodatage():
    """Retourne l'horodatage local au format de la Matrice."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def charger_classeur():
    """Retourne le contenu du classeur-variables (lecture seule)."""
    with open(CHEMIN_CLASSEUR, "r", encoding=ENCODAGE) as flux:
        return json.load(flux)


def trouver_defcon(donnees):
    """Retourne (niveau_courant, entree_defcon) ou (None, None) si absente."""
    for variable in donnees.get("variables", ()):
        if variable.get("cle") == CLE_DEFCON:
            return int(variable.get("valeur")), variable
    return None, None


def lire_niveau():
    """Retourne (niveau_courant, message_absence). (niveau, "") si presente."""
    donnees = charger_classeur()
    niveau, _ = trouver_defcon(donnees)
    if niveau is None:
        return None, "Variable '" + CLE_DEFCON + "' absente du classeur : la definir via bdd-variables."
    return niveau, ""


def appliquer_transition(donnees, entree, cible, source):
    """Met a jour l'entree defcon en place puis ecrit le classeur entier.

    Motif porte unique : atomique (tmp + remplacement), LF forces,
    empreinte SHA-256 recalculee apres ecriture.
    """
    entree["valeur"] = str(cible)
    entree["source"] = source
    entree["date"] = horodatage()

    chemin_temporaire = CHEMIN_CLASSEUR.with_name(NOM_CLASSEUR_TMP)
    with open(chemin_temporaire, "w", encoding=ENCODAGE, newline="\n") as flux:
        json.dump(donnees, flux, indent=INDENTATION_JSON, ensure_ascii=True)
        flux.write("\n")
    os.replace(chemin_temporaire, CHEMIN_CLASSEUR)

    hacheur = hashlib.sha256()
    with open(CHEMIN_CLASSEUR, "rb") as flux:
        for bloc in iter(lambda: flux.read(TAILLE_BLOC_LECTURE), b""):
            hacheur.update(bloc)
    empreinte = hacheur.hexdigest()
    with open(CHEMIN_EMPREINTE_CLASSEUR, "w", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(empreinte + "\n")
    return empreinte


def extraire_options(arguments, noms_connus):
    """Extrait les options --nom valeur d'une liste d'arguments (forme seulement)."""
    options = {}
    index = 0
    while index < len(arguments):
        nom = arguments[index]
        if nom in noms_connus and index + 1 < len(arguments):
            options[nom] = arguments[index + 1]
            index += 2
        else:
            index += 1
    return options


def journaliser_transition(depuis, vers, raison, source):
    """Append une ligne JSON au journal des transitions (jamais bloquant)."""
    ligne = {
        "quand": horodatage(),
        "de": depuis,
        "vers": vers,
        "raison": raison,
        "source": source,
    }
    with open(CHEMIN_JOURNAL, "a", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(ligne, ensure_ascii=True) + "\n")


def lire_journal(n=5):
    """Retourne les n dernieres transitions (les plus recentes en premier)."""
    if not CHEMIN_JOURNAL.exists():
        return []
    transitions = []
    for ligne in CHEMIN_JOURNAL.read_text(encoding=ENCODAGE).splitlines():
        try:
            transitions.append(json.loads(ligne))
        except json.JSONDecodeError:
            continue
    return list(reversed(transitions))[:n]
