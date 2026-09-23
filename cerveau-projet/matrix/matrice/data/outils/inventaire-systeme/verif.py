"""Verification de la fiche machine : contre la MACHINE, et contre le PILOTE.

Quatre mesures, et ce que chacune protege :
  1. la fiche EXISTE -- sinon il n y a rien a verifier (refus nomme, code 2) ;
  2. elle porte sa CARTE D IDENTITE et la section RESUME MACHINE -- sans la
     section, l entree d injection ferait un refus nomme a la source suivante ;
  3. ses champs COMPARES s accordent avec une mesure FRAICHE (OS, architecture,
     hote, versions des outils principaux) : c est la PREUVE que la fiche a
     pouri, ou qu elle tient ;
  4. le CATALOGUE d injection DECLARE l entree qui sert la fiche : la relation
     fiche -> pilote est un contrat MESURE, jamais une intention ecrite dans un
     commentaire (M-076 / L-032).

Codes : 0 = tout s accorde ; 1 = ecart(s) nomme(s) ; 2 = refus (fiche absente).
"""
import json

from constants import (CARTE_IDENTITE, CASES_RESUME, CHAMPS_COMPARES,
                       CHEMIN_CATALOGUE_ABSOLU, CHEMIN_FICHE, ENCODAGE,
                       ID_INJECTION, NOM_FICHE, TITRE_RESUME)
from fiche import lire
from mesure import extraire_version, mesurer_tout


def rangees_tables(texte):
    """Toutes les RANGEES de toutes les tables markdown, cellules separees.

    Les lignes de separation (---|---) sont ecartees : elles ne portent aucun fait.
    """
    rangees = []
    for ligne in (texte or "").splitlines():
        propre = ligne.strip()
        if not propre.startswith("|") or not propre.endswith("|"):
            continue
        cellules = [cellule.strip() for cellule in propre.split("|")[1:-1]]
        if not cellules:
            continue
        if set("".join(cellules)) <= set("-: "):
            continue
        rangees.append(cellules)
    return rangees


def valeur_systeme(texte, nom):
    """La 2e colonne de la rangee dont la 1ere colonne est `nom`, ou None."""
    for cellules in rangees_tables(texte):
        if len(cellules) >= 2 and cellules[0] == nom:
            return cellules[1]
    return None


def outil_fiche(texte, nom):
    """La rangee OUTILS d un outil : disponible + version, ou None."""
    for cellules in rangees_tables(texte):
        if len(cellules) >= 3 and cellules[0] == nom:
            return {"disponible": cellules[1] == "Oui", "version": cellules[2]}
    return None


def controler_structure(texte, ecarts):
    """La carte d identite, la section servie, et les cases du resume."""
    carte = "\n".join(CARTE_IDENTITE)
    if carte not in texte[:400]:
        ecarts.append("carte d identite ABSENTE en tete de la fiche " + str(CHEMIN_FICHE))
    if TITRE_RESUME not in texte:
        ecarts.append("section " + TITRE_RESUME + " ABSENTE : l injection la demande par ce nom")
    for case in CASES_RESUME:
        if "- **" + case + "**" not in texte:
            ecarts.append("case de resume ABSENTE : " + case)


def controler_machine(texte, mesure, ecarts):
    """Les champs compares : la fiche contre une mesure FRAICHE."""
    systeme = mesure["systeme"]
    outils = {entree["nom"]: entree for entree in mesure["outils"]}
    for section, nom, champ in CHAMPS_COMPARES:
        if section == "systeme":
            lu = valeur_systeme(texte, nom)
            attendu = systeme.get(champ)
            if lu != attendu:
                ecarts.append("SYSTEME " + nom + " : fiche " + str(lu)
                              + " / machine " + str(attendu))
            continue
        lu = outil_fiche(texte, nom)
        if lu is None:
            ecarts.append("OUTIL " + nom + " : ABSENT de la table OUTILS de la fiche")
            continue
        entree = outils.get(nom)
        attendu = extraire_version(entree["version"]) if entree else "-"
        if extraire_version(lu["version"]) != attendu:
            ecarts.append("OUTIL " + nom + " : fiche " + str(lu["version"])
                          + " / machine " + str(attendu))


def controler_catalogue(ecarts):
    """L entree d injection qui sert la fiche : declaree, pointant la fiche, avec SA section."""
    if not CHEMIN_CATALOGUE_ABSOLU.is_file():
        ecarts.append("catalogue d injection INTROUVABLE : " + str(CHEMIN_CATALOGUE_ABSOLU))
        return
    try:
        with open(CHEMIN_CATALOGUE_ABSOLU, "r", encoding=ENCODAGE) as flux:
            catalogue = json.load(flux)
    except (OSError, ValueError) as erreur:
        ecarts.append("catalogue d injection ILLISIBLE (" + str(erreur) + ")")
        return
    entrees = [entree for entree
               in catalogue.get("injections", {}).get("avant-mission", [])
               if entree.get("id") == ID_INJECTION]
    if not entrees:
        ecarts.append("catalogue : l entree " + ID_INJECTION
                      + " n est PAS declaree dans avant-mission")
        return
    entree = entrees[0]
    if str(entree.get("source", "")).replace("\\\\", "/").split("/")[-1] != NOM_FICHE:
        ecarts.append("catalogue : l entree " + ID_INJECTION + " ne pointe PAS " + NOM_FICHE
                      + " (source " + str(entree.get("source")) + ")")
    section = TITRE_RESUME.replace("## ", "")
    if entree.get("section", "") != section:
        ecarts.append("catalogue : l entree " + ID_INJECTION + " ne demande PAS la section "
                      + section)


def verifier():
    """Rend (code, ecarts) : l appelant DECIDE de l affichage, jamais le module."""
    texte = lire()
    if texte is None:
        return 2, ["fiche ABSENTE : " + str(CHEMIN_FICHE)
                   + " -- le remede est inventaire-systeme mesurer"]
    ecarts = []
    controler_structure(texte, ecarts)
    controler_machine(texte, mesurer_tout(), ecarts)
    controler_catalogue(ecarts)
    return (1 if ecarts else 0), ecarts
