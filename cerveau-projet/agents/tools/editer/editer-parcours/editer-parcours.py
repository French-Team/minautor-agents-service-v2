#!/usr/bin/env python3
# -*- coding: ascii -*-
# editer-parcours.py
#
# Edite les parcours de decision JSON (parcours-*.json) de maniere SURE :
# insertion / retrait de case, modification de branche / suivant,
# increment de version. Toutes les operations sont --dry-run par defaut.
#
# Pourquoi ? Les agents ecrivaient des scripts temporaires (.zz-insertion-*.py,
# .zz-fix-version-*.py) pour modifier les parcours a la main, ce qui a cause
# des erreurs (suivant auto-reference, cases non joignables). Cet outil
# centralise ces operations avec backup, dry-run et validation.
#
# Options :
#   --agent <nom>              : parcours cible (ex : cerberus)
#   --inserer-case <json>      : JSON de la case a ajouter (id, titre, type, ...)
#   --retirer-case <id>        : supprime une case et re-pointe vers elle
#   --vers <id>                : cible de re-pointage (avec --retirer-case)
#   --branche <case> <reponse> --vers <cible> : modifie une branche
#   --suivant <case> --vers <cible>           : modifie le suivant
#   --bump                     : incremente la version mineure (x.y.z -> x.y.z+1)
#   --backup                   : sauvegarde .bak avant modification (defaut)
#   --no-backup                : desactive le backup
#   --dry-run                  : simule sans ecrire (defaut si aucune action)
#   --wet                      : ecrit reellement
#   --version
#
# Usage:
#   python3 editer-parcours.py --agent cerberus --inserer-case '{"id":"c15b",...}' --wet
#   python3 editer-parcours.py --agent buffy --retirer-case c42 --vers c22 --wet
#   python3 editer-parcours.py --agent cerberus --branche c15 OUI --vers c15b --wet
#   python3 editer-parcours.py --agent cerberus --suivant c15c --vers c15b --wet
#   python3 editer-parcours.py --agent vulcain --bump --wet
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (editer-).
# =============================================================================
import argparse
import io
import json
import os
import re
import shutil
import sys

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


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def chemin_parcours(racine, agent):
    return os.path.join(racine, "cerveau-projet", "agents", agent,
                        "parcours", "parcours-%s.json" % agent)


def charger(chemin):
    with io.open(chemin, encoding="utf-8", newline="") as fh:
        return json.load(fh)


def sauver(chemin, d):
    txt = json.dumps(d, ensure_ascii=True, indent=1)
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(txt + "\n")


def normaliser_id(case):
    """Retourne l'id d'une case (cle 'id' ou cle unique du dict si dict plat)."""
    if "id" in case:
        return case["id"]
    # dict {id: {...}} ou {titre/...: ...} : on prend la premiere cle qui ressemble a cXX
    for k in case:
        if re.match(r"^c[A-Za-z0-9]+$", k):
            return k
    return None


def trouver_suivants(cases, cible):
    """Liste des cases qui pointent vers cible (suivant ou branches)."""
    resultat = []
    for k, c in cases.items():
        if c.get("suivant") == cible:
            resultat.append((k, "suivant"))
        for b in c.get("branches", []):
            if b.get("vers") == cible:
                resultat.append((k, "branche %r" % b.get("reponse")))
    return resultat


