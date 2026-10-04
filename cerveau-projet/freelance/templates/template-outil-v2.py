#!/usr/bin/env python3
"""
<outil> -- <Description>
Template v2 : zero valeur en dur (P4), separation code/donnees (D15).
"""
import argparse
import json
import os
import sys

# RACINE : detection OBLIGATOIRE via os_path (P10, jamais de ../.. comptes)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'os_path', 'fonctions'))
from racine import trouver_racine

RACINE = trouver_racine(__file__)

# Fichier de donnees (D15) - JAMAIS de valeurs en dur dans le code
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         '<outil>-data.json')


def charger_donnees():
    """Charger les donnees depuis le fichier JSON (D15)."""
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERREUR: Fichier de donnees introuvable: {DATA_FILE}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERREUR: JSON invalide dans {DATA_FILE}: {e}")
        sys.exit(1)


def valider_formulaire(champs, donnees):
    """Valider les champs selon le formulaire (D7)."""
    erreurs = []
    for champ in champs:
        nom = champ["nom"]
        requis = champ.get("requis", False)
        valeur = donnees.get(nom)

        if requis and valeur is None:
            erreurs.append(f"Champ requis manquant: {nom}")
        elif valeur is not None:
            type_attendu = champ.get("type", "texte")
            if type_attendu == "nombre" and not isinstance(valeur, (int, float)):
                erreurs.append(f"Champ {nom}: type nombre attendu, {type(valeur).__name__} trouve")
            elif type_attendu == "boolean" and not isinstance(valeur, bool):
                erreurs.append(f"Champ {nom}: type boolean attendu, {type(valeur).__name__} trouve")
            elif type_attendu == "enum" and "valeurs" in champ:
                if valeur not in champ["valeurs"]:
                    erreurs.append(f"Champ {nom}: valeur '{valeur}' pas dans {champ['valeurs']}")

    return erreurs


def cmd_aide(donnees):
    """Afficher l'aide et les commandes disponibles."""
    print(f"\n{donnees.get('description', '<outil>')}")
    print(f"Version: {donnees.get('version', '0.1.0')}")
    print("\nCommandes:")
    print("  --help      Afficher cette aide")
    print("  --lister    Lister les elements")
    # Ajouter les commandes specifiques ici


def cmd_lister(donnees):
    """Lister les elements du fichier de donnees."""
    elements = donnees.get("elements", [])
    if not elements:
        print("Aucun element.")
        return
    print(f"\n{len(elements)} element(s):")
    for i, elem in enumerate(elements, 1):
        print(f"  {i}. {elem}")


def main():
    parser = argparse.ArgumentParser(description="<outil> -- <Description>")
    parser.add_argument("--lister", action="store_true", help="Lister les elements")
    args = parser.parse_args()

    donnees = charger_donnees()

    if args.lister:
        cmd_lister(donnees)
    else:
        cmd_aide(donnees)


if __name__ == "__main__":
    main()
