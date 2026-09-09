"""Fonctions communes de l'outil corriger-ascii : une seule tache chacune."""
import os

from constants import (
    CARTE_CONVERSION,
    DOSSIERS_CIBLES,
    DOSSIERS_EXCLUS,
    ENCODAGE,
    EXTENSIONS_CIBLES,
    SUFFIXES_EXCLUS,
)


def lister_fichiers_cibles():
    """Retourne la liste triee des fichiers cibles (extensions, exclusions, etalons)."""
    cibles = []
    for dossier in DOSSIERS_CIBLES:
        if not dossier.exists():
            continue
        for racine, dossiers, fichiers in os.walk(dossier):
            dossiers[:] = [d for d in dossiers if d not in DOSSIERS_EXCLUS]
            for nom in fichiers:
                if not nom.endswith(EXTENSIONS_CIBLES):
                    continue
                if nom.endswith(SUFFIXES_EXCLUS):
                    continue
                chemin = os.path.join(racine, nom)
                if os.path.exists(chemin + ".sha256"):
                    continue  # BDD empreintee : JAMAIS reecrite
                cibles.append(chemin)
    return sorted(cibles)


def lire_texte(chemin):
    """Retourne le texte du fichier."""
    with open(chemin, "r", encoding=ENCODAGE, newline="") as flux:
        return flux.read()


def scanner_texte(texte):
    """Retourne les ecarts (ligne, colonne, caractere, remplacement ou None)."""
    ecarts = []
    numero_ligne = 1
    numero_colonne = 1
    for caractere in texte:
        if caractere == "\n":
            numero_ligne += 1
            numero_colonne = 1
            continue
        if ord(caractere) > 127:
            ecarts.append((numero_ligne, numero_colonne, caractere, CARTE_CONVERSION.get(caractere)))
        numero_colonne += 1
    return ecarts


def convertir_texte(texte):
    """Retourne (texte_converti, caracteres_non_convertis) via la carte."""
    non_convertis = []
    morceaux = []
    for caractere in texte:
        if ord(caractere) <= 127:
            morceaux.append(caractere)
            continue
        remplacement = CARTE_CONVERSION.get(caractere)
        if remplacement is None:
            non_convertis.append(caractere)
            morceaux.append(caractere)
        else:
            morceaux.append(remplacement)
    return "".join(morceaux), non_convertis


def ecrire_texte_atomique(chemin, texte):
    """Ecrit de facon atomique (tmp + remplacement), fins de ligne LF forcees."""
    texte = texte.replace("\r\n", "\n").replace("\r", "\n")
    chemin_tmp = chemin + ".tmp"
    with open(chemin_tmp, "w", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(texte)
    os.replace(chemin_tmp, chemin)
