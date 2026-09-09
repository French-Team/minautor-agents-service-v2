"""Fonctions simples de la categorie retirer : une seule tache chacune.

M-058 : sortie PROPRE du vrac (gap revele en M-055 : E-027 purgee a la main
faute de porte). Le vrac ne doit contenir que du vrai.
"""
try:
    from stockage import horodater
except ImportError:  # importe comme paquet (depuis le pilote) : chemin complet
    from entonnoir.stockage import horodater


def retirer_du_vrac(etat, identifiant):
    """Retire UNE mission du vrac par son id exact. Retourne (code, message).

    Codes alignes sur classer : mission inconnue -> 1, succes -> 0.
    La mission retiree est JAMAIS effacee du monde : elle part avec son
    historique (retiree_le note dans le message), mais sort de l'entonnoir.
    Une mission deja classee (dans une file) n'est JAMAIS touchee ici :
    ce verbe ne parle qu'au vrac (echelon 0).
    """
    vrac = etat.get("vrac", [])
    for mission in vrac:
        if mission.get("id") == identifiant:
            vrac.remove(mission)
            return 0, (
                "Mission " + identifiant + " retiree du vrac (theme : "
                + mission.get("theme", "?") + ", deposee le "
                + mission.get("deposee_le", "?") + ", retiree le "
                + horodater() + ")"
            )
    return 1, "Mission inconnue au vrac : " + identifiant
