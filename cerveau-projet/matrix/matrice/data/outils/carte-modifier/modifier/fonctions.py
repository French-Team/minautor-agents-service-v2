"""Logique de carte-modifier : UN champ change, le bloc RESULTAT est juge.

La conformite vient du DOMICILE partage (carte_identite valider_carte) : les
memes jugements que le garde, consommes jamais copie (M-076). Le changement se
fait sur le BLOC extrait, puis la porte ecrire le remplace (occurrence
unique) : si la porte refuse, la cible reste INTACTE.
"""
# commun D ABORD : son bloc de lancement pose data/commun (cible,
# carte_identite, ...) sur le chemin avant tout import du domicile partage.
from commun import extraire_bloc, lire_texte, poser_bloc, relatif
from constants import (CODE_ECHEC, CODE_OK, CODE_REFUS, ENCODAGE,
                       MODELE_COMPLET, REPERTOIRE_OUTIL)

from cible import resoudre
from carte_identite import CLES_OBLIGATOIRES, lire_carte, valider_carte

INDENTATION_DEFAUT = "  "


def cles_du_modele():
    """Le vocabulaire DECLARE des champs : les cles du modele de reference."""
    try:
        texte = MODELE_COMPLET.read_text(encoding=ENCODAGE)
    except OSError:
        return []
    carte = lire_carte(texte)
    return list(carte) if carte else []


def ligne_de_cle(bloc, cle):
    """(index, ligne exacte) de la cle dans le bloc, ou (None, None)."""
    for index, ligne in enumerate(bloc.splitlines(keepends=True)):
        propre = ligne.strip()
        if propre.startswith(cle + ":"):
            return index, ligne
    return None, None


def appliquer(bloc, cle, valeur, supprimer):
    """(nouveau bloc, refus) : la ligne de la cle est remplacee, inseree ou retiree."""
    lignes = bloc.splitlines(keepends=True)
    index, ligne = ligne_de_cle(bloc, cle)
    if supprimer:
        if index is None:
            return "", "cle absente de la carte : rien a retirer : " + cle
        if cle in CLES_OBLIGATOIRES:
            return "", "cle obligatoire : on ne la retire pas : " + cle
        del lignes[index]
        return "".join(lignes), None
    if index is not None:
        fin = "\n" if ligne.endswith("\n") else ""
        indentation = ligne[:len(ligne) - len(ligne.lstrip())]
        lignes[index] = indentation + cle + ": " + valeur + fin
        return "".join(lignes), None
    # La cle est ABSENTE : elle s insere juste apres `identite:`, avec
    # l indentation des autres cles (une carte qui deroge est un accident).
    position_identite = None
    for index, ligne in enumerate(lignes):
        if ligne.strip() == "identite:":
            position_identite = index
            break
    if position_identite is None:
        return "", "ligne `identite:` introuvable dans le bloc"
    indentation = INDENTATION_DEFAUT
    for ligne in lignes[position_identite + 1:]:
        propre = ligne.strip()
        if propre and not propre.startswith("#") and ":" in propre:
            indentation = ligne[:len(ligne) - len(ligne.lstrip())]
            break
    lignes.insert(position_identite + 1, indentation + cle + ": " + valeur + "\n")
    return "".join(lignes), None


def changer(options):
    """Change UN champ de la carte -- toute ecriture passe par la porte."""
    brut = options.get("fichier")
    chemin, motif = resoudre(brut, REPERTOIRE_OUTIL)
    if chemin is None:
        print("REFUS : " + motif)
        return CODE_REFUS
    if not chemin.is_file():
        print("REFUS : ce n'est pas un fichier : " + str(chemin))
        return CODE_REFUS
    texte = lire_texte(chemin)
    bloc = extraire_bloc(texte)
    if bloc is None:
        print("REFUS : " + relatif(chemin) + " n a PAS de carte a changer"
              " (poser la carte d abord : carte-creer)")
        return CODE_REFUS
    cle = options.get("cle", "").strip()
    connues = cles_du_modele()
    presente = ligne_de_cle(bloc, cle)[0] is not None
    if cle not in connues and not presente:
        carte = lire_carte(bloc) or {}
        print("REFUS : cle inconnue : " + cle)
        print("  cles du modele : " + ", ".join(connues))
        print("  cles de la carte : " + ", ".join(carte))
        return CODE_REFUS
    supprimer = "supprimer" in options
    valeur = options.get("valeur")
    if valeur is not None:
        valeur = str(valeur).strip()
        if not valeur:
            print("REFUS : --valeur vide : retirez le champ avec --supprimer")
            return CODE_REFUS
    nouveau, refus = appliquer(bloc, cle, valeur, supprimer)
    if refus:
        print("REFUS : " + refus)
        return CODE_REFUS
    nouvelle_carte = lire_carte(nouveau)
    ecarts = valider_carte(nouvelle_carte, chemin, REPERTOIRE_OUTIL)
    if ecarts:
        print("REFUS : le changement rendrait la carte non conforme :")
        for ecart in ecarts:
            print("  - " + ecart)
        return CODE_REFUS
    if nouveau == bloc:
        print("RIEN A FAIRE : la carte porte deja " + cle + " = " + str(valeur))
        return CODE_OK
    code, message = poser_bloc(chemin, bloc, nouveau, "modifier-" + chemin.stem)
    if code != CODE_OK:
        print(str(message))
        return code
    if supprimer:
        print("CHAMP RETIRE : " + relatif(chemin) + " -- " + cle)
    else:
        print("CHAMP CHANGE : " + relatif(chemin) + " -- " + cle + " = " + valeur)
    return CODE_OK
