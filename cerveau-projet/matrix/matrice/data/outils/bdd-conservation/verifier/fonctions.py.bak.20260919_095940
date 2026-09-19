"""Fonctions de verification du registre de conservation."""
from constants import CATEGORIES, PREFIXE_ID, STATUTS, VERDICTS


def verifier_structure(donnees):
    erreurs = []
    ids = set()
    for entree in donnees.get("elements", []):
        identifiant = entree.get("id", "")
        if not identifiant.startswith(PREFIXE_ID) or not identifiant[len(PREFIXE_ID):].isdigit():
            erreurs.append("id invalide : " + str(identifiant))
        if identifiant in ids:
            erreurs.append("id duplique : " + identifiant)
        ids.add(identifiant)
        if entree.get("categorie") not in CATEGORIES:
            erreurs.append("categorie invalide : " + identifiant)
        if entree.get("statut") not in STATUTS:
            erreurs.append("statut invalide : " + identifiant)
        verdict = entree.get("verdict", "")
        if verdict and verdict not in VERDICTS:
            erreurs.append("verdict invalide : " + identifiant)
        if not entree.get("source"):
            erreurs.append("source absente : " + identifiant)
        if not entree.get("raison"):
            erreurs.append("raison absente : " + identifiant)
        if not entree.get("tags"):
            erreurs.append("tags absents : " + identifiant)
        if entree.get("verdict") == "archiver" and not entree.get("destination"):
            erreurs.append("destination absente pour archivage : " + identifiant)
    return erreurs


def verifier_integrite(empreinte_reelle, empreinte_enregistree):
    if empreinte_reelle is None:
        return False, "ECART : BDD absente ou illisible"
    if empreinte_enregistree is None:
        return False, "ECART : empreinte absente"
    if empreinte_reelle != empreinte_enregistree:
        return False, "ECART : empreinte reelle differente de l etalon"
    return True, "Integrite verifiee : empreinte " + empreinte_reelle[:16] + "..."
