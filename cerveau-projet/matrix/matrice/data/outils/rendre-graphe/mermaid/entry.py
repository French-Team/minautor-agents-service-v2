"""Categorie mermaid : la SOURCE -> le TEXTE Mermaid (impression, ou depot par la porte).

DRY PAR DEFAUT : sans `--appliquer`, ce verbe IMPRIME le texte et n ecrit RIEN. Une
vue qui se poserait sans le dire serait une vue qui remplace la precedente sans
laisser de trace.
"""
from commun import ecrire_par_la_porte, extraire_options, resume
from constants import (
    DOSSIER_MERMAID,
    SOURCE_ARBRE,
    SOURCE_PARCOURS,
    SOURCE_VIVIER,
    SOURCES,
    VUE_INDEX,
)
from mermaid.fonctions import (
    modele_arbre,
    modele_parcours_index,
    modele_parcours_theme,
    modele_vivier,
    serialiser,
)

# `appliquer` est un DRAPEAU : il figure dans les DEUX listes, et c est le
# contrat du domicile partage (data/commun/options.py, point 4) -- la liste des
# noms RECONNUS dit qu il existe, la liste des drapeaux dit qu il ne prend PAS de
# valeur. Ne le mettre que dans les drapeaux fait REFUSER `--appliquer` comme une
# option inconnue (un drapeau absent des noms connus n est jamais reconnu).
NOMS_OPTIONS = ("source", "theme", "arbre", "sortie", "appliquer")
DRAPEAUX = ("appliquer",)
EXTENSION = ".mmd"

USAGE = (
    "    python main.py mermaid [--source " + "|".join(SOURCES) + "] [--theme <NOM>]\n"
    "                           [--arbre <fichier.json>] [--sortie <fichier>] [--appliquer]\n"
    "                                       (rend le TEXTE Mermaid d une source : le parcours\n"
    "                                       d Optimus -- l index, ou UN theme --, le vivier, ou\n"
    "                                       un arbre. DRY par defaut : imprime, n ecrit rien)\n"
)


def modele_de(source, theme="", arbre=""):
    """Le MODELE de la source demandee. Une source inconnue se REFUSE (jamais un repli muet)."""
    if source not in (SOURCE_PARCOURS, SOURCE_VIVIER, SOURCE_ARBRE):
        return None, None
    if source == SOURCE_VIVIER:
        return modele_vivier()
    if source == SOURCE_ARBRE:
        return modele_arbre(arbre)
    if theme and theme.strip().upper() != VUE_INDEX.upper():
        return modele_parcours_theme(theme)
    return modele_parcours_index()


def nom_fichier(source, theme="", suffixe=EXTENSION):
    """Le nom du fichier de vue : la source, et le theme quand il y en a un."""
    morceaux = [source]
    if source == SOURCE_PARCOURS:
        morceaux.append(theme.strip().lower() if theme and theme.strip().upper()
                        != VUE_INDEX.upper() else VUE_INDEX)
    return "-".join(morceaux) + suffixe


def executer(arguments):
    """Rend le TEXTE Mermaid de la source, ou le DEPOSE (avec `--appliquer`)."""
    options = extraire_options(arguments, NOMS_OPTIONS, drapeaux=DRAPEAUX)
    source = (options.get("source") or SOURCE_PARCOURS).strip().lower()
    theme = (options.get("theme") or "").strip()
    arbre = (options.get("arbre") or "").strip()
    sortie = (options.get("sortie") or "").strip()
    appliquer = bool(options.get("appliquer"))

    modele, incoherences = modele_de(source, theme, arbre)
    if modele is None:
        print("REFUS : source inconnue (" + repr(source) + "). Sources : "
              + ", ".join(SOURCES) + ".")
        print(USAGE)
        return 2
    texte = serialiser(modele)
    print("VUE : " + modele["titre"])
    if modele.get("sous_titre"):
        print("  " + str(modele["sous_titre"])[:150])
    print("  " + str(len(modele["noeuds"])) + " noeud(s), "
          + str(len(modele["aretes"])) + " arete(s), "
          + str(len(incoherences or [])) + " incoherence(s) rendue(s) VISIBLE(s)")
    if not appliquer and not sortie:
        print("")
        print(texte, end="")
        print("  (DRY : RIEN n a ete ecrit. Pour deposer la vue : ajouter --appliquer.)")
        return 0
    cible = sortie or str(DOSSIER_MERMAID / nom_fichier(source, theme))
    code, message = ecrire_par_la_porte(cible, texte, "mermaid")
    print("  " + ("OK" if code == 0 else "REFUS") + " : " + cible
          + (" -- " + resume(message) if message else ""))
    return code
