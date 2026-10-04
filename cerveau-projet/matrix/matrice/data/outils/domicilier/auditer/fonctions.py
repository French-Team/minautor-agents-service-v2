"""Fonctions de l'audit d'une classe (une fonction = une chose)."""
import json

from commun import auditer


def lignes_rapport(rapport):
    """Rapport lisible : ce qui est aligne, ce qui reste, ce que le plan EXCLUT."""
    lignes = [
        "Classe : " + rapport["classe"],
        "Domicile : " + rapport["domicile"],
        "Copies alignees : " + str(len(rapport["alignees"])),
        "Copies a aligner : " + str(len(rapport["a_aligner"])),
    ]
    for rel in rapport["a_aligner"]:
        lignes.append("  A ALIGNER : " + rel)
    lignes.append("Exclusions DECLAREES : " + str(len(rapport["exclues"])))
    for rel in rapport["exclues"]:
        lignes.append("  EXCLUE : " + rel)
    lignes.append("Perimetre DECLARE : " + ("oui" if rapport["perimetre_declare"] else "NON (plan en perimetre ouvert)"))
    lignes.append("HORS PLAN (copies que le plan ne liste pas) : " + str(len(rapport["hors_plan"])))
    for rel in rapport["hors_plan"]:
        lignes.append("  TROU : " + rel)
    lignes.append("Copies ATTENDUES disparues (plan perime) : " + str(len(rapport["disparues"])))
    for rel in rapport["disparues"]:
        lignes.append("  PERIMEE : " + rel)
    return lignes


def verdict_code(rapport):
    """Le verdict, en CODE : 0 alignee, 1 ecart (ou plan perime), 2 refuse."""
    if rapport["hors_plan"]:
        return 2
    if rapport["disparues"] or rapport["a_aligner"]:
        return 1
    return 0


def verdict_texte(rapport):
    """Le verdict, en clair -- jamais muet : il DIT ce qu'il a trouve."""
    if rapport["hors_plan"]:
        return "REFUS : " + str(len(rapport["hors_plan"])) + " copie(s) hors plan -- le plan ne couvre pas la classe."
    if rapport["disparues"]:
        return "ECART : " + str(len(rapport["disparues"])) + " copie(s) attendue(s) ne porte(nt) plus la fonction -- plan PERIME."
    if rapport["a_aligner"]:
        return "ECART : " + str(len(rapport["a_aligner"])) + " copie(s) ne consomment pas le domicile."
    return "OK : la classe est entierement alignee sur son domicile."


def executer(plan, brut=False, perimetre=None):
    """Imprime le rapport et rend le CODE d'etat.

    En mode --json, la sortie ne porte QUE le rapport : un consommateur machine
    n'a pas a decouper de la prose (c'est le CODE qui porte le verdict).
    """
    rapport = auditer(plan, perimetre)
    if brut:
        print(json.dumps(rapport, ensure_ascii=True, indent=2, sort_keys=True))
    else:
        for ligne in lignes_rapport(rapport):
            print(ligne)
        print(verdict_texte(rapport))
    return verdict_code(rapport)
