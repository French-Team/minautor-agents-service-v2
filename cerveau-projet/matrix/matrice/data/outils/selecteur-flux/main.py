#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selecteur-flux.py -- Gestionnaire du selecteur de flux Matrice

Gere le basculement entre Flux 1 (Cameleon) et Flux 2 (Optimus).

Usage:
  python selecteur-flux.py actuel
  python selecteur-flux.py basculer <flux> --par <qui> [--raison <texte>]
  python selecteur-flux.py historique [--derniers <n>]
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


REPERTOIRE_OUTIL = Path(__file__).resolve().parent
# L'outil vit dans outils/selecteur-flux/ ; le selecteur vit deux niveaux au-dessus (dans data/).
RACINE = REPERTOIRE_OUTIL.parent.parent
if RACINE.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(RACINE) + " n'est pas le dossier data/"
    )
SELECTEUR_PATH = RACINE / "selecteur-flux.json"


def load_selecteur() -> dict:
    """Charger le selecteur."""
    if SELECTEUR_PATH.exists():
        with open(SELECTEUR_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"flux_actif": None, "dernier_changement": None, "changement_par": None, "historique": []}


def save_selecteur(data: dict):
    """Sauvegarder le selecteur."""
    SELECTEUR_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SELECTEUR_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def actuel():
    """Afficher le flux actuel."""
    sel = load_selecteur()
    flux = sel.get("flux_actif")
    
    if flux is None:
        print("AUCUN FLUX ACTIF - Selectionnez flux1 ou flux2")
        return 1
    
    print(f"FLUX ACTIF: {flux.upper()}")
    print(f"Depuis: {sel.get('dernier_changement', 'inconnu')}")
    print(f"Par: {sel.get('changement_par', 'inconnu')}")
    
    if flux == "flux1":
        print("\n--- FLUX 1: CAMELEON ---")
        print("Mode: COMMUNICATION")
        print("Agent: cameleon")
        print("Pilote: matrice/pilote -- il te dirige")
        print("Watchdog: flux1")
    elif flux == "flux2":
        print("\n--- FLUX 2: OPTIMUS ---")
        print("Mode: MAINTENANCE")
        print("Agent: optimus-prime")
        print("Pilote: _operateur/optimus-prime/pilote -- tu le conduis")
        print("Watchdog: flux2")
    
    return 0


def basculer(flux: str, par: str, raison: str = None):
    """Basculer vers un flux."""
    if flux not in ["flux1", "flux2"]:
        print(f"ERREUR: Flux invalide '{flux}'. Utilisez 'flux1' ou 'flux2'")
        return 1
    
    sel = load_selecteur()
    ancien_flux = sel.get("flux_actif")
    
    # Verification: on ne peut pas basculer vers le meme flux
    if ancien_flux == flux:
        print(f"Deja sur {flux.upper()}")
        return 0
    
    # Historiser le changement
    maintenant = datetime.now().isoformat()
    entree = {
        "de": ancien_flux,
        "vers": flux,
        "par": par,
        "timestamp": maintenant
    }
    if raison:
        entree["raison"] = raison
    
    if "historique" not in sel:
        sel["historique"] = []
    sel["historique"].append(entree)
    
    # Garder seulement les 50 dernieres entrees
    sel["historique"] = sel["historique"][-50:]
    
    # Mettre a jour
    sel["flux_actif"] = flux
    sel["dernier_changement"] = maintenant
    sel["changement_par"] = par
    
    save_selecteur(sel)
    
    print(f"FLUX BASCULE: {ancien_flux or 'AUCUN'} -> {flux.upper()}")
    print(f"Par: {par}")
    if raison:
        print(f"Raison: {raison}")
    
    # Instructions
    if flux == "flux1":
        print("\n>>> Pour demarrer le Cameleon: python demarrer-cameleon.md")
    elif flux == "flux2":
        print("\n>>> Pour demarrer Optimus: python demarrer-optimus-prime.md")
    
    return 0


def historique(derniers: int = 10):
    """Afficher l'historique des changements."""
    sel = load_selecteur()
    hist = sel.get("historique", [])
    
    if not hist:
        print("Aucun historique")
        return 0
    
    print(f"Derniers {min(derniers, len(hist))} changements:")
    for entree in hist[-derniers:]:
        de = entree.get("de") or "AUCUN"
        vers = entree.get("vers") or "AUCUN"
        par = entree.get("par", "inconnu")
        ts = entree.get("timestamp", "?")
        raison = entree.get("raison", "")
        
        ligne = f"  {ts}: {de.upper()} -> {vers.upper()} (par {par})"
        if raison:
            ligne += f" - {raison}"
        print(ligne)
    
    return 0


USAGE = ("Usage : python main.py actuel | basculer <flux1|flux2> --par <qui> [--raison <texte>]"
         " | historique [--derniers <n>]")
# Les options LONGUES que ce parseur connait : le DOMICILE refuse les autres et les
# NOMME (T3 de PB-002, MO-302). MESURE du 2026-09-20 : `--option-bidon-mo202 1` rendait
# code 2 en accusant la VALEUR ("argument commande: invalid choice: '1'") -- argparse
# met de cote un optionnel inconnu, et la fautive n etait donc JAMAIS nommee : un refus
# muet, comme les 32 de la chaine PB-002. La carte l annoncait "conforme par un autre
# chemin" : la MESURE a dementi, et c est la mesure qui decide.
OPTIONS = ("par", "raison", "derniers")


def principal(arguments):
    from options import extraire_options
    # Le garde du DOMICILE passe AVANT argparse : lui seul NOMME l option fautive (et
    # le texte du refus n existe qu une fois, au domicile -- M-076).
    extraire_options(arguments, OPTIONS, outil="selecteur-flux", usage=USAGE)
    parser = argparse.ArgumentParser(description="Selecteur de flux Matrice")
    subparsers = parser.add_subparsers(dest="commande", help="Commande a executer")
    
    # Commande: actuel
    subparsers.add_parser("actuel", help="Afficher le flux actuel")
    
    # Commande: basculer
    p_basculer = subparsers.add_parser("basculer", help="Basculer vers un flux")
    p_basculer.add_argument("flux", choices=["flux1", "flux2"], help="Flux cible")
    p_basculer.add_argument("--par", required=True, help="Qui fait le changement")
    p_basculer.add_argument("--raison", help="Raison du changement")
    
    # Commande: historique
    p_historique = subparsers.add_parser("historique", help="Afficher l'historique")
    p_historique.add_argument("--derniers", type=int, default=10, help="Nombre d'entrees")
    
    args = parser.parse_args()
    
    if args.commande == "actuel":
        return actuel()
    elif args.commande == "basculer":
        return basculer(args.flux, args.par, args.raison)
    elif args.commande == "historique":
        return historique(args.derniers)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    # Pas de constants.py ici (recette incomplete, deja signalee) : le pont vers
    # data/commun est derive sur place, ANCRE par le NOM du dossier (aucun parents[N]).
    REPERTOIRE_DATA = Path(__file__).resolve().parent.parent.parent
    if REPERTOIRE_DATA.name != "data":
        raise RuntimeError("Structure inattendue : " + str(REPERTOIRE_DATA)
                           + " n'est pas le dossier data/")
    sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))
    from sac_a_dos import envelopper
    sys.exit(envelopper(principal, sys.argv[1:]))
