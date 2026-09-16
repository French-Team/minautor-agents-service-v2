"""Fonctions simples de la categorie retirer : une seule tache chacune.

M-058 : sortie PROPRE du vrac (gap revele en M-055 : E-027 purgee a la main
faute de porte). Le vrac ne doit contenir que du vrai.
MO-035 : la sortie des FILES (une mission classee a tort restait A VIE dans sa
file et le brin la ressertait a chaque tissage). Porte alignee sur celle de
l'entonnoir d'Optimus le 2026-09-13 : les deux copies du meme outil doivent
offrir la meme porte, sinon une reparation faite d'un cote reste absente de
l'autre -- c'est exactement par cette derive qu'un prefixe a pu etre partage.
"""
try:
    from stockage import horodater, verifier_famille
except ImportError:  # importe comme paquet (depuis le pilote) : chemin complet
    from entonnoir.stockage import horodater, verifier_famille


def retirer_des_files(etat, identifiant):
    """Retire UNE mission CLASSEE (echelons 1-2) par son id exact.

    MO-035 : le verbe retirer ne parlait qu'au vrac, donc une mission classee
    a tort (doublon d'une mission deja executee) restait A VIE dans sa file
    et le brin la reprenait a chaque tissage. Meme classe de gap que M-058
    (E-027 purgee a la main faute de porte) : la porte manquante est ici.
    Le brin n'est jamais edite ici : il est DERIVE des files, donc recompose
    par l'appelant (recomposer_brin). Codes alignes sur le vrac.
    """
    code, message = verifier_famille(identifiant)
    if code != 0:
        return code, message
    for type_file, missions in etat.get("files", {}).items():
        for mission in missions:
            if mission.get("id") == identifiant:
                missions.remove(mission)
                return 0, (
                    "Mission " + identifiant + " retiree de la file " + type_file
                    + " (categorie : " + mission.get("categorie", "?")
                    + ", deposee le " + mission.get("deposee_le", "?")
                    + ", retiree le " + horodater() + ")"
                )
    return 1, "Mission inconnue aux files : " + identifiant


def recomposer_brin(etat):
    """Recompose le brin APRES un retrait (deterministe : tresser + marquer).

    Un retrait dans une file laisse le brin perime (il garderait la mission
    fantome en tete et le pilote la consommerait). Import differe : le brin
    n'appartient qu'a sa porte officielle (tresse), jamais a retirer.
    Retourne le nombre de missions du brin recompose.
    """
    from tresse.fonctions import marquer_brin, tresser

    etat["brin"] = marquer_brin(tresser(etat.get("files", {})))
    return len(etat["brin"])


def retirer_du_vrac(etat, identifiant):
    """Retire UNE mission du vrac par son id exact. Retourne (code, message).

    Codes alignes sur classer : mission inconnue -> 1, succes -> 0.
    La mission retiree est JAMAIS effacee du monde : elle part avec son
    historique (retiree_le note dans le message), mais sort de l'entonnoir.
    Une mission deja classee (dans une file) n'est JAMAIS touchee ici :
    ce verbe ne parle qu'au vrac (echelon 0).
    """
    code, message = verifier_famille(identifiant)
    if code != 0:
        return code, message
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
