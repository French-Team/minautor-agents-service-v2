#!/usr/bin/env python3
# -*- coding: ascii -*-
# migrer-cases-relecture.py
#
# Migre les 15 parcours d agents vers la structure de relecture OBLIGATOIRE :
#   c0  [action]   RELIRE OBLIGATOIRE : corrections puis fiche   -> c0b
#   c0b [question] Confirmation : As-tu LU et compris ?          OUI -> c0c, NON -> c0
#   c0c [action]   CONTEXTE obligatoire (inchange, suivant conserve)
#
# Pourquoi : l ancienne structure (c0 question "EN MEMOIRE ?" avec OUI -> c0c)
# permettait de contourner la lecture de la fiche en repondant OUI. La lecture
# est desormais TOUJOURS exigee, puis la confirmation est posee.
#
# Options :
#   --agent <nom>       migrer UN parcours (cerveau-projet/agents/<nom>/parcours/)
#   (arguments multiples) migrer plusieurs parcours
#   --tous              migrer les 15 parcours
#   --dry-run           afficher les transformations sans ecrire
#   --rapport <fichier> ecrire un rapport markdown
#   --verbose           detail par parcours
#   --version
#
# Usage:
#   python3 migrer-cases-relecture.py --tous
#   python3 migrer-cases-relecture.py --agent buffy
#   python3 migrer-cases-relecture.py --agent buffy janus --dry-run
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (migrer-).
# =============================================================================

import argparse
import io
import json
import os
import sys

VERSION = "0.1.0"
STATUT = "ebauche"

