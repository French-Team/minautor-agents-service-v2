"""Fonctions simples de la categorie canoniser : une seule tache chacune.

EO-363 : la BDD portait DEUX CLES pour un meme fichier (158 cas mesures le
2026-09-22). Cette categorie REUNIT les deux histoires -- sans en perdre une.

Le TEMOIN de non-perte est le MULTISET des entrees, jamais leur NOMBRE : un
compte reste juste si une entree disparait pendant qu'une autre est dupliquee
-- le pire des temoins, celui qui rassure (L-032).
"""
import json


def recenser_modifications(donnees):
    """Le MULTISET des modifications : chaque entree y compte pour ce qu'elle EST.

    La cle du recensement est l'entree serialisee a ORDRE DE CLES FIXE : deux
    entrees ne se confondent que si tous leurs champs sont egaux, et leur ordre
    d'ecriture dans le JSON ne change rien. C'est ce recensement qu'on compare
    AVANT et APRES la migration : deux comptages egaux ne prouvent RIEN, deux
    recensements egaux prouvent que la BDD porte exactement les memes entrees.
    """
    recensement = {}
    for fiche in ((donnees or {}).get("fichiers", {}) or {}).values():
        for entree in (fiche.get("modifications", []) or []):
            marque = json.dumps(entree, sort_keys=True, ensure_ascii=True)
            recensement[marque] = recensement.get(marque, 0) + 1
    return recensement


def comparer_recensements(avant, apres):
    """(succes, message) : la migration ne PERD ni ne FABRIQUE aucune entree.

    Un refus qui ne dit pas ce qu'il protege coute trois essais (friction 77) :
    le message nomme donc la PREMIERE entree perdue, pas seulement le compte.
    """
    perdues = sorted(reference for reference, nombre in avant.items()
                     if nombre > apres.get(reference, 0))
    neuves = sorted(reference for reference, nombre in apres.items()
                    if nombre > avant.get(reference, 0))
    if not perdues and not neuves:
        return (True, "Aucune perte, aucune alteration : "
                + str(sum(avant.values())) + " modification(s) intacte(s).")
    message = ("REFUS : la migration changerait les ENTREES elles-memes -- "
               + str(len(perdues)) + " perdue(s), " + str(len(neuves))
               + " apparue(s) -- la BDD n'a PAS ete ecrite.")
    if perdues:
        message += " Premiere perdue : " + perdues[0][:160]
    return (False, message)


def fusionner_cles(donnees, canoniser):
    """(rapport, recensement_avant, recensement_apres) : une cle par fichier.

    La REGLE de canonisation n'est pas ecrite ici : elle est PASSEE en argument
    (`commun.canoniser_cle`). Un seul domicile de regle (L-029) -- si la regle
    change, cette migration suit sans qu'on la retouche.

    Les modifications des deux fiches sont REUNIES et TRIEES par date : le
    resultat ne depend pas de l'ordre de parcours (deux executions donnent la
    MEME BDD). La fonction ne juge pas : elle rend les DEUX recensements pour que
    l'appelant puisse REFUSER une migration qui perdrait une entree
    (comparer_recensements).

    Ne touche a rien d'autre : l'enregistrement est fait par l'appelant
    (commun.enregistrer_bdd), comme pour `noter`.
    """
    fichiers = donnees.get("fichiers", {}) or {}
    recensement_avant = recenser_modifications(donnees)
    rapport = []
    for cle in sorted(list(fichiers)):
        canonique = canoniser(cle)
        if not canonique or canonique == cle:
            continue
        fiche = fichiers[cle]
        cible = fichiers.setdefault(canonique, {"modifications": [], "tags": []})
        cible.setdefault("modifications", [])
        cible.setdefault("tags", [])
        fusion = list(cible["modifications"]) + list(fiche.get("modifications", []) or [])
        fusion.sort(key=lambda entree: str(entree.get("date", "")))
        cible["modifications"] = fusion
        for tag in (fiche.get("tags", []) or []):
            if tag not in cible["tags"]:
                cible["tags"].append(tag)
        rapport.append((cle, canonique, len(fiche.get("modifications", []) or [])))
        del fichiers[cle]
    return rapport, recensement_avant, recenser_modifications(donnees)
