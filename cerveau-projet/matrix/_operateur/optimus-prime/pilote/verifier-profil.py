#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-profil.py -- Verificateur de profil utilisateur

Verifie l'etat de la fiche USER-PROFIL.md et determine si un remplissage est necessaire.

Usage:
  python verifier-profil.py
  python verifier-profil.py --remplir
"""

import sys
import json
import argparse
from pathlib import Path


RACINE = Path(__file__).resolve().parent.parent.parent
PROFIL_PATH = RACINE / "USER-PROFIL.md"


def charger_profil() -> dict:
    """Charger la fiche profil."""
    if not PROFIL_PATH.exists():
        return {"statut": "inexistant", "champs": {}}
    
    with open(PROFIL_PATH, "r", encoding="utf-8") as f:
        contenu = f.read()
    
    # Parser le contenu (simplifie)
    champs = {}
    for ligne in contenu.split("\n"):
        if "**Pseudo**" in ligne:
            champs["pseudo"] = extraire_valeur(ligne)
        elif "**Age**" in ligne:
            champs["age"] = extraire_valeur(ligne)
        elif "**Langue**" in ligne:
            champs["langue"] = extraire_valeur(ligne)
        elif "**Style de conversation**" in ligne:
            champs["style"] = extraire_valeur(ligne)
        elif "**Sujets d'interet**" in ligne:
            champs["interets"] = extraire_valeur(ligne)
        elif "**Mode d'apprentissage**" in ligne:
            champs["apprentissage"] = extraire_valeur(ligne)
        elif "**Niveau technique**" in ligne:
            champs["niveau"] = extraire_valeur(ligne)
    
    return {"statut": "existant", "champs": champs}


def extraire_valeur(ligne: str) -> str:
    """Extraire la valeur d'une ligne de tableau."""
    parties = ligne.split("|")
    if len(parties) >= 3:
        valeur = parties[2].strip()
        if valeur and valeur != "A remplir" and valeur != "A choisir":
            return valeur
    return ""


def calculer_pourcentage(champs: dict) -> int:
    """Calculer le pourcentage de remplissage."""
    champs_requis = ["pseudo", "age", "style", "interets", "apprentissage", "niveau"]
    remplis = sum(1 for c in champs_requis if champs.get(c))
    return int((remplis / len(champs_requis)) * 100)


def afficher_etat(profil: dict):
    """Afficher l'etat du profil."""
    print("=" * 60)
    print("ETAT DU PROFIL UTILISATEUR")
    print("=" * 60)
    print()
    
    if profil["statut"] == "inexistant":
        print("Fichier USER-PROFIL.md inexistant")
        print("Action requise : creer et remplir la fiche")
        return
    
    champs = profil["champs"]
    pourcentage = calculer_pourcentage(champs)
    
    print(f"Pourcentage de remplissage : {pourcentage}%")
    print()
    
    for nom, valeur in champs.items():
        statut = "REMPLI" if valeur else "VIDE"
        print(f"  {nom:20} : {statut:10} {valeur if valeur else ''}")
    
    print()
    
    if pourcentage < 100:
        print("ACTION REQUISE : Completer la fiche")
        print("Commande : python verifier-profil.py --remplir")
    else:
        print("FICHE COMPLETE")


def main():
    parser = argparse.ArgumentParser(description="Verificateur de profil utilisateur")
    parser.add_argument("--remplir", action="store_true", help="Lancer le questionnaire de remplissage")
    args = parser.parse_args()
    
    profil = charger_profil()
    
    if args.remplir:
        print("Demarrage du questionnaire de remplissage...")
        print("(A implementer avec le pilote)")
        return 0
    
    afficher_etat(profil)
    return 0


if __name__ == "__main__":
    sys.exit(main())
