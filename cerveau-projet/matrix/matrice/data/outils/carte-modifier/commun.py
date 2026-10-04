"""Fonctions communes de carte-modifier : lire le document, passer par la porte.

Chaque fonction fait UNE chose (convention-architecture-outils). UNE seule
regle d'ecriture : ce noutil n'ecrit JAMAIS lui-meme -- fragments et cible
passent par la porte ecrire (decision createur MO-430), ce qui donne la
validation de la porte, le point de restauration et le refus a occurrence
unique sans rien inventer ici.
"""

import subprocess
import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-416, bloc autosuffisant) -------------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu), refus sinon.
_RACINE_LANCEMENT = Path(__file__).resolve().parent
while _RACINE_LANCEMENT.name != "matrix":
    if _RACINE_LANCEMENT.parent == _RACINE_LANCEMENT:
        raise RuntimeError("racine `matrix` introuvable en remontant depuis " + __file__)
    _RACINE_LANCEMENT = _RACINE_LANCEMENT.parent
_REPERTOIRE_COMMUN_LANCEMENT = _RACINE_LANCEMENT / "matrice" / "data" / "commun"
if not (_REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(_REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(_REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(_REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402

# Le parseur d options EST le domicile partage (EO-158), jamais recopie.
from options import CLE_SANS_VALEUR, extraire_options  # noqa: E402
# EO-287 : la resolution d un outil par son NOM est PARTAGEE (un seul domicile).
from resolution_outils import chemin_outil  # noqa: E402

from constants import CODE_OK, ENCODAGE, NOM_PORTE_ECRIRE, RACINE, ZONE_FRAGMENTS  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())


def relatif(chemin):
    """Chemin du workspace, tel que la PORTE l'attend (racine-relative)."""
    return Path(chemin).resolve().relative_to(RACINE).as_posix()


def appeler_porte(arguments):
    """Passe par la porte ecrire : le seul ecrivain de ce dossier."""
    resultat = lancer_enfant(
        [sys.executable, str(chemin_outil(NOM_PORTE_ECRIRE))] + list(arguments),
        capture_output=True, text=True, cwd=str(RACINE),
    )
    sortie = ((resultat.stdout or "") + (resultat.stderr or "")).strip().splitlines()
    return resultat.returncode, (sortie[-1] if sortie else "code " + str(resultat.returncode))


def lire_texte(chemin):
    """Texte UTF-8 d un fichier, ou chaine vide s il est illisible."""
    try:
        return Path(chemin).read_text(encoding=ENCODAGE)
    except (OSError, UnicodeDecodeError):
        return ""


def ecrire_fragment(nom, contenu):
    """Ecrire UN fragment dans la zone jetable, PAR la porte (jamais en direct)."""
    chemin = ZONE_FRAGMENTS / nom
    code, message = appeler_porte(["ecrire", "--fichier", relatif(chemin),
                                   "--contenu", contenu, "--mode", "remplacer"])
    return code, message, chemin


def poser_bloc(fichier, ancien, nouveau, etiquette):
    """Remplacer `ancien` par `nouveau` dans la cible, PAR la porte.

    Fragments ecrits par la porte puis cible editee par la porte : si l edition
    refuse (occurrence non unique, forme refusee), la cible reste INTACTE.
    Les fragments sont RETIRES dans tous les cas : la zone ne garde rien.
    Forme des fragments : canonique mo-430-<souche>.txt (garde-residus-zone).
    """
    souche = "".join(lettre if lettre.isalnum() else "-" for lettre in etiquette)
    souche = souche.lower().strip("-")
    nom_ancien = "mo-430-" + souche + "-ancien.txt"
    nom_nouveau = "mo-430-" + souche + "-nouveau.txt"
    try:
        code, message, chemin_ancien = ecrire_fragment(nom_ancien, ancien)
        if code != CODE_OK:
            return code, "REFUS fragment ancien : " + str(message)
        code, message, chemin_nouveau = ecrire_fragment(nom_nouveau, nouveau)
        if code != CODE_OK:
            return code, "REFUS fragment nouveau : " + str(message)
        code, message = appeler_porte(
            ["editer", "--fichier", relatif(fichier),
             "--ancien-fichier", relatif(chemin_ancien),
             "--nouveau-fichier", relatif(chemin_nouveau)]
        )
        if code != CODE_OK:
            return code, "REFUS " + relatif(fichier) + " : " + str(message) + " (cible intacte)"
        return CODE_OK, "POSE : " + relatif(fichier)
    finally:
        for nom in (nom_ancien, nom_nouveau):
            try:
                (ZONE_FRAGMENTS / nom).unlink()
            except OSError:
                pass


def extraire_bloc(texte):
    """Le front-matter COMPLET (-- ... --) du document, ou None (pas de carte).

    Les bornes sont celles de la grammaire : la carte vit ENTRE deux
    marqueurs en tete de fichier (jamais devinee ailleurs).
    """
    lignes = texte.splitlines(keepends=True)
    if not lignes or lignes[0].strip() != "---":
        return None
    for index, ligne in enumerate(lignes[1:], start=1):
        if ligne.strip() == "---":
            return "".join(lignes[:index + 1])
    return None
