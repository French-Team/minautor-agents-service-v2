"""cobayes_jetables -- la FABRIQUE DE FIXTURES JETABLES d'un garde (moteur PARTAGE).

Moteur partage (un seul domicile -- L-029/L-102) : douze gardes ouvraient chacun
leur `mkdtemp` puis leur `rmtree` dans un `finally`. Le meme geste recopie douze
fois, et la copie qui oublie le `finally` laisse un residu que personne ne voit.
La fabrique donne ce geste UNE fois.

Ce qu'elle DONNE :

    fixtures(prefixe, journal)  dossier de fixtures JETABLES (`Path`), retire
                                TOUJOURS -- meme si le bloc LEVE
    retirer(dossier)            retire et REND (retires, echecs) : une purge
                                partielle ne se tait JAMAIS
    copier(zone, dossier, ...)  des COPIES de fichiers reels (l'original n'est
                                jamais touche : c'est la copie qu'on eprouve)
    litteraux(chemin)           les declarations de chaine de MODULE (lecture
                                par AST : aucun import, la SOURCE fait foi)
    muter_litteral(...)         change (genre `valeur`) ou RETIRE (genre
                                `absent`) une de ces declarations, dans une
                                COPIE seulement

Ce qu'elle NE fait PAS : la trace. Elle ne sait pas ou chaque flux journalise :
elle REND les faits (verdict de retrait, succes de mutation) et l'appelant les
ecrit avec ses mots, dans ses propres ecarts.

Chargement : les outils de la matrice portent des TIRETS, donc ne sont JAMAIS
importables par nom. Chaque consommateur charge ce fichier par son CHEMIN, sur
le dossier partage que le motif M-076 lui donne deja (`matrice/data/commun`) :

    spec = importlib.util.spec_from_file_location("cobayes_jetables", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
"""

import ast
import contextlib
import shutil
import tempfile
from pathlib import Path

# Le prefixe d'une zone de cobaye dit D'OU elle vient : un residu laisse dans le
# temporaire du systeme reste identifiable (le nom porte le nom du garde).
PREFIXE_DEFAUT = "cobaye-"
# Les deux genres de mutation d'une declaration : lui donner une valeur fausse
# (divergence a voir), ou la RETIRER (absence a voir).
GENRE_VALEUR = "valeur"
GENRE_ABSENT = "absent"
SUFFIXE_VALEUR = "_FANTOME"
COMMENTAIRE_ABSENT = " RETIREE PAR LE COBAYE (fixture jetable)"


@contextlib.contextmanager
def fixtures(prefixe=PREFIXE_DEFAUT, journal=None):
    """Ouvre un dossier de fixtures JETABLES et le retire TOUJOURS.

    Rend un `Path` pose dans le temporaire du systeme. Le retrait a lieu meme si
    le bloc LEVE (`finally`). Un element qui resiste n'est pas avale : le verdict
    est ANNEXE a `journal` (liste fournie par l'appelant), qui le dira dans son
    rapport -- un retrait partiel qui se tait serait une purge menteuse (lecon de
    `zone_tmp.vider`, meme dossier partage).
    """
    dossier = Path(tempfile.mkdtemp(prefix=prefixe))
    try:
        yield dossier
    finally:
        _, echecs = retirer(dossier)
        if journal is not None:
            journal.extend(echecs)


def retirer(dossier):
    """Retire un dossier jetable. Rend (retires, echecs), chacun NOMME.

    Un echec n'est jamais avale : sans lui, un garde dirait "sain" sur un dossier
    encore plein. Un dossier deja absent n'est pas une erreur (le retrait est
    idempotent) : il ne produit ni retire, ni echec.
    """
    dossier = Path(dossier)
    if not dossier.is_dir():
        return [], []
    try:
        shutil.rmtree(str(dossier))
    except OSError:
        return [], [str(dossier)]
    return [dossier.name], []


def copier(zone, dossier, relatifs):
    """Pose des COPIES de fichiers reels comme fixtures. Rend les copies, DANS L ORDRE.

    L'original n'est JAMAIS touche : c'est la copie qu'on eprouve et qu'on mute.
    """
    copies = []
    for relatif in relatifs:
        destination = Path(dossier) / Path(relatif).name
        shutil.copyfile(str(Path(zone) / relatif), str(destination))
        copies.append(destination)
    return copies


def litteraux(chemin):
    """Les declarations de chaine au niveau MODULE d'un fichier : nom -> (valeur, ligne).

    Lecture par AST : AUCUN import du fichier lu (un module importe peut avoir des
    effets) et la SOURCE fait foi -- c'est elle qu'on compare, pas ce qu'un import
    en aurait fait.
    """
    arbre = ast.parse(Path(chemin).read_text(encoding="utf-8"))
    trouves = {}
    for noeud in arbre.body:
        if (isinstance(noeud, ast.Assign) and isinstance(noeud.value, ast.Constant)
                and isinstance(noeud.value.value, str)):
            for cible in noeud.targets:
                if isinstance(cible, ast.Name):
                    trouves[cible.id] = (noeud.value.value, noeud.lineno)
    return trouves


def muter_litteral(chemin, nom, genre, suffixe=SUFFIXE_VALEUR):
    """Change (genre `valeur`) ou RETIRE (genre `absent`) une declaration d'une COPIE.

    Rend False si la declaration n'est pas la : l'appelant le DIT alors, au lieu de
    faire semblant d'avoir eprouve. Le contenu est reecrit en LF (convention du
    depot) : la copie doit rester lisible par le meme lecteur que l'original.
    """
    table = litteraux(chemin)
    if nom not in table:
        return False
    valeur, ligne = table[nom]
    chemin = Path(chemin)
    lignes = chemin.read_text(encoding="utf-8").split("\n")
    if genre == GENRE_VALEUR:
        lignes[ligne - 1] = nom + " = " + repr(valeur + suffixe)
    elif genre == GENRE_ABSENT:
        lignes[ligne - 1] = "# " + nom + COMMENTAIRE_ABSENT
    else:
        return False
    with open(str(chemin), "w", encoding="utf-8", newline="\n") as flux:
        flux.write("\n".join(lignes))
    return True
