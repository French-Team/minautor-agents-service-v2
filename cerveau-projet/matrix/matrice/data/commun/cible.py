"""Le DOMICILE de la resolution d un CHEMIN DE CIBLE (argument d un outil).

Probleme fondamental (convention-chemins-liens-noms-flags, point 1.1) : un
chemin d argument resolu contre le CWD depend de QUI lance. Mesure du
2026-09-17 (friction 80) : sc-001 acceptait `--fichier <relatif a matrix/>`
lance depuis la racine, et REFUSAIT la MEME cible lancee depuis son propre
dossier -- deux verdicts pour un seul fichier, et un rouge qui accusait la
cible au lieu d accuser l ancrage.

Trois formes couvertes, dans CET ordre :
  1. chemin ABSOLU : tel quel, aucune base ;
  2. relatif a la RACINE du workspace (celle qui porte AGENTS.md) ;
  3. relatif a <racine>/cerveau-projet/matrix, puis <racine>/matrix.

Le cwd n est JAMAIS une base. Un refus NOMME les bases essayees : un refus qui
ne dit pas OU il a cherche coute trois essais (friction 77).

La racine est DETECTEE par le motif partage (racine.py, L-013) : ce module la
CONSOMME, il ne la recopie jamais (M-076 : une valeur recopiee derive en
silence ; L-100/L-102).
"""
import os
from pathlib import Path

from racine import detecter_racine

# Les deux formes reelles du depot : la Matrice vit sous cerveau-projet/matrix,
# et peut vivre directement sous la racine dans une installation depliee.
NOMS_MATRICE = ("cerveau-projet/matrix", "matrix")


def bases(depart):
    """Les bases d ancrage, dans l ordre : la racine du workspace, puis matrix/."""
    racine = detecter_racine(depart)
    return (racine,) + tuple(racine / nom for nom in NOMS_MATRICE)


def resoudre(fichier, depart):
    """(chemin, motif) : ancre <fichier> sur la racine detectee depuis <depart>.

    Rend (None, motif) si la cible est introuvable -- et le motif NOMME alors
    les bases essayees, pour que l appelant puisse le dire tel quel.
    """
    brut = Path(str(fichier).strip())
    if not brut.name:
        return None, "cible vide (aucun chemin fourni)"
    if brut.is_absolute():
        if brut.exists():
            return brut, "cible presente : " + str(brut)
        return None, "cible INTROUVABLE : " + str(brut) + " (chemin absolu)"
    essayees = bases(depart)
    for base in essayees:
        candidat = base / brut
        if candidat.exists():
            return candidat, "cible presente : " + str(candidat)
    return None, (
        "cible INTROUVABLE : " + str(fichier) + " -- essaye sous "
        + ", ".join(str(base) for base in essayees)
        + " (le cwd n est JAMAIS une base : convention 1.1)"
    )


def racine_matrice(depart):
    """La racine de la MATRICE : le dossier qui porte `matrice/` et `_operateur/`.

    C est la base de travail des chemins de BDD (plan de conservation : chemins
    relatifs a la racine `matrix/`). Deux installations reelles : la Matrice vit
    sous `<racine>/cerveau-projet/matrix` (depot de developpement) ou directement
    sous `<racine>/matrix` (installation depliee). Si aucune n existe, on rend la
    racine du workspace : un appelant qui tenterait d ecrire DANS la Matrice sera
    refuse plus loin par le perimetre, jamais ici en silence.
    """
    racine = detecter_racine(depart)
    for nom in NOMS_MATRICE:
        candidat = racine / nom
        if candidat.is_dir():
            return candidat
    return racine


def resoudre_dans_matrice(fichier, depart):
    """(chemin, motif) : ancre une DESTINATION (cible A CREER) sur la Matrice.

    Pourquoi une fonction de plus que `resoudre` : `resoudre` exige que la cible
    EXISTE -- c est une verification de LECTURE. Une destination, elle, n existe
    pas encore ; mais elle n a qu UNE base possible et DECLAREE (la Matrice), la
    ou les sources se cherchent dans une liste de bases.

    Toute cible qui SORTIRAIT de la Matrice (chemin absolu dehors, ou `..`) est
    REFUSEE : c est le plan de conservation qui l exige (aucune operation hors de
    `matrix/`). Le refus NOMME la base, pour que l appelant puisse le dire tel quel.
    """
    base = racine_matrice(depart)
    brut = Path(str(fichier).strip())
    if not brut.name:
        return None, "destination vide (aucun chemin fourni)"
    candidat = brut if brut.is_absolute() else base / brut
    candidat = Path(os.path.normpath(str(candidat)))
    try:
        candidat.relative_to(base)
    except ValueError:
        return None, (
            "destination REFUSEE : " + str(fichier) + " sort de la Matrice ("
            + str(base) + ")"
        )
    return candidat, "destination dans la Matrice : " + str(candidat)
