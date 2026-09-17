"""Fonctions communes de l'outil corriger-ascii : une seule tache chacune."""
import os

from constants import (
    CARTE_CONVERSION,
    DOSSIERS_CIBLES,
    DOSSIERS_EXCLUS,
    ENCODAGE,
    EXTENSIONS_CIBLES,
    EXTENSIONS_JOURNAUX,
    MOTIF_BDD_EMPREINTE,
    MOTIF_JOURNAL,
    SUFFIXE_ETALON,
    SUFFIXES_EXCLUS,
)


def classer_fichiers_cibles():
    """Retourne (fichiers_cibles, fichiers_exemptes).

    Un EXEMPTE est un fichier de contenu que l'outil voit mais ne reecrit JAMAIS :
      - BDD empreintee : un etalon `.sha256` garde son contenu (toute reecriture
        ferait crier l'espion d'integrite) ;
      - journal en ajout seul (`.jsonl`) : jamais reecrit non plus.
    L'exemption est NOMMEE (chemin + motif) pour que le rapport la MONTRE au lieu
    de la taire : une exclusion muette est un angle mort qu'aucune suite ne voit.
    """
    cibles = []
    exemptes = []
    for dossier in DOSSIERS_CIBLES:
        if not dossier.exists():
            continue
        for racine, dossiers, fichiers in os.walk(dossier):
            dossiers[:] = [d for d in dossiers if d not in DOSSIERS_EXCLUS]
            for nom in fichiers:
                if nom.endswith(SUFFIXES_EXCLUS):
                    continue
                chemin = os.path.join(racine, nom)
                # L'ETALON passe AVANT le journal : un .jsonl empreinte
                # (suivi-optimus.jsonl) est une BDD a part entiere, et son motif
                # doit dire la protection la plus forte qui le couvre.
                if os.path.exists(chemin + SUFFIXE_ETALON):
                    exemptes.append((chemin, MOTIF_BDD_EMPREINTE))
                    continue
                if nom.endswith(EXTENSIONS_JOURNAUX):
                    exemptes.append((chemin, MOTIF_JOURNAL))
                    continue
                if not nom.endswith(EXTENSIONS_CIBLES):
                    continue
                cibles.append(chemin)
    return sorted(cibles), sorted(exemptes)


def lister_fichiers_cibles():
    """Retourne la liste triee des fichiers cibles (extensions, exclusions, etalons).

    Vue COURTE de `classer_fichiers_cibles` : les appelants qui n'ont besoin que
    des cibles reecrivables ne changent pas. Le rapport, lui, passe par la vue
    complete (il doit MONTRER les exemptes).
    """
    cibles, _ = classer_fichiers_cibles()
    return cibles


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
