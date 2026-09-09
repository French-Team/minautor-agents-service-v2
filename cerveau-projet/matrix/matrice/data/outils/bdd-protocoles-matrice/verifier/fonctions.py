"""Fonctions simples de la categorie verifier : une seule tache chacune."""


def verifier_integrite(empreinte_reelle, empreinte_enregistree):
    """Compare l'empreinte recalculee a l'empreinte enregistree (etalon-or).

    Retourne (succes, message) : le message dit ce qui casse, ou pourquoi.
    """
    if empreinte_reelle is None:
        return (False, "ECART : la BDD est absente ou illisible a l'emplacement attendu.")
    if empreinte_enregistree is None:
        return (False, "ECART : aucune empreinte enregistree (la BDD n'a jamais ete ecrite par l'outil).")
    if empreinte_reelle == empreinte_enregistree:
        return (True, "Integrite verifiee : empreinte " + empreinte_reelle[:16] + "...")
    return (
        False,
        "ECART : empreinte reelle "
        + empreinte_reelle[:16]
        + "... != enregistree "
        + empreinte_enregistree[:16]
        + "... (la BDD a ete modifiee hors de l'outil).",
    )
