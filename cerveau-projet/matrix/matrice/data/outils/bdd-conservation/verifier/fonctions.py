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


def controler_census(donnees):
    """CONTROLE (volet 3 de la friction 88, MO-192) : les trois champs du
    recensement (lecteurs/ecrivains/index) sont-ils remplis ?

    Une colonne vide se lit comme un fait ("aucun lecteur") alors qu'elle dit
    souvent "personne ne l'a ecrite". Ce controle REND LE COMPTE au lieu de le
    laisser croire : il rapporte, il ne bloque pas (remplir le recensement est
    un ACTE, pas une condition de validite -- cf. le refus d'archivage qui, lui,
    est le garde-fou).
    """
    elements = donnees.get("elements", [])
    total = len(elements)
    vides = {"lecteurs": 0, "ecrivains": 0, "index": 0}
    for entree in elements:
        for nom in vides:
            if not entree.get(nom):
                vides[nom] += 1
    return ("Recensement (lecteurs/ecrivains/index) : "
            + str(total - vides["lecteurs"]) + "/" + str(total) + " lecteurs, "
            + str(total - vides["ecrivains"]) + "/" + str(total) + " ecrivains, "
            + str(total - vides["index"]) + "/" + str(total) + " index"
            + " -- un 0 dit que le champ n'a jamais ete ECRIT, pas qu'il n'a rien.")


def verifier_integrite(empreinte_reelle, empreinte_enregistree):
    if empreinte_reelle is None:
        return False, "ECART : BDD absente ou illisible"
    if empreinte_enregistree is None:
        return False, "ECART : empreinte absente"
    if empreinte_reelle != empreinte_enregistree:
        return False, "ECART : empreinte reelle differente de l etalon"
    return True, "Integrite verifiee : empreinte " + empreinte_reelle[:16] + "..."
