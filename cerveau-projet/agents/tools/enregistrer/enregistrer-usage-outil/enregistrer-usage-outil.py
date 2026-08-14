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
# Depuis v0.2.0 : le mode "script-temporaire" permet de DECLARER la creation
# d'un script temporaire (.zz-*.py / .tmp-*.py). Cette declaration alimente
# le croisement de detecter-usage-scripts-temporaires : tout script trouve
# sur disque / dans git / dans les lecons doit avoir sa declaration ici.
#
# Champs par entree :
#   date     : YYYY-MM-DD HH:MM:SS
#   agent    : nom de l'agent (obligatoire)
#   outil    : nom de l'outil utilise (obligatoire)
#   mode     : generateur | direct | combo | script-temporaire (defaut : direct)
#   commande : commande reelle lancee (optionnel)
#   contexte : contexte de l'usage (optionnel)
#
# Usage:
#   python3 enregistrer-usage-outil.py --agent morpheus --outil valider-case --mode direct
#   python3 enregistrer-usage-outil.py --agent vulcain --outil test-023-grep-budget-pondere \
#       --mode generateur --commande "python3 ...py" --contexte "refonte spec"
#   python3 enregistrer-usage-outil.py --agent buffy --outil .zz-insertion-parcours.py \
#       --mode script-temporaire --contexte "inserer case c42 dans parcours buffy"
#   python3 enregistrer-usage-outil.py --agent morpheus --outil valider-case --dry-run
#
# Version : 0.3.0
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

VERSION = "0.3.0"
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


def valider_champs(agent, outil):
    """Valide les champs obligatoires (round 8 : un agent/outil vide est une
    entree inexploitable, silencieusement acceptee avant). Retourne (ok, msg)."""
    if not agent or not agent.strip():
        return False, "champ '--agent' vide (obligatoire)"
    if not outil or not outil.strip():
        return False, "champ '--outil' vide (obligatoire)"
    return True, ""


def verifier_registre(registre):
    """Verifie l integrite du registre avant ajout (round 8). Retourne
    (lignes_invalides, deja_present) : signale les lignes non-JSON et les
    doublons sans bloquer l ajout (un usage peut etre legitiment rejoue)."""
    invalides = 0
    deja = set()
    if not os.path.isfile(registre):
        return 0, deja
    try:
        fh = io.open(registre, encoding="utf-8")
    except Exception:
        return 0, deja
    with fh:
        for l in fh:
            if not l.strip():
                continue
            try:
                e = json.loads(l)
                deja.add((e.get("agent"), e.get("outil"), e.get("mode"),
                          e.get("commande", ""), e.get("contexte", "")))
            except ValueError:
                invalides += 1
    return invalides, deja


def trier_registre(registre):
    """Trie le registre par date puis heure, DECROISSANT (le plus recent en
    premier, demande utilisateur 2026-08-14). Les lignes non-JSON sont
    PRESERVEES (signalees, jamais perdues) et placees en fin de fichier.
    Retourne le nombre de lignes triees."""
    if not os.path.isfile(registre):
        return 0
    try:
        with io.open(registre, encoding="utf-8") as fh:
            lignes = [l.rstrip("\n") for l in fh if l.strip()]
    except Exception:
        return 0
    valides = []
    invalides = []
    for l in lignes:
        try:
            e = json.loads(l)
            valides.append((e.get("date", ""), l))
        except ValueError:
            invalides.append(l)
    # tri decroissant par date (format YYYY-MM-DD HH:MM:SS - tri lexicographique
    # equivalent au tri chronologique)
    valides.sort(key=lambda paire: paire[0], reverse=True)
    triees = [l for _, l in valides] + invalides
    with io.open(registre, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(triees) + "\n")
    if invalides:
        print(_couleur("[AVERTISSEMENT] %d ligne(s) non-JSON conservees en fin de registre"
                       % len(invalides), "jaune"))
    return len(valides)


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
    # integrite + doublons (round 8)
    invalides, deja = verifier_registre(registre)
    if invalides:
        print(_couleur("[AVERTISSEMENT] %d ligne(s) non-JSON dans le registre (corrompu ?)"
                       % invalides, "jaune"))
    cle = (agent, outil, mode, commande or "", contexte or "")
    if cle in deja:
        print(_couleur("[AVERTISSEMENT] entree identique deja presente (usage rejoue ?)", "jaune"))
    dossier = os.path.dirname(registre)
    if dossier and not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)
    with io.open(registre, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(ligne + "\n")
    # tri par date/heure DECROISSANT apres chaque ajout (demande utilisateur)
    trier_registre(registre)
    print(_couleur("[OK] Usage enregistre : %s -> %s (mode %s)" % (agent, outil, mode), "vert"))
    print("Registre : %s" % registre)
    return entree


def main():
    parser = argparse.ArgumentParser(description="Enregistre un usage d'outil dans le registre JSONL")
    parser.add_argument("--agent", type=str, required=True, help="Nom de l'agent (obligatoire)")
    parser.add_argument("--outil", type=str, required=True, help="Nom de l'outil utilise (obligatoire)")
    parser.add_argument("--mode", type=str, default="direct",
                        choices=["generateur", "direct", "combo", "script-temporaire"],
                        help="Mode d'usage (defaut : direct ; script-temporaire = declaration d'un script jetable)")
    parser.add_argument("--commande", type=str, default="", help="Commande reelle lancee (optionnel)")
    parser.add_argument("--contexte", type=str, default="", help="Contexte de l'usage (optionnel)")
    parser.add_argument("--registre", type=str, default="", help="Chemin du registre (defaut : fixe)")
    parser.add_argument("--dry-run", action="store_true", help="Afficher la ligne sans l'ecrire")
    parser.add_argument("--version", action="version", version="enregistrer-usage-outil v%s" % VERSION)
    args = parser.parse_args()

    ok, msg = valider_champs(args.agent, args.outil)
    if not ok:
        print(_couleur("[ERREUR] %s" % msg, "rouge"))
        return 1

    registre = args.registre or registre_defaut()
    ajouter_entree(registre, args.agent, args.outil, args.mode, args.commande, args.contexte,
                   dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
