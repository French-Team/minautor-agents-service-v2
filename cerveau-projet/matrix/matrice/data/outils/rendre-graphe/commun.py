"""Fonctions partagees de rendre-graphe : lire une source, ecrire une vue, lancer.

DEUX REGLES, et elles viennent de loin :
  - L ECRITURE PASSE PAR LA PORTE (`ecrire`) : une vue est un FICHIER de la Matrice,
    donc elle se POSE par le passage unique -- celui qui mesure l ASCII, pose un
    point de restauration et TRACE l ecriture. L outil ne se donne pas le droit
    d ecrire seul : il COMPOSE la vue, puis il la PORTE ;
  - LES TEXTES PASSENT PAR DES FICHIERS : un argument traverse le shell, ou un
    accent grave est EXECUTE et troue la trace (mesure MO-142). Le contenu va donc
    dans un fichier de la zone jetable, et la ligne de commande ne porte que des
    CHEMINS.

L ANCRAGE DES CHEMINS suit le domicile partage (data/commun/cible.py) : la porte
resout un chemin contre la RACINE du workspace (celle qui porte AGENTS.md). Un
chemin relatif a la Matrice serait donc resolu AILLEURS -- et refuse.
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

from constants import (
    CHEMIN_LANCEUR,
    NOM_OUTIL,
    RACINE,
    REPERTOIRE_COMMUN,
    REPERTOIRE_JETABLE,
    REPERTOIRE_OUTILS,
)

# LE DOMICILE PARTAGE DE LA MATRICE (M-076) : installe sur le chemin ICI, une fois,
# pour que `drapeaux_popen` et `extraire_options` ne puissent pas etre reecrits a
# nu -- un sous-processus lance sans ses drapeaux fait clignoter une fenetre chez
# le createur (E-056), et des options redevinees divergent en silence.
if str(REPERTOIRE_COMMUN) not in sys.path:
    sys.path.insert(0, str(REPERTOIRE_COMMUN))
from lancement import drapeaux_popen  # noqa: E402,F401  (re-export : le domicile)
from options import extraire_options  # noqa: E402,F401  (re-export : le domicile)

import subprocess  # noqa: E402  (les drapeaux viennent du domicile, pas d ici)

APPELANT = "operateur"
LARGEUR_RESUME = 200


def charger_json(chemin):
    """Le contenu de <chemin>, ou None. Un fichier illisible se DIT, jamais un vide muet."""
    chemin = Path(chemin)
    if not chemin.is_file():
        return None
    try:
        with open(str(chemin), "r", encoding="utf-8") as flux:
            return json.load(flux)
    except (OSError, ValueError):
        return None


def charger_module(chemin, nom):
    """Le module <chemin> charge PAR SON CHEMIN (pas de nom nu).

    POURQUOI : un `import constants` prendrait le module d un AUTRE outil deja en
    memoire. Ce chargeur ne touche pas a sys.path : le module est lu a sa place.
    """
    chemin = Path(chemin)
    if not chemin.is_file():
        return None
    try:
        specification = importlib.util.spec_from_file_location(nom, str(chemin))
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        return module
    except Exception:  # noqa: BLE001 -- un domicile illisible n arrete pas l outil
        return None


def domicile_vivier():
    """(chemin de la BDD du vivier, categories FERMEES) LUS a leur domicile (M-076).

    Le vivier a UNE maison (`data/outils/theme-vivier/constants.py`) : son nom de
    BDD et sa liste de categories s y lisent. Recopier ici le nom du fichier ou la
    liste des categories ferait deux verites, et la premiere d entre elles
    divergerait le jour ou le vivier bouge.
    """
    module = charger_module(REPERTOIRE_OUTILS / "theme-vivier" / "constants.py",
                            "domicile_vivier")
    if module is None:
        return None, ()
    return Path(getattr(module, "CHEMIN_BDD", "")), tuple(
        getattr(module, "CATEGORIES", ()) or ())


def ecrire_texte(chemin, texte):
    """Ecrit <texte> en ASCII, LF forces, ATOMIQUEMENT (tmp + remplacement)."""
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    temporaire = chemin.with_name(chemin.name + ".tmp")
    with open(str(temporaire), "w", encoding="ascii", newline="\n") as flux:
        flux.write(texte)
    os.replace(str(temporaire), str(chemin))


def en_relatif(chemin):
    """Le chemin RELATIF a la RACINE du workspace (ce que la porte attend).

    La porte `ecrire` resout ses chemins contre la RACINE (le dossier qui porte
    AGENTS.md -- domicile partage `data/commun/cible.py`) : c est donc SOUS CETTE
    FORME qu une cible doit lui etre presentee. Un chemin qui tomberait hors de la
    racine est rendu tel quel : c est la porte qui refuse en le NOMMANT.
    """
    chemin = Path(chemin).resolve()
    try:
        return chemin.relative_to(Path(RACINE).resolve()).as_posix()
    except ValueError:
        return chemin.as_posix()


def lancer_enfant(commande, **options):
    """Le SEUL lancement de processus de cet outil : les drapeaux viennent du domicile.

    POURQUOI un point de passage unique : un sous-processus lance A NU fait
    apparaitre une fenetre console chez le createur (E-056). Les drapeaux se LISENT
    au domicile partage (`data/commun/lancement.py`), ils ne se recopient pas.
    """
    return subprocess.run(commande, **options, **drapeaux_popen())


def ecrire_par_la_porte(chemin, texte, jeton):
    """POSE <texte> dans <chemin> par la porte `ecrire`. Rend (code, sortie).

    Le texte part dans un fichier de la zone jetable, et la commande ne porte que
    des chemins : rien ne traverse le shell.
    """
    REPERTOIRE_JETABLE.mkdir(parents=True, exist_ok=True)
    temporaire = Path(REPERTOIRE_JETABLE) / (NOM_OUTIL + "-" + jeton + ".txt")
    ecrire_texte(temporaire, texte)
    commande = [sys.executable, str(CHEMIN_LANCEUR), "--appelant", APPELANT,
                "ecrire", "ecrire",
                "--fichier", en_relatif(chemin),
                "--contenu-fichier", en_relatif(temporaire)]
    resultat = lancer_enfant(commande, capture_output=True, text=True)
    sortie = ((resultat.stdout or "") + (resultat.stderr or "")).strip()
    try:
        temporaire.unlink()
    except OSError:
        pass
    return resultat.returncode, sortie


def resume(sortie):
    """La derniere ligne utile d une sortie de porte (pour un diagnostic lisible)."""
    lignes = [ligne.strip() for ligne in (sortie or "").splitlines() if ligne.strip()]
    return (lignes[-1] if lignes else "")[:LARGEUR_RESUME]
