"""Categorie svg : le TEXTE Mermaid -> l IMAGE SVG (impression, ou depot par la porte).

DEUX ENTREES, et c est ce qui fait < N IMPORTE QUOI > :
  - `--mermaid <fichier>` : un texte Mermaid ECRIT A LA MAIN (le createur compose en
    Mermaid) -- il est LU, jamais reecrit ;
  - `--source ...` : une source de la Matrice (parcours, vivier, arbre), qui passe
    d abord par le generateur, puis par le MEME moteur.
Le moteur ne voit donc jamais un modele : il voit du TEXTE, exactement comme la v1.
"""
from cible import resoudre  # domicile partage de l ancrage des chemins (M-076)
from commun import ecrire_par_la_porte, extraire_options, resume
from constants import (
    DOSSIER_SVG,
    REPERTOIRE_OUTIL,
    SOURCE_PARCOURS,
    SOURCES,
)
from mermaid.entry import modele_de, nom_fichier
from mermaid.fonctions import serialiser
from svg.fonctions import rendre_svg

# `appliquer` est un DRAPEAU : il figure dans les DEUX listes, et c est le
# contrat du domicile partage (data/commun/options.py, point 4) -- la liste des
# noms RECONNUS dit qu il existe, la liste des drapeaux dit qu il ne prend PAS de
# valeur. Ne le mettre que dans les drapeaux fait REFUSER `--appliquer` comme une
# option inconnue (un drapeau absent des noms connus n est jamais reconnu).
NOMS_OPTIONS = ("mermaid", "source", "theme", "arbre", "sortie", "appliquer")
DRAPEAUX = ("appliquer",)
EXTENSION = ".svg"

USAGE = (
    "    python main.py svg (--mermaid <fichier.mmd> | [--source " + "|".join(SOURCES) + "]\n"
    "                        [--theme <NOM>] [--arbre <fichier.json>]) [--sortie <fichier>]\n"
    "                        [--appliquer]\n"
    "                                       (rend l IMAGE SVG d un texte Mermaid : celui\n"
    "                                       qu on a ecrit a la main, ou celui d une source\n"
    "                                       de la Matrice. DRY par defaut)\n"
)


def executer(arguments):
    """Rend l image SVG du texte Mermaid (ecrit a la main, ou genere depuis une source)."""
    options = extraire_options(arguments, NOMS_OPTIONS, drapeaux=DRAPEAUX)
    reference = (options.get("mermaid") or "").strip()
    source = (options.get("source") or SOURCE_PARCOURS).strip().lower()
    theme = (options.get("theme") or "").strip()
    arbre = (options.get("arbre") or "").strip()
    sortie = (options.get("sortie") or "").strip()
    appliquer = bool(options.get("appliquer"))

    if reference:
        # L ANCRAGE se CONSOMME au domicile partage (data/commun/cible.py) : absolu,
        # ou cherche sous la racine du workspace puis sous la Matrice. Un refus
        # NOMME les bases essayees -- le cwd n a jamais ete une base (friction 80),
        # et une ancre recopiee ici divergerait le jour ou la Matrice deplie bouge.
        chemin, motif_ancre = resoudre(reference, REPERTOIRE_OUTIL)
        if chemin is None:
            print("REFUS : fichier Mermaid " + motif_ancre)
            return 2
        try:
            texte = chemin.read_text(encoding="utf-8", errors="replace")
        except OSError as erreur:
            print("REFUS : le fichier Mermaid est ILLISIBLE (" + str(erreur) + ")")
            return 2
        titre, sous_titre, nom = "Mermaid ecrit a la main", str(chemin.name), chemin.stem
        print("SOURCE : " + str(chemin) + " (lu, jamais reecrit)")
    else:
        modele, incoherences = modele_de(source, theme, arbre)
        if modele is None:
            print("REFUS : source inconnue (" + repr(source) + "). Sources : "
                  + ", ".join(SOURCES) + ".")
            print(USAGE)
            return 2
        texte = serialiser(modele)
        titre, sous_titre = modele["titre"], modele.get("sous_titre", "")
        nom = nom_fichier(source, theme, "")
        print("SOURCE : " + titre)
        print("  " + str(len(incoherences or [])) + " incoherence(s) rendue(s) VISIBLE(s)")

    image = rendre_svg(texte, titre, sous_titre)
    print("  image : " + str(len(image.splitlines())) + " lignes, "
          + str(len(image)) + " octets")
    if not appliquer and not sortie:
        print("")
        print(image, end="")
        print("  (DRY : RIEN n a ete ecrit. Pour deposer l image : ajouter --appliquer.)")
        return 0
    cible = sortie or str(DOSSIER_SVG / (nom + EXTENSION))
    code, message = ecrire_par_la_porte(cible, image, "svg")
    print("  " + ("OK" if code == 0 else "REFUS") + " : " + cible
          + (" -- " + resume(message) if message else ""))
    return code