def main():
    parser = argparse.ArgumentParser(description="Edite les parcours de decision JSON de maniere sure")
    parser.add_argument("--agent", type=str, required=True, help="Nom de l'agent (obligatoire)")
    parser.add_argument("--inserer-case", type=str, default="", help="JSON de la case a ajouter")
    parser.add_argument("--retirer-case", type=str, default="", help="Id de la case a retirer")
    parser.add_argument("--vers", type=str, default="", help="Cible de re-pointage (avec --retirer-case)")
    parser.add_argument("--branche", type=str, default="", nargs="?", help="Case dont une branche change")
    parser.add_argument("--reponse", type=str, default="", help="Reponse de la branche a modifier")
    parser.add_argument("--suivant", type=str, default="", nargs="?", help="Case dont le suivant change")
    parser.add_argument("--cible", type=str, default="", help="Nouvelle cible (pour --branche/--suivant)")
    parser.add_argument("--bump", action="store_true", help="Incremente la version mineure")
    parser.add_argument("--backup", action="store_true", help="Sauvegarde .bak avant modification (defaut)")
    parser.add_argument("--no-backup", action="store_true", help="Desactive le backup")
    parser.add_argument("--dry-run", action="store_true", help="Simule sans ecrire")
    parser.add_argument("--wet", action="store_true", help="Ecrit reellement")
    parser.add_argument("--version", action="version", version="editer-parcours v%s" % VERSION)
    args = parser.parse_args()

    racine = racine_projet()
    chemin = chemin_parcours(racine, args.agent)
    if not os.path.isfile(chemin):
        print(_couleur("[ERREUR] Parcours introuvable : %s" % chemin, "rouge"))
        return 2

    d = charger(chemin)
    cases = d.get("cases", {})
    modifications = []

    # --- insertion de case
    if args.inserer_case:
        try:
            nouvelle = json.loads(args.inserer_case)
        except ValueError as e:
            print(_couleur("[ERREUR] JSON invalide pour --inserer-case : %s" % e, "rouge"))
            return 2
        ident = normaliser_id(nouvelle)
        if not ident:
            print(_couleur("[ERREUR] Impossible de determiner l'id de la case (cle cXX ou champ id)", "rouge"))
            return 2
        if ident in cases:
            print(_couleur("[ERREUR] Case %s deja presente" % ident, "rouge"))
            return 2
        # re-formater : {id: contenu sans 'id'}
        contenu = dict(nouvelle)
        contenu.pop("id", None)
        cases[ident] = contenu
        modifications.append("INSERT case %s" % ident)

    # --- retrait de case (avec re-pointage)
    if args.retirer_case:
        ident = args.retirer_case
        if ident not in cases:
            print(_couleur("[ERREUR] Case %s absente" % ident, "rouge"))
            return 2
        cible = args.vers or ident
        pointeurs = trouver_suivants(cases, ident)
        for k, nature in pointeurs:
            c = cases[k]
            if c.get("suivant") == ident:
                c["suivant"] = cible
                modifications.append("REPOINT %s.suivant -> %s" % (k, cible))
            for b in c.get("branches", []):
                if b.get("vers") == ident:
                    b["vers"] = cible
                    modifications.append("REPOINT %s.branche(%r) -> %s" % (k, b.get("reponse"), cible))
        del cases[ident]
        modifications.append("DELETE case %s (repointe %d pointeur(s) -> %s)" % (ident, len(pointeurs), cible))

    # --- modification de branche
    if args.branche:
        if not args.reponse or not args.cible:
            print(_couleur("[ERREUR] --branche exige --reponse et --cible", "rouge"))
            return 2
        if args.branche not in cases:
            print(_couleur("[ERREUR] Case %s absente" % args.branche, "rouge"))
            return 2
        trouve = False
        for b in cases[args.branche].get("branches", []):
            if b.get("reponse") == args.reponse:
                b["vers"] = args.cible
                trouve = True
                modifications.append("BRANCHE %s[%r] -> %s" % (args.branche, args.reponse, args.cible))
        if not trouve:
            print(_couleur("[ERREUR] Branche %r introuvable dans %s" % (args.reponse, args.branche), "rouge"))
            return 2

    # --- modification de suivant
    if args.suivant:
        if not args.cible:
            print(_couleur("[ERREUR] --suivant exige --cible", "rouge"))
            return 2
        if args.suivant not in cases:
            print(_couleur("[ERREUR] Case %s absente" % args.suivant, "rouge"))
            return 2
        cases[args.suivant]["suivant"] = args.cible
        modifications.append("SUIVANT %s -> %s" % (args.suivant, args.cible))

    # --- bump de version
    if args.bump:
        v = d.get("parcours", {}).get("version", "")
        m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", v)
        if not m:
            print(_couleur("[ERREUR] Version non standard : %r" % v, "rouge"))
            return 2
        nouvelle = "%s.%s.%s" % (m.group(1), m.group(2), int(m.group(3)) + 1)
        d.setdefault("parcours", {})["version"] = nouvelle
        modifications.append("VERSION %s -> %s" % (v, nouvelle))

    if not modifications:
        print(_couleur("[AVERTISSEMENT] Aucune modification demandee. "
                       "Utilisez --inserer-case / --retirer-case / --branche / --suivant / --bump.", "jaune"))
        return 1

    d["cases"] = cases
    ecriture = args.wet and not args.dry_run
    if not ecriture:
        print(_couleur("[DRY-RUN] Modifications simulees (utilisez --wet pour ecrire) :", "jaune"))
    else:
        print(_couleur("[WET] Modifications appliquees :", "vert"))

    for mod in modifications:
        print("   - %s" % mod)

    if ecriture:
        backup = args.backup and not args.no_backup
        if backup:
            shutil.copyfile(chemin, chemin + ".bak")
            print(_couleur("[OK] Backup : %s.bak" % chemin, "vert"))
        sauver(chemin, d)
        print(_couleur("[OK] Parcours ecrit : %s (JSON/LF preserves)" % chemin, "vert"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
