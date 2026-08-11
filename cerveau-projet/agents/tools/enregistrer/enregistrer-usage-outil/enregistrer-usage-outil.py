#!/usr/bin/env python3
# -*- coding: ascii -*-
# enregistrer-usage-outil.py
#
# Enregistre l'utilisation d'un outil du cerveau-projet dans le registre
# d'usage (registre-usages-outils.jsonl) : une ligne JSON par usage.
#
# Pourquoi ? Les controles (Janus, Themis) et les tests de non-regression
# ont besoin d'une SOURCE DE VERITE sur qui utilise quel outil, quand et
# comment. Sans registre, aucun controle ne peut detecter qu'un agent
# contourne nos outils (ex : outils tiers) ou compose des commandes en dur.
#
# Champs par entree :
#   date     : YYYY-MM-DD HH:MM:SS
#   agent    : nom de l'agent (obligatoire)
#   outil    : nom de l'outil utilise (obligatoire)
#   mode     : generateur | direct | combo (defaut : direct)
#   commande : commande reelle lancee (optionnel)
#   contexte : contexte de l'usage (optionnel)
#
# Usage:
#   python3 enregistrer-usage-outil.py --agent morpheus --outil valider-case --mode direct
#   python3 enregistrer-usage-outil.py --agent vulcain --outil test-023-grep-budget-pondere \
#       --mode generateur --commande "python3 ...py" --contexte "refonte spec"
#   python3 enregistrer-usage-outil.py --agent morpheus --outil valider-case --dry-run
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (enregistrer-).
# =============================================================================
import argparse
import io
import json
import os
import sys
from datetime import datetime

VERSION = "0.1.0"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[0;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    return "%s%s%s" % (_COULEURS.get(nom, _COULEURS["neutre"]), texte, _COULEURS["neutre"])


def registre_defaut():
    """Chemin du registre d'usage par defaut (dossier agents/traces/)."""
    dossier_script = os.path.dirname(os.path.abspath(__file__))
    # remonter : enregistrer-usage-outil/ -> enregistrer/ -> tools/ -> agents/
    agents_dir = os.path.abspath(os.path.join(dossier_script, "..", "..", ".."))
    return os.path.join(agents_dir, "traces", "registre-usages-outils.jsonl")


def ajouter_entree(registre, agent, outil, mode, commande, contexte, dry_run=False):
    """Ajoute une entree JSON (une ligne) au registre. Retourne le dict cree."""
    entree = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": agent,
        "outil": outil,
        "mode": mode,
        "commande": commande or "",
        "contexte": contexte or "",
    }
    ligne = json.dumps(entree, ensure_ascii=True, separators=(",", ":"))
    if dry_run:
        print(_couleur("[DRY-RUN] Ligne a enregistrer :", "jaune"))
        print(ligne)
        return entree
    dossier = os.path.dirname(registre)
    if dossier and not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)
    with io.open(registre, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(ligne + "\n")
    print(_couleur("[OK] Usage enregistre : %s -> %s (mode %s)" % (agent, outil, mode), "vert"))
    print("Registre : %s" % registre)
    return entree


def main():
    parser = argparse.ArgumentParser(description="Enregistre un usage d'outil dans le registre JSONL")
    parser.add_argument("--agent", type=str, required=True, help="Nom de l'agent (obligatoire)")
    parser.add_argument("--outil", type=str, required=True, help="Nom de l'outil utilise (obligatoire)")
    parser.add_argument("--mode", type=str, default="direct",
                        choices=["generateur", "direct", "combo"],
                        help="Mode d'usage (defaut : direct)")
    parser.add_argument("--commande", type=str, default="", help="Commande reelle lancee (optionnel)")
    parser.add_argument("--contexte", type=str, default="", help="Contexte de l'usage (optionnel)")
    parser.add_argument("--registre", type=str, default="", help="Chemin du registre (defaut : fixe)")
    parser.add_argument("--dry-run", action="store_true", help="Afficher la ligne sans l'ecrire")
    parser.add_argument("--version", action="version", version="enregistrer-usage-outil v%s" % VERSION)
    args = parser.parse_args()

    registre = args.registre or registre_defaut()
    ajouter_entree(registre, args.agent, args.outil, args.mode, args.commande, args.contexte,
                   dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
