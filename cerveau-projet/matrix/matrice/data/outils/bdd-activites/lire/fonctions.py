"""Fonctions simples de la categorie lire : une seule tache chacune."""


def filtrer(donnees, section=None, tag=None):
    """Retourne la liste (section, activites) demandee, filtrees par tag.

    section None = toutes les sections (ordre de declaration).
    """
    sections = donnees.get("sections", {})
    if section:
        sections = {nom: sections.get(nom, ()) for nom in (section,)}
    if tag:
        sections = {
            nom: [a for a in activites if tag in a.get("tags", ())]
            for nom, activites in sections.items()
        }
    return list(sections.items())


def afficher(couples):
    """Affiche les activites par section (format lisible, ASCII strict)."""
    total = 0
    for nom, activites in couples:
        print("== " + nom + " (" + str(len(activites)) + " activite(s)) ==")
        for activite in activites:
            print(
                "  " + activite["date"] + "  " + activite["detail"]
                + "  [" + ", ".join(activite.get("tags", ())) + "]"
            )
            total += 1
    print(str(total) + " activite(s) affichee(s).")
