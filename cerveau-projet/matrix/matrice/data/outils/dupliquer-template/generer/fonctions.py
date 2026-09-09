"""Fonctions simples de la categorie generer : une seule tache chacune."""
import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path

from constants import (
    CHEMIN_MOULE,
    MOTIF_JETON,
    MOTIF_NOM,
    MOTIF_NOM_THEME,
    NOM_MOULE_PRINCIPAL,
    REPERTOIRE_OUTILS,
    REPERTOIRE_TEMPLATES,
    SUFFIXE_MOULE,
)


USAGES_PAR_MOULE = {
    "outil-bdd": 'Usage : python main.py generer --moule outil-bdd --nom bdd-xxx --bdd xxx.json --prefixe X --liste xxx --champ xxx',
    "theme-bdd": 'Usage : python main.py generer --moule theme-bdd --nom theme-xxx --bdd xxx.json --prefixe TH [--nom-affiche "NOM"]',
}


def valider_parametres(moule, nom, bdd, prefixe, liste, champ):
    """Verifie la forme des parametres SELON LE MOULE (forme fermee par moule).

    Retourne (code, message) : code 2 si un parametre manque ou deroge.
    """
    requis = {
        "outil-bdd": [nom, bdd, prefixe, liste, champ],
        "theme-bdd": [nom, bdd, prefixe],
    }.get(moule)
    if requis is None:
        return 2, "Moule inconnu : " + repr(moule) + " (moules connus : " + ", ".join(USAGES_PAR_MOULE) + ")"
    if not all(requis):
        return 2, USAGES_PAR_MOULE.get(moule, "Usage : consulter la fiche du manuel.")
    motif = MOTIF_NOM_THEME if moule == "theme-bdd" else MOTIF_NOM
    if not motif.match(nom):
        return 2, "Nom invalide pour ce moule : " + repr(nom) + " (forme attendue : " + motif.pattern + ")"
    if REPERTOIRE_OUTILS is None:
        return 1, "ECART : le dossier outils/ est introuvable."
    return 0, ""


def substitutions(moule, nom, bdd, prefixe, liste, champ, humain, nom_affiche):
    """Retourne la table des jetons -> valeurs SELON LE MOULE.

    Chaque moule ne consomme que SES jetons : un jeton absent du moule
    recoit une valeur vide (le generateur refuse tout jeton residuel de
    toute facon, donc une erreur de moule reste detectee).
    """
    table = {
        "__NOM_OUTIL__": nom,
        "__NOM_BDD__": bdd,
        "__PREFIXE_ID__": prefixe,
    }
    if moule == "outil-bdd":
        humain = humain or champ
        table.update(
            {
                "__CLE_LISTE__": liste,
                "__CHAMP__": champ,
                "__HUMAIN__": humain,
                "__HUMAIN_CAP__": (humain[0].upper() + humain[1:]) if humain else "",
            }
        )
    if moule == "theme-bdd":
        table["__NOM_AFFICHE__"] = nom_affiche or prefixe.upper()
    return table


def lire_moules(moule):
    """Retourne la liste triee des fichiers .moule du template demande (liste vide si absent)."""
    racine = REPERTOIRE_TEMPLATES / moule
    if not racine.exists():
        return []
    return sorted(chemin for chemin in racine.rglob("*" + SUFFIXE_MOULE) if chemin.is_file())


def traduire(chemin_moule, table):
    """Retourne le chemin de destination et le contenu traduit (jetons remplaces).

    Le chemin cible est relatif a la RACINE DU MOULE (le dossier direct de
    templates/, a n'importe quelle profondeur de fichier .moule).
    """
    racine_moule = chemin_moule.parent
    while racine_moule.parent.name != "templates":
        racine_moule = racine_moule.parent
    chemin_relatif = chemin_moule.relative_to(racine_moule)
    cible = Path(str(chemin_relatif)[: -len(SUFFIXE_MOULE)])
    contenu = chemin_moule.read_text(encoding="utf-8")
    for jeton, valeur in table.items():
        contenu = contenu.replace(jeton, valeur)
    return cible, contenu


def verifier_sources(en_memoire):
    """Verifie CHAQUE source AVANT ecriture : py_compile + ASCII + aucun jeton residuel.

    Retourne (code, messages) : code 1 si au moins un ecart (jamais d'outil a moitie livre).
    """
    messages = []
    with tempfile.TemporaryDirectory() as dossier_temp:
        for cible, contenu in en_memoire:
            if MOTIF_JETON.search(contenu):
                messages.append("jeton residuel dans " + str(cible))
                continue
            if any(octet > 127 for octet in contenu.encode("utf-8")):
                messages.append("non-ASCII dans " + str(cible))
                continue
            if cible.suffix != ".py":
                continue
            source_temp = Path(dossier_temp) / cible.name
            source_temp.write_text(contenu, encoding="utf-8", newline="\n")
            try:
                py_compile.compile(str(source_temp), doraise=True)
            except Exception as erreur:
                messages.append("py_compile echoue pour " + str(cible) + " : " + str(erreur))
    return (1 if messages else 0), messages


def verifier_outil_executable(repertoire_outil, moule):
    """Verifie le clone executable : le MOULE doit porter main.py.moule (controle
    contre le TEMPLATE, pas contre le clone), puis le clone doit donner
    docstring + code 2 sans argument."""
    if not (REPERTOIRE_TEMPLATES / moule / NOM_MOULE_PRINCIPAL).exists():
        return 1, "le moule principal " + NOM_MOULE_PRINCIPAL + " est absent du template " + moule
    resultat = subprocess.run(
        [sys.executable, str(repertoire_outil / "main.py")],
        capture_output=True,
        text=True,
        check=False,
    )
    if resultat.returncode == 2:
        return 0, ""
    return 1, "le clone n'a pas le comportement attendu sans argument (code " + str(resultat.returncode) + ")"


def ecrire_outil(repertoire_outil, en_memoire):
    """Ecrit le clone (atomique par conception : rien n'est ecrit si les verifications ont echoue)."""
    for cible, contenu in en_memoire:
        destination = repertoire_outil / cible
        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "w", encoding="utf-8", newline="\n") as flux:
            flux.write(contenu)