# ---------------------------------------------------------------------------
# Detection de la racine du projet (fichier AGENTS.md a la racine)
# ---------------------------------------------------------------------------
def trouver_racine():
    """Remonte depuis le fichier de l outil jusqu a la racine du projet."""
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(d, "AGENTS.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


RACINE = trouver_racine()
if RACINE is None:
    sys.stderr.write("ERREUR : racine du projet introuvable (AGENTS.md absent).\n")
    sys.exit(2)

AGENTS_DIR = os.path.join(RACINE, "cerveau-projet", "agents")

# ---------------------------------------------------------------------------
# Structure cible
# ---------------------------------------------------------------------------
TITRE_C0 = "RELIRE OBLIGATOIRE : corrections puis fiche"
QUESTION_C0B = ("As-tu reellement LU ta fiche et tes corrections, capables de "
                "les appliquer SANS relire ? Reponds la VERITE "
                "(regles-veracite).")
TITRE_C0B = "Confirmation : as-tu lu ta fiche et tes corrections ?"


def lister_parcours():
    """Retourne {agent: chemin_parcours} pour les parcours trouves."""
    resultat = {}
    if not os.path.isdir(AGENTS_DIR):
        return resultat
    for nom in sorted(os.listdir(AGENTS_DIR)):
        d_agent = os.path.join(AGENTS_DIR, nom)
        if not os.path.isdir(d_agent):
            continue
        d_parcours = os.path.join(d_agent, "parcours")
        if not os.path.isdir(d_parcours):
            continue
        f = os.path.join(d_parcours, "parcours-%s.json" % nom)
        if os.path.isfile(f):
            resultat[nom] = f
    return resultat


def charger_parcours(chemin):
    """Charge un parcours JSON (utf-8)."""
    with io.open(chemin, encoding="utf-8") as fh:
        return json.load(fh)


def ecrire_parcours(chemin, parcours):
    """Ecrit un parcours JSON en ASCII strict + LF pur."""
    contenu = json.dumps(parcours, ensure_ascii=True, indent=2) + "\n"
    with io.open(chemin, "w", encoding="ascii", newline="\n") as fh:
        fh.write(contenu)


def analyser(agent, parcours):
    """Analyse la structure actuelle. Retourne (problemes, anciens_lecture)."""
    problemes = []
    anciens = {}
    cases = parcours.get("cases", {})
    c0 = cases.get("c0")
    c0b = cases.get("c0b")
    if not isinstance(c0, dict):
        problemes.append("C0_ABSENT")
    if not isinstance(c0b, dict):
        problemes.append("C0B_ABSENT")
    if isinstance(c0b, dict):
        for idx in c0b.get("indices", []):
            if idx.get("type") == "outil" and idx.get("nom") == "lire-fichier":
                anciens[idx.get("commande", "")] = idx
    return problemes, anciens


def transformer(agent, parcours, verbose=False):
    """Applique la transformation c0/c0b. Retourne True si modifie."""
    cases = parcours.get("cases", {})
    c0 = cases.get("c0")
    c0b = cases.get("c0b")
    c0c = cases.get("c0c")
    if not isinstance(c0, dict) or not isinstance(c0b, dict):
        return False

    # --- c0 : action RELIRE OBLIGATOIRE (corrections puis fiche) -> c0b ---
    indices_lecture = []
    for idx in c0b.get("indices", []):
        if idx.get("type") == "outil" and idx.get("nom") == "lire-fichier":
            indices_lecture.append(idx)
    # Secours : si aucun outil de lecture trouve, reconstruire les 2 commandes
    if len(indices_lecture) < 2:
        indices_lecture = [
            {"type": "outil", "nom": "lire-fichier",
             "catalogue": "lire-fichier",
             "chemin": "cerveau-projet/agents/tools/lire/lire-fichier/",
             "commande": "python3 cerveau-projet/agents/tools/lire/lire-fichier/lire-fichier.py "
                         "cerveau-projet/agents/%s/corrections.md" % agent},
            {"type": "outil", "nom": "lire-fichier",
             "catalogue": "lire-fichier",
             "chemin": "cerveau-projet/agents/tools/lire/lire-fichier/",
             "commande": "python3 cerveau-projet/agents/tools/lire/lire-fichier/lire-fichier.py "
                         "cerveau-projet/agents/%s/%s.md" % (agent, agent)},
        ]
    indices_lecture.insert(0, {
        "type": "regle",
        "texte": ("ACTION OBLIGATOIRE : je relis MES corrections EN PREMIER puis "
                  "MA fiche avant de continuer. Je ne lis jamais les fichiers "
                  "des autres agents.")
    })
    c0_nouveau = {
        "titre": TITRE_C0,
        "type": "action",
        "indices": indices_lecture,
        "suivant": "c0b",
    }

    # --- c0b : question confirmation (OUI -> c0c, NON -> c0) ---
    c0b_nouveau = {
        "titre": TITRE_C0B,
        "type": "question",
        "question": QUESTION_C0B,
        "indices": [{
            "type": "regle",
            "texte": ("REGLE ABSOLUE -- RELECTURE : seul OUI prouve la lecture "
                      "et la memorisation. NON ou INCERTAIN -> relecture (c0). "
                      "Reponds la VERITE.")
        }],
        "branches": [
            {"reponse": "OUI", "vers": "c0c"},
            {"reponse": "NON", "vers": "c0"},
        ],
    }

    cases["c0"] = c0_nouveau
    cases["c0b"] = c0b_nouveau

    # --- bump de version (patch +1) ---
    parcours.setdefault("parcours", {})
    v = str(parcours["parcours"].get("version", "0.0.0"))
    parties = v.split(".")
    while len(parties) < 3:
        parties.append("0")
    try:
        parties[2] = str(int(parties[2]) + 1)
    except ValueError:
        parties.append("1")
    parcours["parcours"]["version"] = ".".join(parties)

    if verbose:
        print("  [verbose] %s : c0 -> action RELIRE, c0b -> question "
              "confirmation, c0c conserve (%s)" %
              (agent, c0c.get("suivant") if isinstance(c0c, dict) else "?"))
    return True


def main():
    ap = argparse.ArgumentParser(description="Migrer les parcours vers la "
                                             "relecture obligatoire (c0 action + "
                                             "c0b confirmation)")
    ap.add_argument("--agent", nargs="*", default=None,
                    help="Agent(s) a migrer (un ou plusieurs)")
    ap.add_argument("--tous", action="store_true",
                    help="Migrer tous les parcours")
    ap.add_argument("--dry-run", action="store_true",
                    help="Afficher sans ecrire")
    ap.add_argument("--rapport", metavar="FICHIER", default=None,
                    help="Ecrire un rapport markdown")
    ap.add_argument("--verbose", action="store_true", help="Detail")
    ap.add_argument("--version", action="version", version=VERSION)
    args = ap.parse_args()

    tous = lister_parcours()
    if not tous:
        sys.stderr.write("ERREUR : aucun parcours trouve sous %s\n" % AGENTS_DIR)
        sys.exit(2)

    if args.tous:
        cibles = tous
    elif args.agent:
        cibles = {}
        for nom in args.agent:
            if nom in tous:
                cibles[nom] = tous[nom]
            else:
                sys.stderr.write("AVERTISSEMENT : parcours inconnu '%s' "
                                 "(agents trouves: %s)\n" %
                                 (nom, ", ".join(sorted(tous))))
    else:
        ap.print_help()
        sys.exit(2)

    lignes_rapport = []
    ok, ko = 0, 0
    for agent, chemin in sorted(cibles.items()):
        parcours = charger_parcours(chemin)
        problemes, _ = analyser(agent, parcours)
        modifie = transformer(agent, parcours, args.verbose)
        if modifie:
            if not args.dry_run:
                ecrire_parcours(chemin, parcours)
            ok += 1
            lignes_rapport.append(
                "| %s | %s | %s | %s |" %
                (agent, chemin.split("/")[-1],
                 parcours["parcours"].get("version"),
                 "DRY-RUN" if args.dry_run else "MIGRE"))
            print("  [OK] %s -> version %s%s" %
                  (agent, parcours["parcours"].get("version"),
                   " (dry-run)" if args.dry_run else ""))
        else:
            ko += 1
            lignes_rapport.append("| %s | %s | - | PROBLEME (%s) |" %
                                  (agent, chemin.split("/")[-1],
                                   ", ".join(problemes) or "non transformable"))
            print("  [KO] %s : %s" % (agent, ", ".join(problemes)
                                      or "structure non transformable"))

    print("")
    print("=== RESULTAT : %d migres / %d problemes (%d parcours analyses) ===" %
          (ok, ko, len(cibles)))
    if args.dry_run:
        print("=== MODE DRY-RUN : aucun fichier ecrit ===")

    if args.rapport:
        with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Rapport migrer-cases-relecture\n\n")
            fh.write("**Version outil** : %s\n\n" % VERSION)
            fh.write("**Date** : rapport genere\n\n")
            fh.write("**Mode** : %s\n\n" %
                     ("dry-run" if args.dry_run else "migration reelle"))
            fh.write("| Agent | Fichier | Version | Etat |\n")
            fh.write("|---|---|---|---|\n")
            fh.write("\n".join(lignes_rapport))
            fh.write("\n")
        print("=== RAPPORT : %s ===" % args.rapport)

    return 0


if __name__ == "__main__":
    sys.exit(main())
