"""Fonctions communes de editer-agents-md : racine, bloc delimite, ecriture.

Garantie structurelle : l'outil ne modifie QUE le bloc delimite session-matrix ;
le reste de AGENTS.md (encarts v1/v2, marbre constitution) est preserve octet
par octet. Ecriture atomique + empreinte SHA-256 (convention-integrite).
"""
import hashlib
import os
from datetime import datetime

from constants import (
    CHEMIN_EMPREINTE,
    ENCODAGE,
    LIGNE_ANCRE,
    MARQUEUR_DEBUT,
    MARQUEUR_FIN,
    NOM_AGENTS_MD,
    NOM_AGENTS_TMP,
    REPERTOIRE_OUTIL,
    TAILLE_BLOC_LECTURE,
    # MO-216 (EO-209) : l outil etait MORT -- commun.py appelait detecter_racine
    # (ligne 26) sans l importer : NameError a la premiere utilisation, la seule
    # porte qui ecrit l encart v3 de AGENTS.md ne pouvait plus rien faire.
    # constants.py le consomme DEJA du domicile partage (motif M-076) : commun.py
    # le consomme A SON TOUR depuis constants, jamais d une 3e copie.
    detecter_racine,
)


def trouver_agents_md():
    """AGENTS.md a la racine DETECTEE (motif unique partage, M-076)."""
    return detecter_racine(REPERTOIRE_OUTIL) / NOM_AGENTS_MD


def horodatage():
    """Retourne la date-heure locale au format de la Matrice."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def charger_texte(chemin):
    """Retourne le texte de AGENTS.md."""
    return chemin.read_text(encoding=ENCODAGE)


def composer_bloc(nom_llm, agent, raison):
    """Compose le bloc delimite session-matrix (marqueurs inclus)."""
    lignes = [
        MARQUEUR_DEBUT,
        "",
        "### Session : session-matrix (v3 / Matrice)",
        "",
        "| Champ | Valeur |",
        "|---|---|",
        "| **Nom LLM** | " + nom_llm + " |",
        "| **Agent actif** | " + agent + " |",
        "| **Role Agent** | agent unique de la Matrice (personnalite fournie par le vivier) |",
        "| **Derniere mise a jour** | " + horodatage() + " |",
        "| **Raison** | " + raison + " |",
        "",
        "Flux v3 : la Matrice accueille au demarrage -> l'operateur fait sa demande ->",
        "la Matrice lance le cameleon pour sa mission (serial stricte).",
        "",
        MARQUEUR_FIN,
    ]
    return "\n".join(lignes)


def remplacer_ou_inserer_bloc(texte, bloc):
    """Retourne le nouveau texte : le bloc remplace l'ancien (idempotent) ou est insere.

    Insertion : juste avant l'ancre (fin de la zone sessions) si presente,
    sinon en fin de fichier. Le reste du texte est preserve octet par octet.
    """
    if MARQUEUR_DEBUT in texte and MARQUEUR_FIN in texte:
        debut = texte.index(MARQUEUR_DEBUT)
        fin = texte.index(MARQUEUR_FIN) + len(MARQUEUR_FIN)
        return texte[:debut] + bloc + texte[fin:]
    if MARQUEUR_DEBUT in texte or MARQUEUR_FIN in texte:
        raise RuntimeError("Marqueurs session-matrix incoherents : DEBUT/FIN non apparies.")
    if LIGNE_ANCRE in texte:
        index = texte.index(LIGNE_ANCRE)
        return texte[:index] + bloc + "\n\n" + texte[index:]
    return texte + "\n\n" + bloc


def texte_hors_bloc(texte):
    """Retourne le texte SANS le bloc delimite (pour prouver que le reste ne bouge pas)."""
    if MARQUEUR_DEBUT in texte and MARQUEUR_FIN in texte:
        debut = texte.index(MARQUEUR_DEBUT)
        fin = texte.index(MARQUEUR_FIN) + len(MARQUEUR_FIN)
        return texte[:debut] + texte[fin:]
    return texte


def garde_structurelle(texte_avant, texte_apres):
    """True si rien hors du bloc delimite n'a bouge entre avant et apres.

    Cas 1 (remplacement) : texte hors bloc STRICTEMENT identique.
    Cas 2 (insertion) : la seule difference admise hors bloc est le couple de
    sauts de ligne ajoute devant l'ancre (ou en fin de fichier si pas d'ancre).
    """
    if MARQUEUR_DEBUT in texte_avant and MARQUEUR_FIN in texte_avant:
        return texte_hors_bloc(texte_apres) == texte_hors_bloc(texte_avant)
    if LIGNE_ANCRE in texte_avant:
        index = texte_avant.index(LIGNE_ANCRE)
        attendu = texte_avant[:index] + "\n\n" + texte_avant[index:]
    else:
        attendu = texte_avant + "\n\n"
    return texte_hors_bloc(texte_apres) == attendu


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus, sans_tirets=True)


def lire_empreinte_enregistree():
    """Retourne l'empreinte enregistree pour AGENTS.md, ou None si absente."""
    if not CHEMIN_EMPREINTE.exists():
        return None
    return CHEMIN_EMPREINTE.read_text(encoding=ENCODAGE).strip()


def ecrire_texte(chemin, texte):
    """Ecrit de facon atomique puis enregistre l'empreinte (convention-integrite)."""
    chemin_temporaire = chemin.with_name(NOM_AGENTS_TMP)
    with open(chemin_temporaire, "w", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(texte)
    os.replace(chemin_temporaire, chemin)

    hacheur = hashlib.sha256()
    with open(chemin, "rb") as flux:
        for bloc in iter(lambda: flux.read(TAILLE_BLOC_LECTURE), b""):
            hacheur.update(bloc)
    empreinte = hacheur.hexdigest()
    with open(CHEMIN_EMPREINTE, "w", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(empreinte + "\n")
    return empreinte
